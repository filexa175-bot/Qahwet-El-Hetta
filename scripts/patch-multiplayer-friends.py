from pathlib import Path

path = Path('www/game.html')
src = path.read_text(encoding='utf-8')
marker = '''      <div class="qh-id-row"><div><small>PLAYER ID</small><b>${esc(S.playerId||"لسه مش مربوط بحساب")}</b></div><button class="qh-copy-id" onclick="copyPlayerId()">نسخ المعرف <span>↗</span></button></div>'''
if 'id="qh-friends-panel"' not in src:
    footer = '      <footer class="qh-footer">'
    if footer not in src:
        raise SystemExit('Expected main-screen footer was not found; refusing to patch an unknown layout.')
    panel = r'''
      ${S.authenticated?`<section class="qh-panel" id="qh-friends-panel" style="margin-top:16px;padding:16px;border:1px solid #c49a5b66;border-radius:20px;background:linear-gradient(145deg,#173f43 0%,#102f35 100%);box-shadow:0 12px 28px #071d2040;color:#f8f0df">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:15px">
          <div aria-hidden="true" style="width:44px;height:44px;flex:0 0 44px;border-radius:14px;display:grid;place-items:center;background:#d4ad6c1c;border:1px solid #d4ad6c70">
            <svg viewBox="0 0 24 24" width="25" height="25" fill="none" stroke="#e2bd7d" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h13v7a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4V8Z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17M7 4c0 1 1 1 1 2M12 3c0 1 1 1 1 2M5 22h14"/></svg>
          </div>
          <div style="min-width:0;flex:1"><div style="font-size:17px;font-weight:800;color:#f5dfb8">أصحابك في القهوة</div><div style="font-size:12px;color:#c7d4cf;margin-top:3px">كوّن شِلّتك والعبوا سوا</div></div>
          <span aria-hidden="true" style="font-size:20px;color:#d9b779">♧</span>
        </div>
        <div style="padding:12px;border:1px solid #d2ad7650;border-radius:15px;background:#0c292e80">
          <div style="font-size:12px;color:#d8bd8c;margin-bottom:8px">إضافة صديق باستخدام PLAYER ID</div>
          <div style="display:flex;gap:8px;direction:ltr;align-items:center"><input id="qh-friend-player-id" class="name-input" maxlength="8" autocomplete="off" placeholder="PLAYER ID" aria-label="PLAYER ID للصديق" style="min-width:0;flex:1;text-transform:uppercase;border:1px solid #b98b50;border-radius:10px"><button class="pri" type="button" onclick="qhSendFriendRequest()" style="white-space:nowrap">إضافة +</button></div>
          <p id="qh-friend-status" role="status" aria-live="polite" style="min-height:20px;font-size:12px;margin:8px 0 0;color:#f2d18b"></p>
        </div>
        <div style="margin-top:15px">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><b style="font-size:14px;color:#f5dfb8">طلبات الصداقة</b><button class="sec" type="button" onclick="qhRefreshFriends()" style="font-size:12px">↻ تحديث</button></div>
          <div id="qh-friend-requests" style="margin-top:8px;font-size:13px;color:#d9e2dc"></div>
        </div>
        <div style="margin-top:15px;padding-top:13px;border-top:1px solid #d2ad7640">
          <div style="display:flex;align-items:center;gap:7px"><span aria-hidden="true" style="color:#e2bd7d">●</span><b style="font-size:14px;color:#f5dfb8">قائمة الأصدقاء</b></div>
          <div id="qh-friend-list" style="margin-top:8px;font-size:13px;color:#d9e2dc"></div>
        </div>
      </section>`:''}'''
    src = src.replace('      <footer class="qh-footer">', panel + '\n      <footer class="qh-footer">', 1)

