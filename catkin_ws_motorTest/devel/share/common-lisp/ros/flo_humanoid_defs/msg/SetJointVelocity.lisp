; Auto-generated. Do not edit!


(cl:in-package flo_humanoid_defs-msg)


;//! \htmlinclude SetJointVelocity.msg.html

(cl:defclass <SetJointVelocity> (roslisp-msg-protocol:ros-message)
  ((id
    :reader id
    :initarg :id
    :type cl:fixnum
    :initform 0)
   (endposition
    :reader endposition
    :initarg :endposition
    :type cl:integer
    :initform 0)
   (velocity
    :reader velocity
    :initarg :velocity
    :type cl:integer
    :initform 0))
)

(cl:defclass SetJointVelocity (<SetJointVelocity>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetJointVelocity>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetJointVelocity)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name flo_humanoid_defs-msg:<SetJointVelocity> is deprecated: use flo_humanoid_defs-msg:SetJointVelocity instead.")))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <SetJointVelocity>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-msg:id-val is deprecated.  Use flo_humanoid_defs-msg:id instead.")
  (id m))

(cl:ensure-generic-function 'endposition-val :lambda-list '(m))
(cl:defmethod endposition-val ((m <SetJointVelocity>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-msg:endposition-val is deprecated.  Use flo_humanoid_defs-msg:endposition instead.")
  (endposition m))

(cl:ensure-generic-function 'velocity-val :lambda-list '(m))
(cl:defmethod velocity-val ((m <SetJointVelocity>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-msg:velocity-val is deprecated.  Use flo_humanoid_defs-msg:velocity instead.")
  (velocity m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetJointVelocity>) ostream)
  "Serializes a message object of type '<SetJointVelocity>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'endposition)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'velocity)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetJointVelocity>) istream)
  "Deserializes a message object of type '<SetJointVelocity>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'endposition) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'velocity) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetJointVelocity>)))
  "Returns string type for a message object of type '<SetJointVelocity>"
  "flo_humanoid_defs/SetJointVelocity")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetJointVelocity)))
  "Returns string type for a message object of type 'SetJointVelocity"
  "flo_humanoid_defs/SetJointVelocity")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetJointVelocity>)))
  "Returns md5sum for a message object of type '<SetJointVelocity>"
  "849c7d5675e0a15566e7a31f1fcf93be")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetJointVelocity)))
  "Returns md5sum for a message object of type 'SetJointVelocity"
  "849c7d5675e0a15566e7a31f1fcf93be")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetJointVelocity>)))
  "Returns full string definition for message of type '<SetJointVelocity>"
  (cl:format cl:nil "#Message definition to set the velocity of the end effector~%uint8 id~%int32 endposition~%int32 velocity~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetJointVelocity)))
  "Returns full string definition for message of type 'SetJointVelocity"
  (cl:format cl:nil "#Message definition to set the velocity of the end effector~%uint8 id~%int32 endposition~%int32 velocity~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetJointVelocity>))
  (cl:+ 0
     1
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetJointVelocity>))
  "Converts a ROS message object to a list"
  (cl:list 'SetJointVelocity
    (cl:cons ':id (id msg))
    (cl:cons ':endposition (endposition msg))
    (cl:cons ':velocity (velocity msg))
))
