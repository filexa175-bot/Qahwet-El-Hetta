from pathlib import Path
import json

root=Path(".")
pkg=json.loads((root/"package.json").read_text())
pkg.setdefault("dependencies",{})
pkg["dependencies"]["@capacitor-firebase/authentication"]="7.2.0"
pkg["dependencies"]["firebase"]="^11.10.0"
(root/"package.json").write_text(json.dumps(pkg,ensure_ascii=False,indent=2)+"\n")

cfg=root/"capacitor.config.json"
data=json.loads(cfg.read_text())
data.setdefault("plugins",{})["FirebaseAuthentication"]={"providers":["google.com"],"skipNativeAuth":True}
cfg.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")

for name in ["www/index.html","www/game.html"]:
 p=root/name
 s=p.read_text()
 tag='<script>window.QHApplyProfile=(p)=>{try{S.playerName=p.displayName||S.playerName;S.playerId=p.playerId||S.playerId;S.ch=Number.isInteger(p.avatarIndex)?p.avatarIndex:S.ch;S.profileStep=1;persist();if(typeof startScreen==="function")startScreen()}catch(e){console.error(e)}};window.QHApplySignedOut=()=>{S.playerId="";persist();startScreen()};</script><script src="firebase-auth.js"></script>'
 if tag not in s:
  s=s.replace("</body>",tag+"\\n</body>")
 p.write_text(s)
print("Firebase JS SDK owns the authenticated session; native Google sign-in skips native auth.")
