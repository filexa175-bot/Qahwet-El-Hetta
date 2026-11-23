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
window.QHRenderWalletBubble = () => {
  if (!window.__QHWalletBubbleEnabled && !window.S?.authenticated && !window.QHAuth?.currentUser) return;
  let root = document.getElementById("qh-wallet-bubble-root");
  if (!root) {
    root = document.createElement("div");
    root.id = "qh-wallet-bubble-root";
    root.style.cssText = "position:fixed;z-index:2147483000;top:calc(10px + env(safe-area-inset-top));left:10px;direction:rtl;font-family:system-ui;max-width:calc(100vw - 20px);pointer-events:none";
    root.innerHTML = '<button id="qh-wallet-bubble" type="button" aria-label="رصيدك" style="pointer-events:auto;display:flex;align-items:center;gap:8px;padding:8px 12px;border:1px solid #d8c18b;border-radius:24px;background:linear-gradient(145deg,#202a23,#101713);color:#fff0ca;box-shadow:0 5px 18px #0009;font-weight:900;font-size:13px"><span style="display:flex;align-items:center;padding-left:2px"><i style="display:grid;place-items:center;width:19px;height:19px;margin-left:-5px;border:1px solid #ffffffaa;border-radius:50%;background:radial-gradient(circle at 32% 25%,#8be18b,#17843d 65%,#075326);box-shadow:0 1px 3px #0008;color:#eaffea;font-size:8px;font-style:normal">●</i><i style="display:grid;place-items:center;width:19px;height:19px;margin-left:-5px;border:1px solid #ffffffaa;border-radius:50%;background:radial-gradient(circle at 32% 25%,#ff9a9a,#c82e35 65%,#78141c);box-shadow:0 1px 3px #0008;color:#fff0f0;font-size:8px;font-style:normal">●</i><i style="display:grid;place-items:center;width:19px;height:19px;margin-left:-5px;border:1px solid #ffffffaa;border-radius:50%;background:radial-gradient(circle at 32% 25%,#8ecaff,#176ac1 65%,#0b3978);box-shadow:0 1px 3px #0008;color:#eff8ff;font-size:8px;font-style:normal">●</i><i style="display:grid;place-items:center;width:19px;height:19px;border:1px solid #ffffffaa;border-radius:50%;background:radial-gradient(circle at 32% 25%,#8be18b,#17843d 65%,#075326);box-shadow:0 1px 3px #0008;color:#eaffea;font-size:8px;font-style:normal">●</i></span><span style="text-align:right"><small style="display:block;font-size:9px;opacity:.82">ماركاتك</small><b id="qh-wallet-bubble-balance">0</b> <small>ماركة</small></span><span id="qh-wallet-bubble-arrow">⌄</span></button><div id="qh-wallet-bubble-panel" hidden style="pointer-events:auto;margin-top:7px;padding:12px;border:1px solid #c9b27d;border-radius:15px;background:rgba(20,29,23,.98);color:#ffebc7;box-shadow:0 8px 24px #0009;min-width:190px"><div style="font-weight:900;margin-bottom:8px">ماركاتك في قهوة الحتة</div><div style="font-size:22px;font-weight:900;margin-bottom:10px"><span id="qh-wallet-bubble-balance-large">0</span> ماركة</div><div style="display:flex;gap:5px;margin:0 0 10px"><span style="width:16px;height:16px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#8be18b,#17843d 65%,#075326)"></span><span style="width:16px;height:16px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#ff9a9a,#c82e35 65%,#78141c)"></span><span style="width:16px;height:16px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#8ecaff,#176ac1 65%,#0b3978)"></span><span style="width:16px;height:16px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#8be18b,#17843d 65%,#075326)"></span></div><button id="qh-wallet-bubble-gift" type="button" style="width:100%;border:1px solid #d7c18b;border-radius:10px;padding:9px;background:#435b3f;color:#fff0cf;font-weight:800">استلام الهدية اليومية · 500</button></div>';
    document.body.appendChild(root);
    document.getElementById("qh-wallet-bubble").addEventListener("click", () => {
      const panel = document.getElementById("qh-wallet-bubble-panel");
      const arrow = document.getElementById("qh-wallet-bubble-arrow");
      panel.hidden = !panel.hidden;
      arrow.textContent = panel.hidden ? "⌄" : "⌃";
    });
    document.getElementById("qh-wallet-bubble-gift").addEventListener("click", () => window.QHAuth?.claimDailyGift());
  } else if (!root.isConnected) {
    document.body.appendChild(root);
  }
};
window.__QHWalletBubbleEnabled = false;
const qhKeepWalletBubble = new MutationObserver(() => {
  if (window.__QHWalletBubbleEnabled) {
    const root = document.getElementById("qh-wallet-bubble-root");
    if (root && !root.isConnected) document.body.appendChild(root);
    else if (!root) window.QHRenderWalletBubble?.();
  }
});
qhKeepWalletBubble.observe(document.documentElement, {childList:true,subtree:true});
window.QHApplyProfile = (p) => {
  try {
    S.playerName = p.displayName || S.playerName;
    S.playerId = p.playerId || S.playerId;
    S.authenticated = true;
    window.__QHWalletBubbleEnabled = true;
    S.ch = Number.isInteger(p.avatarIndex) ? p.avatarIndex : S.ch;
    S.profileStep = 1;
    persist();
    if (typeof startScreen === "function") startScreen();
    window.QHRenderWalletBubble?.();
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
    window.__QHWalletBubbleEnabled = false;
    document.getElementById("qh-wallet-bubble-root")?.remove();
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
