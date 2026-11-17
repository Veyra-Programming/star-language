cmake_minimum_required(VERSION 3.22.1)
project("starnative")

add_library(starnative SHARED star_jni_bridge.cpp)

find_library(log-lib log)
find_library(android-lib android)

target_link_libraries(starnative ${log-lib} ${android-lib})

