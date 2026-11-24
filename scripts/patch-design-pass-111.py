from pathlib import Path

css = r"""
/* QH DESIGN PASS 111 — compact emblem, calm surfaces, reachable onboarding actions */
.qh-brand-emblem{
 display:block!important;width:min(34vw,112px)!important;height:auto!important;
 max-width:112px!important;max-height:112px!important;object-fit:contain!important;
 margin:0 auto 5px!important;image-rendering:auto!important;
 filter:drop-shadow(0 3px 5px rgba(9,47,56,.18))!important
}
.qh-hero{
 min-height:0!important;height:auto!important;padding:10px 14px 12px!important;
 margin:0 0 14px!important;border-radius:17px!important;gap:0!important;
 box-shadow:0 5px 13px rgba(9,47,56,.10)!important
}
.qh-hero:before{inset:5px!important;border-radius:12px!important;opacity:.55}
.qh-hero:after{display:none!important}
.qh-hero-copy{margin:0!important}
.qh-hero-copy .qh-eyebrow{font-size:10px!important;line-height:1.4!important}
.qh-hero-copy p{margin:2px 0 0!important;font-size:11px!important}
.qh-panel{
 overflow:visible!important;max-height:none!important;
 background:transparent!important;border:0!important;border-radius:0!important;
 box-shadow:none!important;padding:17px 0!important;margin:0!important
}
.qh-profile-panel,.qh-choice-panel,.qh-game-panel,.qh-stake-section,.qh-difficulty-panel{
 border-bottom:1px solid rgba(18,63,73,.10)!important
}
.qh-section-title{border:0!important;background:transparent!important;box-shadow:none!important;padding:0!important}
.qh-index{box-shadow:none!important}
.qh-field-label{margin-top:16px!important}
.qh-input-wrap{border:0!important;border-bottom:1px solid rgba(18,63,73,.32)!important;border-radius:0!important;background:rgba(255,248,235,.38)!important;box-shadow:none!important}
.qh-name-input{border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important}
.qh-id-row,.qh-account-state,.qh-google-login{
 border:0!important;border-bottom:1px solid rgba(18,63,73,.10)!important;
 border-radius:0!important;box-shadow:none!important;background:transparent!important
}
.qh-character-head{border-top:1px solid rgba(18,63,73,.10)!important}
.qh-avatar-pick{gap:10px!important}
.qh-avatar-pick button{
 min-height:0!important;padding:7px 3px 8px!important;
 border:0!important;border-radius:0!important;background:transparent!important;
 box-shadow:none!important
}
.qh-avatar-pick button.on{
 border:0!important;border-bottom:2px solid var(--qh-copper)!important;
 border-radius:0!important;background:rgba(213,168,94,.08)!important;box-shadow:none!important
}
.qh-mode-grid,.qh-games-grid{gap:9px!important}
.qh-mode-card,.qh-game-card{
 border:0!important;border-bottom:1px solid rgba(18,63,73,.15)!important;
 border-radius:14px!important;box-shadow:none!important;
 background:rgba(255,248,235,.42)!important
}
.qh-mode-card.selected,.qh-game-card.on{
 border:1px solid rgba(169,81,53,.55)!important;
 background:rgba(213,168,94,.13)!important;box-shadow:inset 0 -2px 0 rgba(169,81,53,.20)!important
}
.qh-game-card{min-height:108px!important}
.qh-stake-opt,.qh-difficulty-panel .difficulty-opt{
 border:1px solid rgba(18,63,73,.14)!important;border-radius:12px!important;box-shadow:none!important
}
#app{height:auto!important;min-height:100dvh!important;max-height:none!important;overflow:visible!important}
html,body{height:auto!important;min-height:100%!important;overflow-x:hidden!important;overflow-y:auto!important}
.start.neo-home.qh-experience{
 height:auto!important;min-height:100dvh!important;max-height:none!important;
 overflow:visible!important;overflow-y:visible!important;
 padding-bottom:calc(34px + env(safe-area-inset-bottom))!important
}
#app .start.qh-experience .qh-profile-actions,
#app .start.qh-experience .qh-bottom-actions{
 display:flex!important;visibility:visible!important;opacity:1!important;
 position:relative!important;inset:auto!important;transform:none!important;
 z-index:2!important;float:none!important;clear:both!important;
 width:100%!important;height:auto!important;min-height:0!important;max-height:none!important;
 overflow:visible!important;box-sizing:border-box!important;
 flex-direction:column!important;align-items:stretch!important;gap:9px!important;
 margin:20px 0 6px!important;padding:13px 0 2px!important;
 border:0!important;border-top:1px solid rgba(18,63,73,.12)!important;
 border-radius:0!important;background:transparent!important;box-shadow:none!important;
 backdrop-filter:none!important
}
#app .start.qh-experience .qh-step-caption{
 display:block!important;visibility:visible!important;opacity:1!important;
 color:var(--qh-muted)!important;text-align:center!important;font-size:11px!important
}
#app .start.qh-experience .qh-profile-actions .qh-primary,
#app .start.qh-experience .qh-bottom-actions .qh-primary{
 display:flex!important;visibility:visible!important;opacity:1!important;
 width:100%!important;min-width:0!important;min-height:54px!important;height:auto!important;
 align-items:center!important;justify-content:center!important;gap:10px!important;
 border:1px solid #e8c98e!important;border-radius:14px!important;
 background:linear-gradient(135deg,#e3bf7d,#c38a4c)!important;
 color:#173941!important;font-size:17px!important;font-weight:900!important;
 box-shadow:0 4px 10px rgba(93,64,34,.13)!important
}
.qh-two-actions{flex-direction:row!important}
.qh-two-actions .qh-primary{flex:1!important}
.qh-footer{margin-top:18px!important;border-top:0!important}
@media(max-width:390px){
 .qh-brand-emblem{width:104px!important;max-width:104px!important;max-height:104px!important}
 .qh-hero{padding:9px 12px 11px!important;margin-bottom:10px!important}
 .qh-panel{padding:13px 0!important}
 .qh-profile-actions{margin-top:16px!important}
 .qh-avatar-pick{gap:6px!important}
 .qh-game-card{min-height:100px!important}
}
"""
for name in ("www/index.html", "www/game.html"):
    path = Path(name)
    src = path.read_text(encoding="utf-8")
    if "QH DESIGN PASS 111" in src:
        print(f"Build 111 already present in {name}; skipping.")
        continue
    if "</head>" not in src:
        raise SystemExit(f"Missing </head> in {name}")
    src = src.replace("</head>", '<style id="qh-design-pass-111">\\n'+css+'\\n</style>\\n</head>', 1)
    path.write_text(src, encoding="utf-8")
print("QH Design Pass 111 applied.")
