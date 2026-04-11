[app]
title = MyAsalApp
package.name = myasalapp
package.domain = org.asal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,sdl2,sdl2_image,sdl2_ttf,sdl2_mixer,pysdl2
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
android.logcat_filters = *:S python:D
