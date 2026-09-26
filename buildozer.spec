[app]
# (str) Title of your application
title = Fitzone

# (str) Package name
package.name = fitzone

# (str) Package domain (needed for android/ios packaging)
package.domain = org.umutfits

# (str) Source code where main.py live
source.dir = .

# (list) Source files to include (let buildozer include the common types)
source.include_exts = py,png,jpg,jpeg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
requirements = python3,kivy,plyer

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash of the application
 #presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
 #icon.filename = %(source.dir)s/data/icon.png

# (str) Supported Android ABI
android.archs = arm64-v8a

# (bool) Accept Android SDK license automatically in CI
android.accept_sdk_license = True

# (list) List of service to declare
 #services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

[buildozer]
# (str) Log level (0 = error only, 1 = error + warning, 2 = info, 3 = debug)
 log_level = 2

# (str) Warn the user before cleaning the build directory if it would be necessary
 warn_on_root = 1
