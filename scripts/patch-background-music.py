from pathlib import Path

root = Path(".")
targets = list(root.glob("www/*.html"))
if not targets:
    raise SystemExit("No www/*.html files found in extracted Android source.")

needle = "document.addEventListener('click',()=>{initAudio();startCafeMusic()});"
lifecycle = """// Stop cafe music whenever the app leaves the foreground.
  // Resume only if it was playing before the app was backgrounded.
  let cafeMusicWasPlayingBeforeBackground = false;
  function pauseCafeMusicForBackground(){
    const a = cafeAudio();
    if(!a) return;
    cafeMusicWasPlayingBeforeBackground = !a.paused && cafeMusicOn;
    if(!a.paused) a.pause();
  }
  function resumeCafeMusicOnForeground(){
    if(document.visibilityState !== 'visible') return;
    if(cafeMusicWasPlayingBeforeBackground && cafeMusicOn) startCafeMusic();
    cafeMusicWasPlayingBeforeBackground = false;
  }
  document.addEventListener('visibilitychange',()=>{
    if(document.visibilityState === 'hidden') pauseCafeMusicForBackground();
    else resumeCafeMusicOnForeground();
  });
  window.addEventListener('pagehide',pauseCafeMusicForBackground);
  window.addEventListener('pageshow',resumeCafeMusicOnForeground);
  document.addEventListener('freeze',pauseCafeMusicForBackground);
  document.addEventListener('resume',resumeCafeMusicOnForeground);

  """ + needle

patched = 0
for path in targets:
    source = path.read_text(encoding="utf-8")
    if "pauseCafeMusicForBackground" in source:
        continue
    if source.count(needle) != 1:
        raise SystemExit(f"Expected exactly one music-start hook in {path}, found {source.count(needle)}")
    path.write_text(source.replace(needle, lifecycle, 1), encoding="utf-8")
    patched += 1

if patched == 0:
    raise SystemExit("No HTML files needed patching.")
print(f"Patched background music lifecycle in {patched} HTML file(s).")
