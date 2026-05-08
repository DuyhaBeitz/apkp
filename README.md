# apkp
apkp is a command line tool android build system.
right now only Kotlin supported.
inspired by https://github.com/ajinasokan/apkc and how bloated Android Studio is
# How to use it?
1) Install JDk and Android SDK and setup your environment variables: ANDROID_HOME and JAVA_HOME
2) run ```./apkp create``` to create your project. It will have the following structure:
```
├── myapp
│   ├── AndroidManifest.xml
│   ├── res
│   │   ├── layout
│   │   │   └── main.xml
│   │   └── values
│   │       └── styles.xml
│   └── src
│       └── com
│           └── myapp
│               └── MainActivity.kt
```
5) Write your program
6) run ```./apkd build``` to build your APK. You will be prompted to create your signing key
7) After that you can test ```adb install -r apkp_build/my_app_signed.apk``` or deploy your app
