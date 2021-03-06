[app]

title = Lake of Fire
package.name = lakeoffire
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = Static/*,
version = 0.1
requirements = python3,kivy,pytube,android,certifi,ffpyplayer, ffpyplayer_codecs, openssl

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE,MANAGE_EXTERNAL_STORAGE
android.arch = armeabi-v7a

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2

