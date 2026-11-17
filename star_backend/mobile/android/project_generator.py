"""
Star Android Gradle Project Generator
Authoritative Reference: STAR_ANDROID.md (Section 7)
"""

import os
import shutil
from typing import Dict, Any, Optional
from star_backend.mobile.packaging import MobileBundle
from star_backend.mobile.android.jni_bridge import AndroidJNIBridge
from star_backend.mobile.android.activity import StarActivity
from star_backend.mobile.android.surface_renderer import AndroidSurfaceRenderer
from star_backend.mobile.android.sdk import AndroidSDK


class AndroidProjectGenerator:
    """
    Generates standard Android Gradle project structures incorporating
    JNI native bridges, SurfaceView render pipelines, and embedded .starmobile bundles.
    """
    def __init__(self):
        self.sdk = AndroidSDK.find_sdk()

    def generate_project(
        self,
        bundle: MobileBundle,
        bundle_path: str,
        output_dir: str
    ) -> str:
        os.makedirs(output_dir, exist_ok=True)
        manifest = bundle.manifest
        pkg_name = manifest.package_id
        pkg_dir = os.path.join(output_dir, "app", "src", "main", "java", *pkg_name.split("."))
        runtime_pkg_dir = os.path.join(output_dir, "app", "src", "main", "java", "org", "starlang", "runtime")
        cpp_dir = os.path.join(output_dir, "app", "src", "main", "cpp")
        assets_dir = os.path.join(output_dir, "app", "src", "main", "assets")

        os.makedirs(pkg_dir, exist_ok=True)
        os.makedirs(runtime_pkg_dir, exist_ok=True)
        os.makedirs(cpp_dir, exist_ok=True)
        os.makedirs(assets_dir, exist_ok=True)

        # 0. Android SDK Configuration (local.properties & gradle.properties)
        if self.sdk and self.sdk.is_valid:
            self.sdk.generate_local_properties(output_dir)
        else:
            with open(os.path.join(output_dir, "local.properties"), "w", encoding="utf-8") as f:
                f.write("## Android SDK local.properties\n")

        with open(os.path.join(output_dir, "gradle.properties"), "w", encoding="utf-8") as f:
            f.write("org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8\nandroid.useAndroidX=true\nandroid.nonTransitiveRClass=true\n")

        # 1. Root settings.gradle
        with open(os.path.join(output_dir, "settings.gradle"), "w", encoding="utf-8") as f:
            f.write(f'rootProject.name = "{manifest.name}"\ninclude(":app")\n')

        # 2. Root build.gradle
        with open(os.path.join(output_dir, "build.gradle"), "w", encoding="utf-8") as f:
            f.write("""buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:8.2.0"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
""")

        # 3. app/build.gradle
        with open(os.path.join(output_dir, "app", "build.gradle"), "w", encoding="utf-8") as f:
            f.write(f"""plugins {{
    id "com.android.application"
}}

android {{
    namespace "{pkg_name}"
    compileSdk 34

    defaultConfig {{
        applicationId "{pkg_name}"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "{manifest.version}"

        ndk {{
            abiFilters "arm64-v8a", "armeabi-v7a", "x86_64"
        }}
        externalNativeBuild {{
            cmake {{
                cppFlags "-std=c++20"
            }}
        }}
    }}

    externalNativeBuild {{
        cmake {{
            path "src/main/cpp/CMakeLists.txt"
        }}
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"
        }}
    }}
}}

dependencies {{
    implementation "androidx.appcompat:appcompat:1.6.1"
}}
""")

        # 4. AndroidManifest.xml
        perm_tags = ""
        for p in manifest.permissions:
            if p == "vibrate":
                perm_tags += '    <uses-permission android:name="android.permission.VIBRATE" />\n'
            elif p == "network":
                perm_tags += '    <uses-permission android:name="android.permission.INTERNET" />\n'

        with open(os.path.join(output_dir, "app", "src", "main", "AndroidManifest.xml"), "w", encoding="utf-8") as f:
            f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{pkg_name}">

{perm_tags}
    <application
        android:allowBackup="true"
        android:label="{manifest.name}"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="{manifest.orientation}"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
