# M35 Final Project

### This repository is my submission for the final project on the Master 35 course, which for me is employer based/set due to my apprenticeship.

## What is the project:

- The final project is based around the Android device ecosystem and more specifically device enrollment to streamline the device setup process + APK/application install on Android devices.

- When run, the main.py file will both create a QR code PNG image file and automatically open a QR code in a web browser - this can be used to enroll an Android device (I believe on Android 6 and above?...), by tapping the setup screen on boot 6 times. 
- Also included in my repo is the Android devloped ADB (Android Debug Bridge) command line tool, used for performing a multitude of actions on Android devices such as traversing through a phones directories, executing commands (e.g. installing apps) and more.

## How to use:

- Task 1 - :
-- As breifly mentioned above, simply run the main.py file using an appropriate Python interpreter (3.10+) and a scannable QR code PNG is created in the project directory (root) and one is also opened in a web browser.

- Task 2 - App/APK install:
-- For part two of the task, I discovered that this could be achieved using the Android developed ADB (Android Debug Bridge). I successfully installed an APK through the execution of the following commands in command line: MENTION CONNECT VIA USB
--- adb
--- adb devices
--- adb install *path to apk file*

## Nerdy Stuff:

- Project was built in Python (version 3.10) due to overall accessibility and existing documentation from Google's API resources - I am also incredibily familiar with Python.
- I also prefer to develop in virtual environments for Python, choosing to use pipenv (built in venv and package manager) and so all required packages are stored in Pipfile and can be installed using pipenv install in same directory.