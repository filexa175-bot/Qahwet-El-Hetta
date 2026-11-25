from pathlib import Path
import re
p=Path("www/game.html")
s=p.read_text(encoding="utf-8")
pattern=r'\n\s*\\$'+'{S\\.authenticated\\?[\x60]<section class="qh-panel" id="qh-friends-panel"[\s\S]*?</section>[\x60]:\'\'}'
s,n=re.subn(pattern,"",s,count=1)
if n!=1: raise SystemExit("Could not remove exactly one previous friends card: "+str(n))
a=s.find("/* QH FRIENDS UI */")
if a<0: raise SystemExit("Previous friends UI marker missing")
b=s.find("</script>",a)
if b<0: raise SystemExit("Closing script tag missing")
js=r"""
/* Persistent floating friends icon and modal */
(function(){
 const ROOT="qh-friends-float-root",by=id=>document.getElementById(id);
 const el=(tag,cls,txt)=>{const x=document.createElement(tag);if(cls)x.className=cls;if(txt!==undefined)x.textContent=String(txt);return x;};
 const css=[
 '#'+ROOT+'{position:fixed;z-index:1250;top:calc(5px + env(safe-area-inset-top));right:max(54px,calc((100vw - 560px)/2 + 54px));font-family:Cairo,system-ui;direction:rtl;pointer-events:none}',
 '#'+ROOT+' *{box-sizing:border-box;font-family:Cairo,system-ui}',
 '#qh-friends-float-button{pointer-events:auto;width:39px;height:34px;display:grid;place-items:center;position:relative;border:1px solid #b89a62;border-radius:12px;background:linear-gradient(145deg,#25464a,#142d31);color:#f5dfb8;box-shadow:0 3px 10px #0006;cursor:pointer;padding:0}',
 '#qh-friends-float-button svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}',
 '#qh-friends-float-badge{position:absolute;top:-5px;left:-5px;min-width:16px;height:16px;padding:0 4px;border-radius:20px;background:#c74a42;color:#fff;font-size:10px;font-weight:900;display:none;align-items:center;justify-content:center;border:1px solid #f5dfb8}',
 '#qh-friends-overlay{position:fixed;inset:0;z-index:2147483000;background:#061719c9;backdrop-filter:blur(7px);display:flex;align-items:center;justify-content:center;padding:16px;direction:rtl}',
 '#qh-friends-dialog{width:min(100%,440px);max-height:82dvh;overflow:auto;border:1px solid #b99a63;border-radius:22px;background:linear-gradient(155deg,#1b4145,#102d32 72%,#0d252b);color:#f7f0df;box-shadow:0 20px 70px #0009;padding:16px}',
 '#qh-friends-dialog button{cursor:pointer;font-weight:800}',
 '.qhf-head{display:flex;align-items:center;gap:10px;margin-bottom:14px}.qhf-head-icon{width:42px;height:42px;display:grid;place-items:center;border:1px solid #c8a86c66;border-radius:14px;background:#d3ad6820;color:#e5c78d;font-size:22px}',
 '.qhf-title{font-size:17px;font-weight:900;color:#f4dfb7}.qhf-sub{font-size:11px;color:#c2d0c9;margin-top:2px}.qhf-close{margin-right:auto;width:32px;height:32px;border:1px solid #ffffff30;border-radius:10px;background:#ffffff0c;color:#f6e8c9;font-size:18px}',
 '.qhf-card{padding:12px;margin-top:10px;border:1px solid #c6a56a45;border-radius:15px;background:#0b252b80}.qhf-label{font-size:12px;color:#e4c88e;font-weight:800;margin-bottom:8px}',
 '.qhf-addrow{display:flex;gap:7px;direction:ltr}.qhf-addrow input{min-width:0;flex:1;height:40px;border:1px solid #b89a62;border-radius:10px;background:#f8f1e3;color:#1b3333;padding:0 10px;text-transform:uppercase;text-align:center;font-weight:900;letter-spacing:1px}',
 '.qhf-primary,.qhf-secondary{border-radius:10px;padding:8px 12px;border:1px solid #c7a66c;font-size:12px}.qhf-primary{background:linear-gradient(145deg,#d6b779,#b38a4c);color:#183437}.qhf-secondary{background:#ffffff0d;color:#f5e8cb;border-color:#ffffff38}',
 '.qhf-status{font-size:11px;color:#efd18e;min-height:17px;margin:7px 0 0}.qhf-section-title{display:flex;align-items:center;justify-content:space-between;font-size:13px;font-weight:900;color:#f3dfb8;margin-bottom:7px}.qhf-list{display:grid;gap:7px}.qhf-empty{font-size:12px;color:#bdcbc5;padding:7px 2px}',
 '.qhf-row{display:flex;align-items:center;gap:8px;padding:9px;border:1px solid #ffffff16;border-radius:12px;background:#ffffff08}.qhf-avatar{width:32px;height:32px;flex:0 0 32px;border-radius:11px;display:grid;place-items:center;background:#d4ad6820;color:#f2d69e;font-size:16px}.qhf-person{min-width:0;flex:1}.qhf-name{font-size:12px;font-weight:800;color:#f6ecd7}.qhf-id{font-size:10px;color:#b8c8c1;direction:ltr;text-align:right}.qhf-presence{font-size:10px;white-space:nowrap;color:#c8d4cb}.qhf-dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-left:4px;background:#7b8b83}.qhf-dot.online{background:#61d49b;box-shadow:0 0 7px #61d49b88}.qhf-actions{display:flex;gap:5px}.qhf-actions button{padding:6px 8px;font-size:10px;border-radius:8px;border:1px solid #ffffff30;background:#ffffff0d;color:#f6e8c9}.qhf-actions .accept{background:#d0b176;color:#173337;border-color:#d0b176}'
 ].join('\n');
 function style(){if(!by("qh-friends-float-style")){const s=el("style");s.id="qh-friends-float-style";s.textContent=css;document.head.appendChild(s);}}
 function root(){style();let r=by(ROOT);if(r)return r;r=el("div");r.id=ROOT;r.innerHTML='<button id="qh-friends-float-button" type="button" aria-label="الأصدقاء والطلبات"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M20 8v6M17 11h6"/></svg><span id="qh-friends-float-badge"></span></button>';document.body.appendChild(r);by("qh-friends-float-button").addEventListener("click",open);return r;}
 function close(){by("qh-friends-overlay")?.remove();}
 function open(){
  close();const ov=el("div");ov.id="qh-friends-overlay";const box=el("div");box.id="qh-friends-dialog";const h=el("div","qhf-head");h.append(el("div","qhf-head-icon","♧"));const t=el("div");t.append(el("div","qhf-title","أصحابك في القهوة"),el("div","qhf-sub","قائمة أصحابك وطلبات الصداقة"));h.append(t);const x=el("button","qhf-close","×");x.addEventListener("click",close);h.append(x);box.append(h);
  if(!window.QHAuth?.currentUser){const c=el("div","qhf-card");c.append(el("div","qhf-label","اربط حسابك الأول"),el("div","qhf-empty","سجّل الدخول بحساب Google علشان تضيف أصحابك وتستقبل الطلبات."));const login=el("button","qhf-primary","تسجيل الدخول");login.addEventListener("click",()=>window.QHAuth?.signIn());c.append(login);box.append(c);}
  else{
   const c=el("div","qhf-card");c.append(el("div","qhf-label","إضافة صديق باستخدام PLAYER ID"));const row=el("div","qhf-addrow"),input=el("input"),send=el("button","qhf-primary","إضافة +");input.id="qhf-player-id";input.maxLength=8;input.placeholder="PLAYER ID";input.autocomplete="off";send.addEventListener("click",sendRequest);row.append(input,send);c.append(row);const st=el("p","qhf-status","");st.id="qhf-status";c.append(st);box.append(c);
   const rc=el("div","qhf-card"),rt=el("div","qhf-section-title","طلبات الصداقة"),refresh=el("button","qhf-secondary","تحديث ↻"),rq=el("div","qhf-list");refresh.addEventListener("click",refreshFriends);rt.append(refresh);rq.id="qhf-requests";rc.append(rt,rq);box.append(rc);
   const fc=el("div","qhf-card");fc.append(el("div","qhf-section-title","قائمة الأصدقاء"));const fl=el("div","qhf-list");fl.id="qhf-friends";fc.append(fl);box.append(fc);
   const me=el("div");me.style.cssText="margin-top:10px;text-align:center;font-size:10px;color:#b8c8c1";me.textContent="PLAYER ID الخاص بي: "+(window.S?.playerId||"—");box.append(me);refreshFriends();
  }
  ov.append(box);ov.addEventListener("click",e=>{if(e.target===ov)close();});document.body.append(ov);
 }
 async function sendRequest(){const i=by("qhf-player-id"),st=by("qhf-status");if(!i||!st)return;const id=i.value.trim().toUpperCase();if(!id){st.textContent="اكتب PLAYER ID الأول";return;}st.textContent="جاري إرسال الطلب...";try{const target=await window.QHFriends.sendFriendRequest(id);st.textContent="تم إرسال الطلب إلى "+(target.displayName||"اللاعب")+" ☕";i.value="";await refreshFriends();}catch(e){st.textContent=e?.message||"تعذر إرسال طلب الصداقة";}}
 function person(name,id,online){const r=el("div","qhf-row");r.append(el("div","qhf-avatar","♟"));const p=el("div","qhf-person");p.append(el("div","qhf-name",name||"لاعب"),el("div","qhf-id",id||""));r.append(p);const st=el("span","qhf-presence");st.append(el("i","qhf-dot"+(online?" online":"")));st.append(document.createTextNode(online?"متصل":"غير متصل"));r.append(st);return r;}
 async function refreshFriends(){const rq=by("qhf-requests"),fb=by("qhf-friends");if(!rq||!fb||!window.QHFriends)return;rq.replaceChildren(el("div","qhf-empty","جاري تحميل الطلبات..."));fb.replaceChildren(el("div","qhf-empty","جاري تحميل الأصدقاء..."));try{const d=await window.QHFriends.listFriendRequests();rq.replaceChildren();if(!d.incoming.length&&!d.outgoing.length)rq.append(el("div","qhf-empty","مفيش طلبات صداقة حاليًا."));d.incoming.forEach(item=>{const r=el("div","qhf-row");r.append(el("div","qhf-avatar","✉"));const p=el("div","qhf-person");p.append(el("div","qhf-name","طلب صداقة جديد"),el("div","qhf-id",item.fromPlayerId||""));r.append(p);const a=el("div","qhf-actions"),yes=el("button","accept","قبول"),no=el("button","","رفض");yes.addEventListener("click",()=>respond(item.id,true));no.addEventListener("click",()=>respond(item.id,false));a.append(yes,no);r.append(a);rq.append(r);});if(d.outgoing.length)rq.append(el("div","qhf-empty","طلبات مرسلة معلّقة: "+d.outgoing.length));const list=await window.QHFriends.listFriends();fb.replaceChildren();if(!list.length)fb.append(el("div","qhf-empty","لسه مفيش أصحاب — ابدأ بإضافة PLAYER ID."));list.forEach(f=>fb.append(person(f.displayName,f.playerId,f.online)));const badge=by("qh-friends-float-badge");if(badge){const n=d.incoming.length;badge.textContent=n>9?"9+":String(n);badge.style.display=n?"flex":"none";}}catch(e){rq.replaceChildren(el("div","qhf-empty",e?.message||"تعذر تحميل الطلبات"));fb.replaceChildren(el("div","qhf-empty","تعذر تحميل قائمة الأصدقاء"));}}
 async function respond(id,accept){const st=by("qhf-status");if(st)st.textContent=accept?"جاري قبول الطلب...":"جاري رفض الطلب...";try{await window.QHFriends.respondFriendRequest(id,accept);if(st)st.textContent=accept?"تم قبول طلب الصداقة ☕":"تم رفض الطلب";await refreshFriends();}catch(e){if(st)st.textContent=e?.message||"تعذر تحديث الطلب";}}
 let timer=null;function badge(){if(!window.QHAuth?.currentUser||!window.QHFriends)return;window.QHFriends.listFriendRequests().then(d=>{const b=by("qh-friends-float-badge");if(!b)return;const n=d.incoming.length;b.textContent=n>9?"9+":String(n);b.style.display=n?"flex":"none";}).catch(()=>{});}
 function ensure(){root();if(window.QHAuth?.currentUser){badge();if(!timer)timer=setInterval(badge,45000);}}
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",ensure,{once:true});else ensure();
 const obs=new MutationObserver(()=>{if(!by(ROOT))ensure();else if(window.QHAuth?.currentUser&&!timer)ensure();});obs.observe(document.documentElement,{childList:true,subtree:true});
 window.QHFriendsOpen=open;
})();
"""
s=s[:a]+js+"\n"+s[b:]
p.write_text(s,encoding="utf-8")
print("Persistent friends icon/modal installed; previous inline card removed.")
