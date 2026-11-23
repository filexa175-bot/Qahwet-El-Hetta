import { Capacitor } from '@capacitor/core';
import { initializeApp } from 'firebase/app';
import { getAuth, initializeAuth, indexedDBLocalPersistence, GoogleAuthProvider, signInWithCredential, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, doc, getDoc, setDoc, runTransaction, serverTimestamp } from 'firebase/firestore';
import { FirebaseAuthentication } from '@capacitor-firebase/authentication';

const firebaseConfig = {
  apiKey: "AIzaSyDUmw1It8TxURmAv0yAZqW33yW0sM2fQ7U",
  authDomain: "qahwet-el-hetta.firebaseapp.com",
  projectId: "qahwet-el-hetta",
  storageBucket: "qahwet-el-hetta.firebasestorage.app",
  messagingSenderId: "572837784692",
  appId: "1:572837784692:android:2ba62f673af102ed79f521"
};
const app=initializeApp(firebaseConfig);
let auth;
try { auth=Capacitor.isNativePlatform()?initializeAuth(app,{persistence:indexedDBLocalPersistence}):getAuth(app); }
catch(e){ auth=getAuth(app); }
const db=getFirestore(app);
const alphabet="ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
function makeId(){let out="";for(let i=0;i<8;i++)out+=alphabet[Math.floor(Math.random()*alphabet.length)];return out;}
function cleanName(v){return String(v||"").trim().replace(/[<>]/g,"").slice(0,18);}
function errorText(e){
  const code=e?.code?String(e.code)+" — ":"";
  const msg=String(e?.message||"خطأ غير معروف").replace(/^Firebase:\\s*/,"");
  return (code+msg).slice(0,260);
}
function authNotice(message){
  console.error("[QH AUTH]",message);
  try {
    let el=document.getElementById("qh-auth-diagnostic");
    if(!el){
      el=document.createElement("div");
      el.id="qh-auth-diagnostic";
      Object.assign(el.style,{position:"fixed",zIndex:"2147483647",left:"12px",right:"12px",bottom:"18px",padding:"14px 16px",borderRadius:"12px",background:"#172c29",color:"#fff",font:"bold 14px/1.6 sans-serif",direction:"rtl",textAlign:"right",boxShadow:"0 4px 24px #0008"});
      document.body.appendChild(el);
    }
    el.textContent=message;
    el.style.display="block";
  } catch (_) {}
}
async function reservePlayerId(uid){
  for(let attempt=0;attempt<8;attempt++){
    const id=makeId();
    try{
      await runTransaction(db,async tx=>{
        const ref=doc(db,"playerIds",id);
        const snap=await tx.get(ref);
        if(snap.exists())throw new Error("ID_TAKEN");
        tx.set(ref,{uid,createdAt:serverTimestamp()});
      });
      return id;
    }catch(e){if(e.message!=="ID_TAKEN")throw e;}
  }
  throw new Error("تعذر إنشاء معرف لاعب، حاول مرة أخرى");
}
// Share one profile-creation operation per UID. signInWithCredential triggers
// onAuthStateChanged while signIn() also calls saveProfile(); without this lock
// both paths can reserve different IDs and race to create the same user document.
const profileJobs = new Map();
async function saveProfile(user){
  const uid=user.uid;
  if(profileJobs.has(uid)) return profileJobs.get(uid);
  const job=(async()=>{
    let stage="قراءة ملف اللاعب";
    try{
      const ref=doc(db,"users",uid);
      const snap=await getDoc(ref);
      if(snap.exists()){
        const p=snap.data();
        window.QHApplyProfile?.(p,user);
        return p;
      }
      stage="حجز معرّف اللاعب";
      const suggested=cleanName(user.displayName)||"لاعب جديد";
      const id=await reservePlayerId(uid);
      stage="إنشاء ملف اللاعب";
      const p={uid,displayName:suggested,avatarIndex:0,playerId:id,createdAt:serverTimestamp(),updatedAt:serverTimestamp()};
      await setDoc(ref,p);
      window.QHApplyProfile?.(p,user);
      return p;
    }catch(e){
      throw new Error(stage+": "+errorText(e));
    }
  })();
  profileJobs.set(uid,job);
  try{return await job;}
  finally{if(profileJobs.get(uid)===job) profileJobs.delete(uid);}
}
async function signIn(){
  let stage="فتح نافذة اختيار حساب Google";
  authNotice("جاري فتح تسجيل Google...");
  try{
    const result=await FirebaseAuthentication.signInWithGoogle();
    const idToken=result?.credential?.idToken;
    const accessToken=result?.credential?.accessToken;
    if(!idToken && !accessToken){
      const keys=result?.credential?Object.keys(result.credential).join(", "):"لا يوجد credential";
      throw new Error("اختيار الحساب انتهى لكن لم يصل رمز Google. بيانات credential: "+keys);
    }
    stage="التحقق من الحساب لدى Firebase";
    const credential=GoogleAuthProvider.credential(idToken||null,accessToken||null);
    const signed=await signInWithCredential(auth,credential);
    stage="حفظ ملف اللاعب ومعرّفه في Firestore";
    const profile=await saveProfile(signed.user);
    window.QHApplyProfile?.(profile,signed.user);
    authNotice("تم ربط حسابك وحفظ ملفك بنجاح ☕");
    return profile;
  }catch(e){
    const message="تعذر "+stage+": "+errorText(e);
    authNotice(message);
    return null;
  }
}
async function updateProfile(displayName,avatarIndex){
  const user=auth.currentUser;if(!user)throw new Error("سجل دخولك الأول");
  const name=cleanName(displayName);if(name.length<2)throw new Error("الاسم لازم يكون حرفين على الأقل");
  const ref=doc(db,"users",user.uid);
  await setDoc(ref,{displayName:name,avatarIndex:Number(avatarIndex)||0,updatedAt:serverTimestamp()},{merge:true});
  const p=(await getDoc(ref)).data();window.QHApplyProfile?.(p,user);return p;
}
async function signOut(){
  await FirebaseAuthentication.signOut();
  const {signOut:jsSignOut}=await import('firebase/auth');
  await jsSignOut(auth);
  window.QHApplySignedOut?.();
}
async function restore(){
  const user=auth.currentUser;
  if(user){try{await saveProfile(user);}catch(e){console.warn("QH restore/profile",e);window.showToast?.("تعذر تحميل ملف اللاعب: "+errorText(e));}}
}
window.QHAuth={signIn,updateProfile,signOut,restore,get currentUser(){return auth.currentUser;},get db(){return db;}};
window.QHAuthReady=true;
console.info("[QH AUTH] Firebase auth bundle initialized; native="+Capacitor.isNativePlatform());
onAuthStateChanged(auth,user=>{if(user)restore().catch(e=>console.warn("QH auth state",e));});
window.addEventListener("DOMContentLoaded",()=>setTimeout(restore,300));
