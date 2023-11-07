# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "dynamixel_sdk_examples: 3 messages, 3 services")

set(MSG_I_FLAGS "-Idynamixel_sdk_examples:/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(dynamixel_sdk_examples_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg" NAME_WE)
add_custom_target(_dynamixel_sdk_examples_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dynamixel_sdk_examples" "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg" ""
)

get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg" NAME_WE)
add_custom_target(_dynamixel_sdk_examples_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dynamixel_sdk_examples" "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg" ""
)

get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg" NAME_WE)
add_custom_target(_dynamixel_sdk_examples_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dynamixel_sdk_examples" "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg" ""
)

get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv" NAME_WE)
add_custom_target(_dynamixel_sdk_examples_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dynamixel_sdk_examples" "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv" ""
)

get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv" NAME_WE)
add_custom_target(_dynamixel_sdk_examples_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dynamixel_sdk_examples" "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv" ""
)

get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv" NAME_WE)
add_custom_target(_dynamixel_sdk_examples_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dynamixel_sdk_examples" "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_cpp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_cpp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Services
_generate_srv_cpp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_cpp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_cpp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Module File
_generate_module_cpp(dynamixel_sdk_examples
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dynamixel_sdk_examples
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(dynamixel_sdk_examples_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(dynamixel_sdk_examples_generate_messages dynamixel_sdk_examples_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_cpp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_cpp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_cpp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_cpp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_cpp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_cpp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dynamixel_sdk_examples_gencpp)
add_dependencies(dynamixel_sdk_examples_gencpp dynamixel_sdk_examples_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dynamixel_sdk_examples_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_eus(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_eus(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Services
_generate_srv_eus(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_eus(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_eus(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Module File
_generate_module_eus(dynamixel_sdk_examples
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dynamixel_sdk_examples
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(dynamixel_sdk_examples_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(dynamixel_sdk_examples_generate_messages dynamixel_sdk_examples_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_eus _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_eus _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_eus _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_eus _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_eus _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_eus _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dynamixel_sdk_examples_geneus)
add_dependencies(dynamixel_sdk_examples_geneus dynamixel_sdk_examples_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dynamixel_sdk_examples_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_lisp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_lisp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Services
_generate_srv_lisp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_lisp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_lisp(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Module File
_generate_module_lisp(dynamixel_sdk_examples
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dynamixel_sdk_examples
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(dynamixel_sdk_examples_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(dynamixel_sdk_examples_generate_messages dynamixel_sdk_examples_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_lisp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_lisp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_lisp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_lisp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_lisp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_lisp _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dynamixel_sdk_examples_genlisp)
add_dependencies(dynamixel_sdk_examples_genlisp dynamixel_sdk_examples_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dynamixel_sdk_examples_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_nodejs(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_nodejs(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Services
_generate_srv_nodejs(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_nodejs(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_nodejs(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Module File
_generate_module_nodejs(dynamixel_sdk_examples
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dynamixel_sdk_examples
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(dynamixel_sdk_examples_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(dynamixel_sdk_examples_generate_messages dynamixel_sdk_examples_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_nodejs _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_nodejs _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_nodejs _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_nodejs _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_nodejs _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_nodejs _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dynamixel_sdk_examples_gennodejs)
add_dependencies(dynamixel_sdk_examples_gennodejs dynamixel_sdk_examples_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dynamixel_sdk_examples_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_py(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_msg_py(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Services
_generate_srv_py(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_py(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples
)
_generate_srv_py(dynamixel_sdk_examples
  "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples
)

### Generating Module File
_generate_module_py(dynamixel_sdk_examples
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(dynamixel_sdk_examples_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(dynamixel_sdk_examples_generate_messages dynamixel_sdk_examples_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_py _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/SyncSetPosition.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_py _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/msg/BulkSetItem.msg" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_py _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/GetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_py _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/SyncGetPosition.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_py _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ajay/catkin_ws_dynamixel/src/dynamixel_sdk_examples/srv/BulkGetItem.srv" NAME_WE)
add_dependencies(dynamixel_sdk_examples_generate_messages_py _dynamixel_sdk_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dynamixel_sdk_examples_genpy)
add_dependencies(dynamixel_sdk_examples_genpy dynamixel_sdk_examples_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dynamixel_sdk_examples_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dynamixel_sdk_examples)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dynamixel_sdk_examples
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(dynamixel_sdk_examples_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dynamixel_sdk_examples)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dynamixel_sdk_examples
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(dynamixel_sdk_examples_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dynamixel_sdk_examples)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dynamixel_sdk_examples
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(dynamixel_sdk_examples_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dynamixel_sdk_examples)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dynamixel_sdk_examples
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(dynamixel_sdk_examples_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dynamixel_sdk_examples
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(dynamixel_sdk_examples_generate_messages_py std_msgs_generate_messages_py)
endif()
