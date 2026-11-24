from pathlib import Path
import re

css = r"""
/* QH DESIGN PASS 118 — controlled ornamental plaque, no circular overlay */
#app .start.neo-home.qh-experience .hero.qh-hero{
 position:relative!important;isolation:isolate!important;display:flex!important;flex-direction:column!important;
 align-items:center!important;justify-content:center!important;gap:3px!important;
 width:100%!important;min-height:218px!important;height:auto!important;box-sizing:border-box!important;
 margin:0 0 15px!important;padding:13px 18px 12px!important;
 overflow:visible!important;border:0!important;border-radius:0!important;
 background:transparent!important;background-image:none!important;box-shadow:none!important;
 clip-path:none!important;transform:none!important
}
#app .start.neo-home.qh-experience .hero.qh-hero::before{
 content:""!important;display:block!important;position:absolute!important;z-index:0!important;
 inset:0!important;width:100%!important;height:100%!important;margin:0!important;padding:0!important;
 border:0!important;border-radius:0!important;transform:none!important;
 background:linear-gradient(135deg,#d7b56f 0%,#f0d99f 14%,#a47c43 50%,#e7cc8e 86%,#9b713c 100%)!important;
 clip-path:polygon(7% 0,93% 0,96% 5%,98% 14%,100% 25%,98% 37%,100% 50%,98% 63%,100% 75%,98% 86%,96% 95%,93% 100%,7% 100%,4% 95%,2% 86%,0 75%,2% 63%,0 50%,2% 37%,0 25%,2% 14%,4% 5%)!important;
 filter:drop-shadow(0 7px 9px rgba(55,36,17,.17))!important;pointer-events:none!important
}
#app .start.neo-home.qh-experience .hero.qh-hero::after{
 content:""!important;display:block!important;position:absolute!important;z-index:0!important;
 inset:3px!important;width:auto!important;height:auto!important;margin:0!important;padding:0!important;
 border:1px solid rgba(243,222,181,.9)!important;border-radius:0!important;transform:none!important;
 background:linear-gradient(145deg,#19483c 0%,#123d34 58%,#0d332e 100%)!important;
 clip-path:polygon(7% 0,93% 0,96% 5%,98% 14%,100% 25%,98% 37%,100% 50%,98% 63%,100% 75%,98% 86%,96% 95%,93% 100%,7% 100%,4% 95%,2% 86%,0 75%,2% 63%,0 50%,2% 37%,0 25%,2% 14%,4% 5%)!important;
 box-shadow:none!important;pointer-events:none!important
}
#app .start.neo-home.qh-experience .hero.qh-hero .qh-brand-emblem{
 display:block!important;position:relative!important;z-index:2!important;
 width:min(40vw,158px)!important;height:auto!important;max-width:158px!important;max-height:158px!important;
 aspect-ratio:1/1!important;object-fit:contain!important;object-position:center!important;
 margin:0 auto!important;padding:0!important;border:0!important;border-radius:0!important;
 background:transparent!important;background-image:none!important;box-shadow:none!important;
 filter:drop-shadow(0 2px 2px rgba(0,0,0,.28))!important;image-rendering:auto!important
}
#app .start.neo-home.qh-experience .hero.qh-hero .qh-emblem-fallback{display:none!important}
#app .start.neo-home.qh-experience .hero.qh-hero .qh-hero-copy{
 position:relative!important;z-index:2!important;display:flex!important;flex-direction:column!important;
 align-items:center!important;gap:2px!important;max-width:100%!important;margin:0!important;padding:0!important;
 background:transparent!important;text-align:center!important
}
#app .start.neo-home.qh-experience .hero.qh-hero .qh-hero-copy .qh-eyebrow{
 color:#f2dfb7!important;font-size:12px!important;line-height:1.4!important;font-weight:800!important;letter-spacing:0!important
}
#app .start.neo-home.qh-experience .hero.qh-hero .qh-hero-copy p{
 margin:0!important;color:#d9bb83!important;font-size:10px!important;line-height:1.45!important;font-weight:600!important
}
@media(max-width:390px){
 #app .start.neo-home.qh-experience .hero.qh-hero{min-height:198px!important;padding:11px 14px 10px!important}
 #app .start.neo-home.qh-experience .hero.qh-hero .qh-brand-emblem{width:min(39vw,142px)!important;max-width:142px!important;max-height:142px!important}
 #app .start.neo-home.qh-experience .hero.qh-hero .qh-hero-copy .qh-eyebrow{font-size:11px!important}
}
"""

for name in ("www/index.html", "www/game.html"):
    path = Path(name)
    html = path.read_text(encoding="utf-8")
    html = re.sub(r'<style id="qh-design-pass-118">.*?</style>', '', html, flags=re.S)
    if "</head>" not in html:
        raise SystemExit(f"Missing </head> in {name}")
    block = '<style id="qh-design-pass-118">\n/* QH DESIGN PASS 118 */\n' + css + '\n</style>\n</head>'
    html = html.replace("</head>", block, 1)
    path.write_text(html, encoding="utf-8")

for name in ("www/index.html", "www/game.html"):
    html = Path(name).read_text(encoding="utf-8")
    assert "QH DESIGN PASS 118" in html
    assert "#app .start.neo-home.qh-experience .hero.qh-hero::before" in html
    assert "clip-path:polygon" in html
    assert "width:min(39vw,142px)" in html
print("QH Design Pass 118 applied: bounded scalloped plaque, no circular overlay, compact emblem.")
