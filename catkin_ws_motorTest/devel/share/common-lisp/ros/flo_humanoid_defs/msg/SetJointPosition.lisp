; Auto-generated. Do not edit!


(cl:in-package flo_humanoid_defs-msg)


;//! \htmlinclude SetJointPosition.msg.html

(cl:defclass <SetJointPosition> (roslisp-msg-protocol:ros-message)
  ((id
    :reader id
    :initarg :id
    :type cl:fixnum
    :initform 0)
   (position
    :reader position
    :initarg :position
    :type cl:integer
    :initform 0))
)

(cl:defclass SetJointPosition (<SetJointPosition>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetJointPosition>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetJointPosition)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name flo_humanoid_defs-msg:<SetJointPosition> is deprecated: use flo_humanoid_defs-msg:SetJointPosition instead.")))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <SetJointPosition>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-msg:id-val is deprecated.  Use flo_humanoid_defs-msg:id instead.")
  (id m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <SetJointPosition>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-msg:position-val is deprecated.  Use flo_humanoid_defs-msg:position instead.")
  (position m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetJointPosition>) ostream)
  "Serializes a message object of type '<SetJointPosition>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'position)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetJointPosition>) istream)
  "Deserializes a message object of type '<SetJointPosition>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'position) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetJointPosition>)))
  "Returns string type for a message object of type '<SetJointPosition>"
  "flo_humanoid_defs/SetJointPosition")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetJointPosition)))
  "Returns string type for a message object of type 'SetJointPosition"
  "flo_humanoid_defs/SetJointPosition")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetJointPosition>)))
  "Returns md5sum for a message object of type '<SetJointPosition>"
  "0a775458729eb3272bc88b4f5f764cc8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetJointPosition)))
  "Returns md5sum for a message object of type 'SetJointPosition"
  "0a775458729eb3272bc88b4f5f764cc8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetJointPosition>)))
  "Returns full string definition for message of type '<SetJointPosition>"
  (cl:format cl:nil "#message definition to set the positon of one joint of the humanoid robot~%uint8 id~%int32 position~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetJointPosition)))
  "Returns full string definition for message of type 'SetJointPosition"
  (cl:format cl:nil "#message definition to set the positon of one joint of the humanoid robot~%uint8 id~%int32 position~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetJointPosition>))
  (cl:+ 0
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetJointPosition>))
  "Converts a ROS message object to a list"
  (cl:list 'SetJointPosition
    (cl:cons ':id (id msg))
    (cl:cons ':position (position msg))
))
