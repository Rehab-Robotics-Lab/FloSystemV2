; Auto-generated. Do not edit!


(cl:in-package dynamixel_sdk_examples-msg)


;//! \htmlinclude SetPosition.msg.html

(cl:defclass <SetPosition> (roslisp-msg-protocol:ros-message)
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

(cl:defclass SetPosition (<SetPosition>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetPosition>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetPosition)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dynamixel_sdk_examples-msg:<SetPosition> is deprecated: use dynamixel_sdk_examples-msg:SetPosition instead.")))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <SetPosition>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dynamixel_sdk_examples-msg:id-val is deprecated.  Use dynamixel_sdk_examples-msg:id instead.")
  (id m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <SetPosition>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dynamixel_sdk_examples-msg:position-val is deprecated.  Use dynamixel_sdk_examples-msg:position instead.")
  (position m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetPosition>) ostream)
  "Serializes a message object of type '<SetPosition>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'position)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetPosition>) istream)
  "Deserializes a message object of type '<SetPosition>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'position) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetPosition>)))
  "Returns string type for a message object of type '<SetPosition>"
  "dynamixel_sdk_examples/SetPosition")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetPosition)))
  "Returns string type for a message object of type 'SetPosition"
  "dynamixel_sdk_examples/SetPosition")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetPosition>)))
  "Returns md5sum for a message object of type '<SetPosition>"
  "0a775458729eb3272bc88b4f5f764cc8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetPosition)))
  "Returns md5sum for a message object of type 'SetPosition"
  "0a775458729eb3272bc88b4f5f764cc8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetPosition>)))
  "Returns full string definition for message of type '<SetPosition>"
  (cl:format cl:nil "uint8 id~%int32 position~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetPosition)))
  "Returns full string definition for message of type 'SetPosition"
  (cl:format cl:nil "uint8 id~%int32 position~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetPosition>))
  (cl:+ 0
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetPosition>))
  "Converts a ROS message object to a list"
  (cl:list 'SetPosition
    (cl:cons ':id (id msg))
    (cl:cons ':position (position msg))
))
