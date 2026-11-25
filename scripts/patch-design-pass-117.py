from pathlib import Path
import re

css = r"""
/* QH DESIGN PASS 117 — refined ornamental café plaque */
.qh-hero{
 position:relative!important;isolation:isolate!important;display:flex!important;flex-direction:column!important;
 align-items:center!important;justify-content:center!important;gap:2px!important;width:100%!important;
 min-height:222px!important;height:auto!important;box-sizing:border-box!important;margin:0 0 15px!important;
 padding:15px 24px 12px!important;overflow:visible!important;border:0!important;border-radius:0!important;
 background:transparent!important;box-shadow:none!important
}
.qh-hero:before{
 content:""!important;display:block!important;position:absolute!important;z-index:-2!important;inset:0!important;
 background:linear-gradient(135deg,#d8b66e 0%,#9e7844 22%,#e3c98e 50%,#9e7844 78%,#d8b66e 100%)!important;
 clip-path:polygon(8% 3%,13% 0,87% 0,92% 3%,95% 10%,98% 18%,100% 28%,98% 38%,100% 50%,98% 62%,100% 72%,98% 82%,95% 90%,92% 97%,87% 100%,13% 100%,8% 97%,5% 90%,2% 82%,0 72%,2% 62%,0 50%,2% 38%,0 28%,2% 18%,5% 10%)!important;
 filter:drop-shadow(0 8px 11px rgba(50,34,18,.18))!important
}
.qh-hero:after{
 content:""!important;display:block!important;position:absolute!important;z-index:-1!important;inset:4px!important;
 border:1px solid rgba(242,221,177,.95)!important;
 background:radial-gradient(circle at 50% 5%,rgba(226,190,125,.18) 0 2px,transparent 3px),radial-gradient(circle at 50% 95%,rgba(226,190,125,.18) 0 2px,transparent 3px),linear-gradient(145deg,#19483c 0%,#123d34 55%,#0e332e 100%)!important;
 clip-path:polygon(8% 3%,13% 0,87% 0,92% 3%,95% 10%,98% 18%,100% 28%,98% 38%,100% 50%,98% 62%,100% 72%,98% 82%,95% 90%,92% 97%,87% 100%,13% 100%,8% 97%,5% 90%,2% 82%,0 72%,2% 62%,0 50%,2% 38%,0 28%,2% 18%,5% 10%)!important;
 pointer-events:none!important
}
.qh-brand-emblem{
 display:block!important;position:relative!important;z-index:2!important;width:min(48vw,190px)!important;
 height:auto!important;max-width:190px!important;max-height:190px!important;aspect-ratio:1/1!important;
 object-fit:contain!important;margin:0 auto!important;padding:0!important;border:0!important;border-radius:0!important;
 background:transparent!important;box-shadow:none!important;
 filter:drop-shadow(0 2px 0 rgba(245,229,198,.72)) drop-shadow(0 4px 7px rgba(0,0,0,.28))!important;
 image-rendering:auto!important
}
.qh-emblem-fallback{display:none!important}
.qh-hero-copy{position:relative!important;z-index:2!important;display:flex!important;flex-direction:column!important;
 align-items:center!important;gap:2px!important;max-width:100%!important;margin:0!important;padding:0!important;text-align:center!important}
.qh-hero-copy .qh-eyebrow{color:#f2dfb7!important;font-size:12px!important;line-height:1.4!important;font-weight:800!important;letter-spacing:0!important}
.qh-hero-copy p{margin:0!important;color:#d9bb83!important;font-size:10px!important;line-height:1.45!important;font-weight:600!important}
.qh-footer{display:flex!important;flex-direction:row!important;align-items:center!important;justify-content:center!important;gap:5px!important;
 margin:22px auto 8px!important;padding:8px 12px!important;color:#17434a!important;background:transparent!important;
 border:0!important;box-shadow:none!important;text-align:center!important}
.qh-footer .qh-dev-kicker{display:inline!important;color:#8b7256!important;font-size:10px!important;font-weight:700!important;letter-spacing:.25px!important}
.qh-footer b{display:inline!important;color:#17434a!important;font-size:12px!important;font-weight:900!important;letter-spacing:.2px!important}
.qh-footer i,.qh-footer small,.qh-footer:before{display:none!important;content:none!important}
@media(max-width:390px){
 .qh-hero{min-height:204px!important;padding:12px 18px 10px!important;gap:2px!important}
 .qh-brand-emblem{width:min(46vw,174px)!important;max-width:174px!important;max-height:174px!important}
 .qh-hero-copy .qh-eyebrow{font-size:11px!important}
}
"""

template = Path("../scripts/player-home-screen.html.txt")
source = template.read_text(encoding="utf-8")
footer = '<footer class="qh-footer"><span class="qh-dev-kicker">Powered by</span><b>Filexawy</b></footer>'
source, count = re.subn(r'<footer class="qh-footer">.*?</footer>', lambda _: footer, source, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f"Expected exactly one developer signature, found {count}")
if "Powered by</span><b>Filexawy</b>" not in source:
    raise SystemExit("Developer signature order validation failed")
template.write_text(source, encoding="utf-8")

for name in ("www/index.html", "www/game.html"):
    path = Path(name)
    html = path.read_text(encoding="utf-8")
    html = re.sub(r'<style id="qh-design-pass-117">.*?</style>', '', html, flags=re.S)
    if "</head>" not in html:
        raise SystemExit(f"Missing </head> in {name}")
    block = '<style id="qh-design-pass-117">\n/* QH DESIGN PASS 117 */\n' + css + '\n</style>\n</head>'
    html = html.replace("</head>", block, 1)
    path.write_text(html, encoding="utf-8")

assert "QH DESIGN PASS 117" in Path("www/index.html").read_text(encoding="utf-8")
assert "QH DESIGN PASS 117" in Path("www/game.html").read_text(encoding="utf-8")
assert "Powered by</span><b>Filexawy</b>" in template.read_text(encoding="utf-8")
print("QH Design Pass 117 applied: refined café plaque and exact Powered by Filexawy signature.")
