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
async function saveProfile(user){
  const ref=doc(db,"users",user.uid);
  const snap=await getDoc(ref);
  if(snap.exists()){
    const p=snap.data();
    window.QHApplyProfile?.(p,user);
    return p;
  }
  const suggested=cleanName(user.displayName)||"لاعب جديد";
  const id=await reservePlayerId(user.uid);
  const p={uid:user.uid,displayName:suggested,avatarIndex:0,playerId:id,createdAt:serverTimestamp(),updatedAt:serverTimestamp()};
  await setDoc(ref,p);
  window.QHApplyProfile?.(p,user);
  return p;
}
async function signIn(){
  try{
    window.showToast?.("جاري فتح تسجيل Google...");
    const result=await FirebaseAuthentication.signInWithGoogle();
    if(!result.credential?.idToken)throw new Error("لم نستلم رمز Google");
    const credential=GoogleAuthProvider.credential(result.credential.idToken);
    const signed=await signInWithCredential(auth,credential);
    const profile=await saveProfile(signed.user);
    window.QHApplyProfile?.(profile,signed.user);
    window.showToast?.("أهلاً بيك في قهوة الحتة ☕");
    return profile;
  }catch(e){
    console.error("QH sign in",e);
    window.showToast?.("تعذر تسجيل الدخول: "+(e.message||"حاول مرة أخرى"));
    throw e;
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
  if(user){try{await saveProfile(user);}catch(e){console.warn(e);}}
}
window.QHAuth={signIn,updateProfile,signOut,restore,get currentUser(){return auth.currentUser;},get db(){return db;}};
onAuthStateChanged(auth,user=>{if(user)restore().catch(console.warn);});
window.addEventListener("DOMContentLoaded",()=>setTimeout(restore,300));
