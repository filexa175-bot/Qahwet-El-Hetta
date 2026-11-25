from pathlib import Path
import re

css = r"""
/* QH DESIGN PASS 116 — premium ornamental café plaque + exact developer signature */
.qh-hero{
 position:relative!important;isolation:isolate!important;
 display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;
 gap:3px!important;width:100%!important;min-height:224px!important;height:auto!important;
 box-sizing:border-box!important;margin:0 0 15px!important;padding:17px 22px 13px!important;
 overflow:visible!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important
}
.qh-hero:before{
 content:""!important;display:block!important;position:absolute!important;z-index:-2!important;inset:1px 0!important;
 background:linear-gradient(145deg,#d8b875 0%,#a98247 48%,#e3c98f 100%)!important;
 clip-path:polygon(8% 2%,14% 0,86% 0,92% 2%,95% 7%,97% 14%,100% 22%,98% 30%,100% 38%,98% 46%,100% 54%,98% 62%,100% 70%,97% 78%,95% 86%,92% 93%,86% 96%,14% 96%,8% 93%,5% 86%,3% 78%,0 70%,2% 62%,0 54%,2% 46%,0 38%,2% 30%,0 22%,3% 14%,5% 7%)!important;
 filter:drop-shadow(0 9px 12px rgba(48,34,19,.18))!important
}
.qh-hero:after{
 content:""!important;display:block!important;position:absolute!important;z-index:-1!important;inset:5px 5px!important;
 border:1px solid rgba(242,220,174,.92)!important;
 background:radial-gradient(circle at 50% 7%,rgba(235,198,127,.16) 0 2px,transparent 3px),radial-gradient(circle at 50% 93%,rgba(235,198,127,.16) 0 2px,transparent 3px),radial-gradient(circle at 4% 50%,rgba(235,198,127,.14) 0 3px,transparent 4px),radial-gradient(circle at 96% 50%,rgba(235,198,127,.14) 0 3px,transparent 4px),linear-gradient(145deg,#19463b 0%,#123c34 54%,#0d302c 100%)!important;
 clip-path:polygon(8% 2%,14% 0,86% 0,92% 2%,95% 7%,97% 14%,100% 22%,98% 30%,100% 38%,98% 46%,100% 54%,98% 62%,100% 70%,97% 78%,95% 86%,92% 93%,86% 96%,14% 96%,8% 93%,5% 86%,3% 78%,0 70%,2% 62%,0 54%,2% 46%,0 38%,2% 30%,0 22%,3% 14%,5% 7%)!important;
 pointer-events:none!important
}
.qh-brand-emblem{
 display:block!important;position:relative!important;z-index:2!important;width:min(54vw,204px)!important;height:auto!important;
 max-width:204px!important;max-height:204px!important;aspect-ratio:1/1!important;object-fit:contain!important;
 margin:0 auto!important;padding:0!important;border:0!important;border-radius:0!important;background:transparent!important;
 box-shadow:none!important;image-rendering:auto!important;
 filter:drop-shadow(0 2px 0 rgba(241,224,190,.72)) drop-shadow(0 5px 8px rgba(0,0,0,.32))!important
}
.qh-emblem-fallback{display:none!important}
.qh-hero-copy{position:relative!important;z-index:2!important;display:flex!important;flex-direction:column!important;align-items:center!important;gap:2px!important;max-width:100%!important;margin:0!important;padding:0!important;text-align:center!important}
.qh-hero-copy .qh-eyebrow{color:#f3dfb7!important;font-size:12px!important;line-height:1.4!important;font-weight:800!important;letter-spacing:0!important}
.qh-hero-copy p{margin:0!important;color:#d7b77e!important;font-size:10px!important;line-height:1.45!important;font-weight:600!important}
.qh-footer{display:flex!important;flex-direction:row!important;align-items:center!important;justify-content:center!important;gap:5px!important;margin:22px auto 8px!important;padding:8px 12px!important;color:#17434a!important;background:transparent!important;border:0!important;box-shadow:none!important;text-align:center!important;font-family:inherit!important}
.qh-footer .qh-dev-kicker{display:inline!important;color:#8b7256!important;font-size:10px!important;font-weight:700!important;letter-spacing:.25px!important}
.qh-footer i,.qh-footer small{display:none!important}
.qh-footer b{display:inline!important;color:#17434a!important;font-size:12px!important;font-weight:900!important;letter-spacing:.2px!important}
@media(max-width:390px){.qh-hero{min-height:204px!important;padding:13px 18px 11px!important;gap:2px!important}.qh-brand-emblem{width:min(51vw,184px)!important;max-width:184px!important;max-height:184px!important}.qh-hero-copy .qh-eyebrow{font-size:11px!important}}
"""

template = Path("../scripts/player-home-screen.html.txt")
source = template.read_text(encoding="utf-8")
footer = '<footer class="qh-footer"><span class="qh-dev-kicker">Powered by</span><b>Filexawy</b></footer>'
source, count = re.subn(r'<footer class="qh-footer">.*?</footer>', footer, source, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f"Expected one developer footer, found {count}.")
if "Powered by</span><b>Filexawy</b>" not in source:
    raise SystemExit("Developer signature order validation failed.")
template.write_text(source, encoding="utf-8")

for name in ("www/index.html", "www/game.html"):
    path = Path(name)
    html = path.read_text(encoding="utf-8")
    marker = "QH DESIGN PASS 116"
    html = re.sub(r'<style id="qh-design-pass-116">.*?</style>', '', html, flags=re.S)
    if "</head>" not in html:
        raise SystemExit(f"Missing </head> in {name}")
    html = html.replace("</head>", '<style id="qh-design-pass-116">\n' + marker + "\n" + css + '\n</style>\n</head>', 1)
    path.write_text(html, encoding="utf-8")

print("QH Design Pass 116 applied: ornamental plaque and exact Powered by Filexawy signature.")
