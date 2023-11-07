;; Auto-generated. Do not edit!


(when (boundp 'dynamixel_sdk_examples::BulkGetItem)
  (if (not (find-package "DYNAMIXEL_SDK_EXAMPLES"))
    (make-package "DYNAMIXEL_SDK_EXAMPLES"))
  (shadow 'BulkGetItem (find-package "DYNAMIXEL_SDK_EXAMPLES")))
(unless (find-package "DYNAMIXEL_SDK_EXAMPLES::BULKGETITEM")
  (make-package "DYNAMIXEL_SDK_EXAMPLES::BULKGETITEM"))
(unless (find-package "DYNAMIXEL_SDK_EXAMPLES::BULKGETITEMREQUEST")
  (make-package "DYNAMIXEL_SDK_EXAMPLES::BULKGETITEMREQUEST"))
(unless (find-package "DYNAMIXEL_SDK_EXAMPLES::BULKGETITEMRESPONSE")
  (make-package "DYNAMIXEL_SDK_EXAMPLES::BULKGETITEMRESPONSE"))

(in-package "ROS")





(defclass dynamixel_sdk_examples::BulkGetItemRequest
  :super ros::object
  :slots (_id1 _id2 _item1 _item2 ))

(defmethod dynamixel_sdk_examples::BulkGetItemRequest
  (:init
   (&key
    ((:id1 __id1) 0)
    ((:id2 __id2) 0)
    ((:item1 __item1) "")
    ((:item2 __item2) "")
    )
   (send-super :init)
   (setq _id1 (round __id1))
   (setq _id2 (round __id2))
   (setq _item1 (string __item1))
   (setq _item2 (string __item2))
   self)
  (:id1
   (&optional __id1)
   (if __id1 (setq _id1 __id1)) _id1)
  (:id2
   (&optional __id2)
   (if __id2 (setq _id2 __id2)) _id2)
  (:item1
   (&optional __item1)
   (if __item1 (setq _item1 __item1)) _item1)
  (:item2
   (&optional __item2)
   (if __item2 (setq _item2 __item2)) _item2)
  (:serialization-length
   ()
   (+
    ;; uint8 _id1
    1
    ;; uint8 _id2
    1
    ;; string _item1
    4 (length _item1)
    ;; string _item2
    4 (length _item2)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _id1
       (write-byte _id1 s)
     ;; uint8 _id2
       (write-byte _id2 s)
     ;; string _item1
       (write-long (length _item1) s) (princ _item1 s)
     ;; string _item2
       (write-long (length _item2) s) (princ _item2 s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _id1
     (setq _id1 (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _id2
     (setq _id2 (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; string _item1
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _item1 (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _item2
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _item2 (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass dynamixel_sdk_examples::BulkGetItemResponse
  :super ros::object
  :slots (_value1 _value2 ))

(defmethod dynamixel_sdk_examples::BulkGetItemResponse
  (:init
   (&key
    ((:value1 __value1) 0)
    ((:value2 __value2) 0)
    )
   (send-super :init)
   (setq _value1 (round __value1))
   (setq _value2 (round __value2))
   self)
  (:value1
   (&optional __value1)
   (if __value1 (setq _value1 __value1)) _value1)
  (:value2
   (&optional __value2)
   (if __value2 (setq _value2 __value2)) _value2)
  (:serialization-length
   ()
   (+
    ;; int32 _value1
    4
    ;; int32 _value2
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _value1
       (write-long _value1 s)
     ;; int32 _value2
       (write-long _value2 s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _value1
     (setq _value1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _value2
     (setq _value2 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass dynamixel_sdk_examples::BulkGetItem
  :super ros::object
  :slots ())

(setf (get dynamixel_sdk_examples::BulkGetItem :md5sum-) "f0b74b4d53178e0d0ede26a30b687544")
(setf (get dynamixel_sdk_examples::BulkGetItem :datatype-) "dynamixel_sdk_examples/BulkGetItem")
(setf (get dynamixel_sdk_examples::BulkGetItem :request) dynamixel_sdk_examples::BulkGetItemRequest)
(setf (get dynamixel_sdk_examples::BulkGetItem :response) dynamixel_sdk_examples::BulkGetItemResponse)

(defmethod dynamixel_sdk_examples::BulkGetItemRequest
  (:response () (instance dynamixel_sdk_examples::BulkGetItemResponse :init)))

(setf (get dynamixel_sdk_examples::BulkGetItemRequest :md5sum-) "f0b74b4d53178e0d0ede26a30b687544")
(setf (get dynamixel_sdk_examples::BulkGetItemRequest :datatype-) "dynamixel_sdk_examples/BulkGetItemRequest")
(setf (get dynamixel_sdk_examples::BulkGetItemRequest :definition-)
      "uint8 id1
uint8 id2
string item1
string item2
---
int32 value1
int32 value2

")

(setf (get dynamixel_sdk_examples::BulkGetItemResponse :md5sum-) "f0b74b4d53178e0d0ede26a30b687544")
(setf (get dynamixel_sdk_examples::BulkGetItemResponse :datatype-) "dynamixel_sdk_examples/BulkGetItemResponse")
(setf (get dynamixel_sdk_examples::BulkGetItemResponse :definition-)
      "uint8 id1
uint8 id2
string item1
string item2
---
int32 value1
int32 value2

")



(provide :dynamixel_sdk_examples/BulkGetItem "f0b74b4d53178e0d0ede26a30b687544")


