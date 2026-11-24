from pathlib import Path

css = r"""
/* QH DESIGN PASS 112 — true document scrolling on Android WebView */
html,body{
 height:auto!important;min-height:100%!important;max-height:none!important;
 overflow-x:hidden!important;overflow-y:auto!important;
}
html{scroll-behavior:smooth}
body{
 display:block!important;position:relative!important;
 overflow-y:auto!important;overscroll-behavior-y:auto!important;
 -webkit-overflow-scrolling:touch!important;touch-action:pan-y!important;
}
#app:has(.qh-experience){
 display:block!important;position:relative!important;
 width:100%!important;height:auto!important;min-height:100dvh!important;
 max-height:none!important;overflow:visible!important;
}
.start.neo-home.qh-experience{
 display:block!important;position:relative!important;inset:auto!important;
 flex:none!important;flex-basis:auto!important;
 width:min(100%,620px)!important;height:auto!important;
 min-height:100dvh!important;max-height:none!important;
 margin:0 auto!important;overflow:visible!important;overflow-y:visible!important;
 box-sizing:border-box!important;
 padding-bottom:calc(38px + env(safe-area-inset-bottom))!important;
 touch-action:pan-y!important;
}
.start.neo-home.qh-experience .qh-panel,
.start.neo-home.qh-experience .qh-profile-panel,
.start.neo-home.qh-experience .qh-choice-panel,
.start.neo-home.qh-experience .qh-game-panel,
.start.neo-home.qh-experience .qh-stake-section,
.start.neo-home.qh-experience .qh-difficulty-panel{
 display:block!important;position:relative!important;
 height:auto!important;min-height:0!important;max-height:none!important;
 overflow:visible!important;contain:none!important;
}
.start.neo-home.qh-experience .qh-bottom-actions,
.start.neo-home.qh-experience .qh-profile-actions{
 position:relative!important;inset:auto!important;left:auto!important;right:auto!important;bottom:auto!important;
 transform:none!important;float:none!important;clear:both!important;
 display:flex!important;visibility:visible!important;opacity:1!important;
 width:100%!important;height:auto!important;min-height:0!important;max-height:none!important;
 margin:22px 0 8px!important;padding:14px 0 4px!important;
 overflow:visible!important;z-index:1!important;
 border:0!important;border-top:1px solid rgba(91,61,43,.16)!important;
 border-radius:0!important;background:transparent!important;box-shadow:none!important;
 backdrop-filter:none!important;
}
.start.neo-home.qh-experience .qh-primary{
 position:relative!important;display:flex!important;visibility:visible!important;opacity:1!important;
 width:100%!important;min-height:54px!important;height:auto!important;
 align-items:center!important;justify-content:center!important;
}
.start.neo-home.qh-experience .qh-avatar-pick,
.start.neo-home.qh-experience .qh-mode-grid,
.start.neo-home.qh-experience .qh-games-grid,
.start.neo-home.qh-experience .difficulty-grid{
 overflow:visible!important;max-height:none!important;
}
.qh-brand-emblem{
 display:block!important;flex:0 0 auto!important;
 width:min(30vw,100px)!important;height:auto!important;
 max-width:100px!important;max-height:100px!important;
 object-fit:contain!important;image-rendering:auto!important;
}
.qh-emblem-fallback{
 display:none;flex-direction:column;align-items:center;justify-content:center;
 gap:2px;width:min(30vw,100px);min-height:82px;flex:0 0 auto;
 color:#173b45;text-align:center;line-height:1.1;
}
.qh-emblem-fallback strong{font-size:14px;font-weight:1000;text-shadow:0 1px #fff4}
.qh-emblem-fallback span{font-size:25px}
.qh-emblem-fallback small{font-size:8px;color:#a85f3c;font-weight:800}
@media(max-width:390px){
 .start.neo-home.qh-experience{padding-bottom:calc(30px + env(safe-area-inset-bottom))!important}
 .qh-brand-emblem,.qh-emblem-fallback{width:88px!important;max-width:88px!important}
 .start.neo-home.qh-experience .qh-bottom-actions{margin-top:18px!important}
}
"""
for name in ("www/index.html", "www/game.html"):
    path = Path(name)
    src = path.read_text(encoding="utf-8")
    if "QH DESIGN PASS 112" in src:
        print(f"Build 112 already present in {name}; skipping.")
        continue
    if "</head>" not in src:
        raise SystemExit(f"Missing </head> in {name}")
    src = src.replace("</head>", '<style id="qh-design-pass-112">' + chr(10) + css + chr(10) + '</style>' + chr(10) + '</head>', 1)
    path.write_text(src, encoding="utf-8")
print("QH Design Pass 112 applied.")
