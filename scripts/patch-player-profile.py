from pathlib import Path

files = [Path("www/index.html"), Path("www/game.html")]
old_state = "const S={game:0,ch:0,df:1,playerName:'',playerId:'',"
new_state = "const S={game:0,ch:0,df:1,playerName:'',playerId:'',profileStep:1,mode:'ai',"
for path in files:
    src=path.read_text(encoding="utf-8")
    if "profileStep:1" not in src:
        if src.count(old_state)!=1: raise SystemExit(f"Unexpected state declaration in {path}")
        src=src.replace(old_state,new_state,1)
    src=src.replace("if(SAVED.profile)Object.assign(S,{playerId:SAVED.profile.playerId??'',playerName:SAVED.profile.playerName??S.playerName,ch:SAVED.profile.ch??S.ch});",
      "if(SAVED.profile)Object.assign(S,{playerId:SAVED.profile.playerId??'',playerName:SAVED.profile.playerName??S.playerName,ch:SAVED.profile.ch??S.ch,profileStep:SAVED.profile.profileStep??1,mode:SAVED.profile.mode??'ai'});")
    src=src.replace("profile:{playerId:S.playerId,playerName:S.playerName,ch:S.ch}",
      "profile:{playerId:S.playerId,playerName:S.playerName,ch:S.ch,profileStep:S.profileStep,mode:S.mode}")
    start=src.index("function startScreen(){")
    end=src.index("\nfunction go(){",start)
    src=src[:start]+Path("../scripts/player-home-screen.html.txt").read_text(encoding="utf-8").rstrip()+src[end:]
    # Keep a branded visual over the WebView's initial blank period.
    if "qh-boot-screen" not in src:
        marker="<body"
        p=src.find(marker)
        if p<0: raise SystemExit(f"No body tag in {path}")
        gt=src.find(">",p)+1
        boot='''\n<div id="qh-boot-screen" style="position:fixed;inset:0;z-index:100000;background:radial-gradient(circle at 50% 42%,#28483e 0,#142a25 48%,#0b1715 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;color:#f5dfb4;font-family:system-ui;text-align:center"><div style="font-size:76px;line-height:1">☕</div><div style="font-size:30px;font-weight:900;margin-top:14px">قهوة الحتة</div><div style="font-size:12px;letter-spacing:2px;margin-top:8px;color:#c49a60">اللَمّة ليها حكاية</div><div style="width:42px;height:3px;background:#b88a4d;border-radius:5px;margin-top:28px"></div></div>\n<script>window.addEventListener('load',()=>{const s=document.getElementById('qh-boot-screen');if(s){s.style.transition='opacity .25s';s.style.opacity='0';setTimeout(()=>s.remove(),280)}});</script>\n'''
        src=src[:gt]+boot+src[gt:]
    path.write_text(src,encoding="utf-8")
print("Two-step home screen and branded startup screen applied.")
