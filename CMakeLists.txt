cmake_minimum_required(VERSION 3.10)

# Build options
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)

set(CMAKE_CXX_FLAGS "-Wall -Wextra -Wpedantic")
if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address -fno-omit-frame-pointer")
endif ()

# Building
project(rclib VERSION 0.0.1 DESCRIPTION "Python wrapper for rcLib")
include_directories(/usr/include/python3.6/)

set(SOURCES rclibmodule.c)

set(LIBS)

include_directories(${CMAKE_SOURCE_DIR})
add_library(${PROJECT_NAME} SHARED ${SOURCES})
target_link_libraries(${PROJECT_NAME} ${LIBS})