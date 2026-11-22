from pathlib import Path

p = Path("android/variables.gradle")
s = p.read_text()

if "rgcfaIncludeGoogle" not in s:
    start = s.find("ext {")
    if start < 0:
        raise SystemExit("variables.gradle ext block not found")

    end = s.find("\n}", start)
    if end < 0:
        raise SystemExit("variables.gradle ext block end not found")

    additions = "\n    rgcfaIncludeGoogle = true\n    androidxCredentialsVersion = '1.3.0'"
    s = s[:end] + additions + s[end:]

p.write_text(s)
print("Google Credential Manager native dependencies configured")
