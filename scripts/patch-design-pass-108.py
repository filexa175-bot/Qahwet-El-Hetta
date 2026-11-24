from pathlib import Path

css = r"""
/* QH DESIGN PASS 108 — editorial layout, natural scrolling, single game identity */
html,body{min-height:100%;height:auto!important;overflow-x:hidden!important;overflow-y:auto!important;background:#eadcc5!important}
body{overscroll-behavior-y:contain}
#app{height:auto!important;min-height:100dvh!important;max-height:none!important;overflow:visible!important}
.start.neo-home.qh-experience{
 box-sizing:border-box;width:min(100%,620px);min-height:100dvh;height:auto!important;max-height:none!important;
 margin:0 auto;padding:clamp(16px,4vw,26px) clamp(16px,4vw,24px) calc(28px + env(safe-area-inset-bottom))!important;
 overflow:visible!important;overflow-y:visible!important;position:relative;
 background:radial-gradient(ellipse at 50% -12%,#fff8eb 0,#f1e5d1 48%,#e8d8bf 100%)!important;
 color:#38271f!important
}
.qh-topline,.qh-brand-sign,.qh-sign-art,.qh-sign-ar,.qh-sign-sub{display:none!important}
.qh-hero{
 min-height:126px;margin:0 0 18px;padding:22px 22px 27px!important;
 border:0!important;border-radius:0!important;
 border-block:1px solid rgba(141,91,54,.55)!important;
 background:linear-gradient(110deg,#4b3024 0%,#39251c 72%,#2d1e18 100%)!important;
 box-shadow:0 10px 24px rgba(54,34,22,.12)!important;overflow:hidden
}
.qh-hero:before{width:180px;height:180px;right:-92px;top:-65px;border-color:#e7c99b22;box-shadow:0 0 0 16px #e7c99b08,0 0 0 34px #e7c99b06}
.qh-hero:after{inset:auto 22px 11px;height:1px;background:linear-gradient(90deg,transparent,#d0a875aa,transparent)}
.qh-hero-copy{max-width:80%}
.qh-eyebrow{font-size:11px;color:#e5c79e}
.qh-hero h1{font-size:clamp(30px,8vw,40px)!important;letter-spacing:-1.2px;color:#fff0d7!important}
.qh-hero p{font-size:12px!important;color:#d7c2a7!important}
.qh-hero-seal{width:70px;height:70px;flex-basis:70px;border-radius:50%;border-color:#d9b88699;outline:0;background:transparent}
.qh-hero-rule{display:none!important}
.qh-stepper{margin:0 auto 22px;padding:8px 2px 13px;border:0;border-bottom:1px solid rgba(91,61,43,.16);gap:16px}
.qh-stepper>div{font-size:12px;color:#927e68}
.qh-stepper>div b{width:27px;height:27px;background:transparent;border-color:#bba58a;color:#80684f}
.qh-stepper>div.active b{background:#a85f3c;border-color:#a85f3c;color:#fff4e5;box-shadow:none}
.qh-stepper>i{width:36px;background:#c6aa87}
.qh-panel{
 margin:0 0 22px;padding:7px 0 18px!important;
 border:0!important;border-radius:0!important;border-bottom:1px solid rgba(91,61,43,.17)!important;
 background:transparent!important;box-shadow:none!important
}
.qh-section-title{gap:11px;margin:0 0 18px}
.qh-index{width:auto;height:auto;flex:0 0 auto;border:0;border-radius:0;background:transparent;color:#a85f3c;font:800 12px system-ui}
.qh-section-title h3,.qh-character-head h3{font-size:17px!important;color:#402b20!important}
.qh-section-title p,.qh-character-head p{font-size:11px!important;color:#8a755e!important}
.qh-section-tag{font-size:8px;color:#9b8469}
.qh-field-label{font-size:12px;color:#64452f;margin-bottom:8px}
.qh-input-wrap{position:relative;isolation:isolate}
.qh-input-wrap:before,.qh-input-wrap:after{content:none!important;display:none!important}
.qh-input-wrap .brand-mark,.qh-input-wrap [class*="brand"],.qh-input-wrap img{display:none!important}
.qh-name-input,.neo-home .name-input.qh-name-input{
 width:100%;height:54px!important;min-height:54px!important;box-sizing:border-box;
 padding:0 15px!important;border:0!important;border-bottom:2px solid #b99570!important;border-radius:0!important;
 background:#fff9ef!important;background-image:none!important;color:#39281f!important;
 font-size:16px!important;font-weight:700;text-align:right;box-shadow:none!important
}
.qh-name-input::placeholder{color:#a28e78!important;font-weight:400}
.qh-name-input:focus{outline:0!important;border-bottom-color:#a85f3c!important;box-shadow:0 2px 0 #a85f3c!important}
.qh-id-row{margin:13px 0 15px;padding:9px 0;border:0;border-bottom:1px solid rgba(91,61,43,.14);border-radius:0;background:transparent}
.qh-copy-id{border:0;border-bottom:1px solid #b99672;border-radius:0;background:transparent;padding:7px 2px;color:#744b32}
.qh-google-login{border:0;border-bottom:1px solid #c7ad90;border-radius:0;background:transparent;padding:12px 0;color:#493124}
.qh-google-g{border-radius:50%;box-shadow:none;background:#fff}
.qh-login-note{margin:8px 0 13px;text-align:right}
.qh-account-state{margin:0 0 15px;padding:9px 0;border:0;border-bottom:1px solid rgba(91,61,43,.14);border-radius:0;background:transparent}
.qh-account-state>span{background:#718052}
.qh-account-state b{color:#4b392a}
.qh-character-head{margin:18px 0 10px;padding-top:14px;border-top:1px solid rgba(91,61,43,.12)}
.qh-avatar-pick{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:18px!important}
.qh-avatar-pick button,.qh-avatar-pick button.on{
 min-height:0!important;padding:7px 3px 9px!important;border:0!important;border-bottom:2px solid transparent!important;
 border-radius:0!important;background:transparent!important;box-shadow:none!important;color:#503829!important;transform:none!important
}
.qh-avatar-pick button.on{border-bottom-color:#a85f3c!important}
.qh-avatar-art{font-size:34px;line-height:1.2}
.qh-avatar-pick button small{font-size:9px;color:#806b56}
.qh-mode-grid{display:flex;flex-direction:column;gap:0}
.qh-mode-card{
 display:grid;grid-template-columns:42px 1fr auto;grid-template-rows:auto auto;align-items:center;column-gap:12px;
 min-height:0;padding:12px 0!important;border:0;border-bottom:1px solid rgba(91,61,43,.14);
 border-radius:0;background:transparent;color:#503829;text-align:right
}
.qh-mode-card.selected{border-color:rgba(168,95,60,.45);background:transparent;box-shadow:none}
.qh-mode-symbol{grid-row:1/3;width:36px;height:36px;border-radius:50%;background:#e4d2b9;color:#875438}
.qh-mode-card b{font-size:13px;color:#4b3024}
.qh-mode-card small{font-size:10px;color:#907a63}
.qh-mode-card i{position:static;grid-column:3;grid-row:1/3;font-size:17px;color:#a85f3c}
.qh-mode-card:disabled{opacity:.58;filter:none}
.qh-games-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:12px!important}
.qh-game-card,.qh-game-card.on{
 min-height:0!important;padding:8px 2px 11px!important;border:0!important;border-bottom:2px solid transparent!important;
 border-radius:0!important;background:transparent!important;box-shadow:none!important;color:#503829!important
}
.qh-game-card.on{border-bottom-color:#a85f3c!important}
.qh-game-card>b{font-size:32px;color:#6f4932;filter:none}
.qh-game-card strong{font-size:13px!important;color:#4b3024!important}
.qh-game-card small{font-size:10px!important;color:#8d7964!important}
.qh-game-card.off{opacity:.5;filter:grayscale(.35)}
.qh-stake-grid{gap:10px}
.qh-stake-opt{border:0!important;border-bottom:1px solid #c5ad90!important;border-radius:0!important;background:transparent!important;color:#503829!important}
.qh-stake-opt.on{border-bottom:2px solid #a85f3c!important;background:transparent!important}
.qh-difficulty-panel .difficulty-opt{border:0!important;border-bottom:1px solid #c5ad90!important;border-radius:0!important;background:transparent!important;color:#503829!important}
.qh-difficulty-panel .difficulty-opt.on{border-bottom:2px solid #a85f3c!important;background:transparent!important}
.qh-bottom-actions{
 position:static!important;inset:auto!important;transform:none!important;z-index:auto!important;
 display:flex!important;flex-direction:column;gap:9px;width:100%;box-sizing:border-box;
 margin:18px 0 0!important;padding:0!important;border:0!important;border-radius:0!important;
 background:transparent!important;box-shadow:none!important;backdrop-filter:none!important
}
.qh-two-actions{flex-direction:row}
.qh-step-caption{text-align:center;color:#907a63;font-size:10px}
.qh-primary{min-height:50px;border:0!important;border-radius:7px!important;background:#a85f3c!important;color:#fff8ed!important;box-shadow:none!important;font-size:15px!important}
.qh-primary span{font-size:17px}
.qh-back{min-width:92px;border:1px solid #b99b7b!important;border-radius:7px!important;background:transparent!important;color:#62432f!important}
.qh-footer{
 display:flex;align-items:center;justify-content:center;gap:7px;flex-wrap:wrap;
 margin:28px auto 0;padding:14px 0 0;border-top:1px solid rgba(91,61,43,.14);color:#907a63
}
.qh-footer .qh-dev-kicker{font:700 7px system-ui;letter-spacing:1.5px;color:#9b8469}
.qh-footer b{font:800 12px system-ui;color:#68452f}
.qh-footer i{width:3px;height:3px;border-radius:50%;background:#b58b52}
.qh-footer small{font:700 7px system-ui;letter-spacing:1.3px;color:#a18c73}
.qh-experience .brand-mark,.qh-experience .hero-cup,.qh-experience .step-progress{display:none!important}
.qh-experience .wallet-bubble,.qh-experience .wallet-pill,.qh-experience .qh-wallet-bubble{background:#4b3024!important;color:#fff1dc!important;border-color:#bd986b!important}
@media(max-width:390px){
 .start.neo-home.qh-experience{padding:14px 14px calc(25px + env(safe-area-inset-bottom))!important}
 .qh-hero{min-height:112px;padding:18px 16px 22px!important}
 .qh-hero-seal{width:61px;height:61px;flex-basis:61px}
 .qh-hero h1{font-size:29px!important}
 .qh-panel{padding:5px 0 16px!important}
 .qh-avatar-pick{gap:12px!important}
 .qh-mode-card{grid-template-columns:38px 1fr auto}
 .qh-game-card>b{font-size:28px}
}
"""
for name in ("www/index.html", "www/game.html"):
    path=Path(name)
    src=path.read_text(encoding="utf-8")
    if "QH DESIGN PASS 108" in src:
        raise SystemExit(f"Build 108 already applied in {name}")
    if "</head>" not in src:
        raise SystemExit(f"Missing </head> in {name}")
    src=src.replace("</head>", '<style id="qh-design-pass-108">\n'+css+'\n</style>\n</head>', 1)
    path.write_text(src,encoding="utf-8")
print("QH Design Pass 108 applied: normal-flow actions, open editorial layout, one game identity and independent developer credit.")
