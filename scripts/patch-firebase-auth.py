from pathlib import Path
import json

root = Path(".")
pkg_path = root / "package.json"
pkg = json.loads(pkg_path.read_text())
pkg.setdefault("dependencies", {})
pkg["dependencies"]["@capacitor-firebase/authentication"] = "7.2.0"
pkg["dependencies"]["firebase"] = "^11.10.0"
pkg_path.write_text(json.dumps(pkg, ensure_ascii=False, indent=2) + "\n")

cfg_path = root / "capacitor.config.json"
cfg = json.loads(cfg_path.read_text())
cfg.setdefault("plugins", {})["FirebaseAuthentication"] = {
    "providers": ["google.com"],
    "skipNativeAuth": True
}
cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")

bridge = """<script>
window.QHApplyProfile = (p) => {
  try {
    S.playerName = p.displayName || S.playerName;
    S.playerId = p.playerId || S.playerId;
    S.ch = Number.isInteger(p.avatarIndex) ? p.avatarIndex : S.ch;
    S.profileStep = 1;
    persist();
    if (typeof startScreen === "function") startScreen();
  } catch (e) { console.error("QH profile bridge", e); }
};
window.QHApplySignedOut = () => {
  try {
    if (!window.S) return;
    S.playerId = "";
    persist();
    if (typeof startScreen === "function") startScreen();
  } catch (e) { console.error("QH sign-out bridge", e); }
};
</script>
<script src="firebase-auth.js"></script>"""

for rel in ("www/index.html", "www/game.html"):
    path = root / rel
    html = path.read_text()
    # Remove an earlier copy of our bridge/script before adding one clean copy.
    import re
    html = re.sub(
        r'<script>\s*window\.QHApplyProfile[\s\S]*?</script>\s*<script src="firebase-auth\.js"></script>',
        "",
        html
    )
    if "</body>" in html:
        html = html.replace("</body>", bridge + "\\n</body>", 1)
    else:
        # These game pages are distributed as body fragments without a closing body tag.
        html = html.rstrip() + "\\n" + bridge + "\\n"
    path.write_text(html)

print("Firebase auth bridge and bundle appended to both game pages.")
