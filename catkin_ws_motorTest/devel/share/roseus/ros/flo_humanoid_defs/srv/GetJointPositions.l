;; Auto-generated. Do not edit!


(when (boundp 'flo_humanoid_defs::GetJointPositions)
  (if (not (find-package "FLO_HUMANOID_DEFS"))
    (make-package "FLO_HUMANOID_DEFS"))
  (shadow 'GetJointPositions (find-package "FLO_HUMANOID_DEFS")))
(unless (find-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONS")
  (make-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONS"))
(unless (find-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONSREQUEST")
  (make-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONSREQUEST"))
(unless (find-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONSRESPONSE")
  (make-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONSRESPONSE"))

(in-package "ROS")





(defclass flo_humanoid_defs::GetJointPositionsRequest
  :super ros::object
  :slots (_id1 _id2 _id3 _id4 _item1 _item2 _item3 _item4 ))

(defmethod flo_humanoid_defs::GetJointPositionsRequest
  (:init
   (&key
    ((:id1 __id1) 0)
    ((:id2 __id2) 0)
    ((:id3 __id3) 0)
    ((:id4 __id4) 0)
    ((:item1 __item1) "")
    ((:item2 __item2) "")
    ((:item3 __item3) "")
    ((:item4 __item4) "")
    )
   (send-super :init)
   (setq _id1 (round __id1))
   (setq _id2 (round __id2))
   (setq _id3 (round __id3))
   (setq _id4 (round __id4))
   (setq _item1 (string __item1))
   (setq _item2 (string __item2))
   (setq _item3 (string __item3))
   (setq _item4 (string __item4))
   self)
  (:id1
   (&optional __id1)
   (if __id1 (setq _id1 __id1)) _id1)
  (:id2
   (&optional __id2)
   (if __id2 (setq _id2 __id2)) _id2)
  (:id3
   (&optional __id3)
   (if __id3 (setq _id3 __id3)) _id3)
  (:id4
   (&optional __id4)
   (if __id4 (setq _id4 __id4)) _id4)
  (:item1
   (&optional __item1)
   (if __item1 (setq _item1 __item1)) _item1)
  (:item2
   (&optional __item2)
   (if __item2 (setq _item2 __item2)) _item2)
  (:item3
   (&optional __item3)
   (if __item3 (setq _item3 __item3)) _item3)
  (:item4
   (&optional __item4)
   (if __item4 (setq _item4 __item4)) _item4)
  (:serialization-length
   ()
   (+
    ;; uint8 _id1
    1
    ;; uint8 _id2
    1
    ;; uint8 _id3
    1
    ;; uint8 _id4
    1
    ;; string _item1
    4 (length _item1)
    ;; string _item2
    4 (length _item2)
    ;; string _item3
    4 (length _item3)
    ;; string _item4
    4 (length _item4)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _id1
       (write-byte _id1 s)
     ;; uint8 _id2
       (write-byte _id2 s)
     ;; uint8 _id3
       (write-byte _id3 s)
     ;; uint8 _id4
       (write-byte _id4 s)
     ;; string _item1
       (write-long (length _item1) s) (princ _item1 s)
     ;; string _item2
       (write-long (length _item2) s) (princ _item2 s)
     ;; string _item3
       (write-long (length _item3) s) (princ _item3 s)
     ;; string _item4
       (write-long (length _item4) s) (princ _item4 s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _id1
     (setq _id1 (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _id2
     (setq _id2 (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _id3
     (setq _id3 (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _id4
     (setq _id4 (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; string _item1
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _item1 (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _item2
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _item2 (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _item3
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _item3 (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _item4
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _item4 (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass flo_humanoid_defs::GetJointPositionsResponse
  :super ros::object
  :slots (_value1 _value2 _value3 _value4 ))

(defmethod flo_humanoid_defs::GetJointPositionsResponse
  (:init
   (&key
    ((:value1 __value1) 0)
    ((:value2 __value2) 0)
    ((:value3 __value3) 0)
    ((:value4 __value4) 0)
    )
   (send-super :init)
   (setq _value1 (round __value1))
   (setq _value2 (round __value2))
   (setq _value3 (round __value3))
   (setq _value4 (round __value4))
   self)
  (:value1
   (&optional __value1)
   (if __value1 (setq _value1 __value1)) _value1)
  (:value2
   (&optional __value2)
   (if __value2 (setq _value2 __value2)) _value2)
  (:value3
   (&optional __value3)
   (if __value3 (setq _value3 __value3)) _value3)
  (:value4
   (&optional __value4)
   (if __value4 (setq _value4 __value4)) _value4)
  (:serialization-length
   ()
   (+
    ;; int32 _value1
    4
    ;; int32 _value2
    4
    ;; int32 _value3
    4
    ;; int32 _value4
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
     ;; int32 _value3
       (write-long _value3 s)
     ;; int32 _value4
       (write-long _value4 s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _value1
     (setq _value1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _value2
     (setq _value2 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _value3
     (setq _value3 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _value4
     (setq _value4 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass flo_humanoid_defs::GetJointPositions
  :super ros::object
  :slots ())

(setf (get flo_humanoid_defs::GetJointPositions :md5sum-) "7b1fb47a48cf84af19e240b1f04307c5")
(setf (get flo_humanoid_defs::GetJointPositions :datatype-) "flo_humanoid_defs/GetJointPositions")
(setf (get flo_humanoid_defs::GetJointPositions :request) flo_humanoid_defs::GetJointPositionsRequest)
(setf (get flo_humanoid_defs::GetJointPositions :response) flo_humanoid_defs::GetJointPositionsResponse)

(defmethod flo_humanoid_defs::GetJointPositionsRequest
  (:response () (instance flo_humanoid_defs::GetJointPositionsResponse :init)))

(setf (get flo_humanoid_defs::GetJointPositionsRequest :md5sum-) "7b1fb47a48cf84af19e240b1f04307c5")
(setf (get flo_humanoid_defs::GetJointPositionsRequest :datatype-) "flo_humanoid_defs/GetJointPositionsRequest")
(setf (get flo_humanoid_defs::GetJointPositionsRequest :definition-)
      "#Service definition to get the position of all the joints of 1 arm in the humanoid robot
#(5 joints in each arm, 2 at the shoulder, 2 at the elbow and 1 at the end effector)
uint8 id1
uint8 id2
uint8 id3
uint8 id4
string item1
string item2
string item3
string item4
---
int32 value1
int32 value2
int32 value3
int32 value4





")

(setf (get flo_humanoid_defs::GetJointPositionsResponse :md5sum-) "7b1fb47a48cf84af19e240b1f04307c5")
(setf (get flo_humanoid_defs::GetJointPositionsResponse :datatype-) "flo_humanoid_defs/GetJointPositionsResponse")
(setf (get flo_humanoid_defs::GetJointPositionsResponse :definition-)
      "#Service definition to get the position of all the joints of 1 arm in the humanoid robot
#(5 joints in each arm, 2 at the shoulder, 2 at the elbow and 1 at the end effector)
uint8 id1
uint8 id2
uint8 id3
uint8 id4
string item1
string item2
string item3
string item4
---
int32 value1
int32 value2
int32 value3
int32 value4





")



(provide :flo_humanoid_defs/GetJointPositions "7b1fb47a48cf84af19e240b1f04307c5")


