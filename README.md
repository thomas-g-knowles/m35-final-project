# M35 Final Project

### This repository is my submission for the final project on the Master 35 course, which for me is employer based/set due to my apprenticeship.

## What is the Project:

- The final project is based around the Android device ecosystem and more specifically device enrollment to streamline the device setup process + APK/application install on Android devices.
- In layman's terms, the device setup wizard needs to be skipped by scanning a QR code to take the user to the home screen of the device and once the device is setup an application needs to be sideloaded onto the phone.
- This repository and README contain all the required files (excluding .env (auth) and packages, use pipenv install) and instructions to acheive the above.

## How to Use:

- Task 1 - QR Code Enrollment:
  - Simply run the main.py file using an appropriate Python interpreter (3.10+) and a scannable QR code PNG is created in the project directory (root) and one is also automatically opened in a web browser (the PNG file is more of a failsafe incase files (drivers etc.) for web browser act up). This QR code can then be used to enroll an Android device (I believe on Android 6 and above?...), by tapping the setup screen on boot 6 times.

- Task 2 - App/APK install:
  - For part two of the task, I discovered that this could be achieved using the Android developed ADB (Android Debug Bridge). Therefore, also included in my repo is the Android devloped ADB (Android Debug Bridge) command line tool, used for performing a multitude of actions on Android devices such as traversing through a phones directories, executing commands (e.g. installing apps) and more.
  - I successfully installed an APK through the execution of the following commands in command line (cmd opened in same folder as adb.exe so it can be found implicitly) and by connecting the Android device to the PC via USB (note regarding the USB, some cables will NOT work, it may have to be brand specific? I had this issue, however swapping to a different cable worked):
    - adb ===>>> not strictly neccessary, however checks for install/executable of ADB
    - adb devices ===>>> not strictly neccessary, however can assist in establishing connection to phone.
    - adb install WhatsApp.apk ===>>> adb install ***path* to apk file**
  - Note that I have wrote a batch script which does this hassle free (included in ADB), just run it and the APK (I chose WhatsApp) will be installed.

## Authentication:

For the authentication, I have chosen to use a .env file to store variables with sensitive information in them (included in the .gitignore), therefore to adapt the code in main.py for yourself simply just modify the supplied "template.env" file filling in the blanks and rename the file to just ".env" when finished. The first three variable names refer to your/a Google Cloud Project's details, one can be setup on the platform using the web GUI/console.

Note: replace <> and text inside it with relevant fields, e.g. "POLICY_PATH = enterprises/<enterprise_name>/policies/" would become "POLICY_PATH = enterprises/my_enterprise/policies/"

- https://cloud.google.com/

## Nerdy Stuff (extra info):

- Project was built in Python (version 3.10) due to overall accessibility and existing documentation from Google's API resources - I am also incredibily familiar with Python and its syntax.
- Furthermore, there were mutliple techniques I could have used to achieve the device enrollment procedure, however I went down the root of utilising Google's Android Management API.
- I also prefer to develop in virtual environments for Python, choosing to use pipenv (built in venv and package manager) and so all required packages are stored in Pipfile and can be installed using "**pipenv install**" command in terminal, in same directory.
- In regards to app installation onto a phone, I found a way of specifying a list of apps to be downloaded automatically upon completion of device setup and so I decided to implement this as well as the APK sideloader.