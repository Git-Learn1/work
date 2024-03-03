cmake_minimum_required(VERSION 3.4)
project(work)

set(PYTHON_EXECUTABLE "D:/Soft/Python/38/python.exe")
set(PYTHON_INCLUDE_DIRECTORY "D:/Soft/Python/38/include")

add_subdirectory(extern/pybind11)
pybind11_add_module(speedup src/cpp/speedup.cpp)
