import { Capacitor } from '@capacitor/core';
import { initializeApp } from 'firebase/app';
import { getAuth, initializeAuth, indexedDBLocalPersistence, GoogleAuthProvider, signInWithCredential, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, doc, getDoc, setDoc, runTransaction, serverTimestamp, collection, query, where, getDocs, updateDoc } from 'firebase/firestore';
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
        if(p.playerId) await setDoc(doc(db,"publicProfiles",p.playerId),{uid,playerId:p.playerId,displayName:p.displayName||"لاعب",avatarIndex:Number(p.avatarIndex)||0,updatedAt:serverTimestamp()},{merge:true});
        window.QHApplyProfile?.(p,user);
        setTimeout(loadWallet,350);
        return p;
      }
      stage="حجز معرّف اللاعب";
      const suggested=cleanName(user.displayName)||"لاعب جديد";
      const id=await reservePlayerId(uid);
      stage="إنشاء ملف اللاعب";
      const p={uid,displayName:suggested,avatarIndex:0,playerId:id,createdAt:serverTimestamp(),updatedAt:serverTimestamp()};
      await setDoc(ref,p);
      await setDoc(doc(db,"publicProfiles",id),{uid,playerId:id,displayName:suggested,avatarIndex:0,updatedAt:serverTimestamp()});
      window.QHApplyProfile?.(p,user);
      setTimeout(loadWallet,350);
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
    // saveProfile applies the profile and shows the single temporary success toast.
    // Keep the persistent diagnostic notice for errors only.
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
  const p=(await getDoc(ref)).data();
  if(p?.playerId)await setDoc(doc(db,"publicProfiles",p.playerId),{uid:user.uid,playerId:p.playerId,displayName:name,avatarIndex:Number(avatarIndex)||0,updatedAt:serverTimestamp()},{merge:true});
  window.QHApplyProfile?.(p,user);return p;
}
const walletRefFor = uid => doc(db,"wallets",uid);
const walletCacheKey = uid => "qh_wallet_cache_v1_" + uid;
const walletInitialData = uid => ({
  uid, balance: 500, totalEarned: 500,
  registrationGiftClaimed: true,
  lastDailyGiftAt: null,
  createdAt: serverTimestamp(),
  updatedAt: serverTimestamp()
});
const DAILY_GIFT_MS = 24 * 60 * 60 * 1000;
let walletLoadJob = null;
let currentWalletData = null;

function readWalletCache(uid){
  try{
    const raw=localStorage.getItem(walletCacheKey(uid));
    if(!raw)return null;
    const data=JSON.parse(raw);
    if(!data || !Number.isFinite(Number(data.balance)))return null;
    return data;
  }catch(_){return null;}
}
function writeWalletCache(uid,data){
  try{
    const last=data.lastDailyGiftAt?.toMillis?.() ??
      (typeof data.lastDailyGiftAt==="number"?data.lastDailyGiftAt:null);
    const safe={
      balance:Number(data.balance||0),
      totalEarned:Number(data.totalEarned||0),
      lastDailyGiftAt:last
    };
    localStorage.setItem(walletCacheKey(uid),JSON.stringify(safe));
  }catch(_){}
}
function paintWallet(data){
  if(!data)return;
  currentWalletData=data;
  const balanceEl=document.getElementById("qh-wallet-balance");
  const noteEl=document.getElementById("qh-wallet-note");
  const giftBtn=document.getElementById("qh-daily-gift");
  const last=data.lastDailyGiftAt?.toMillis?.() ??
    (typeof data.lastDailyGiftAt==="number"?data.lastDailyGiftAt:null);
  const ready=last===null || (Date.now()-last)>=DAILY_GIFT_MS;
  if(balanceEl)balanceEl.textContent=Number(data.balance||0).toLocaleString("en-US")+" عملة";
  if(giftBtn){giftBtn.disabled=!ready;giftBtn.textContent=ready?"🎁 استلام الهدية اليومية · 500 عملة":"✓ الهدية اليومية مستلمة";}
  if(noteEl)noteEl.textContent=ready?"هدية 500 عملة متاحة بعد مرور 24 ساعة على آخر استلام.":"تقدر تستلم هدية جديدة بعد مرور 24 ساعة على آخر استلام.";
}

async function loadWallet(){
  const user=auth.currentUser;
  if(!user)return null;
  // Paint the last known balance immediately; Firebase refreshes it below.
  const cached=readWalletCache(user.uid);
  if(cached)paintWallet(cached);
  if(walletLoadJob)return walletLoadJob;
  walletLoadJob=(async()=>{
    try{
      const ref=walletRefFor(user.uid);
      let snap=await getDoc(ref);
      if(!snap.exists()){
        // Create the starter wallet only when it truly does not exist.
        await runTransaction(db,async tx=>{
          const fresh=await tx.get(ref);
          if(!fresh.exists())tx.set(ref,walletInitialData(user.uid));
        });
        snap=await getDoc(ref);
      }
      if(!snap.exists())throw new Error("wallet document missing after initialization");
      const data=snap.data();
      writeWalletCache(user.uid,data);
      paintWallet(data);
      return data;
    }catch(e){
      // Keep a previously cached balance visible during temporary network errors.
      if(!cached){
        const balanceEl=document.getElementById("qh-wallet-balance");
        const giftBtn=document.getElementById("qh-daily-gift");
        const noteEl=document.getElementById("qh-wallet-note");
        if(balanceEl)balanceEl.textContent="تعذر تحميل الرصيد";
        if(giftBtn)giftBtn.disabled=true;
        if(noteEl)noteEl.textContent="تعذر تحديث المحفظة. الرصيد المحفوظ سيظهر عند توفر الاتصال.";
      }
      console.warn("[QH WALLET] load",e);
      return cached;
    }finally{walletLoadJob=null;}
  })();
  return walletLoadJob;
}

