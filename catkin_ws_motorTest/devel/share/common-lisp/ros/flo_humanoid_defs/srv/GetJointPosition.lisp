; Auto-generated. Do not edit!


(cl:in-package flo_humanoid_defs-srv)


;//! \htmlinclude GetJointPosition-request.msg.html

(cl:defclass <GetJointPosition-request> (roslisp-msg-protocol:ros-message)
  ((id
    :reader id
    :initarg :id
    :type cl:fixnum
    :initform 0))
)

(cl:defclass GetJointPosition-request (<GetJointPosition-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetJointPosition-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetJointPosition-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name flo_humanoid_defs-srv:<GetJointPosition-request> is deprecated: use flo_humanoid_defs-srv:GetJointPosition-request instead.")))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <GetJointPosition-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:id-val is deprecated.  Use flo_humanoid_defs-srv:id instead.")
  (id m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetJointPosition-request>) ostream)
  "Serializes a message object of type '<GetJointPosition-request>"
  (cl:let* ((signed (cl:slot-value msg 'id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetJointPosition-request>) istream)
  "Deserializes a message object of type '<GetJointPosition-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'id) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetJointPosition-request>)))
  "Returns string type for a service object of type '<GetJointPosition-request>"
  "flo_humanoid_defs/GetJointPositionRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointPosition-request)))
  "Returns string type for a service object of type 'GetJointPosition-request"
  "flo_humanoid_defs/GetJointPositionRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetJointPosition-request>)))
  "Returns md5sum for a message object of type '<GetJointPosition-request>"
  "114a36cda781057b95290a137ea72b98")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetJointPosition-request)))
  "Returns md5sum for a message object of type 'GetJointPosition-request"
  "114a36cda781057b95290a137ea72b98")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetJointPosition-request>)))
  "Returns full string definition for message of type '<GetJointPosition-request>"
  (cl:format cl:nil "#service defintion to get the position of one joint of the robot~%int8 id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetJointPosition-request)))
  "Returns full string definition for message of type 'GetJointPosition-request"
  (cl:format cl:nil "#service defintion to get the position of one joint of the robot~%int8 id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetJointPosition-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetJointPosition-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetJointPosition-request
    (cl:cons ':id (id msg))
))
;//! \htmlinclude GetJointPosition-response.msg.html

(cl:defclass <GetJointPosition-response> (roslisp-msg-protocol:ros-message)
  ((position
    :reader position
    :initarg :position
    :type cl:integer
    :initform 0))
)

(cl:defclass GetJointPosition-response (<GetJointPosition-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetJointPosition-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetJointPosition-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name flo_humanoid_defs-srv:<GetJointPosition-response> is deprecated: use flo_humanoid_defs-srv:GetJointPosition-response instead.")))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <GetJointPosition-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:position-val is deprecated.  Use flo_humanoid_defs-srv:position instead.")
  (position m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetJointPosition-response>) ostream)
  "Serializes a message object of type '<GetJointPosition-response>"
  (cl:let* ((signed (cl:slot-value msg 'position)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetJointPosition-response>) istream)
  "Deserializes a message object of type '<GetJointPosition-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'position) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetJointPosition-response>)))
  "Returns string type for a service object of type '<GetJointPosition-response>"
  "flo_humanoid_defs/GetJointPositionResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointPosition-response)))
  "Returns string type for a service object of type 'GetJointPosition-response"
  "flo_humanoid_defs/GetJointPositionResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetJointPosition-response>)))
  "Returns md5sum for a message object of type '<GetJointPosition-response>"
  "114a36cda781057b95290a137ea72b98")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetJointPosition-response)))
  "Returns md5sum for a message object of type 'GetJointPosition-response"
  "114a36cda781057b95290a137ea72b98")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetJointPosition-response>)))
  "Returns full string definition for message of type '<GetJointPosition-response>"
  (cl:format cl:nil "int32 position~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetJointPosition-response)))
  "Returns full string definition for message of type 'GetJointPosition-response"
  (cl:format cl:nil "int32 position~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetJointPosition-response>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetJointPosition-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetJointPosition-response
    (cl:cons ':position (position msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetJointPosition)))
  'GetJointPosition-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetJointPosition)))
  'GetJointPosition-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointPosition)))
  "Returns string type for a service object of type '<GetJointPosition>"
  "flo_humanoid_defs/GetJointPosition")