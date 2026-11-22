from pathlib import Path
p=Path("android/variables.gradle")
s=p.read_text()
if "rgcfaIncludeGoogle" not in s:
    pos=s.find("ext {")
    if pos<0: raise SystemExit("variables.gradle ext block not found")
    end=s.find("\\n}",pos)
    if end<0: raise SystemExit("variables.gradle ext block end not found")
    s=s[:end]+"\\n    rgcfaIncludeGoogle = true\\n    androidxCredentialsVersion = '1.3.0'"+s[end:]
p.write_text(s)
print("Google Credential Manager native dependencies configured")
