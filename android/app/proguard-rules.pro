# ProGuard rules for Star Go Android Companion App
-keep class org.starlang.go.** { *; }
-keep class org.starlang.runtime.** { *; }
-keepclassmembers class * {
    native <methods>;
}
-dontwarn org.starlang.**

