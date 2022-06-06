ECHO OFF
:: Sets the name of the window:
TITLE APK Install
ECHO.
ECHO Starting ADB - Android Debug Bridge
ECHO.
:: Checks if ADB can be located/is installed:
adb
ECHO.
:: Lists connected devices for ADB interaction:
adb devices
:: Installs specified APK file through launch of ADB:
adb install WhatsApp.apk
ECHO.
ECHO WhatsApp has been installed on the connected Android device.
ECHO.
:: Allows for user to read messages before manual terminal close:
PAUSE