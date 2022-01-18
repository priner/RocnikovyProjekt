cmake_minimum_required(VERSION 3.5)
project(final_version)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -static-libgcc -static-libstdc++")

set(SOURCE_FILES
    cesky.cpp
    common.cpp
    common.h)

add_executable(final_version ${SOURCE_FILES})