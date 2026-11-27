[app]
title = ABC Kids
package.name = abckids
package.domain = io.github.haseebhussain345

source.dir = .
source.include_exts = py,png,jpg,ttf
source.exclude_dirs = tests, tools, store, docs, .github, bin
version = 1.0.0
android.numeric_version = 1

requirements = python3,kivy==2.3.1,pyjnius

orientation = portrait
fullscreen = 0

# Icons (launcher, adaptive icon for Android 8+, and splash screen)
icon.filename = %(source.dir)s/assets/icon.png
icon.adaptive_foreground.filename = %(source.dir)s/assets/icon_fg.png
icon.adaptive_background.filename = %(source.dir)s/assets/icon_bg.png
presplash.filename = %(source.dir)s/assets/presplash.png
android.presplash_color = #FFF8E8

# Android
android.permissions =
android.api = 36
android.minapi = 24
android.ndk = 28c
android.ndk_api = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

# debug = APK for testing on your own phone
# release = AAB for Google Play
android.debug_artifact = apk
android.release_artifact = aab

# python-for-android develop branch (untested; the v2026.05.09 release failed on a pip wheel error)
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
