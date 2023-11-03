; Auto-generated. Do not edit!


(cl:in-package flo_humanoid_defs-srv)


;//! \htmlinclude GetJointPositions-request.msg.html

(cl:defclass <GetJointPositions-request> (roslisp-msg-protocol:ros-message)
  ((id1
    :reader id1
    :initarg :id1
    :type cl:fixnum
    :initform 0)
   (id2
    :reader id2
    :initarg :id2
    :type cl:fixnum
    :initform 0)
   (id3
    :reader id3
    :initarg :id3
    :type cl:fixnum
    :initform 0)
   (id4
    :reader id4
    :initarg :id4
    :type cl:fixnum
    :initform 0)
   (item1
    :reader item1
    :initarg :item1
    :type cl:string
    :initform "")
   (item2
    :reader item2
    :initarg :item2
    :type cl:string
    :initform "")
   (item3
    :reader item3
    :initarg :item3
    :type cl:string
    :initform "")
   (item4
    :reader item4
    :initarg :item4
    :type cl:string
    :initform ""))
)

(cl:defclass GetJointPositions-request (<GetJointPositions-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetJointPositions-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetJointPositions-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name flo_humanoid_defs-srv:<GetJointPositions-request> is deprecated: use flo_humanoid_defs-srv:GetJointPositions-request instead.")))

(cl:ensure-generic-function 'id1-val :lambda-list '(m))
(cl:defmethod id1-val ((m <GetJointPositions-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:id1-val is deprecated.  Use flo_humanoid_defs-srv:id1 instead.")
  (id1 m))

(cl:ensure-generic-function 'id2-val :lambda-list '(m))
(cl:defmethod id2-val ((m <GetJointPositions-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:id2-val is deprecated.  Use flo_humanoid_defs-srv:id2 instead.")
  (id2 m))

(cl:ensure-generic-function 'id3-val :lambda-list '(m))
(cl:defmethod id3-val ((m <GetJointPositions-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:id3-val is deprecated.  Use flo_humanoid_defs-srv:id3 instead.")
  (id3 m))

(cl:ensure-generic-function 'id4-val :lambda-list '(m))
(cl:defmethod id4-val ((m <GetJointPositions-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:id4-val is deprecated.  Use flo_humanoid_defs-srv:id4 instead.")
  (id4 m))

(cl:ensure-generic-function 'item1-val :lambda-list '(m))
(cl:defmethod item1-val ((m <GetJointPositions-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:item1-val is deprecated.  Use flo_humanoid_defs-srv:item1 instead.")
  (item1 m))

(cl:ensure-generic-function 'item2-val :lambda-list '(m))
(cl:defmethod item2-val ((m <GetJointPositions-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:item2-val is deprecated.  Use flo_humanoid_defs-srv:item2 instead.")
  (item2 m))

(cl:ensure-generic-function 'item3-val :lambda-list '(m))
(cl:defmethod item3-val ((m <GetJointPositions-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:item3-val is deprecated.  Use flo_humanoid_defs-srv:item3 instead.")
  (item3 m))

(cl:ensure-generic-function 'item4-val :lambda-list '(m))
(cl:defmethod item4-val ((m <GetJointPositions-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:item4-val is deprecated.  Use flo_humanoid_defs-srv:item4 instead.")
  (item4 m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetJointPositions-request>) ostream)
  "Serializes a message object of type '<GetJointPositions-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id1)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id2)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id3)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id4)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'item1))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'item1))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'item2))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'item2))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'item3))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'item3))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'item4))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'item4))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetJointPositions-request>) istream)
  "Deserializes a message object of type '<GetJointPositions-request>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id1)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id2)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id3)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id4)) (cl:read-byte istream))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'item1) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'item1) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'item2) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'item2) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'item3) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'item3) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'item4) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'item4) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetJointPositions-request>)))
  "Returns string type for a service object of type '<GetJointPositions-request>"
  "flo_humanoid_defs/GetJointPositionsRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointPositions-request)))
  "Returns string type for a service object of type 'GetJointPositions-request"
  "flo_humanoid_defs/GetJointPositionsRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetJointPositions-request>)))
  "Returns md5sum for a message object of type '<GetJointPositions-request>"
  "7b1fb47a48cf84af19e240b1f04307c5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetJointPositions-request)))
  "Returns md5sum for a message object of type 'GetJointPositions-request"
  "7b1fb47a48cf84af19e240b1f04307c5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetJointPositions-request>)))
  "Returns full string definition for message of type '<GetJointPositions-request>"
  (cl:format cl:nil "#Service definition to get the position of all the joints of 1 arm in the humanoid robot~%#(5 joints in each arm, 2 at the shoulder, 2 at the elbow and 1 at the end effector)~%uint8 id1~%uint8 id2~%uint8 id3~%uint8 id4~%string item1~%string item2~%string item3~%string item4~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetJointPositions-request)))
  "Returns full string definition for message of type 'GetJointPositions-request"
  (cl:format cl:nil "#Service definition to get the position of all the joints of 1 arm in the humanoid robot~%#(5 joints in each arm, 2 at the shoulder, 2 at the elbow and 1 at the end effector)~%uint8 id1~%uint8 id2~%uint8 id3~%uint8 id4~%string item1~%string item2~%string item3~%string item4~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetJointPositions-request>))
  (cl:+ 0
     1
     1
     1
     1
     4 (cl:length (cl:slot-value msg 'item1))
     4 (cl:length (cl:slot-value msg 'item2))
     4 (cl:length (cl:slot-value msg 'item3))
     4 (cl:length (cl:slot-value msg 'item4))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetJointPositions-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetJointPositions-request
    (cl:cons ':id1 (id1 msg))
    (cl:cons ':id2 (id2 msg))
    (cl:cons ':id3 (id3 msg))
    (cl:cons ':id4 (id4 msg))
    (cl:cons ':item1 (item1 msg))
    (cl:cons ':item2 (item2 msg))
    (cl:cons ':item3 (item3 msg))
    (cl:cons ':item4 (item4 msg))
))
;//! \htmlinclude GetJointPositions-response.msg.html

(cl:defclass <GetJointPositions-response> (roslisp-msg-protocol:ros-message)
  ((value1
    :reader value1
    :initarg :value1
    :type cl:integer
    :initform 0)
   (value2
    :reader value2
    :initarg :value2
    :type cl:integer
    :initform 0)
   (value3
    :reader value3
    :initarg :value3
    :type cl:integer
    :initform 0)
   (value4
    :reader value4
    :initarg :value4
    :type cl:integer
    :initform 0))
)

(cl:defclass GetJointPositions-response (<GetJointPositions-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetJointPositions-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetJointPositions-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name flo_humanoid_defs-srv:<GetJointPositions-response> is deprecated: use flo_humanoid_defs-srv:GetJointPositions-response instead.")))

(cl:ensure-generic-function 'value1-val :lambda-list '(m))
(cl:defmethod value1-val ((m <GetJointPositions-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:value1-val is deprecated.  Use flo_humanoid_defs-srv:value1 instead.")
  (value1 m))

(cl:ensure-generic-function 'value2-val :lambda-list '(m))
(cl:defmethod value2-val ((m <GetJointPositions-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:value2-val is deprecated.  Use flo_humanoid_defs-srv:value2 instead.")
  (value2 m))

(cl:ensure-generic-function 'value3-val :lambda-list '(m))
(cl:defmethod value3-val ((m <GetJointPositions-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:value3-val is deprecated.  Use flo_humanoid_defs-srv:value3 instead.")
  (value3 m))

(cl:ensure-generic-function 'value4-val :lambda-list '(m))
(cl:defmethod value4-val ((m <GetJointPositions-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader flo_humanoid_defs-srv:value4-val is deprecated.  Use flo_humanoid_defs-srv:value4 instead.")
  (value4 m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetJointPositions-response>) ostream)
  "Serializes a message object of type '<GetJointPositions-response>"
  (cl:let* ((signed (cl:slot-value msg 'value1)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'value2)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'value3)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'value4)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetJointPositions-response>) istream)
  "Deserializes a message object of type '<GetJointPositions-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'value1) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'value2) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'value3) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'value4) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetJointPositions-response>)))
  "Returns string type for a service object of type '<GetJointPositions-response>"
  "flo_humanoid_defs/GetJointPositionsResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointPositions-response)))
  "Returns string type for a service object of type 'GetJointPositions-response"
  "flo_humanoid_defs/GetJointPositionsResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetJointPositions-response>)))
  "Returns md5sum for a message object of type '<GetJointPositions-response>"
  "7b1fb47a48cf84af19e240b1f04307c5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetJointPositions-response)))
  "Returns md5sum for a message object of type 'GetJointPositions-response"
  "7b1fb47a48cf84af19e240b1f04307c5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetJointPositions-response>)))
  "Returns full string definition for message of type '<GetJointPositions-response>"
  (cl:format cl:nil "int32 value1~%int32 value2~%int32 value3~%int32 value4~%~%~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetJointPositions-response)))
  "Returns full string definition for message of type 'GetJointPositions-response"
  (cl:format cl:nil "int32 value1~%int32 value2~%int32 value3~%int32 value4~%~%~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetJointPositions-response>))
  (cl:+ 0
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetJointPositions-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetJointPositions-response
    (cl:cons ':value1 (value1 msg))
    (cl:cons ':value2 (value2 msg))
    (cl:cons ':value3 (value3 msg))
    (cl:cons ':value4 (value4 msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetJointPositions)))
  'GetJointPositions-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetJointPositions)))
  'GetJointPositions-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointPositions)))
  "Returns string type for a service object of type '<GetJointPositions>"
  "flo_humanoid_defs/GetJointPositions")