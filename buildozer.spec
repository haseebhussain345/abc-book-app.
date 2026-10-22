[app]
title = ABC Book
package.name = abcbook
package.domain = org.myname

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,ogg,mp3
version = 1.0.0

requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

# Optional: uncomment after adding these image files to your project
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/presplash.png

# Android
android.permissions =
android.api = 35
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

# Build an Android App Bundle for Google Play
android.release_artifact = aab

[buildozer]
log_level = 2
warn_on_root = 1
