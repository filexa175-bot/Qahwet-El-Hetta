from pathlib import Path
for rel in ("www/index.html", "www/game.html"):
    path = Path(rel)
    src = path.read_text(encoding="utf-8")
    if "qh-friends-panel" in src:
        continue
    marker = "      \${S.mode==='ai'?<section class=\\\"difficulty-section\\\">"
    panel = r'''      \${S.mode==='friend'?<section class="game-section" id="qh-friends-panel"><div class="section-heading"><span class="step">03</span><div><h3>أصحابك في القهوة</h3><small>ابحث عن صاحبك باستخدام PLAYER ID</small></div></div><div style="display:flex;gap:8px;direction:ltr"><input id="qh-friend-player-id" class="name-input" maxlength="8" placeholder="PLAYER ID" style="text-transform:uppercase;min-width:0;flex:1"><button class="pri" onclick="qhSendFriendRequest()">إضافة</button></div><p id="qh-friend-status" style="color:#f2d18b;font-size:13px;min-height:22px"></p><div style="display:flex;justify-content:space-between;align-items:center"><b>طلبات الصداقة الواردة</b><button class="sec" onclick="qhRefreshFriendRequests()">تحديث</button></div><div id="qh-friend-inbox" style="margin-top:10px;color:#fff0d1">اضغط تحديث لعرض الطلبات</div></section>':''}
'''
    if marker not in src:
        raise SystemExit("Cannot find insertion marker in " + rel)
    src = src.replace(marker, panel + marker, 1)
    js = r"""
async function qhSendFriendRequest(){
 const input=document.getElementById('qh-friend-player-id');
 const status=document.getElementById('qh-friend-status');
 if(!input||!status)return;
 status.textContent='جاري البحث وإرسال الطلب...';
 try{const target=await window.QHFriends.sendFriendRequest(input.value);status.textContent='اتبعث طلب الصداقة بنجاح إلى '+target.displayName+' ☕';input.value='';}
 catch(e){status.textContent=e.message||'حصل خطأ، حاول مرة تانية';}
}
async function qhRefreshFriendRequests(){
 const box=document.getElementById('qh-friend-inbox');if(!box)return;box.textContent='جاري تحميل الطلبات...';
 try{const data=await window.QHFriends.listFriendRequests();if(!data.incoming.length){box.textContent='مفيش طلبات صداقة جديدة دلوقتي.';return;}
 box.innerHTML=data.incoming.map(function(x){return '<div style="padding:10px;margin:8px 0;border:1px solid #b98b50;border-radius:12px">لاعب · '+(x.fromPlayerId||'PLAYER')+' <button class="pri" onclick="qhRespondFriendRequest(\\''+x.id+'\\',true)">قبول</button> <button class="sec" onclick="qhRespondFriendRequest(\\''+x.id+'\\',false)">رفض</button></div>';}).join('');}
 catch(e){box.textContent=e.message||'تعذر تحميل الطلبات';}
}
async function qhRespondFriendRequest(id,accept){try{await window.QHFriends.respondFriendRequest(id,accept);await qhRefreshFriendRequests();}catch(e){const box=document.getElementById('qh-friend-inbox');if(box)box.textContent=e.message||'تعذر تحديث الطلب';}}
"""
    pos = src.rfind("</script>")
    if pos < 0: raise SystemExit("No script close")
    src = src[:pos] + js + "\n" + src[pos:]
    path.write_text(src, encoding="utf-8")
print("Friend lookup/request UI patch applied.")
