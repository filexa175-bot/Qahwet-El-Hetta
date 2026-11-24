from pathlib import Path

css = r"""
/* QH DESIGN PASS 115 — ornamental café sign + exact developer signature */
.qh-hero{
  position:relative!important;isolation:isolate!important;
  display:flex!important;flex-direction:column!important;
  align-items:center!important;justify-content:center!important;
  gap:4px!important;
  width:100%!important;min-height:218px!important;height:auto!important;
  box-sizing:border-box!important;
  margin:0 0 15px!important;padding:18px 24px 14px!important;
  overflow:visible!important;border:0!important;border-radius:0!important;
  background:transparent!important;box-shadow:none!important;
}
.qh-hero:before{
  content:""!important;display:block!important;position:absolute!important;
  z-index:-2!important;inset:5px 1px!important;
  background:linear-gradient(145deg,#17463d 0%,#103b35 52%,#0c302e 100%)!important;
  clip-path:polygon(7% 3%,12% 0,88% 0,93% 3%,96% 16%,99% 29%,100% 50%,97% 70%,94% 84%,91% 97%,9% 97%,6% 84%,3% 70%,0 50%,3% 29%,6% 16%)!important;
  filter:drop-shadow(0 9px 10px rgba(42,31,19,.18))!important;
}
.qh-hero:after{
  content:""!important;display:block!important;position:absolute!important;
  z-index:-1!important;inset:10px 7px!important;
  border:1px solid rgba(211,169,99,.9)!important;
  background:
    radial-gradient(ellipse at 50% 0%,rgba(225,188,123,.10),transparent 48%),
    repeating-linear-gradient(135deg,transparent 0 17px,rgba(224,191,139,.025) 18px 19px),
    linear-gradient(145deg,#17443a,#10372f)!important;
  clip-path:polygon(7% 3%,12% 0,88% 0,93% 3%,96% 16%,99% 29%,100% 50%,97% 70%,94% 84%,91% 97%,9% 97%,6% 84%,3% 70%,0 50%,3% 29%,6% 16%)!important;
  pointer-events:none!important;
}
.qh-brand-emblem{
  display:block!important;position:relative!important;z-index:2!important;
  width:min(56vw,218px)!important;height:auto!important;
  max-width:218px!important;max-height:218px!important;
  aspect-ratio:1/1!important;object-fit:contain!important;
  margin:0 auto!important;padding:0!important;
  border:0!important;border-radius:0!important;
  background:transparent!important;box-shadow:none!important;
  filter:drop-shadow(0 2px 0 rgba(239,220,184,.8)) drop-shadow(0 5px 7px rgba(0,0,0,.32))!important;
}
.qh-emblem-fallback{display:none!important}
.qh-hero-copy{
  position:relative!important;z-index:2!important;
  display:flex!important;flex-direction:column!important;align-items:center!important;
  gap:2px!important;max-width:100%!important;margin:0!important;padding:0!important;
  text-align:center!important;
}
.qh-hero-copy .qh-eyebrow{
  color:#f2dfb7!important;font-size:12px!important;line-height:1.4!important;
  font-weight:800!important;letter-spacing:0!important
}
.qh-hero-copy p{
  margin:0!important;color:#d6b77f!important;font-size:10px!important;
  line-height:1.45!important;font-weight:600!important
}
.qh-footer{
  display:flex!important;flex-direction:row!important;align-items:center!important;
  justify-content:center!important;gap:5px!important;
  margin:22px auto 8px!important;padding:8px 12px!important;
  color:#17434a!important;background:transparent!important;
  border:0!important;box-shadow:none!important;text-align:center!important;
  font-family:inherit!important
}
.qh-footer:before{content:"Powered by"!important;display:inline!important;
  color:#8b7256!important;font-size:10px!important;font-weight:700!important;
  letter-spacing:.25px!important}
.qh-footer .qh-dev-kicker,.qh-footer i,.qh-footer small{display:none!important}
.qh-footer b{display:inline!important;color:#17434a!important;
  font-size:12px!important;font-weight:900!important;letter-spacing:.2px!important}
@media(max-width:390px){
 .qh-hero{min-height:192px!important;padding:14px 20px 12px!important;gap:3px!important}
 .qh-brand-emblem{width:min(53vw,190px)!important;max-width:190px!important;max-height:190px!important}
 .qh-hero-copy .qh-eyebrow{font-size:11px!important}
}
"""

for name in ("www/index.html", "www/game.html"):
    path = Path(name)
    src = path.read_text(encoding="utf-8")
    marker = "QH DESIGN PASS 115"
    if marker in src:
        print(f"{marker} already present in {name}; skipping.")
        continue
    if "</head>" not in src:
        raise SystemExit(f"Missing </head> in {name}")
    src = src.replace("</head>", '<style id="qh-design-pass-115">\\n' + css + '\\n</style>\\n</head>', 1)
    path.write_text(src, encoding="utf-8")
print("QH Design Pass 115 applied.")
