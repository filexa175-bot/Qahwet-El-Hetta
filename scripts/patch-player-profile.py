from pathlib import Path

files = [Path("www/index.html"), Path("www/game.html")]
home = Path("../scripts/player-home-screen.html.txt").read_text(encoding="utf-8").rstrip()
# Keep the wallet in sync whenever the profile screen is rebuilt (Next/Back).
# Inject the wallet refresh before startScreen() closes. Fail the build if the
# expected template ending changes, rather than silently shipping an unpatched APK.
wallet_refresh = "    if (S.authenticated) { window.QHRenderWalletBubble?.(); setTimeout(() => window.QHAuth?.loadWallet(), 0); }"
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

    if "stake:50" not in src:
        if "mode:'ai'," not in src:
            raise SystemExit(f"Cannot locate game mode for stake default in {path}")
        src = src.replace("mode:'ai',", "mode:'ai',stake:50,", 1)

    saved_needle = "if(SAVED.settings)Object.assign(S,{game:SAVED.settings.game??0,ch:SAVED.settings.ch??0,df:SAVED.settings.df??1,playerName:SAVED.settings.playerName??''});"
    saved_replacement = "if(SAVED.settings)Object.assign(S,{game:SAVED.settings.game??0,ch:SAVED.settings.ch??0,df:SAVED.settings.df??1,playerName:SAVED.settings.playerName??'',playerId:SAVED.settings.playerId??'',profileStep:SAVED.settings.profileStep??1,mode:SAVED.settings.mode??'ai',stake:SAVED.settings.stake??50});"
    if "stake:SAVED.settings.stake" not in src:
        if saved_needle in src:
            src = src.replace(saved_needle, saved_replacement, 1)
        elif "mode:SAVED.settings.mode??'ai'" in src:
            src = src.replace("mode:SAVED.settings.mode??'ai'", "mode:SAVED.settings.mode??'ai',stake:SAVED.settings.stake??50", 1)
        else:
            raise SystemExit(f"Cannot locate saved settings in {path}")

    persist_needle = "function persist(){try{localStorage.setItem(STORE_KEY,JSON.stringify({settings:{game:S.game,ch:S.ch,df:S.df,playerName:S.playerName}}))}catch(e){}}"
    persist_replacement = "function persist(){try{localStorage.setItem(STORE_KEY,JSON.stringify({settings:{game:S.game,ch:S.ch,df:S.df,playerName:S.playerName,playerId:S.playerId,profileStep:S.profileStep,mode:S.mode,stake:S.stake||50}}))}catch(e){}}"
    if "stake:S.stake" not in src:
        if persist_needle in src:
            src = src.replace(persist_needle, persist_replacement, 1)
        elif "mode:S.mode}}" in src:
            src = src.replace("mode:S.mode}}", "mode:S.mode,stake:S.stake||50}}", 1)
        else:
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

    if "qh-stake-grid" not in src:
        style_marker = "</style>"
        if style_marker not in src:
            raise SystemExit(f"No style close in {path}")
        src = src.replace(style_marker, "\n.qh-stake-section{padding:8px 10px!important;margin:6px 0!important}\n.qh-stake-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}\n.qh-stake-opt{min-height:42px!important;padding:5px 2px!important;border:1px solid #3b5c87!important;border-radius:10px!important;background:linear-gradient(145deg,#172b4b,#101b33)!important;color:#f1f6ff!important}\n.qh-stake-opt b{font-size:15px!important;line-height:1.1}\n.qh-stake-opt small{font-size:9px!important}\n.qh-stake-opt.on{border-color:#35d7ed!important;background:linear-gradient(145deg,#145071,#172a4b)!important}\n.qh-stake-summary{font-size:11px;color:#b8cbe4;margin-top:6px}\n.qh-stake-summary b{color:#8deaff}\n" + style_marker, 1)
    path.write_text(src, encoding="utf-8")

print("Two-step home screen and branded startup screen applied.")
