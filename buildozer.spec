[app]

title = IMPOSTER
package.name = imposter
package.domain = org.prx15
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Android build configuration
android.api = 35
android.minapi = 24
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.copy_libs = 1
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
