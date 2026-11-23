from pathlib import Path

targets = [Path("www/index.html"), Path("www/game.html")]
css = """
<style id="qh-dismissible-system-ui">
.top .bub{position:relative;padding-right:34px}
.qh-bubble-close{position:absolute;right:5px;top:4px;width:24px;height:24px;border:0;border-radius:50%;background:#6b3c2c;color:#fff;font-size:18px;line-height:20px;font-weight:900;cursor:pointer}
#qh-system-notice{position:fixed;inset:0;z-index:200000;display:none;align-items:center;justify-content:center;padding:22px;background:#0009}
#qh-system-notice.show{display:flex}
#qh-system-notice .qh-notice-card{position:relative;width:min(420px,100%);padding:24px 20px 20px;border:2px solid #b88a4d;border-radius:18px;background:linear-gradient(145deg,#29473e,#142a25);color:#fff0d1;box-shadow:0 16px 50px #0009;text-align:center;font:600 16px/1.7 system-ui}
#qh-system-notice .qh-notice-close{position:absolute;right:9px;top:8px;width:32px;height:32px;border:1px solid #d2ad72;border-radius:50%;background:#52382c;color:#fff;font-size:23px;line-height:25px;cursor:pointer}
#qh-system-notice .qh-notice-text{white-space:pre-wrap;overflow-wrap:anywhere;padding:10px 8px}
</style>
"""
js = """
<div id="qh-system-notice" role="alertdialog" aria-modal="true" aria-live="assertive">
 <div class="qh-notice-card"><button class="qh-notice-close" type="button" aria-label="إغلاق" onclick="qhCloseSystemNotice()">×</button><div class="qh-notice-text" id="qh-system-notice-text"></div><button class="pri" type="button" onclick="qhCloseSystemNotice()">حاضر</button></div>
</div>
<script id="qh-dismissible-system-messages">
function qhCloseSystemNotice(){const n=document.getElementById('qh-system-notice');if(n)n.classList.remove('show')}
function qhShowSystemNotice(message){const n=document.getElementById('qh-system-notice'),t=document.getElementById('qh-system-notice-text');if(!n||!t)return; t.textContent=String(message??'');n.classList.add('show')}
window.alert=function(message){qhShowSystemNotice(message)};
document.addEventListener('keydown',function(e){if(e.key==='Escape')qhCloseSystemNotice()});
document.addEventListener('click',function(e){if(e.target&&e.target.id==='qh-system-notice')qhCloseSystemNotice()});
function qhDismissOpponentMessage(){if(!G)return;clearTimeout(G.msgTimer);G.msgVisible=false;G.msg='';render()}
</script>
"""
for path in targets:
    src = path.read_text(encoding="utf-8")
    if "qh-dismissible-system-messages" in src:
        continue
    # Add a close control to every in-game opponent speech bubble.
    src, count = __import__("re").subn(
        r"\$\{esc\(G\.msg\)\}(?=</div>)",
        "${esc(G.msg)}<button class=\\"qh-bubble-close\\" type=\\"button\\" aria-label=\\"إغلاق\\" onclick=\\"qhDismissOpponentMessage()\\">×</button>",
        src
    )
    if count < 1:
        raise SystemExit(f"No opponent message bubble found in {path}")
    body_close = src.rfind("</body>")
    if body_close < 0:
        raise SystemExit(f"No body close tag in {path}")
    src = src[:body_close] + css + js + "\n" + src[body_close:]
    path.write_text(src, encoding="utf-8")
print("Added dismissible system alerts and opponent message bubbles to both HTML entry points.")
