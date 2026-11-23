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
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

# APK for testing on your own phone (switch to aab + api 35 for Google Play later)
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
