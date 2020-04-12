cmake_minimum_required(VERSION 3.10)
project(rc_lib)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS "-Wall -Wextra -Wpedantic -Werror -mtune=native -march=native")
if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")
endif ()

set(SOURCES RadioControlProtocolCpp/rcLib.cpp
    RadioControlProtocolCpp/RadioControlProtocolC/rc_lib.c)

add_subdirectory(pybind11)
pybind11_add_module(${PROJECT_NAME} main.cpp ${SOURCES})
