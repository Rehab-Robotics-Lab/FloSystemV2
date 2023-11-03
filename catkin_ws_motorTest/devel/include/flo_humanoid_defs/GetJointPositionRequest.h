// Generated by gencpp from file flo_humanoid_defs/GetJointPositionRequest.msg
// DO NOT EDIT!


#ifndef FLO_HUMANOID_DEFS_MESSAGE_GETJOINTPOSITIONREQUEST_H
#define FLO_HUMANOID_DEFS_MESSAGE_GETJOINTPOSITIONREQUEST_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace flo_humanoid_defs
{
template <class ContainerAllocator>
struct GetJointPositionRequest_
{
  typedef GetJointPositionRequest_<ContainerAllocator> Type;

  GetJointPositionRequest_()
    : id(0)  {
    }
  GetJointPositionRequest_(const ContainerAllocator& _alloc)
    : id(0)  {
  (void)_alloc;
    }



   typedef int8_t _id_type;
  _id_type id;





  typedef boost::shared_ptr< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> const> ConstPtr;

}; // struct GetJointPositionRequest_

typedef ::flo_humanoid_defs::GetJointPositionRequest_<std::allocator<void> > GetJointPositionRequest;

typedef boost::shared_ptr< ::flo_humanoid_defs::GetJointPositionRequest > GetJointPositionRequestPtr;
typedef boost::shared_ptr< ::flo_humanoid_defs::GetJointPositionRequest const> GetJointPositionRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator1> & lhs, const ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator2> & rhs)
{
  return lhs.id == rhs.id;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator1> & lhs, const ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace flo_humanoid_defs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "7d504299943ad968aabe3de24053d208";
  }

  static const char* value(const ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x7d504299943ad968ULL;
  static const uint64_t static_value2 = 0xaabe3de24053d208ULL;
};

template<class ContainerAllocator>
struct DataType< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "flo_humanoid_defs/GetJointPositionRequest";
  }

  static const char* value(const ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "#service defintion to get the position of one joint of the robot\n"
"int8 id\n"
;
  }

  static const char* value(const ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.id);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GetJointPositionRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::flo_humanoid_defs::GetJointPositionRequest_<ContainerAllocator>& v)
  {
    s << indent << "id: ";
    Printer<int8_t>::stream(s, indent + "  ", v.id);
  }
};

} // namespace message_operations
} // namespace ros

#endif // FLO_HUMANOID_DEFS_MESSAGE_GETJOINTPOSITIONREQUEST_H
