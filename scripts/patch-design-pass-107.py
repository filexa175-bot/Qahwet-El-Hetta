from pathlib import Path

# Build 107: replace the olive/green-heavy palette with a warm Egyptian café identity.
css = r"""
/* QH DESIGN PASS 107 — warm café / parchment / espresso identity */
:root{
 --qh-paper:#f3e8d5;--qh-paper-2:#e8d8bd;--qh-ink:#38271f;--qh-ink-2:#52392b;
 --qh-coffee:#4b3024;--qh-coffee-deep:#2d1e18;--qh-copper:#a85f3c;
 --qh-copper-light:#c78358;--qh-brass:#b58b52;--qh-muted:#806d5b;
 --qh-line:rgba(91,61,43,.2);--qh-shadow:0 12px 30px rgba(54,34,22,.13)
}
html,body{background:#eadcc5!important;color:var(--qh-ink)!important}
#app{background:transparent!important}
.start.neo-home.qh-experience{
 box-sizing:border-box;width:min(100%,620px);min-height:100dvh;margin:0 auto;
 padding:clamp(12px,3vw,22px) clamp(13px,4vw,22px) 132px!important;
 background:radial-gradient(ellipse at 50% -12%,#fff8eb 0,#f1e5d1 48%,#e8d8bf 100%)!important;
 color:var(--qh-ink)!important;font-family:'Cairo',system-ui,sans-serif;position:relative;overflow:visible!important
}
.qh-topline{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 auto 14px;max-width:560px}
.qh-brand-sign{display:grid;grid-template-columns:42px auto;grid-template-rows:auto auto;align-items:center;column-gap:8px;color:var(--qh-coffee);min-width:0}
.qh-sign-art{width:42px;height:40px;grid-row:1/3;filter:none}
.qh-sign-ar{font-size:19px;font-weight:900;line-height:1.15;white-space:nowrap;letter-spacing:-.5px;color:var(--qh-coffee)}
.qh-sign-sub{font-size:9px;letter-spacing:.5px;color:#8b6a4c;white-space:nowrap}
.qh-powered{display:flex;flex-direction:column;align-items:flex-end;gap:0;padding:4px 0 4px 11px;border-left:1px solid rgba(91,61,43,.24);line-height:1.15;flex-shrink:0}
.qh-powered span,.qh-powered i{font:700 8px/1.4 system-ui,sans-serif;letter-spacing:1.5px;color:#927a62}
.qh-powered b{font:800 15px/1.25 system-ui,sans-serif;color:var(--qh-coffee)}
.qh-powered i{font-style:normal;font-size:7px;color:#9b7959}
.qh-hero{
 position:relative;display:flex;align-items:center;justify-content:space-between;gap:10px;
 min-height:112px;padding:19px 19px 22px!important;margin:0 0 12px;
 border:1px solid #9e7048!important;border-radius:16px!important;
 background:linear-gradient(112deg,#503326 0%,#3a261e 70%,#2e201a 100%)!important;
 box-shadow:inset 0 1px rgba(255,255,255,.12),0 9px 22px rgba(54,34,22,.18)!important;overflow:hidden
}
.qh-hero:before{content:"";position:absolute;width:190px;height:190px;border:1px solid rgba(226,190,143,.18);border-radius:50%;right:-90px;top:-65px;box-shadow:0 0 0 14px rgba(226,190,143,.035),0 0 0 31px rgba(226,190,143,.025)}
.qh-hero:after{content:"";position:absolute;inset:auto 18px 10px;height:1px;background:linear-gradient(90deg,transparent,#d0a875aa,transparent)}
.qh-hero-copy{position:relative;z-index:1}
.qh-eyebrow{font-size:10px;font-weight:800;color:#e6c79c;letter-spacing:.5px}
.qh-hero h1{margin:4px 0 2px!important;color:#fff2dc!important;font-size:clamp(26px,7vw,36px)!important;line-height:1.3!important;font-weight:900!important;letter-spacing:-1px;text-shadow:0 2px 8px #0005}
.qh-hero p{margin:2px 0 0!important;color:#d9c5ac!important;font-size:11px!important}
.qh-hero-seal{z-index:1;display:flex;flex-direction:column;align-items:center;justify-content:center;width:70px;height:70px;flex:0 0 70px;border:1px solid rgba(231,197,151,.7);border-radius:50%;outline:1px solid rgba(231,197,151,.25);outline-offset:4px;color:#f0d3a8;background:rgba(20,12,8,.18);transform:rotate(-7deg)}
.qh-hero-seal span{font-size:9px;color:#dfc29d}.qh-hero-seal b{font-size:17px;line-height:1.2}.qh-hero-seal small{font:700 7px system-ui;letter-spacing:1px;color:#c4a17a}
.qh-hero-rule{position:absolute;bottom:6px;left:20px;right:20px;display:flex;align-items:center;gap:7px;color:#d1a675;font-size:8px}.qh-hero-rule i{height:1px;flex:1;background:linear-gradient(90deg,transparent,#d1a67588,transparent)}
.qh-stepper{display:flex;align-items:center;justify-content:center;gap:12px;margin:0 auto 14px;max-width:410px;padding:8px 10px 10px;border-bottom:1px solid rgba(91,61,43,.18)}
.qh-stepper>div{display:flex;align-items:center;gap:7px;color:#9a8874;font-size:11px;font-weight:800;white-space:nowrap}
.qh-stepper>div b{display:grid;place-items:center;width:25px;height:25px;border:1px solid #bca78b;border-radius:50%;font:700 9px system-ui;color:#816b55;background:#f8efdf}
.qh-stepper>div.active{color:var(--qh-coffee)}.qh-stepper>div.active b{background:var(--qh-copper);border-color:var(--qh-copper);color:#fff5e7;box-shadow:0 0 0 3px #a85f3c20}
.qh-stepper>i{height:1px;width:42px;background:linear-gradient(90deg,#c4ad8e,#a85f3c)}
.qh-panel{position:relative;margin:0 0 12px;padding:14px 7px 12px!important;border:0!important;border-top:1px solid rgba(91,61,43,.18)!important;border-bottom:1px solid rgba(91,61,43,.14)!important;border-radius:0!important;background:transparent!important;box-shadow:none!important}
.qh-section-title{display:flex;align-items:center;gap:9px;margin:0 0 13px}
.qh-index{display:grid;place-items:center;flex:0 0 30px;height:30px;border:1px solid rgba(168,95,60,.45);border-radius:50%;background:#f8ecda;color:var(--qh-copper);font:800 10px system-ui}
.qh-section-title h3,.qh-character-head h3{margin:0!important;color:var(--qh-coffee)!important;font-size:15px!important;font-weight:900!important;line-height:1.45}
.qh-section-title p,.qh-character-head p{margin:1px 0 0!important;color:#88745f!important;font-size:10px!important}
.qh-section-tag{margin-right:auto;color:#9b8469;font:700 7px system-ui;letter-spacing:1px}
.qh-field-label{display:block;margin:0 0 6px;color:#614431;font-size:11px;font-weight:900}
.qh-input-wrap{position:relative}
.qh-input-icon{position:absolute;right:13px;top:50%;transform:translateY(-50%);color:var(--qh-copper);z-index:1}
.qh-name-input{box-sizing:border-box;width:100%;height:48px;padding:0 37px 0 13px!important;border:1px solid #c3a889!important;border-radius:9px!important;background:#fffaf1!important;color:#39281f!important;font-size:14px!important;box-shadow:inset 0 1px 3px rgba(67,42,25,.06)!important}
.qh-name-input::placeholder{color:#a28e78!important}
.qh-name-input:focus{outline:2px solid rgba(168,95,60,.2);border-color:var(--qh-copper)!important}
.qh-id-row{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:9px 0 12px;padding:8px 2px;border:0;border-bottom:1px solid rgba(91,61,43,.15);border-radius:0;background:transparent}
.qh-id-row>div{display:flex;flex-direction:column;gap:2px;min-width:0}.qh-id-row small{font:700 8px system-ui;letter-spacing:1.3px;color:#9b8268}.qh-id-row b{font:700 10px system-ui;color:#52392b;overflow-wrap:anywhere}
.qh-copy-id{border:1px solid #b99672;border-radius:7px;padding:7px 10px;background:#f8eddd;color:#6d472f;font-size:10px;font-weight:900;white-space:nowrap}
.qh-google-login{display:flex;align-items:center;gap:10px;width:100%;padding:10px 12px;border:1px solid #c6a989;border-radius:9px;background:#fff9ef;color:#39281f;text-align:right}
.qh-google-g{display:grid;place-items:center;width:29px;height:29px;border-radius:8px;background:#fff;color:#4285f4;font:900 17px Arial;box-shadow:0 1px 4px #0001}
.qh-google-login>span:nth-child(2){display:flex;flex-direction:column;flex:1}.qh-google-login b{font-size:12px;color:#493124}.qh-google-login small{font-size:9px;color:#88745f}.qh-google-login i{font-style:normal;font-size:17px;color:var(--qh-copper)}
.qh-login-note{margin:6px 2px 12px;color:#907d68;font-size:9px;text-align:center}
.qh-account-state{display:flex;align-items:center;gap:9px;margin:0 0 12px;padding:8px 0;border:0;border-bottom:1px solid rgba(91,61,43,.16);border-radius:0;background:transparent}
.qh-account-state>span{display:grid;place-items:center;width:24px;height:24px;border-radius:50%;background:#6e7d54;color:#fff}.qh-account-state div{display:flex;flex-direction:column}.qh-account-state b{font-size:11px;color:#4b392a}.qh-account-state small{font-size:9px;color:#8a7865}
.qh-character-head{display:flex;align-items:center;justify-content:space-between;margin:13px 0 8px;padding-top:11px;border-top:1px solid rgba(91,61,43,.14)}.qh-character-head>span{color:var(--qh-copper);font:800 10px system-ui}
.qh-avatar-pick{display:grid!important;grid-template-columns:repeat(auto-fit,minmax(62px,1fr));gap:9px!important}
.qh-avatar-pick button{display:flex!important;flex-direction:column;align-items:center;justify-content:center;gap:4px;min-width:0;min-height:76px;padding:5px 3px!important;border:1px solid transparent!important;border-bottom:2px solid #cdb89a!important;border-radius:8px!important;background:transparent!important;color:#503829!important;box-shadow:none!important;transition:transform .15s,border-color .15s}
.qh-avatar-pick button.on{border:1px solid #b4774d!important;border-bottom:3px solid var(--qh-copper)!important;border-radius:8px!important;background:#f8eddd!important;box-shadow:0 3px 10px rgba(75,48,36,.08)!important;transform:translateY(-2px)}
.qh-avatar-art{font-size:27px;line-height:1.2}.qh-avatar-pick button small{font-size:8px;color:#7b624c}
.qh-bottom-actions{position:fixed!important;left:50%!important;right:auto!important;bottom:calc(7px + env(safe-area-inset-bottom))!important;transform:translateX(-50%);z-index:9999;box-sizing:border-box;width:min(calc(100% - 20px),576px);display:flex;flex-direction:column;gap:6px;margin:0!important;padding:10px 12px calc(8px + env(safe-area-inset-bottom))!important;border:1px solid rgba(117,78,52,.22);border-radius:13px;background:rgba(250,243,230,.97);box-shadow:0 5px 22px rgba(54,34,22,.17);backdrop-filter:blur(12px)}
.qh-step-caption{text-align:center;color:#907a63;font-size:9px}
.qh-primary{width:100%;min-height:46px;padding:10px 16px!important;border:1px solid #87482f!important;border-radius:9px!important;background:linear-gradient(110deg,#b96d48,#984c32)!important;color:#fff5e8!important;font-size:14px!important;font-weight:900!important;box-shadow:0 3px 8px rgba(75,48,36,.18)!important}
.qh-primary span{display:inline-block;margin-right:8px;font-size:17px;vertical-align:-1px}
.qh-two-actions{flex-direction:row}.qh-two-actions .qh-primary{flex:1}.qh-back{min-width:88px;border:1px solid #b99b7b!important;border-radius:9px!important;background:#f8eddd!important;color:#62432f!important}
.qh-mode-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.qh-mode-card{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:5px;min-height:102px;padding:10px 9px!important;border:1px solid #c9b296;border-radius:10px;background:#fff8ed;color:#503829;text-align:right}
.qh-mode-card.selected{border-color:#a85f3c;background:#f5e4d1;box-shadow:inset 0 0 0 1px #a85f3c25}
.qh-mode-card:disabled{opacity:.55;filter:grayscale(.25)}
.qh-mode-symbol{display:grid;place-items:center;width:29px;height:29px;border-radius:8px;background:#ead8c2;color:#8d5036;font-size:18px}
.qh-mode-card b{font-size:11px;color:#4b3024}.qh-mode-card small{font-size:9px;color:#907a63}.qh-mode-card i{position:absolute;left:8px;top:8px;font-style:normal;color:#a85f3c;font-size:12px}
.qh-games-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.qh-game-card{display:flex!important;flex-direction:column;align-items:center;justify-content:center;gap:5px;min-height:94px;padding:9px 5px!important;border:1px solid #c7ae91!important;border-radius:10px!important;background:#fff8ed!important;color:#503829!important;box-shadow:none!important}
.qh-game-card>b{font-size:25px;line-height:1.2;color:#8c5639}.qh-game-card strong{font-size:12px!important;color:#503829!important}.qh-game-card small{font-size:9px!important;color:#907a63!important}
.qh-game-card.on{border-color:#a85f3c!important;background:#f4e2ce!important;box-shadow:inset 0 0 0 1px #a85f3c30!important}
.qh-game-card.off{opacity:.5;filter:grayscale(.45)}
.qh-stake-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px}
.qh-stake-opt{min-height:44px;border:1px solid #c7ae91!important;border-radius:8px!important;background:#fff8ed!important;color:#503829!important}.qh-stake-opt.on{border-color:#a85f3c!important;background:#f3e0cc!important}
.qh-stake-opt b{font-size:15px}.qh-stake-opt small{font-size:9px}
.qh-stake-summary{color:#806b56!important;font-size:10px}.qh-stake-summary b{color:#9d5637!important}
.qh-difficulty-panel .difficulty-grid{gap:7px}.qh-difficulty-panel .difficulty-opt{border-radius:8px!important;background:#fff8ed!important;color:#503829!important}.qh-difficulty-panel .difficulty-opt.on{border-color:#a85f3c!important;background:#f3e0cc!important}
.qh-footer{display:flex;align-items:center;justify-content:center;gap:7px;flex-wrap:wrap;margin:18px auto 0;padding-top:10px;border-top:1px solid rgba(91,61,43,.14);color:#8c765f}
.qh-footer span{font-size:10px;font-weight:900;color:#67432e}.qh-footer i{width:3px;height:3px;border-radius:50%;background:#b58b52}.qh-footer b{font:700 9px system-ui;color:#79543a}.qh-footer small{flex-basis:100%;text-align:center;font:700 7px system-ui;letter-spacing:1.7px;color:#a18c73}
.qh-experience .brand-mark,.qh-experience .hero-cup,.qh-experience .step-progress{display:none!important}
.qh-experience .wallet-bubble,.qh-experience .wallet-pill,.qh-experience .qh-wallet-bubble{background:#4b3024!important;color:#fff1dc!important;border-color:#bd986b!important}
@media(max-width:390px){
 .start.neo-home.qh-experience{padding:9px 10px 138px!important}
 .qh-hero{min-height:104px;padding:15px 14px 20px!important}
 .qh-hero-seal{width:62px;height:62px;flex-basis:62px}
 .qh-hero h1{font-size:26px!important}
 .qh-panel{padding:12px 3px 10px!important}
 .qh-mode-card{min-height:96px;padding:8px 6px!important}
 .qh-mode-card b{font-size:10px}
 .qh-games-grid{gap:6px}.qh-game-card{min-height:88px}
 .qh-avatar-pick{grid-template-columns:repeat(auto-fit,minmax(54px,1fr))!important}
}
@media(min-width:560px){
 .qh-profile-panel,.qh-choice-panel,.qh-game-panel,.qh-stake-section,.qh-difficulty-panel{padding-left:12px!important;padding-right:12px!important}
 .qh-avatar-pick{grid-template-columns:repeat(6,1fr)!important}
}
"""
for name in ("www/index.html", "www/game.html"):
    path = Path(name)
    src = path.read_text(encoding="utf-8")
    if "QH DESIGN PASS 107" in src:
        print(f"Build 107 already applied in {name}; skipping.")
        continue
    if "</head>" not in src:
        raise SystemExit(f"Missing </head> in {name}")
    src = src.replace("</head>", '<style id="qh-design-pass-107">\n' + css + '\n</style>\n</head>', 1)
    path.write_text(src, encoding="utf-8")
print("QH Design Pass 107 applied: parchment/espresso palette and fixed onboarding actions.")
