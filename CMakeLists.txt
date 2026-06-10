cmake_minimum_required(VERSION 3.15...3.30)
project(simddot LANGUAGES CXX)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_core src/main.cpp)

set(SIMDDOT_ISA "generic" CACHE STRING "Target ISA: generic or avx2")
if(SIMDDOT_ISA STREQUAL "avx2")
    target_compile_options(_core PRIVATE -mavx2 -mfma)
    target_compile_definitions(_core PRIVATE SIMDDOT_AVX2=1)
elseif(NOT SIMDDOT_ISA STREQUAL "generic")
    message(FATAL_ERROR "Unknown SIMDDOT_ISA='${SIMDDOT_ISA}' (expected avx2 or generic)")
endif()

install(TARGETS _core DESTINATION simddot)
