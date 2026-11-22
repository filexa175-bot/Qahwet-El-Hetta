from pathlib import Path
import re

files = [Path("www/index.html"), Path("www/game.html")]
old_state = """const S={game:0,ch:0,df:1,playerName:'',domScore:0,cpuDomScore:0,t31Me:0,t31Cpu:0,me:0,cpu:0,mePaid:0,cpuPaid:0,stats:false,set:false};
if(SAVED.settings)Object.assign(S,{game:SAVED.settings.game??0,ch:SAVED.settings.ch??0,df:SAVED.settings.df??1,playerName:SAVED.settings.playerName??''});
if(S.game>2||S.game<0)S.game=0;if(S.ch>2||S.ch<0)S.ch=0;
function persist(){try{localStorage.setItem(STORE_KEY,JSON.stringify({settings:{game:S.game,ch:S.ch,df:S.df,playerName:S.playerName}}))}catch(e){}}
const myName=()=>S.playerName.trim()||'اللاعب';"""
new_state = """const S={game:0,ch:0,df:1,playerName:'',playerId:'',domScore:0,cpuDomScore:0,t31Me:0,t31Cpu:0,me:0,cpu:0,mePaid:0,cpuPaid:0,stats:false,set:false};
if(SAVED.settings)Object.assign(S,{game:SAVED.settings.game??0,ch:SAVED.settings.ch??0,df:SAVED.settings.df??1,playerName:SAVED.settings.playerName??''});
if(SAVED.profile)Object.assign(S,{playerId:SAVED.profile.playerId??'',playerName:SAVED.profile.playerName??S.playerName,ch:SAVED.profile.ch??S.ch});
if(S.game>2||S.game<0)S.game=0;if(S.ch>2||S.ch<0)S.ch=0;
function makeLocalPlayerId(){const bytes=new Uint8Array(8);if(window.crypto&&crypto.getRandomValues)crypto.getRandomValues(bytes);else for(let i=0;i<bytes.length;i++)bytes[i]=Math.random()*256|0;return 'QH-'+Array.from(bytes,b=>b.toString(16).padStart(2,'0')).join('').toUpperCase()}
if(!S.playerId)S.playerId=makeLocalPlayerId();
function persist(){try{localStorage.setItem(STORE_KEY,JSON.stringify({settings:{game:S.game,ch:S.ch,df:S.df,playerName:S.playerName},profile:{playerId:S.playerId,playerName:S.playerName,ch:S.ch}}))}catch(e){}}
const myName=()=>S.playerName.trim()||'اللاعب';
function copyPlayerId(){const value=S.playerId;if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(value).then(()=>showToast('تم نسخ Player ID')).catch(()=>showToast('Player ID: '+value));else showToast('Player ID: '+value)}
function showToast(message){const old=document.getElementById('qh-toast');if(old)old.remove();const el=document.createElement('div');el.id='qh-toast';el.textContent=message;el.style.cssText='position:fixed;z-index:9999;bottom:22px;left:50%;transform:translateX(-50%);background:#172c29;color:#fff1c9;border:1px solid #b88a4d;border-radius:12px;padding:10px 15px;font-weight:800;max-width:90%;text-align:center';document.body.appendChild(el);setTimeout(()=>el.remove(),2600)}
function choosePlayMode(mode){if(mode==='ai'){go();return}showToast(mode==='friend'?'اللعب مع صديق قيد التجهيز':'المطابقة العشوائية قيد التجهيز')}"""
new_home = "";
for path in files:
    src = path.read_text(encoding="utf-8")
    if "function makeLocalPlayerId()" not in src:
        if src.count(old_state) != 1:
            raise SystemExit(f"Unexpected player state in {path}: {src.count(old_state)}")
        src = src.replace(old_state, new_state, 1)
    if "PLAYER ID ·" not in src:
        start = src.index("function startScreen(){")
        end = src.index("\nfunction go(){", start)
        replacement = Path("scripts/player-home-screen.html.txt").read_text(encoding="utf-8")
        src = src[:start] + replacement.rstrip() + src[end:]
    path.write_text(src, encoding="utf-8")
print("Player profile patch applied to both HTML entry files.")
