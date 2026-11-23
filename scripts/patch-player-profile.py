from pathlib import Path

files = [Path("www/index.html"), Path("www/game.html")]
home = Path("../scripts/player-home-screen.html.txt").read_text(encoding="utf-8").rstrip()
# Keep the wallet in sync whenever the profile screen is rebuilt (Next/Back).
# Inject the wallet refresh before startScreen() closes. Fail the build if the
# expected template ending changes, rather than silently shipping an unpatched APK.
wallet_refresh = "    if (S.authenticated) setTimeout(() => window.QHAuth?.loadWallet(), 0);"
if home.count("\n}") != 1:
    raise SystemExit("Cannot uniquely locate the end of startScreen() template")
home = home.rsplit("\n}", 1)[0] + "\n" + wallet_refresh + "\n}\n"
if wallet_refresh not in home:
    raise SystemExit("Wallet refresh hook was not inserted")

for path in files:
    src = path.read_text(encoding="utf-8")

    # Extend the existing local profile without disturbing game counters.
    if "profileStep:1" not in src:
        needle = "const S={game:0,ch:0,df:1,playerName:'',"
        if src.count(needle) != 1:
            raise SystemExit(f"Cannot locate game state in {path}")
        src = src.replace(needle, "const S={game:0,ch:0,df:1,playerName:'',playerId:'',profileStep:1,mode:'ai',", 1)

    saved_needle = "if(SAVED.settings)Object.assign(S,{game:SAVED.settings.game??0,ch:SAVED.settings.ch??0,df:SAVED.settings.df??1,playerName:SAVED.settings.playerName??''});"
    saved_replacement = "if(SAVED.settings)Object.assign(S,{game:SAVED.settings.game??0,ch:SAVED.settings.ch??0,df:SAVED.settings.df??1,playerName:SAVED.settings.playerName??'',playerId:SAVED.settings.playerId??'',profileStep:SAVED.settings.profileStep??1,mode:SAVED.settings.mode??'ai'});"
    if saved_needle in src:
        src = src.replace(saved_needle, saved_replacement, 1)
    elif "SAVED.settings.playerId" not in src:
        raise SystemExit(f"Cannot locate saved settings in {path}")

    persist_needle = "function persist(){try{localStorage.setItem(STORE_KEY,JSON.stringify({settings:{game:S.game,ch:S.ch,df:S.df,playerName:S.playerName}}))}catch(e){}}"
    persist_replacement = "function persist(){try{localStorage.setItem(STORE_KEY,JSON.stringify({settings:{game:S.game,ch:S.ch,df:S.df,playerName:S.playerName,playerId:S.playerId,profileStep:S.profileStep,mode:S.mode}}))}catch(e){}}"
    if persist_needle in src:
        src = src.replace(persist_needle, persist_replacement, 1)
    elif "profileStep:S.profileStep" not in src:
        raise SystemExit(f"Cannot locate persistence function in {path}")

    start = src.index("function startScreen(){")
    end = src.index("\nfunction go(){", start)
    src = src[:start] + home + src[end:]

    if "qh-boot-screen" not in src:
        p = src.find("<body")
        if p < 0:
            raise SystemExit(f"No body tag in {path}")
        gt = src.find(">", p) + 1
        boot = '''
<div id="qh-boot-screen" style="position:fixed;inset:0;z-index:100000;background:radial-gradient(circle at 50% 42%,#28483e 0,#142a25 48%,#0b1715 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;color:#f5dfb4;font-family:system-ui;text-align:center"><div style="font-size:76px;line-height:1">☕</div><div style="font-size:30px;font-weight:900;margin-top:14px">قهوة الحتة</div><div style="font-size:12px;letter-spacing:2px;margin-top:8px;color:#c49a60">اللَمّة ليها حكاية</div><div style="width:42px;height:3px;background:#b88a4d;border-radius:5px;margin-top:28px"></div></div>
<script>window.addEventListener('load',()=>{const s=document.getElementById('qh-boot-screen');if(s){s.style.transition='opacity .25s';s.style.opacity='0';setTimeout(()=>s.remove(),280)}});</script>
'''
        src = src[:gt] + boot + src[gt:]

    path.write_text(src, encoding="utf-8")

print("Two-step home screen and branded startup screen applied.")
