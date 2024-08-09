cmake_minimum_required(VERSION 3.17)
project(exking CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# Use response files when linking objects because of the large number of source files
set(CMAKE_CXX_USE_RESPONSE_FILE_FOR_OBJECTS ON)
if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
  add_compile_options(-fdiagnostics-color=always)
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  add_compile_options(-fcolor-diagnostics)
  # Required to silence "unused argument" warnings for -stdlib=libc++ when using distcc
  add_compile_options(-Wno-unused-command-line-argument)
  # Required to fix source paths in debug info when using distcc
  add_compile_options(-fdebug-prefix-map=/tmp=${CMAKE_CURRENT_BINARY_DIR})
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(exking)

target_include_directories(exking PRIVATE src)
target_compile_definitions(exking PRIVATE NON_MATCHING)
target_compile_options(exking PRIVATE -fno-rtti -fno-exceptions)
target_compile_options(exking PRIVATE -fno-strict-aliasing)
target_compile_options(exking PRIVATE -Wall -Wextra -Wdeprecated)
target_compile_options(exking PRIVATE -Wno-unused-parameter -Wno-unused-private-field)
target_compile_options(exking PRIVATE -Wno-invalid-offsetof)
target_compile_options(exking PRIVATE -Wextra-semi)

# idfk how to figure this out
set(NN_SDK_MAJOR 15)
set(NN_SDK_MINOR 3)
set(NN_SDK_PATCH 1)
set(NN_SDK_TYPE "Release")

# same with this, I just copied it from the botw decomp but it says this isn't even right for that
set(NN_WARE_MAJOR 1)
set(NN_WARE_MINOR 6)
set(NN_WARE_PATCH 1)

add_subdirectory(lib/NintendoSDK)
target_link_libraries(exking PUBLIC NintendoSDK)

add_subdirectory(lib/sead)
target_link_libraries(exking PUBLIC sead)

add_subdirectory(lib/agl)
target_link_libraries(exking PUBLIC agl)

add_subdirectory(src)