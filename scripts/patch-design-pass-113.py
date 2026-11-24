from pathlib import Path

css = r"""
/* QH DESIGN PASS 113 — emblem-first, compact hero; no logo frame */
.qh-hero{
  display:flex!important;flex-direction:column!important;
  align-items:center!important;justify-content:center!important;
  gap:7px!important;
  width:100%!important;height:auto!important;min-height:0!important;max-height:none!important;
  box-sizing:border-box!important;
  margin:0 0 17px!important;padding:15px 14px 13px!important;
  border:1px solid rgba(213,168,94,.62)!important;border-radius:20px!important;
  overflow:hidden!important;
  background:
    radial-gradient(ellipse at 50% 0%,rgba(255,244,220,.09),transparent 58%),
    linear-gradient(145deg,#123f49 0%,#092f38 100%)!important;
  box-shadow:0 8px 18px rgba(9,47,56,.13)!important;
}
.qh-hero:before{
  inset:7px!important;border:1px solid rgba(232,201,142,.16)!important;
  border-radius:14px!important;pointer-events:none!important;
}
.qh-hero:after{display:none!important}
.qh-brand-emblem{
  display:block!important;position:relative!important;z-index:1!important;
  width:min(42vw,156px)!important;height:auto!important;
  max-width:156px!important;max-height:156px!important;
  aspect-ratio:1/1!important;object-fit:contain!important;
  margin:0 auto!important;padding:0!important;border:0!important;
  border-radius:0!important;background:transparent!important;box-shadow:none!important;
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
  color:#e8c98e!important;font-size:11px!important;line-height:1.4!important;
  font-weight:700!important;letter-spacing:.1px!important
}
.qh-hero-copy p{
  margin:0!important;color:#f7eddc!important;font-size:11px!important;
  line-height:1.5!important;font-weight:600!important
}
@media(max-width:390px){
 .qh-hero{padding:12px 12px 11px!important;gap:5px!important}
 .qh-brand-emblem{width:min(40vw,138px)!important;max-width:138px!important}
}
"""
for name in ("www/index.html", "www/game.html"):
    path = Path(name)
    src = path.read_text(encoding="utf-8")
    if "QH DESIGN PASS 113" in src:
        print(f"Build 113 already present in {name}; skipping.")
        continue
    if "</head>" not in src:
        raise SystemExit(f"Missing </head> in {name}")
    src = src.replace("</head>", '<style id="qh-design-pass-113">' + chr(10) + css + chr(10) + '</style>' + chr(10) + '</head>', 1)
    path.write_text(src, encoding="utf-8")
print("QH Design Pass 113 applied.")
