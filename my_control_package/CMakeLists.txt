cmake_minimum_required(VERSION 3.8)
project(my_control_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
# find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(rclpy REQUIRED)
find_package(crazyflie_interfaces)
find_package(crazyflie REQUIRED)
find_package(builtin_interfaces REQUIRED)


# find_package(crazyflie_py REQUIRED)
# find_package(crazyflie_sim REQUIRED)

# Install the package as a Python module
ament_python_install_package(${PROJECT_NAME})

# Install individual Python executables
# Install each script individually with RENAME for each
install(PROGRAMS
  my_control_package/emergency_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME emergency_node
)

install(PROGRAMS
  my_control_package/hello_world.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME hello_world
)

install(PROGRAMS
  my_control_package/battery_reader.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME battery_reader
)

install(PROGRAMS
  my_control_package/L_shape.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME L_shape
)

# Install the launch files
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME}/)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()

  find_package(ament_cmake_pytest REQUIRED)
  set(_pytest_tests
    #test/test_flake8.py
    #test/test_pep257.py
  )
  foreach(_test_path ${_pytest_tests})
    get_filename_component(_test_name ${_test_path} NAME_WE)
    ament_add_pytest_test(${_test_name} ${_test_path}
      APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}
      TIMEOUT 60
      WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    )
  endforeach()
endif()


ament_package()
