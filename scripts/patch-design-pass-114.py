from pathlib import Path

css = r"""
/* QH DESIGN PASS 114 — transparent hero; visual outline hugs the emblem only */
.qh-hero{
  display:flex!important;flex-direction:column!important;
  align-items:center!important;justify-content:center!important;
  gap:7px!important;width:100%!important;height:auto!important;
  min-height:0!important;max-height:none!important;box-sizing:border-box!important;
  margin:0 0 17px!important;padding:8px 0 10px!important;
  border:0!important;border-radius:0!important;
  background:transparent!important;box-shadow:none!important;
  overflow:visible!important;
}
.qh-hero:before,.qh-hero:after{display:none!important;content:none!important}
.qh-brand-emblem{
  display:block!important;position:relative!important;z-index:1!important;
  width:min(42vw,156px)!important;height:auto!important;
  max-width:156px!important;max-height:156px!important;
  aspect-ratio:1/1!important;object-fit:contain!important;
  margin:0 auto!important;padding:0!important;border:0!important;
  border-radius:0!important;background:transparent!important;box-shadow:none!important;
  filter:drop-shadow(0 0 1px rgba(246,235,211,.95))
         drop-shadow(0 0 2px rgba(201,154,80,.78))!important;
  image-rendering:auto!important;
}
.qh-emblem-fallback{display:none!important}
.qh-hero-copy{
  position:relative!important;z-index:1!important;
  display:flex!important;flex-direction:column!important;align-items:center!important;
  gap:3px!important;max-width:100%!important;margin:0!important;padding:0!important;
  text-align:center!important;
}
.qh-hero-copy .qh-eyebrow{
  color:#123f49!important;font-size:13px!important;line-height:1.4!important;
  font-weight:800!important;letter-spacing:0!important
}
.qh-hero-copy p{
  margin:0!important;color:#88745a!important;font-size:11px!important;
  line-height:1.5!important;font-weight:600!important
}
@media(max-width:390px){
 .qh-hero{padding:6px 0 9px!important;gap:5px!important}
 .qh-brand-emblem{width:min(40vw,138px)!important;max-width:138px!important}
}
"""
for name in ("www/index.html", "www/game.html"):
    path = Path(name)
    src = path.read_text(encoding="utf-8")
    if "QH DESIGN PASS 114" in src:
        print(f"Build 114 already present in {name}; skipping.")
        continue
    if "</head>" not in src:
        raise SystemExit(f"Missing </head> in {name}")
    src = src.replace("</head>", '<style id="qh-design-pass-114">' + chr(10) + css + chr(10) + '</style>' + chr(10) + '</head>', 1)
    path.write_text(src, encoding="utf-8")
print("QH Design Pass 114 applied.")
