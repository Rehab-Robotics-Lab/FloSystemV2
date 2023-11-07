;; Auto-generated. Do not edit!


(when (boundp 'dynamixel_sdk_examples::GetPosition)
  (if (not (find-package "DYNAMIXEL_SDK_EXAMPLES"))
    (make-package "DYNAMIXEL_SDK_EXAMPLES"))
  (shadow 'GetPosition (find-package "DYNAMIXEL_SDK_EXAMPLES")))
(unless (find-package "DYNAMIXEL_SDK_EXAMPLES::GETPOSITION")
  (make-package "DYNAMIXEL_SDK_EXAMPLES::GETPOSITION"))
(unless (find-package "DYNAMIXEL_SDK_EXAMPLES::GETPOSITIONREQUEST")
  (make-package "DYNAMIXEL_SDK_EXAMPLES::GETPOSITIONREQUEST"))
(unless (find-package "DYNAMIXEL_SDK_EXAMPLES::GETPOSITIONRESPONSE")
  (make-package "DYNAMIXEL_SDK_EXAMPLES::GETPOSITIONRESPONSE"))

(in-package "ROS")





(defclass dynamixel_sdk_examples::GetPositionRequest
  :super ros::object
  :slots (_id ))

(defmethod dynamixel_sdk_examples::GetPositionRequest
  (:init
   (&key
    ((:id __id) 0)
    )
   (send-super :init)
   (setq _id (round __id))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:serialization-length
   ()
   (+
    ;; uint8 _id
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _id
       (write-byte _id s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _id
     (setq _id (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(defclass dynamixel_sdk_examples::GetPositionResponse
  :super ros::object
  :slots (_position ))

(defmethod dynamixel_sdk_examples::GetPositionResponse
  (:init
   (&key
    ((:position __position) 0)
    )
   (send-super :init)
   (setq _position (round __position))
   self)
  (:position
   (&optional __position)
   (if __position (setq _position __position)) _position)
  (:serialization-length
   ()
   (+
    ;; int32 _position
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _position
       (write-long _position s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _position
     (setq _position (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass dynamixel_sdk_examples::GetPosition
  :super ros::object
  :slots ())

(setf (get dynamixel_sdk_examples::GetPosition :md5sum-) "b532ace3b383dc4c9e64687156423ac0")
(setf (get dynamixel_sdk_examples::GetPosition :datatype-) "dynamixel_sdk_examples/GetPosition")
(setf (get dynamixel_sdk_examples::GetPosition :request) dynamixel_sdk_examples::GetPositionRequest)
(setf (get dynamixel_sdk_examples::GetPosition :response) dynamixel_sdk_examples::GetPositionResponse)

(defmethod dynamixel_sdk_examples::GetPositionRequest
  (:response () (instance dynamixel_sdk_examples::GetPositionResponse :init)))

(setf (get dynamixel_sdk_examples::GetPositionRequest :md5sum-) "b532ace3b383dc4c9e64687156423ac0")
(setf (get dynamixel_sdk_examples::GetPositionRequest :datatype-) "dynamixel_sdk_examples/GetPositionRequest")
(setf (get dynamixel_sdk_examples::GetPositionRequest :definition-)
      "uint8 id
---
int32 position

")

(setf (get dynamixel_sdk_examples::GetPositionResponse :md5sum-) "b532ace3b383dc4c9e64687156423ac0")
(setf (get dynamixel_sdk_examples::GetPositionResponse :datatype-) "dynamixel_sdk_examples/GetPositionResponse")
(setf (get dynamixel_sdk_examples::GetPositionResponse :definition-)
      "uint8 id
---
int32 position

")



(provide :dynamixel_sdk_examples/GetPosition "b532ace3b383dc4c9e64687156423ac0")


