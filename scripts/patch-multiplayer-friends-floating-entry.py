from pathlib import Path
p=Path("www/game.html")
s=p.read_text(encoding="utf-8")
if "QH FRIENDS FLOATING ENTRY" in s:
    print("Floating friends entry already present.")
    raise SystemExit(0)
addon=r"""
<!-- QH FRIENDS FLOATING ENTRY -->
<style id="qh-friends-floating-style">
#qh-friends-panel{display:none!important}
#qh-friends-float-root{position:fixed;z-index:1250;top:calc(5px + env(safe-area-inset-top));right:max(105px,calc((100vw - 560px)/2 + 105px));direction:rtl;pointer-events:none}
#qh-friends-float-button{pointer-events:auto;width:39px;height:34px;display:grid;place-items:center;position:relative;border:1px solid #b89a62;border-radius:12px;background:linear-gradient(145deg,#25464a,#142d31);color:#f5dfb8;box-shadow:0 3px 10px #0006;padding:0}
#qh-friends-float-button svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
#qh-friends-float-badge{position:absolute;top:-5px;left:-5px;min-width:16px;height:16px;padding:0 4px;border-radius:20px;background:#c74a42;color:#fff;font:900 10px Cairo,system-ui;display:none;align-items:center;justify-content:center;border:1px solid #f5dfb8}
#qh-friends-modal{position:fixed;inset:0;z-index:2147483000;background:#061719c9;backdrop-filter:blur(7px);display:flex;align-items:center;justify-content:center;padding:16px;direction:rtl}
#qh-friends-modal-card{width:min(100%,440px);max-height:84dvh;overflow:auto;border:1px solid #b99a63;border-radius:22px;background:linear-gradient(155deg,#1b4145,#102d32 72%,#0d252b);box-shadow:0 20px 70px #0009;padding:12px}
#qh-friends-modal-head{display:flex;align-items:center;gap:10px;padding:4px 4px 10px;color:#f4dfb7;font:900 16px Cairo,system-ui}
#qh-friends-modal-close{margin-right:auto;width:32px;height:32px;border:1px solid #ffffff30;border-radius:10px;background:#ffffff0c;color:#f6e8c9;font-size:18px}
#qh-friends-modal #qh-friends-panel{display:block!important;margin:0!important;max-height:none!important}
</style>
<script>
(function(){
 const id=x=>document.getElementById(x);
 let placeholder=null, panel=null, timer=null;
 function ensure(){
  if(!id("qh-friends-float-root")){
   const root=document.createElement("div");root.id="qh-friends-float-root";
   root.innerHTML='<button id="qh-friends-float-button" type="button" aria-label="الأصدقاء والطلبات" title="الأصدقاء والطلبات"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M20 8v6M17 11h6"/></svg><span id="qh-friends-float-badge"></span></button>';
   document.body.appendChild(root);id("qh-friends-float-button").addEventListener("click",open);
  }
  badge();if(!timer)timer=setInterval(badge,45000);
 }
 function badge(){
  if(!window.QHAuth?.currentUser||!window.QHFriends)return;
  window.QHFriends.listFriendRequests().then(d=>{const b=id("qh-friends-float-badge");if(!b)return;const n=d.incoming.length;b.textContent=n>9?"9+":String(n);b.style.display=n?"flex":"none";}).catch(()=>{});
 }
 function open(){
  if(!window.QHAuth?.currentUser){window.QHShowToast?.("سجّل دخولك بحساب Google علشان تستخدم الأصدقاء");window.QHAuth?.signIn();return;}
  if(id("qh-friends-modal"))return;
  panel=id("qh-friends-panel");
  if(!panel){window.QHShowToast?.("قائمة الأصدقاء غير جاهزة؛ ارجع للشاشة الرئيسية");return;}
  placeholder=document.createElement("div");placeholder.id="qh-friends-modal-placeholder";
  panel.parentNode.insertBefore(placeholder,panel);
  const modal=document.createElement("div");modal.id="qh-friends-modal";
  const card=document.createElement("div");card.id="qh-friends-modal-card";
  const head=document.createElement("div");head.id="qh-friends-modal-head";head.append(document.createTextNode("♧ أصحابك في القهوة"));
  const close=document.createElement("button");close.id="qh-friends-modal-close";close.type="button";close.textContent="×";close.setAttribute("aria-label","إغلاق");close.addEventListener("click",closeModal);head.append(close);
  card.append(head);card.append(panel);modal.append(card);modal.addEventListener("click",e=>{if(e.target===modal)closeModal();});document.body.append(modal);
  panel.style.display="block";panel.dataset.modalOpen="1";window.qhRefreshFriends?.();
 }
 function closeModal(){
  const modal=id("qh-friends-modal");if(!modal)return;
  if(panel&&placeholder?.parentNode){placeholder.parentNode.insertBefore(panel,placeholder);placeholder.remove();}
  if(panel){panel.style.display="";delete panel.dataset.modalOpen;}
  modal.remove();panel=null;placeholder=null;
 }
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",ensure,{once:true});else ensure();
 const observer=new MutationObserver(()=>{if(!id("qh-friends-float-root"))ensure();});observer.observe(document.documentElement,{childList:true,subtree:true});
 window.QHFriendsFloatingOpen=open;
})();
</script>
"""
s=s.replace("</body>",addon+"\n</body>",1)
p.write_text(s,encoding="utf-8")
# Android WebView opens index.html by default; keep both entry documents identical.
Path("www/index.html").write_text(s,encoding="utf-8")
print("Persistent friends icon and modal entry added to both Android entry files.")