""")

        # 5. Java Sources
        with open(os.path.join(pkg_dir, "MainActivity.java"), "w", encoding="utf-8") as f:
            f.write(StarActivity.generate_main_activity_java(pkg_name, manifest.name))

        with open(os.path.join(runtime_pkg_dir, "StarNativeBridge.java"), "w", encoding="utf-8") as f:
            f.write(AndroidJNIBridge.generate_java_bridge_source())

        with open(os.path.join(runtime_pkg_dir, "StarSurfaceView.java"), "w", encoding="utf-8") as f:
            f.write(AndroidSurfaceRenderer.generate_surface_view_java())

        # 6. C++ NDK Bridge & CMakeLists.txt
        with open(os.path.join(cpp_dir, "star_jni_bridge.cpp"), "w", encoding="utf-8") as f:
            f.write(AndroidJNIBridge.generate_cpp_jni_source())

        with open(os.path.join(cpp_dir, "CMakeLists.txt"), "w", encoding="utf-8") as f:
            f.write("""cmake_minimum_required(VERSION 3.22.1)
project("starnative")

add_library(starnative SHARED star_jni_bridge.cpp)

find_library(log-lib log)
find_library(android-lib android)

target_link_libraries(starnative ${log-lib} ${android-lib})
""")

        # 7. Embed .starmobile bundle into assets
        shutil.copyfile(bundle_path, os.path.join(assets_dir, "app.starmobile"))

        # 8. Generate Gradle Wrapper, Proguard Rules & App Icons
        self._generate_gradle_wrapper(output_dir)
        self._generate_proguard_rules(output_dir)
        self._generate_app_icons(output_dir)

        return output_dir

    def _generate_app_icons(self, output_dir: str):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        canonical_res = os.path.join(repo_root, "android", "app", "src", "main", "res")
        res_dir = os.path.join(output_dir, "app", "src", "main", "res")

        if os.path.exists(canonical_res):
            for root, dirs, files in os.walk(canonical_res):
                for f in files:
                    src_f = os.path.join(root, f)
                    rel_p = os.path.relpath(src_f, canonical_res)
                    dst_f = os.path.join(res_dir, rel_p)
                    os.makedirs(os.path.dirname(dst_f), exist_ok=True)
                    shutil.copyfile(src_f, dst_f)
        else:
            from scripts.generate_app_icons import install_all_icons
            install_all_icons(res_dir)

    def _generate_proguard_rules(self, output_dir: str):
        proguard_path = os.path.join(output_dir, "app", "proguard-rules.pro")
        with open(proguard_path, "w", encoding="utf-8") as f:
            f.write("""# Star Android Native Runtime ProGuard / R8 Rules
-keep class org.starlang.runtime.** { *; }
-keepclassmembers class * {
    native <methods>;
}
-dontwarn org.starlang.**
-keepattributes *Annotation*,Signature,InnerClasses,EnclosingMethod
""")

    def _generate_gradle_wrapper(self, output_dir: str):
        wrapper_dir = os.path.join(output_dir, "gradle", "wrapper")
        os.makedirs(wrapper_dir, exist_ok=True)

        # gradle-wrapper.properties
        props_path = os.path.join(wrapper_dir, "gradle-wrapper.properties")
        with open(props_path, "w", encoding="utf-8") as f:
            f.write("""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

        # Minimal valid gradle-wrapper.jar stub
        jar_path = os.path.join(wrapper_dir, "gradle-wrapper.jar")
        if not os.path.exists(jar_path):
            import zipfile
            with zipfile.ZipFile(jar_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("META-INF/MANIFEST.MF", "Manifest-Version: 1.0\nMain-Class: org.gradle.wrapper.GradleWrapperMain\n\n")

        # gradlew.bat
        bat_path = os.path.join(output_dir, "gradlew.bat")
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write("""@if "%DEBUG%" == "" @echo off
@rem Gradle startup script for Windows
if "%OS%"=="Windows_NT" setlocal
set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"
if defined JAVA_HOME goto findJavaFromJavaHome
set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto execute
echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe
if exist "%JAVA_EXE%" goto execute
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
goto fail

:execute
set CLASSPATH=%APP_HOME%\\gradle\\wrapper\\gradle-wrapper.jar
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal
""")

        # gradlew (POSIX)
        sh_path = os.path.join(output_dir, "gradlew")
        with open(sh_path, "w", encoding="utf-8") as f:
            f.write("""#!/bin/sh
APP_BASE_NAME=`basename "$0"`
APP_HOME="`pwd`"
CLASSPATH="$APP_HOME/gradle/wrapper/gradle-wrapper.jar"

if [ -n "$JAVA_HOME" ] ; then
    JAVACMD="$JAVA_HOME/bin/java"
else
    JAVACMD="java"
fi

exec "$JAVACMD" "-Dorg.gradle.appname=$APP_BASE_NAME" -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"
""")

