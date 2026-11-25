from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "www" / "index.html", ROOT / "www" / "game.html"]

for path in FILES:
    if not path.exists():
        continue
    source = path.read_text(encoding="utf-8")
    html_end = source.lower().rfind("</html>")
    body_end = source.lower().rfind("</body>")
    if html_end < 0 or body_end < 0 or html_end < body_end:
        raise SystemExit(f"Unexpected HTML structure in {path}")

    trailing = source[html_end + len("</html>"):]
    if not trailing.strip():
        print(f"{path}: already clean")
        continue

    if not re.fullmatch(r"(?:\s*<style\b[^>]*>.*?</style>\s*)+", trailing, flags=re.I | re.S):
        raise SystemExit(f"Unexpected non-style content after </html> in {path}; refusing destructive edit")

    clean = source[:body_end] + trailing + "\n" + source[body_end:html_end] + "</html>\n"
    path.write_text(clean, encoding="utf-8")
    check = path.read_text(encoding="utf-8")
    if check.lower().rfind("</style>") > check.lower().rfind("</body>"):
        raise SystemExit(f"Validation failed: style remains outside body in {path}")
    if check.lower().rfind("</body>") > check.lower().rfind("</html>"):
        raise SystemExit(f"Validation failed: body/html order in {path}")
    print(f"{path}: moved {len(trailing)} trailing characters inside body; validated")
