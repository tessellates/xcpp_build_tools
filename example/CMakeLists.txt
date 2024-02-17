cmake_minimum_required(VERSION 3.12)

#LANGUAGES can be: C , CXX (i.e. C++)
project(example VERSION 1.0
DESCRIPTION "example engine -- for simple examples"
LANGUAGES CXX)

add_executable(main main.cpp)