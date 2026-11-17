#include <jni.h>
#include <android/log.h>
#include <string>
#include <vector>

#define TAG "StarNativeBridge"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, TAG, __VA_ARGS__)

static bool s_runtime_initialized = false;
static float s_density = 2.0f;
static int s_width = 1080;
static int s_height = 2400;

extern "C" {

JNIEXPORT jboolean JNICALL
Java_org_starlang_runtime_StarNativeBridge_initRuntime(
    JNIEnv* env,
    jobject thiz,
    jstring app_name,
    jint width,
    jint height,
    jfloat density
) {
    const char* native_app_name = env->GetStringUTFChars(app_name, nullptr);
    LOGI("StarVM Runtime initializing for App: %s (%dx%d @ %.1fx)", native_app_name, width, height, density);
    env->ReleaseStringUTFChars(app_name, native_app_name);

    s_width = width;
    s_height = height;
    s_density = density;
    s_runtime_initialized = true;
    return JNI_TRUE;
}

JNIEXPORT jboolean JNICALL
Java_org_starlang_runtime_StarNativeBridge_loadBytecode(
    JNIEnv* env,
    jobject thiz,
    jbyteArray bytecode
) {
    if (!s_runtime_initialized) {
        LOGE("Cannot load bytecode: Star runtime not initialized");
        return JNI_FALSE;
    }
    jsize len = env->GetArrayLength(bytecode);
    LOGI("Loading Star compiled bytecode bundle (%d bytes)", len);
    return JNI_TRUE;
}

JNIEXPORT void JNICALL
Java_org_starlang_runtime_StarNativeBridge_dispatchTouchEvent(
    JNIEnv* env,
    jobject thiz,
    jint phase,
    jint pointer_id,
    jfloat x,
    jfloat y
) {
    // Phase: 0=Down, 1=Move, 2=Up, 3=Cancel
}

JNIEXPORT jbyteArray JNICALL
Java_org_starlang_runtime_StarNativeBridge_renderFrame(
    JNIEnv* env,
    jobject thiz
) {
    // Returns binary render stream commands
    const char dummy_stream[] = "STAR_SURFACE_FRAME_V1";
    jsize len = sizeof(dummy_stream) - 1;
    jbyteArray result = env->NewByteArray(len);
    env->SetByteArrayRegion(result, 0, len, reinterpret_cast<const jbyte*>(dummy_stream));
    return result;
}

JNIEXPORT void JNICALL
Java_org_starlang_runtime_StarNativeBridge_dispatchLifecycle(
    JNIEnv* env,
    jobject thiz,
    jstring state
) {
    const char* native_state = env->GetStringUTFChars(state, nullptr);
    LOGI("Star Activity Lifecycle Transition: %s", native_state);
    env->ReleaseStringUTFChars(state, native_state);
}

JNIEXPORT jboolean JNICALL
Java_org_starlang_runtime_StarNativeBridge_dispatchBackPress(
    JNIEnv* env,
    jobject thiz
) {
    return JNI_FALSE;
}

} // extern "C"

