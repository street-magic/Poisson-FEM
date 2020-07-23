cmake_minimum_required(VERSION 2.4)

project(Poisson-FEM)

add_executable(Poisson-FEM main.c)
target_link_libraries(Poisson-FEM m)