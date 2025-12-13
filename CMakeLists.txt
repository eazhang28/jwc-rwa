set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
cmake_minimum_required(VERSION 4.1)
set(GPL_LIB_ROOT ./include/grblparse)
file(GLOB GPL_SOURCES
  "${GPL_LIB_ROOT}/src/*c"
)

add_library(gpl_library STATIC ${GPL_SOURCES})

target_include_directories(gpl_library PUBLIC
  "${GPL_LIB_ROOT}/src"
)

