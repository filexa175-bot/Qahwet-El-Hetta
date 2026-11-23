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
        src = src.replace(style_marker, "\n/* Qahwet El Hetta — Egyptian heritage design system */\n:root{\n --qh-ink:#17251d;--qh-ink-2:#21362a;--qh-wood:#39281e;\n --qh-emerald:#254b38;--qh-emerald-2:#326248;\n --qh-brass:#b58a4b;--qh-brass-light:#d9bd82;\n --qh-paper:#f1e5c9;--qh-muted:#c7b895;\n}\n.start.neo-home{\n color:var(--qh-paper)!important;\n background:\n  radial-gradient(ellipse at 50% 0%,rgba(181,138,75,.13),transparent 48%),\n  linear-gradient(180deg,#18271f 0%,#101b16 100%)!important;\n padding:14px 12px 24px!important;\n}\n.start.neo-home .brand-mark{color:#cdb98f!important;letter-spacing:.4px}\n.start.neo-home .hero{\n border:1px solid rgba(201,165,101,.42)!important;\n border-radius:20px!important;\n background:\n  linear-gradient(135deg,rgba(35,70,51,.96),rgba(24,39,30,.98))!important;\n box-shadow:inset 0 1px rgba(255,255,255,.06),0 9px 22px rgba(0,0,0,.2)!important;\n position:relative;overflow:hidden;\n}\n.start.neo-home .hero:after{\n content:\"\";position:absolute;inset:7px;border:1px solid rgba(210,177,116,.15);\n border-radius:14px;pointer-events:none;\n}\n.start.neo-home .hero-kicker{color:#d6bd89!important}\n.start.neo-home .hero h1{color:#f3e4c5!important;text-shadow:0 2px 12px #0005}\n.start.neo-home .hero p{color:#d2c5a6!important}\n.start.neo-home .hero-cup{filter:sepia(.45) saturate(.8)}\n.start.neo-home .step-progress{\n background:rgba(181,138,75,.08)!important;border:1px solid rgba(181,138,75,.22);\n border-radius:14px;padding:9px 12px;\n}\n.start.neo-home .step-progress span{color:#b8aa8d!important}\n.start.neo-home .step-progress span.active{color:#f0d39a!important}\n.start.neo-home .step-progress i{background:#78613e!important}\n.start.neo-home .neo-panel,.start.neo-home .game-section,.start.neo-home .difficulty-section{\n background:linear-gradient(145deg,rgba(37,59,44,.96),rgba(25,40,31,.98))!important;\n border:1px solid rgba(181,138,75,.32)!important;border-radius:17px!important;\n box-shadow:0 6px 18px rgba(0,0,0,.16)!important;\n}\n.start.neo-home .section-heading h3{color:#f0dfbd!important}\n.start.neo-home .section-heading small{color:#c4b695!important}\n.start.neo-home .section-heading .step{\n color:#e1c18a!important;background:rgba(181,138,75,.14)!important;\n border:1px solid rgba(181,138,75,.4)!important;\n}\n.start.neo-home .name-input{\n color:#f5e8cb!important;background:#17251d!important;\n border:1px solid #8c7045!important;border-radius:12px!important;\n}\n.start.neo-home .opt{\n color:#f1e5c9!important;background:linear-gradient(145deg,#304b38,#1c3024)!important;\n border:1px solid rgba(190,153,91,.42)!important;border-radius:13px!important;\n box-shadow:inset 0 1px rgba(255,255,255,.04)!important;\n}\n.start.neo-home .opt.on{\n border-color:#e0bd78!important;\n background:linear-gradient(145deg,#536a43,#344c35)!important;\n box-shadow:0 0 0 1px rgba(224,189,120,.18),inset 0 1px rgba(255,255,255,.08)!important;\n}\n.start.neo-home .opt.off{opacity:.52}\n.start.neo-home .pri{\n color:#211b12!important;background:linear-gradient(135deg,#e0c28a,#b68a4e)!important;\n border:1px solid #f0d7a2!important;border-radius:13px!important;\n box-shadow:0 4px 12px rgba(0,0,0,.2)!important;\n}\n.start.neo-home .sec{\n color:#e7d4ae!important;background:#26382b!important;\n border:1px solid #8d744b!important;border-radius:12px!important;\n}\n.start.neo-home .avatar-pick button{\n background:#203428!important;border:1px solid #8e754c!important;\n}\n.start.neo-home .avatar-pick button.on{border:2px solid #e0bd78!important;background:#3b583e!important}\n.start.neo-home .qh-stake-summary{color:#d0c19e!important}\n.start.neo-home .qh-stake-summary b{color:#f0d39a!important}\n@media(max-width:380px){\n .start.neo-home{padding-left:9px!important;padding-right:9px!important}\n .start.neo-home .game-section{padding:10px!important}\n}\n" + "\n.qh-stake-section{padding:8px 10px!important;margin:6px 0!important}\n.qh-stake-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}\n.qh-stake-opt{min-height:42px!important;padding:5px 2px!important;border:1px solid #3b5c87!important;border-radius:10px!important;background:linear-gradient(145deg,#172b4b,#101b33)!important;color:#f1f6ff!important}\n.qh-stake-opt b{font-size:15px!important;line-height:1.1}\n.qh-stake-opt small{font-size:9px!important}\n.qh-stake-opt.on{border-color:#35d7ed!important;background:linear-gradient(145deg,#145071,#172a4b)!important}\n.qh-stake-summary{font-size:11px;color:#b8cbe4;margin-top:6px}\n.qh-stake-summary b{color:#8deaff}\n" + style_marker, 1)
    path.write_text(src, encoding="utf-8")

print("Two-step home screen and branded startup screen applied.")
