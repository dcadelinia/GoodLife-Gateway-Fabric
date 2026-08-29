cmake_minimum_required(VERSION 3.18)
project(GoodLifeGatewayFabric LANGUAGES CXX)

# ---- COMPILATION SETTINGS ----
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# ---- CONFIGURATION DIRECTORIES ----
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/cognitive_layer)

# ---- EXECUTABLE BUILDING TARGETS ----
add_executable(goodlife_gateway 
    cognitive_layer/orchestrator/gateway_core.cpp
)

# ---- PRODUCTION SYSTEM COMPILATION FLAGS ----
target_compile_definitions(goodlife_gateway PRIVATE
    NVIDIA_BLACKWELL_NATIVE=1
    DYNAMO_SHADOW_RECOVERY=1
    GROQ_LPX_ACCELERATED=1
)

# ---- PRINT VERIFICATION PIPELINE DURING GENERATION ----
message(STATUS "--------------------------------------------------------")
message(STATUS "Configuring Project Koridor & Mycelium Core Infrastructure Stack")
message(STATUS "Target Architecture: Universal Hardware-Accelerated Fabric Map")
message(STATUS "--------------------------------------------------------")
