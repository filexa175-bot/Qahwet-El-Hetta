from pathlib import Path

css = r"""
/* QH DESIGN PASS 110 — coherent heritage identity and restrained surfaces */
:root{
 --qh-teal:#123f49;--qh-teal-deep:#092f38;--qh-teal-mid:#23616a;
 --qh-paper:#f7eddc;--qh-parchment:#efe0c5;--qh-cream:#fff8eb;
 --qh-gold:#d5a85e;--qh-gold-soft:#e8c98e;--qh-copper:#a95135;
 --qh-ink:#183b40;--qh-muted:#806e59;--qh-rule:rgba(18,63,73,.15)
}
html,body{background:var(--qh-paper)!important;color:var(--qh-ink)!important}
body{
 background-image:
  radial-gradient(ellipse at 8% 12%,rgba(213,168,94,.10),transparent 26%),
  radial-gradient(ellipse at 92% 58%,rgba(18,63,73,.045),transparent 31%),
  linear-gradient(135deg,rgba(255,255,255,.17) 25%,transparent 25%,transparent 75%,rgba(255,255,255,.17) 75%)!important;
 background-size:auto,auto,34px 34px!important
}
.start.neo-home.qh-experience{
 width:min(100%,620px)!important;min-height:100dvh!important;
 padding:clamp(16px,4vw,25px) clamp(16px,4vw,24px) calc(30px + env(safe-area-inset-bottom))!important;
 background:
  radial-gradient(ellipse at 50% 0%,rgba(255,250,239,.95),transparent 48%),
  linear-gradient(180deg,#f8efdf 0%,#f0e2ca 100%)!important;
 color:var(--qh-ink)!important
}
.qh-hero{
 position:relative;isolation:isolate;overflow:hidden;
 display:flex!important;flex-direction:column;align-items:center;justify-content:center;
 min-height:174px!important;margin:0 0 18px!important;padding:23px 18px 27px!important;
 border:1px solid rgba(213,168,94,.72)!important;border-radius:22px!important;
 background:
  radial-gradient(ellipse at 50% 120%,rgba(213,168,94,.18),transparent 58%),
  linear-gradient(145deg,#164b54 0%,#0c333c 100%)!important;
 box-shadow:0 12px 26px rgba(9,47,56,.14)!important;text-align:center
}
.qh-hero:before{
 content:"";position:absolute;z-index:-1;inset:8px;border:1px solid rgba(232,201,142,.28);
 border-radius:15px;
 background:
  repeating-linear-gradient(45deg,transparent 0 19px,rgba(232,201,142,.035) 19px 20px),
  repeating-linear-gradient(-45deg,transparent 0 19px,rgba(232,201,142,.035) 19px 20px)
}
.qh-hero:after{
 content:"";position:absolute;z-index:-1;width:240px;height:240px;right:calc(50% - 120px);bottom:-205px;
 border:1px solid rgba(232,201,142,.35);border-radius:50%;
 box-shadow:0 0 0 12px rgba(232,201,142,.045),0 0 0 26px rgba(232,201,142,.03)
}
.qh-hero-copy{max-width:100%!important;position:relative;z-index:1}
.qh-eyebrow{display:block;color:var(--qh-gold-soft)!important;font-size:12px!important;letter-spacing:.2px}
.qh-hero h1{
 margin:9px 0 5px!important;color:#fff1d8!important;
 font-size:clamp(34px,9vw,46px)!important;line-height:1.22!important;
 font-weight:950!important;letter-spacing:-1px!important;text-shadow:0 2px 0 rgba(0,0,0,.22)!important
}
.qh-hero p{margin:0!important;color:#e8cfa7!important;font-size:12px!important}
.qh-hero-seal,.qh-hero-rule{display:none!important}
.qh-hero-ornament{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:16px;width:74%;opacity:.8}
.qh-hero-ornament span{height:1px;flex:1;background:linear-gradient(90deg,transparent,var(--qh-gold))}
.qh-hero-ornament span:last-child{transform:scaleX(-1)}
.qh-hero-ornament i{width:5px;height:5px;background:var(--qh-gold);transform:rotate(45deg)}
.qh-stepper{
 margin:0 auto 23px!important;padding:8px 2px 14px!important;
 border:0!important;border-bottom:1px solid var(--qh-rule)!important
}
.qh-stepper>div{color:#8a765f!important;font-weight:700}
.qh-stepper>div b{background:transparent!important;border:1px solid #c6a777!important;color:var(--qh-teal)!important}
.qh-stepper>div.active b{background:var(--qh-copper)!important;border-color:var(--qh-copper)!important;color:#fff7e9!important;box-shadow:0 0 0 4px rgba(169,81,53,.12)!important}
.qh-stepper>i{background:linear-gradient(90deg,var(--qh-gold),var(--qh-teal-mid))!important}
.qh-panel{
 margin:0 0 21px!important;padding:7px 0 19px!important;
 border:0!important;border-bottom:1px solid var(--qh-rule)!important;
 border-radius:0!important;background:transparent!important;box-shadow:none!important
}
.qh-section-title{margin:0 0 17px!important;gap:11px!important}
.qh-section-title h3,.qh-character-head h3{color:var(--qh-teal)!important;font-weight:900!important;letter-spacing:-.2px}
.qh-section-title p,.qh-character-head p{color:var(--qh-muted)!important}
.qh-index{color:var(--qh-copper)!important}
.qh-section-tag{color:#a28a6d!important}
.qh-field-label{color:var(--qh-teal)!important;font-weight:800!important}
.qh-input-wrap{position:relative!important}
.qh-input-wrap:before,.qh-input-wrap:after{display:none!important;content:none!important}
.qh-input-wrap img,.qh-input-wrap [class*="brand"],.qh-input-wrap .brand-mark{display:none!important}
.qh-name-input,.neo-home .name-input.qh-name-input{
 width:100%!important;min-height:54px!important;height:54px!important;box-sizing:border-box!important;
 padding:0 15px!important;border:1px solid rgba(18,63,73,.18)!important;
 border-bottom:2px solid var(--qh-gold)!important;border-radius:11px!important;
 background:rgba(255,250,240,.88)!important;color:var(--qh-teal-deep)!important;
 box-shadow:inset 0 1px 3px rgba(18,63,73,.035)!important;text-align:right!important
}
.qh-name-input:focus{outline:none!important;border-color:var(--qh-gold)!important;border-bottom-color:var(--qh-copper)!important;box-shadow:0 2px 0 var(--qh-copper)!important}
.qh-id-row,.qh-account-state,.qh-google-login{
 margin-top:12px!important;padding:11px 0!important;border:0!important;
 border-bottom:1px solid var(--qh-rule)!important;border-radius:0!important;background:transparent!important
}
.qh-copy-id{border:1px solid rgba(169,81,53,.35)!important;border-radius:8px!important;background:transparent!important;color:var(--qh-teal)!important}
.qh-google-login{color:var(--qh-teal)!important}
.qh-account-state>span{background:var(--qh-teal-mid)!important}
.qh-character-head{margin:19px 0 12px!important;padding-top:16px!important;border-top:1px solid var(--qh-rule)!important}
.qh-avatar-pick{gap:12px!important}
.qh-avatar-pick button{
 min-height:0!important;padding:9px 5px 10px!important;
 border:1px solid transparent!important;border-radius:13px!important;
 background:rgba(255,248,235,.48)!important;box-shadow:none!important;color:var(--qh-teal)!important
}
.qh-avatar-pick button.on{
 border-color:rgba(213,168,94,.9)!important;background:rgba(213,168,94,.12)!important;
 box-shadow:0 0 0 2px rgba(213,168,94,.10)!important
}
.qh-avatar-art{filter:drop-shadow(0 3px 3px rgba(24,59,64,.12))}
.qh-avatar-pick button small{color:var(--qh-muted)!important}
.qh-mode-grid{gap:8px!important}
.qh-mode-card{
 border:1px solid rgba(18,63,73,.12)!important;border-radius:13px!important;
 background:rgba(255,249,238,.62)!important;box-shadow:none!important;color:var(--qh-teal)!important
}
.qh-mode-card.selected{border-color:rgba(169,81,53,.55)!important;background:rgba(213,168,94,.12)!important;box-shadow:inset 0 0 0 1px rgba(169,81,53,.12)!important}
.qh-mode-symbol{background:#ead9bb!important;color:var(--qh-teal)!important}
.qh-mode-card b,.qh-game-card strong{color:var(--qh-teal)!important}
.qh-mode-card small,.qh-game-card small{color:var(--qh-muted)!important}
.qh-games-grid{gap:10px!important}
.qh-game-card{
 min-height:120px!important;padding:12px 5px!important;
 border:1px solid rgba(18,63,73,.13)!important;border-radius:14px!important;
 background:linear-gradient(160deg,rgba(255,250,240,.92),rgba(239,224,197,.55))!important;
 box-shadow:0 4px 10px rgba(24,59,64,.045)!important
}
.qh-game-card.on{
 border-color:var(--qh-gold)!important;background:linear-gradient(160deg,#fff4dc,#ead5ad)!important;
 box-shadow:0 0 0 2px rgba(213,168,94,.16),0 5px 12px rgba(24,59,64,.07)!important
}
.qh-game-card>b{color:var(--qh-copper)!important}
.qh-game-card.off{opacity:.48!important;filter:grayscale(.25)}
.qh-stake-opt,.qh-difficulty-panel .difficulty-opt{
 border:1px solid rgba(18,63,73,.14)!important;border-radius:10px!important;
 background:rgba(255,249,238,.65)!important;color:var(--qh-teal)!important
}
.qh-stake-opt.on,.qh-difficulty-panel .difficulty-opt.on{
 border-color:var(--qh-gold)!important;background:rgba(213,168,94,.16)!important
}
.qh-bottom-actions{
 position:static!important;inset:auto!important;transform:none!important;z-index:auto!important;
 display:flex!important;flex-direction:column;gap:10px!important;
 margin:18px 0 0!important;padding:0!important;border:0!important;border-radius:0!important;
 background:transparent!important;box-shadow:none!important;backdrop-filter:none!important
}
.qh-two-actions{flex-direction:row!important}
.qh-primary{
 min-height:51px!important;border:1px solid #e8c98e!important;border-radius:10px!important;
 background:linear-gradient(135deg,#e3bf7d,#c38a4c)!important;color:#173941!important;
 box-shadow:0 5px 12px rgba(93,64,34,.13)!important;font-weight:900!important
}
.qh-back{min-height:48px!important;border:1px solid var(--qh-gold)!important;border-radius:10px!important;background:var(--qh-teal)!important;color:#fff1d8!important}
.qh-footer{
 display:flex!important;align-items:center;justify-content:center;gap:7px;flex-wrap:wrap;
 margin:27px auto 0!important;padding:13px 0 0!important;
 border-top:1px solid var(--qh-rule)!important;color:var(--qh-muted)!important
}
.qh-footer .qh-dev-kicker,.qh-footer small{color:#9a856a!important}
.qh-footer b{color:var(--qh-teal)!important}
.qh-footer i{background:var(--qh-copper)!important}
/* QH GAME SURFACES 110 — shared teal, parchment and brass material language */
#app{max-width:620px!important;background:transparent!important;box-shadow:none!important}
.top{background:linear-gradient(90deg,#0d333b,#1c5660 50%,#0d333b)!important;border-bottom:2px solid var(--qh-gold)!important}
.bub{background:var(--qh-cream)!important;color:var(--qh-ink)!important;border:1px solid rgba(213,168,94,.6)!important}
.ic,.sec,.bar button{background:linear-gradient(145deg,#174b54,#0d343c)!important;border:1px solid var(--qh-gold)!important;color:#fff0d5!important}
.tb{background:radial-gradient(ellipse at center,#1b6268,#0c343d 78%)!important;border:4px solid #c89a58!important;box-shadow:inset 0 0 0 2px rgba(255,231,187,.38),0 7px 18px rgba(0,0,0,.22)!important}
.table{background:repeating-linear-gradient(90deg,#174b54,#174b54 38px,#123f49 38px,#123f49 40px)!important;border:4px solid #c89a58!important;box-shadow:inset 0 0 0 2px rgba(255,231,187,.38),0 7px 18px rgba(0,0,0,.22)!important}
.basra-zone{background:radial-gradient(ellipse at center,#22646a,#103b43 76%)!important;border:4px solid #c89a58!important;box-shadow:inset 0 0 0 2px rgba(255,231,187,.34),0 7px 18px rgba(0,0,0,.2)!important}
.domino-board-shell{background:radial-gradient(ellipse at center,#1c5961,#103940 76%)!important;border:7px solid #b9874c!important;box-shadow:inset 0 0 0 2px #f0d49b, inset 0 0 28px rgba(4,24,28,.48),0 8px 20px rgba(0,0,0,.25)!important}
.domino-board-shell:before,.backgammon-board:before{border-color:rgba(240,212,155,.55)!important}
.backgammon-board{background:radial-gradient(ellipse at center,#174c58,#0d303a 76%)!important;border-color:#b9874c!important;box-shadow:inset 0 0 0 3px #e3c28e,inset 0 0 30px #050c17,0 7px 22px #0005!important}
.backgammon-board .barr{background:linear-gradient(90deg,#0b3038,#1e5960,#0b3038)!important;border-color:#d6b27d!important}
.score .team{background:linear-gradient(145deg,#174b54,#0c3038)!important;border-color:rgba(213,168,94,.8)!important}
.card{background:linear-gradient(145deg,#174b54,#0d343c)!important;border:1px solid var(--qh-gold)!important;color:#fff1d8!important;box-shadow:0 8px 22px rgba(0,0,0,.2)!important}
.playcard{border-color:#c79b5c!important;box-shadow:inset 0 0 0 2px #fff8,0 2px 0 #8b6336,0 5px 9px #0005!important}
.bar button.pri,.pri{background:linear-gradient(135deg,#e3bf7d,#c38a4c)!important;color:#173941!important;border:1px solid #f0d49b!important;box-shadow:0 3px 0 #805b32!important}
.wait{background:var(--qh-cream)!important;color:var(--qh-ink)!important;border-color:var(--qh-copper)!important}
.wm{color:var(--qh-gold-soft)!important;opacity:.85}

@media(max-width:390px){
 .start.neo-home.qh-experience{padding-left:14px!important;padding-right:14px!important}
 .qh-hero{min-height:155px!important;padding:20px 15px 22px!important;border-radius:18px!important}
 .qh-hero h1{font-size:33px!important}
 .qh-panel{padding-bottom:16px!important}
 .qh-avatar-pick{gap:8px!important}
 .qh-game-card{min-height:108px!important}
}
"""
for name in ("www/index.html", "www/game.html"):
    path=Path(name)
    src=path.read_text(encoding="utf-8")
    if "QH DESIGN PASS 110" in src:
        print(f"Build 110 already present in {name}; skipping.")
        continue
    if "</head>" not in src:
        raise SystemExit(f"Missing </head> in {name}")
    src=src.replace("</head>", '<style id="qh-design-pass-110">\n'+css+'\n</style>\n</head>', 1)
    path.write_text(src,encoding="utf-8")
print("QH Design Pass 110 applied.")
