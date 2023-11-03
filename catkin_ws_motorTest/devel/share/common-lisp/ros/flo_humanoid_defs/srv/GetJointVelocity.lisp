; Auto-generated. Do not edit!


(cl:in-package flo_humanoid_defs-srv)


;//! \htmlinclude GetJointVelocity-request.msg.html

(cl:defclass <GetJointVelocity-request> (roslisp-msg-protocol:ros-message)
  ((id
    :reader id
    :initarg :id
    :type cl:fixnum
    :initform 0))
)

(cl:defclass GetJointVelocity-request (<GetJointVelocity-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetJointVelocity-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetJointVelocity-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name flo_humanoid_defs-srv:<GetJointVelocity-request> is deprecated: use flo_humanoid_defs-srv:GetJointVelocity-request instead.")))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <GetJointVelocity-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:id-val is deprecated.  Use flo_humanoid_defs-srv:id instead.")
  (id m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetJointVelocity-request>) ostream)
  "Serializes a message object of type '<GetJointVelocity-request>"
  (cl:let* ((signed (cl:slot-value msg 'id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetJointVelocity-request>) istream)
  "Deserializes a message object of type '<GetJointVelocity-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'id) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetJointVelocity-request>)))
  "Returns string type for a service object of type '<GetJointVelocity-request>"
  "flo_humanoid_defs/GetJointVelocityRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointVelocity-request)))
  "Returns string type for a service object of type 'GetJointVelocity-request"
  "flo_humanoid_defs/GetJointVelocityRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetJointVelocity-request>)))
  "Returns md5sum for a message object of type '<GetJointVelocity-request>"
  "810f3b5a74591cab058ea94decd15832")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetJointVelocity-request)))
  "Returns md5sum for a message object of type 'GetJointVelocity-request"
  "810f3b5a74591cab058ea94decd15832")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetJointVelocity-request>)))
  "Returns full string definition for message of type '<GetJointVelocity-request>"
  (cl:format cl:nil "#service defintion to get the velocity of one joint of the robot~%int8 id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetJointVelocity-request)))
  "Returns full string definition for message of type 'GetJointVelocity-request"
  (cl:format cl:nil "#service defintion to get the velocity of one joint of the robot~%int8 id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetJointVelocity-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetJointVelocity-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetJointVelocity-request
    (cl:cons ':id (id msg))
))
;//! \htmlinclude GetJointVelocity-response.msg.html

(cl:defclass <GetJointVelocity-response> (roslisp-msg-protocol:ros-message)
  ((velocity
    :reader velocity
    :initarg :velocity
    :type cl:integer
    :initform 0))
)

(cl:defclass GetJointVelocity-response (<GetJointVelocity-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetJointVelocity-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetJointVelocity-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name flo_humanoid_defs-srv:<GetJointVelocity-response> is deprecated: use flo_humanoid_defs-srv:GetJointVelocity-response instead.")))

(cl:ensure-generic-function 'velocity-val :lambda-list '(m))
(cl:defmethod velocity-val ((m <GetJointVelocity-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:velocity-val is deprecated.  Use flo_humanoid_defs-srv:velocity instead.")
  (velocity m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetJointVelocity-response>) ostream)
  "Serializes a message object of type '<GetJointVelocity-response>"
  (cl:let* ((signed (cl:slot-value msg 'velocity)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetJointVelocity-response>) istream)
  "Deserializes a message object of type '<GetJointVelocity-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'velocity) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetJointVelocity-response>)))
  "Returns string type for a service object of type '<GetJointVelocity-response>"
  "flo_humanoid_defs/GetJointVelocityResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointVelocity-response)))
  "Returns string type for a service object of type 'GetJointVelocity-response"
  "flo_humanoid_defs/GetJointVelocityResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetJointVelocity-response>)))
  "Returns md5sum for a message object of type '<GetJointVelocity-response>"
  "810f3b5a74591cab058ea94decd15832")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetJointVelocity-response)))
  "Returns md5sum for a message object of type 'GetJointVelocity-response"
  "810f3b5a74591cab058ea94decd15832")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetJointVelocity-response>)))
  "Returns full string definition for message of type '<GetJointVelocity-response>"
  (cl:format cl:nil "int32 velocity~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetJointVelocity-response)))
  "Returns full string definition for message of type 'GetJointVelocity-response"
  (cl:format cl:nil "int32 velocity~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetJointVelocity-response>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetJointVelocity-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetJointVelocity-response
    (cl:cons ':velocity (velocity msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetJointVelocity)))
  'GetJointVelocity-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetJointVelocity)))
  'GetJointVelocity-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointVelocity)))
  "Returns string type for a service object of type '<GetJointVelocity>"
  "flo_humanoid_defs/GetJointVelocity")