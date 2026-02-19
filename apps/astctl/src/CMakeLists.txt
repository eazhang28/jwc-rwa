cmake_minimum_required(VERSION 3.15)
project(jwc_embedded)

add_executable(jwc_embedded main.cpp)
target_link_libraries(jwc_embedded
  PRIVATE
    Eigen3::Eigen
    gtu_lib
)