js_marker = '/* QH FRIENDS UI */'
if js_marker not in src:
    js = r'''
/* QH FRIENDS UI */
function qhFriendNode(tag,text,cls){
 const el=document.createElement(tag);if(text!==undefined)el.textContent=String(text);if(cls)el.className=cls;return el;
}
async function qhSendFriendRequest(){
 const input=document.getElementById('qh-friend-player-id');
 const status=document.getElementById('qh-friend-status');
 if(!input||!status)return;
 const id=input.value.trim().toUpperCase();
 status.textContent='جاري البحث عن اللاعب...';
 try{
  const target=await window.QHFriends.sendFriendRequest(id);
  status.textContent='اتبعث طلب الصداقة إلى '+(target.displayName||'اللاعب')+' بنجاح ☕';
  input.value='';
  await qhRefreshFriends();
 }catch(e){status.textContent=e?.message||'تعذر إرسال طلب الصداقة';}
}
async function qhRefreshFriends(){
 const requestsBox=document.getElementById('qh-friend-requests');
 const friendsBox=document.getElementById('qh-friend-list');
 if(!requestsBox||!friendsBox)return;
 requestsBox.textContent='جاري تحميل الطلبات...';friendsBox.textContent='جاري تحميل الأصدقاء...';
 try{
  const data=await window.QHFriends.listFriendRequests();
  requestsBox.replaceChildren();
  if(!data.incoming.length&&!data.outgoing.length)requestsBox.append(qhFriendNode('p','لا توجد طلبات صداقة حاليًا.'));
  data.incoming.forEach(item=>{
   const row=qhFriendNode('div',undefined);row.style.cssText='display:flex;gap:8px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:9px;margin:7px 0;border:1px solid #b98b50;border-radius:12px';
   row.append(qhFriendNode('span','PLAYER ID: '+(item.fromPlayerId||'غير متاح')));
   const actions=qhFriendNode('span',undefined);const yes=qhFriendNode('button','قبول','pri');const no=qhFriendNode('button','رفض','sec');
   yes.type=no.type='button';yes.addEventListener('click',()=>qhRespondFriendRequest(item.id,true));no.addEventListener('click',()=>qhRespondFriendRequest(item.id,false));actions.append(yes,no);row.append(actions);requestsBox.append(row);
  });
  if(data.outgoing.length)requestsBox.append(qhFriendNode('p','طلبات مرسلة معلّقة: '+data.outgoing.length));
  const friends=await window.QHFriends.listFriends();friendsBox.replaceChildren();
  if(!friends.length)friendsBox.append(qhFriendNode('p','لسه مفيش أصدقاء مضافين.'));
  friends.forEach(friend=>{
   const row=qhFriendNode('div',undefined);row.style.cssText='display:flex;justify-content:space-between;gap:8px;padding:8px 2px;border-bottom:1px solid #b98b5055';
   row.append(qhFriendNode('span',(friend.displayName||'لاعب')+' · '+(friend.playerId||'')));
   row.append(qhFriendNode('b',friend.online?'متصل الآن':'غير متصل'));friendsBox.append(row);
  });
 }catch(e){requestsBox.textContent=e?.message||'تعذر تحميل طلبات الصداقة';friendsBox.textContent='تعذر تحميل قائمة الأصدقاء';}
}
async function qhRespondFriendRequest(id,accept){
 const status=document.getElementById('qh-friend-status');if(status)status.textContent=accept?'جاري قبول الطلب...':'جاري رفض الطلب...';
 try{await window.QHFriends.respondFriendRequest(id,accept);if(status)status.textContent=accept?'تم قبول طلب الصداقة ☕':'تم رفض الطلب';await qhRefreshFriends();}
 catch(e){if(status)status.textContent=e?.message||'تعذر تحديث الطلب';}
}

// Load the friends panel automatically only after Google authentication renders it.
(function qhObserveFriendsPanel(){
 if(typeof MutationObserver==='undefined'||!document.body)return;
 const load=()=>{const panel=document.getElementById('qh-friends-panel');if(panel&&!panel.dataset.loaded){panel.dataset.loaded='1';qhRefreshFriends();}};
 load();
 const observer=new MutationObserver(load);
 observer.observe(document.body,{childList:true,subtree:true});
})();
'''
    close = src.rfind('</script>')
    if close < 0: raise SystemExit('No closing script tag found; refusing to append JavaScript.')
    src = src[:close] + js + '\n' + src[close:]
path.write_text(src, encoding='utf-8')
print('Friend lookup, requests, and friend-list UI patched into game.html.')
