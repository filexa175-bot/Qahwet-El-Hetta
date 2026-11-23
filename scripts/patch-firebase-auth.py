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
    S.authenticated = true;
    S.ch = Number.isInteger(p.avatarIndex) ? p.avatarIndex : S.ch;
    S.profileStep = 1;
    persist();
    if (typeof startScreen === "function") startScreen();
    // Clear the persistent sign-in progress/diagnostic banner on success.
    const diagnostic = document.getElementById("qh-auth-diagnostic");
    if (diagnostic) diagnostic.remove();
    if (typeof window.QHShowToast === "function") window.QHShowToast("تم ربط حسابك وحفظ ملفك بنجاح ☕");
  } catch (e) { console.error("QH profile bridge", e); }
};
window.QHShowToast = (message) => {
  try {
    let toast = document.getElementById("qh-auth-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "qh-auth-toast";
      toast.style.cssText = "position:fixed;z-index:200000;left:16px;right:16px;bottom:calc(22px + env(safe-area-inset-bottom));padding:15px 18px;border:1px solid #2ec9d5;border-radius:16px;background:rgba(15,37,43,.97);color:#a5f3f5;text-align:center;font:800 14px system-ui;box-shadow:0 12px 35px #0008;opacity:0;transform:translateY(12px);transition:opacity .22s ease,transform .22s ease;pointer-events:none";
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.style.opacity = "1";
    toast.style.transform = "translateY(0)";
    clearTimeout(window.__qhToastTimer);
    window.__qhToastTimer = setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(12px)";
      setTimeout(() => toast.remove(), 260);
    }, 2600);
  } catch (e) { console.warn("QH toast", e); }
};
window.QHApplySignedOut = () => {
  try {
    if (!window.S) return;
    S.playerId = "";
    S.authenticated = false;
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
