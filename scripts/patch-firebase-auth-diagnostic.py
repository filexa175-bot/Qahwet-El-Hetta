from pathlib import Path

path = Path("firebase-auth-entry.js")
if not path.exists():
    raise SystemExit("firebase-auth-entry.js was not copied into app-source")

src = path.read_text(encoding="utf-8")

old_style = 'boxShadow:"0 4px 24px #0008",direction:"rtl",textAlign:"right"'
new_style = 'boxShadow:"0 4px 24px #0008",direction:"rtl",textAlign:"right",whiteSpace:"pre-wrap",overflowWrap:"anywhere",maxHeight:"45vh",overflowY:"auto"'
if old_style in src:
    src = src.replace(old_style, new_style, 1)

old_catch = 'const message="تعذر "+stage+": "+errorText(e);'
new_catch = '''const active=auth.currentUser;
    const uidMatch=!!active && !!e && !!(e.user?.uid) && active.uid===e.user.uid;
    const message="QH-DIAG-20261123-A | تعذر "+stage+
      " | project="+(app.options.projectId||"unknown")+
      " | js-session="+(active?"present":"missing")+
      " | auth-user-match="+(uidMatch?"yes":"unknown")+
      " | error="+errorText(e);'''
if old_catch not in src:
    raise SystemExit("Expected signIn error handler was not found; refusing unsafe patch")
src = src.replace(old_catch, new_catch, 1)

marker = 'console.info("[QH AUTH] Firebase auth bundle initialized; native="+Capacitor.isNativePlatform());'
if marker not in src:
    raise SystemExit("Firebase initialization marker was not found")
src = src.replace(marker, marker + '\nconsole.info("[QH AUTH] diagnostic build QH-DIAG-20261123-A");', 1)

path.write_text(src, encoding="utf-8")
print("Patched Firebase auth diagnostics in the exact source copied into the Android bundle.")
