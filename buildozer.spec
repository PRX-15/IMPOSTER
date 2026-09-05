# This .spec config file tells Buildozer an app's requirements for being built.
#
# It largely follows the syntax of an .ini file.
# See the end of the file for more details and warnings about common mistakes.

[app]

title = IMPOSTER
package.name = imposter
package.domain = org.prx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,pillow
presplash.filename = %(source.dir)s/assets/icons/presplash.png
icon.filename = %(source.dir)s/assets/icons/icon.png
orientation = portrait
fullscreen = 0
android.presplash_color = #080303
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Python-for-android: use the fixed local checkout from GitHub Actions.
# p4a.url, p4a.fork, p4a.branch and p4a.commit are intentionally unset.
p4a.source_dir = ./python-for-android

#
# iOS specific
#

#ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
#ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
