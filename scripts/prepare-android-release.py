from pathlib import Path
import re

root = Path("android")
root_gradle = root / "build.gradle"
app_gradle = root / "app" / "build.gradle"

if not root_gradle.exists() or not app_gradle.exists():
    raise SystemExit("Expected Capacitor Groovy Gradle files were not found.")

root_text = root_gradle.read_text()
app_text = app_gradle.read_text()

plugin_line = "        classpath 'com.google.gms:google-services:4.4.2'"
if "com.google.gms:google-services" not in root_text:
    match = re.search(r"(dependencies\s*\{)", root_text)
    if not match:
        raise SystemExit("Could not locate root Gradle buildscript dependencies block.")
    pos = match.end()
    root_text = root_text[:pos] + "\n" + plugin_line + root_text[pos:]

apply_line = "apply plugin: 'com.google.gms.google-services'"
if "com.google.gms.google-services" not in app_text:
    app_text = app_text.rstrip() + "\n\n" + apply_line + "\n"

if "signingConfigs" not in app_text:
    build_types = re.search(r"(?m)^\s*buildTypes\s*\{", app_text)
    if not build_types:
        raise SystemExit("Could not locate app Gradle buildTypes block.")
    signing = """    signingConfigs {
        release {
            storeFile file(System.getenv('ANDROID_KEYSTORE_FILE'))
            storePassword System.getenv('ANDROID_KEYSTORE_PASSWORD')
            keyAlias System.getenv('ANDROID_KEY_ALIAS')
            keyPassword System.getenv('ANDROID_KEY_PASSWORD')
        }
    }

"""
    app_text = app_text[:build_types.start()] + signing + app_text[build_types.start():]

release_block = re.search(r"(?s)release\s*\{.*?\n\s*\}", app_text)
if not release_block:
    raise SystemExit("Could not locate release buildType block.")
block = release_block.group(0)
if "signingConfig" not in block:
    block_new = block[:-1] + "        signingConfig signingConfigs.release\n    }"
    app_text = app_text[:release_block.start()] + block_new + app_text[release_block.end():]

root_gradle.write_text(root_text)
app_gradle.write_text(app_text)
print("Configured Google Services plugin and release signing.")
