cmake_minimum_required(VERSION 3.12)
project(crypto)

set(CMAKE_C_STANDARD 99)

set(CMAKE_BUILD_TYPE DEBUG)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS} -g3 -Wall -Wextra -fopenmp -fopenmp-simd -Wunused-function")

find_package(ZLIB REQUIRED)
find_package(PkgConfig REQUIRED)

set(LIBRARY_OUTPUT_PATH "../")

add_executable(cryptotest src/main.c src/assets.c src/extract.c src/filter.c src/json.c)
add_library(crypto SHARED src/main.c src/assets.c src/extract.c src/filter.c src/json.c)
target_link_libraries(crypto ZLIB::ZLIB)
target_link_libraries(cryptotest ZLIB::ZLIB)