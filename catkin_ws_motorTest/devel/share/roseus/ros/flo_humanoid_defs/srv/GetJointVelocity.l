;; Auto-generated. Do not edit!


(when (boundp 'flo_humanoid_defs::GetJointVelocity)
  (if (not (find-package "FLO_HUMANOID_DEFS"))
    (make-package "FLO_HUMANOID_DEFS"))
  (shadow 'GetJointVelocity (find-package "FLO_HUMANOID_DEFS")))
(unless (find-package "FLO_HUMANOID_DEFS::GETJOINTVELOCITY")
  (make-package "FLO_HUMANOID_DEFS::GETJOINTVELOCITY"))
(unless (find-package "FLO_HUMANOID_DEFS::GETJOINTVELOCITYREQUEST")
  (make-package "FLO_HUMANOID_DEFS::GETJOINTVELOCITYREQUEST"))
(unless (find-package "FLO_HUMANOID_DEFS::GETJOINTVELOCITYRESPONSE")
  (make-package "FLO_HUMANOID_DEFS::GETJOINTVELOCITYRESPONSE"))

(in-package "ROS")





(defclass flo_humanoid_defs::GetJointVelocityRequest
  :super ros::object
  :slots (_id ))

(defmethod flo_humanoid_defs::GetJointVelocityRequest
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

(defclass flo_humanoid_defs::GetJointVelocityResponse
  :super ros::object
  :slots (_velocity ))

(defmethod flo_humanoid_defs::GetJointVelocityResponse
  (:init
   (&key
    ((:velocity __velocity) 0)
    )
   (send-super :init)
   (setq _velocity (round __velocity))
   self)
  (:velocity
   (&optional __velocity)
   (if __velocity (setq _velocity __velocity)) _velocity)
  (:serialization-length
   ()
   (+
    ;; int32 _velocity
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _velocity
       (write-long _velocity s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _velocity
     (setq _velocity (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass flo_humanoid_defs::GetJointVelocity
  :super ros::object
  :slots ())

(setf (get flo_humanoid_defs::GetJointVelocity :md5sum-) "810f3b5a74591cab058ea94decd15832")
(setf (get flo_humanoid_defs::GetJointVelocity :datatype-) "flo_humanoid_defs/GetJointVelocity")
(setf (get flo_humanoid_defs::GetJointVelocity :request) flo_humanoid_defs::GetJointVelocityRequest)
(setf (get flo_humanoid_defs::GetJointVelocity :response) flo_humanoid_defs::GetJointVelocityResponse)

(defmethod flo_humanoid_defs::GetJointVelocityRequest
  (:response () (instance flo_humanoid_defs::GetJointVelocityResponse :init)))

(setf (get flo_humanoid_defs::GetJointVelocityRequest :md5sum-) "810f3b5a74591cab058ea94decd15832")
(setf (get flo_humanoid_defs::GetJointVelocityRequest :datatype-) "flo_humanoid_defs/GetJointVelocityRequest")
(setf (get flo_humanoid_defs::GetJointVelocityRequest :definition-)
      "#service defintion to get the velocity of one joint of the robot
int8 id
---
int32 velocity

")

(setf (get flo_humanoid_defs::GetJointVelocityResponse :md5sum-) "810f3b5a74591cab058ea94decd15832")
(setf (get flo_humanoid_defs::GetJointVelocityResponse :datatype-) "flo_humanoid_defs/GetJointVelocityResponse")
(setf (get flo_humanoid_defs::GetJointVelocityResponse :definition-)
      "#service defintion to get the velocity of one joint of the robot
int8 id
---
int32 velocity

")



(provide :flo_humanoid_defs/GetJointVelocity "810f3b5a74591cab058ea94decd15832")


