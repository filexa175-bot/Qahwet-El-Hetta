from pathlib import Path

css = r"""
/* QH DESIGN PASS 109 — identity system inspired by the supplied Egyptian café emblem */
:root{
 --qh-teal:#123f49;--qh-teal-deep:#092d36;--qh-teal-mid:#1b5960;
 --qh-parchment:#f4e7cf;--qh-paper:#fbf3e4;--qh-ink:#173941;
 --qh-gold:#d4a65d;--qh-gold-light:#f0d49b;--qh-copper:#a94f32;
 --qh-rust:#c36b43;--qh-muted:#88745b;--qh-line:rgba(18,63,73,.16);
 --qh-shadow:0 10px 24px rgba(31,43,39,.10)
}
html,body{background:var(--qh-parchment)!important;color:var(--qh-ink)!important}
#app{background:transparent!important}
.start.neo-home.qh-experience{
 background:
  radial-gradient(ellipse at 50% -15%,rgba(255,250,237,.95),transparent 55%),
  linear-gradient(180deg,#f8edd9 0%,#f1e2c7 100%)!important;
 color:var(--qh-ink)!important
}
.qh-hero{
 position:relative;isolation:isolate;overflow:hidden;
 min-height:142px!important;padding:25px 23px!important;
 border:1px solid rgba(212,166,93,.85)!important;border-radius:18px!important;
 background:linear-gradient(130deg,var(--qh-teal) 0%,var(--qh-teal-deep) 100%)!important;
 box-shadow:0 12px 26px rgba(9,45,54,.17)!important
}
.qh-hero:before{
 content:"";position:absolute;z-index:-1;inset:9px;border:1px solid rgba(240,212,155,.22);
 border-radius:12px;background:
 repeating-linear-gradient(45deg,transparent 0 17px,rgba(240,212,155,.035) 17px 18px),
 repeating-linear-gradient(-45deg,transparent 0 17px,rgba(240,212,155,.035) 17px 18px)
}
.qh-hero:after{content:"";position:absolute;z-index:-1;width:190px;height:190px;left:-80px;bottom:-135px;border:1px solid #d4a65d55;border-radius:50%;box-shadow:0 0 0 12px #d4a65d0d,0 0 0 25px #d4a65d0a}
.qh-hero-copy{position:relative;z-index:1;max-width:100%}
.qh-eyebrow{color:var(--qh-gold-light)!important;letter-spacing:.4px}
.qh-hero h1{color:#fff0d3!important;text-shadow:0 2px 0 #071f25;font-weight:900!important}
.qh-hero p{color:#e3c99c!important}
.qh-hero-seal{border:1px solid #d4a65d99!important;color:var(--qh-gold-light)!important;background:transparent!important}
.qh-hero-seal b{color:#fff0d3!important}
.qh-stepper{border-bottom:1px solid var(--qh-line)!important}
.qh-stepper>div{color:#7d6a52!important}
.qh-stepper>div b{border:1px solid #b99b69!important;color:var(--qh-teal)!important;background:transparent!important}
.qh-stepper>div.active b{background:var(--qh-copper)!important;border-color:var(--qh-copper)!important;color:#fff5e4!important;box-shadow:0 0 0 4px #a94f3220!important}
.qh-stepper>i{background:linear-gradient(90deg,var(--qh-gold),var(--qh-teal-mid))!important}
.qh-panel{border-bottom:1px solid var(--qh-line)!important;background:transparent!important}
.qh-section-title h3,.qh-character-head h3{color:var(--qh-teal)!important;font-weight:850!important}
.qh-section-title p,.qh-character-head p{color:var(--qh-muted)!important}
.qh-index{color:var(--qh-copper)!important}
.qh-field-label{color:var(--qh-teal)!important;font-weight:750!important}
.qh-name-input,.neo-home .name-input.qh-name-input{
 background:rgba(255,250,239,.88)!important;color:var(--qh-teal-deep)!important;
 border-bottom:2px solid var(--qh-gold)!important
}
.qh-name-input:focus{border-bottom-color:var(--qh-copper)!important;box-shadow:0 2px 0 var(--qh-copper)!important}
.qh-id-row,.qh-account-state,.qh-google-login{border-color:var(--qh-line)!important}
.qh-copy-id{color:var(--qh-teal)!important;border-color:#b9955b!important}
.qh-google-login{color:var(--qh-teal)!important}
.qh-account-state>span{background:var(--qh-teal-mid)!important}
.qh-avatar-pick button{color:var(--qh-teal)!important}
.qh-avatar-pick button.on{border-bottom-color:var(--qh-copper)!important}
.qh-avatar-pick button small{color:var(--qh-muted)!important}
.qh-mode-card,.qh-game-card,.qh-stake-opt,.qh-difficulty-panel .difficulty-opt{
 color:var(--qh-teal)!important;border-color:var(--qh-line)!important
}
.qh-mode-card.selected,.qh-game-card.on,.qh-stake-opt.on,.qh-difficulty-panel .difficulty-opt.on{
 border-bottom-color:var(--qh-copper)!important;background:rgba(212,166,93,.10)!important
}
.qh-mode-symbol{background:#e9d7b8!important;color:var(--qh-teal)!important}
.qh-mode-card b,.qh-game-card strong{color:var(--qh-teal)!important}
.qh-mode-card small,.qh-game-card small{color:var(--qh-muted)!important}
.qh-game-card>b{color:var(--qh-copper)!important}
.qh-bottom-actions{background:transparent!important}
.qh-primary{
 background:linear-gradient(135deg,#d8ad68 0%,#bd8447 100%)!important;
 color:#17343a!important;border:1px solid #f1d49b!important;border-radius:9px!important;
 box-shadow:0 5px 12px rgba(77,53,27,.14)!important;font-weight:850!important
}
.qh-primary:active{transform:translateY(1px)}
.qh-back{background:var(--qh-teal)!important;color:#fff1d5!important;border:1px solid #d4a65d!important;border-radius:9px!important}
.qh-footer{border-top:1px solid var(--qh-line)!important;color:var(--qh-muted)!important}
.qh-footer b{color:var(--qh-teal)!important}
.qh-footer i{background:var(--qh-copper)!important}
.qh-footer .qh-dev-kicker,.qh-footer small{color:var(--qh-muted)!important}
.qh-wallet-bubble,.wallet-bubble,.wallet-pill{background:var(--qh-teal)!important;border-color:var(--qh-gold)!important;color:#fff0d3!important}
@media(max-width:390px){
 .qh-hero{min-height:128px!important;padding:20px 17px!important;border-radius:14px!important}
 .qh-hero h1{font-size:29px!important}
 .qh-stepper{gap:10px!important}
}
"""
for name in ("www/index.html", "www/game.html"):
    path=Path(name)
    src=path.read_text(encoding="utf-8")
    if "QH DESIGN PASS 109" in src:
        print(f"Build 109 already present in {name}; skipping.")
        continue
    if "</head>" not in src:
        raise SystemExit(f"Missing </head> in {name}")
    src=src.replace("</head>", '<style id="qh-design-pass-109">\n'+css+'\n</style>\n</head>', 1)
    path.write_text(src,encoding="utf-8")
print("QH Design Pass 109 applied: teal, parchment, antique gold and copper identity.")
