// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from crazyflie_interfaces:srv/Arm.idl
// generated code does not contain a copyright notice

#ifndef CRAZYFLIE_INTERFACES__SRV__DETAIL__ARM__STRUCT_HPP_
#define CRAZYFLIE_INTERFACES__SRV__DETAIL__ARM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__crazyflie_interfaces__srv__Arm_Request __attribute__((deprecated))
#else
# define DEPRECATED__crazyflie_interfaces__srv__Arm_Request __declspec(deprecated)
#endif

namespace crazyflie_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Arm_Request_
{
  using Type = Arm_Request_<ContainerAllocator>;

  explicit Arm_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->arm = false;
    }
  }

  explicit Arm_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->arm = false;
    }
  }

  // field types and members
  using _arm_type =
    bool;
  _arm_type arm;

  // setters for named parameter idiom
  Type & set__arm(
    const bool & _arg)
  {
    this->arm = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__crazyflie_interfaces__srv__Arm_Request
    std::shared_ptr<crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__crazyflie_interfaces__srv__Arm_Request
    std::shared_ptr<crazyflie_interfaces::srv::Arm_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Arm_Request_ & other) const
  {
    if (this->arm != other.arm) {
      return false;
    }
    return true;
  }
  bool operator!=(const Arm_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Arm_Request_

// alias to use template instance with default allocator
using Arm_Request =
  crazyflie_interfaces::srv::Arm_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace crazyflie_interfaces


#ifndef _WIN32
# define DEPRECATED__crazyflie_interfaces__srv__Arm_Response __attribute__((deprecated))
#else
# define DEPRECATED__crazyflie_interfaces__srv__Arm_Response __declspec(deprecated)
#endif

namespace crazyflie_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Arm_Response_
{
  using Type = Arm_Response_<ContainerAllocator>;

  explicit Arm_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit Arm_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__crazyflie_interfaces__srv__Arm_Response
    std::shared_ptr<crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__crazyflie_interfaces__srv__Arm_Response
    std::shared_ptr<crazyflie_interfaces::srv::Arm_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Arm_Response_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const Arm_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Arm_Response_

// alias to use template instance with default allocator
using Arm_Response =
  crazyflie_interfaces::srv::Arm_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace crazyflie_interfaces

namespace crazyflie_interfaces
{

namespace srv
{

struct Arm
{
  using Request = crazyflie_interfaces::srv::Arm_Request;
  using Response = crazyflie_interfaces::srv::Arm_Response;
};

}  // namespace srv

}  // namespace crazyflie_interfaces

#endif  // CRAZYFLIE_INTERFACES__SRV__DETAIL__ARM__STRUCT_HPP_