async function claimDailyGift(){
  const user=auth.currentUser;
  const giftBtn=document.getElementById("qh-daily-gift");
  const noteEl=document.getElementById("qh-wallet-note");
  const balanceEl=document.getElementById("qh-wallet-balance");
  if(!user) { if(noteEl)noteEl.textContent="سجل دخولك الأول."; return null; }
  if(giftBtn){giftBtn.disabled=true;giftBtn.textContent="جارٍ استلام الهدية...";}
  try{
    const ref=walletRefFor(user.uid);
    const result=await runTransaction(db,async tx=>{
      const snap=await tx.get(ref);
      if(!snap.exists()){
        tx.set(ref,walletInitialData(user.uid));
        return {claimed:false,balance:500,reason:"initialized"};
      }
      const wallet=snap.data();
      const last=wallet.lastDailyGiftAt?.toMillis?.() ?? null;
      if(last!==null && (Date.now()-last)<DAILY_GIFT_MS){
        return {claimed:false,balance:Number(wallet.balance||0),reason:"already-claimed"};
      }
      const balance=Number(wallet.balance||0)+500;
      tx.update(ref,{
        balance,
        totalEarned:Number(wallet.totalEarned||0)+500,
        lastDailyGiftAt:serverTimestamp(),
        updatedAt:serverTimestamp()
      });
      return {claimed:true,balance};
    });
    if(balanceEl)balanceEl.textContent=Number(result.balance||0).toLocaleString("en-US")+" عملة";
    const latest=(await getDoc(ref)).data();
    if(latest){writeWalletCache(user.uid,latest);paintWallet(latest);}
    if(giftBtn){giftBtn.disabled=true;giftBtn.textContent="✓ الهدية اليومية مستلمة";}
    if(noteEl)noteEl.textContent=result.claimed?"مبروك! اتضاف 500 عملة لرصيدك.":"هدية التسجيل موجودة بالفعل. حاول بعد 24 ساعة لاستلام الهدية اليومية.";
    window.QHShowToast?.(result.claimed?"🎁 استلمت 500 عملة هدية يومية":"الهدية اليومية غير متاحة حاليًا");
    return result;
  }catch(e){
    if(giftBtn){giftBtn.disabled=false;giftBtn.textContent="🎁 استلام الهدية اليومية · 500 عملة";}
    if(noteEl)noteEl.textContent="تعذر استلام الهدية. حاول مرة أخرى.";
    console.warn("[QH WALLET] claim",e);
    return null;
  }
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

// Lightweight friends foundation: public player lookup and friend requests.
async function findPlayerById(playerId){
  const id=String(playerId||"").trim().toUpperCase();
  if(!/^[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{8}$/.test(id))throw new Error("اكتب PLAYER ID صحيح من 8 خانات");
  const snap=await getDoc(doc(db,"publicProfiles",id));
  if(!snap.exists())return null;
  const p=snap.data();if(p.uid===auth.currentUser?.uid)return {self:true,...p};
  return p;
}
async function sendFriendRequest(playerId){
  const user=auth.currentUser;if(!user)throw new Error("سجل دخولك الأول");
  const target=await findPlayerById(playerId);if(!target)throw new Error("مش لاقيين لاعب بالمعرف ده");
  if(target.self)throw new Error("مينفعش تبعت طلب لنفسك");
  const requestId=user.uid+"__"+target.uid;
  const ref=doc(db,"friendRequests",requestId);
  const old=await getDoc(ref);if(old.exists())throw new Error("فيه طلب صداقة موجود بالفعل");
  await setDoc(ref,{fromUid:user.uid,toUid:target.uid,fromPlayerId:window.QHProfile?.playerId||"",toPlayerId:target.playerId,status:"pending",createdAt:serverTimestamp()});
  return target;
}
async function listFriendRequests(){
 const user=auth.currentUser;if(!user)throw new Error("سجل دخولك الأول");
 const incoming=await getDocs(query(collection(db,"friendRequests"),where("toUid","==",user.uid)));
 const outgoing=await getDocs(query(collection(db,"friendRequests"),where("fromUid","==",user.uid)));
 return {incoming:incoming.docs.map(x=>({id:x.id,...x.data()})).filter(x=>x.status==="pending"),outgoing:outgoing.docs.map(x=>({id:x.id,...x.data()})).filter(x=>x.status==="pending")};
}
async function respondFriendRequest(requestId,accept){
 const user=auth.currentUser;if(!user)throw new Error("سجل دخولك الأول");
 const ref=doc(db,"friendRequests",requestId);
 await runTransaction(db,async tx=>{const snap=await tx.get(ref);if(!snap.exists()||snap.data().toUid!==user.uid||snap.data().status!=="pending")throw new Error("طلب الصداقة غير متاح");tx.update(ref,{status:accept?"accepted":"declined",respondedAt:serverTimestamp()});});
 return true;
}
window.QHFriends={findPlayerById,sendFriendRequest,listFriendRequests,respondFriendRequest};

window.QHAuth={signIn,updateProfile,signOut,restore,loadWallet,claimDailyGift,get currentUser(){return auth.currentUser;},get db(){return db;}};
window.QHAuthReady=true;
console.info("[QH AUTH] Firebase auth bundle initialized; native="+Capacitor.isNativePlatform());
onAuthStateChanged(auth,user=>{if(user)restore().catch(e=>console.warn("QH auth state",e));});
window.addEventListener("DOMContentLoaded",()=>setTimeout(restore,300));
