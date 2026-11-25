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
  if (!document.getElementById("qh-wallet-layout-style")) { const style=document.createElement("style"); style.id="qh-wallet-layout-style"; style.textContent="#qh-wallet-bubble-root button{font-family:Cairo,system-ui;line-height:1.1}#qh-wallet-bubble-root button:focus-visible{outline:2px solid #d6b36d;outline-offset:2px}#qh-wallet-bubble-panel{backdrop-filter:blur(12px)}"; document.head.appendChild(style); }
  let root = document.getElementById("qh-wallet-bubble-root");
  if (!root) {
    root = document.createElement("div");
    root.id = "qh-wallet-bubble-root";
    root.style.cssText = "position:fixed;z-index:1200;top:calc(4px + env(safe-area-inset-top));right:max(8px,calc((100vw - 560px)/2 + 8px));direction:rtl;font-family:Cairo,system-ui;max-width:calc(100vw - 16px);pointer-events:none";
    root.innerHTML = '<button id="qh-wallet-bubble" type="button" aria-label="رصيد الماركات" style="pointer-events:auto;display:flex;align-items:center;gap:5px;padding:3px 7px;border:1px solid #a98a55;border-radius:14px;background:linear-gradient(145deg,#26372b,#142119);color:#f4e4bd;box-shadow:0 2px 7px #0006;font-weight:900;font-size:9px;min-height:25px;white-space:nowrap"><span style="display:flex;align-items:center;gap:2px;padding-left:1px"><i style="display:grid;place-items:center;width:9px;height:9px;margin-left:0;border:1px solid #ffffffaa;border-radius:50%;background:radial-gradient(circle at 32% 25%,#8be18b,#17843d 65%,#075326);font-size:0;font-style:normal">●</i><i style="display:grid;place-items:center;width:9px;height:9px;margin-left:0;border:1px solid #ffffffaa;border-radius:50%;background:radial-gradient(circle at 32% 25%,#ff9a9a,#c82e35 65%,#78141c);font-size:0;font-style:normal">●</i><i style="display:grid;place-items:center;width:9px;height:9px;margin-left:0;border:1px solid #ffffffaa;border-radius:50%;background:radial-gradient(circle at 32% 25%,#8ecaff,#176ac1 65%,#0b3978);font-size:0;font-style:normal">●</i><i style="display:grid;place-items:center;width:9px;height:9px;border:1px solid #ffffffaa;border-radius:50%;background:radial-gradient(circle at 32% 25%,#8be18b,#17843d 65%,#075326);font-size:0;font-style:normal">●</i></span><b id="qh-wallet-bubble-balance">0</b><small>ماركة</small><span id="qh-wallet-bubble-arrow">+</span></button><div id="qh-wallet-bubble-panel" hidden style="pointer-events:auto;margin-top:5px;padding:10px;border:1px solid #c9b27d;border-radius:13px;background:rgba(20,29,23,.98);color:#ffebc7;box-shadow:0 8px 24px #0009;min-width:165px"><div style="font-weight:900;margin-bottom:6px;font-size:12px">رصيدك في قهوة الحتة</div><div style="font-size:19px;font-weight:900;margin-bottom:7px"><span id="qh-wallet-bubble-balance-large">0</span> ماركة</div><div style="display:flex;gap:4px;margin:0 0 8px"><span style="width:9px;height:9px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#8be18b,#17843d 65%,#075326)"></span><span style="width:9px;height:9px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#ff9a9a,#c82e35 65%,#78141c)"></span><span style="width:9px;height:9px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#8ecaff,#176ac1 65%,#0b3978)"></span><span style="width:9px;height:9px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#8be18b,#17843d 65%,#075326)"></span></div><button id="qh-wallet-bubble-gift" type="button" style="width:100%;border:1px solid #d7c18b;border-radius:9px;padding:7px;background:#435b3f;color:#fff0cf;font-weight:800;font-size:11px">استلام الهدية اليومية · 500</button></div>'
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
