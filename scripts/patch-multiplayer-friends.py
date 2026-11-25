from pathlib import Path

path = Path('www/game.html')
src = path.read_text(encoding='utf-8')
marker = '''      <div class="qh-id-row"><div><small>PLAYER ID</small><b>${esc(S.playerId||"لسه مش مربوط بحساب")}</b></div><button class="qh-copy-id" onclick="copyPlayerId()">نسخ المعرف <span>↗</span></button></div>'''
if 'id="qh-friends-panel"' not in src:
    if marker not in src:
        raise SystemExit('Expected PLAYER ID profile row was not found; refusing to patch an unknown layout.')
    panel = marker + r'''
      ${S.authenticated?`<section class="qh-panel" id="qh-friends-panel" style="margin-top:14px;padding:14px;border:1px solid #b98b50;border-radius:16px">
        <div class="qh-section-title"><div class="qh-index">03</div><div><h3>أصحابك في القهوة</h3><p>ضيف أصحابك بمعرّف PLAYER ID</p></div></div>
        <div style="display:flex;gap:8px;direction:ltr;align-items:center"><input id="qh-friend-player-id" class="name-input" maxlength="8" autocomplete="off" placeholder="PLAYER ID" style="min-width:0;flex:1;text-transform:uppercase"><button class="pri" type="button" onclick="qhSendFriendRequest()">إضافة</button></div>
        <p id="qh-friend-status" role="status" style="min-height:22px;font-size:13px;margin:8px 0;color:#f2d18b"></p>
        <div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><b>طلبات الصداقة</b><button class="sec" type="button" onclick="qhRefreshFriends()">تحديث</button></div>
        <div id="qh-friend-requests" style="margin-top:8px"></div>
        <div style="margin-top:14px"><b>قائمة الأصدقاء</b><div id="qh-friend-list" style="margin-top:8px"></div></div>
      </section>`:''}'''
    src = src.replace(marker, panel, 1)

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
'''
    close = src.rfind('</script>')
    if close < 0: raise SystemExit('No closing script tag found; refusing to append JavaScript.')
    src = src[:close] + js + '\n' + src[close:]
path.write_text(src, encoding='utf-8')
print('Friend lookup, requests, and friend-list UI patched into game.html.')
