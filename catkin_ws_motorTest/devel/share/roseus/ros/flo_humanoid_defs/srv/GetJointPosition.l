;; Auto-generated. Do not edit!


(when (boundp 'flo_humanoid_defs::GetJointPosition)
  (if (not (find-package "FLO_HUMANOID_DEFS"))
    (make-package "FLO_HUMANOID_DEFS"))
  (shadow 'GetJointPosition (find-package "FLO_HUMANOID_DEFS")))
(unless (find-package "FLO_HUMANOID_DEFS::GETJOINTPOSITION")
  (make-package "FLO_HUMANOID_DEFS::GETJOINTPOSITION"))
(unless (find-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONREQUEST")
  (make-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONREQUEST"))
(unless (find-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONRESPONSE")
  (make-package "FLO_HUMANOID_DEFS::GETJOINTPOSITIONRESPONSE"))

(in-package "ROS")





(defclass flo_humanoid_defs::GetJointPositionRequest
  :super ros::object
  :slots (_id ))

(defmethod flo_humanoid_defs::GetJointPositionRequest
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
    ;; int8 _id
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8 _id
       (write-byte _id s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8 _id
     (setq _id (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _id 127) (setq _id (- _id 256)))
   ;;
   self)
  )

(defclass flo_humanoid_defs::GetJointPositionResponse
  :super ros::object
  :slots (_position ))

(defmethod flo_humanoid_defs::GetJointPositionResponse
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

(defclass flo_humanoid_defs::GetJointPosition
  :super ros::object
  :slots ())

(setf (get flo_humanoid_defs::GetJointPosition :md5sum-) "114a36cda781057b95290a137ea72b98")
(setf (get flo_humanoid_defs::GetJointPosition :datatype-) "flo_humanoid_defs/GetJointPosition")
(setf (get flo_humanoid_defs::GetJointPosition :request) flo_humanoid_defs::GetJointPositionRequest)
(setf (get flo_humanoid_defs::GetJointPosition :response) flo_humanoid_defs::GetJointPositionResponse)

(defmethod flo_humanoid_defs::GetJointPositionRequest
  (:response () (instance flo_humanoid_defs::GetJointPositionResponse :init)))

(setf (get flo_humanoid_defs::GetJointPositionRequest :md5sum-) "114a36cda781057b95290a137ea72b98")
(setf (get flo_humanoid_defs::GetJointPositionRequest :datatype-) "flo_humanoid_defs/GetJointPositionRequest")
(setf (get flo_humanoid_defs::GetJointPositionRequest :definition-)
      "#service defintion to get the position of one joint of the robot
int8 id
---
int32 position

")

(setf (get flo_humanoid_defs::GetJointPositionResponse :md5sum-) "114a36cda781057b95290a137ea72b98")
(setf (get flo_humanoid_defs::GetJointPositionResponse :datatype-) "flo_humanoid_defs/GetJointPositionResponse")
(setf (get flo_humanoid_defs::GetJointPositionResponse :definition-)
      "#service defintion to get the position of one joint of the robot
int8 id
---
int32 position

")



(provide :flo_humanoid_defs/GetJointPosition "114a36cda781057b95290a137ea72b98")


