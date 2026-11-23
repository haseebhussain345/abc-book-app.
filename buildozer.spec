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

# Android
android.permissions =
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True
android.release_artifact = apk

# Pinned to a stable release (fixes the Python 3.14 build error)
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
