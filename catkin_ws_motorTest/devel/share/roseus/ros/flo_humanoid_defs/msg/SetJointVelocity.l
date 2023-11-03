;; Auto-generated. Do not edit!


(when (boundp 'flo_humanoid_defs::SetJointVelocity)
  (if (not (find-package "FLO_HUMANOID_DEFS"))
    (make-package "FLO_HUMANOID_DEFS"))
  (shadow 'SetJointVelocity (find-package "FLO_HUMANOID_DEFS")))
(unless (find-package "FLO_HUMANOID_DEFS::SETJOINTVELOCITY")
  (make-package "FLO_HUMANOID_DEFS::SETJOINTVELOCITY"))

(in-package "ROS")
;;//! \htmlinclude SetJointVelocity.msg.html


(defclass flo_humanoid_defs::SetJointVelocity
  :super ros::object
  :slots (_id _endposition _velocity ))

(defmethod flo_humanoid_defs::SetJointVelocity
  (:init
   (&key
    ((:id __id) 0)
    ((:endposition __endposition) 0)
    ((:velocity __velocity) 0)
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _endposition (round __endposition))
   (setq _velocity (round __velocity))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:endposition
   (&optional __endposition)
   (if __endposition (setq _endposition __endposition)) _endposition)
  (:velocity
   (&optional __velocity)
   (if __velocity (setq _velocity __velocity)) _velocity)
  (:serialization-length
   ()
   (+
    ;; uint8 _id
    1
    ;; int32 _endposition
    4
    ;; int32 _velocity
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _id
       (write-byte _id s)
     ;; int32 _endposition
       (write-long _endposition s)
     ;; int32 _velocity
       (write-long _velocity s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _id
     (setq _id (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; int32 _endposition
     (setq _endposition (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _velocity
     (setq _velocity (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get flo_humanoid_defs::SetJointVelocity :md5sum-) "849c7d5675e0a15566e7a31f1fcf93be")
(setf (get flo_humanoid_defs::SetJointVelocity :datatype-) "flo_humanoid_defs/SetJointVelocity")
(setf (get flo_humanoid_defs::SetJointVelocity :definition-)
      "#Message definition to set the velocity of the end effector
uint8 id
int32 endposition
int32 velocity
")



(provide :flo_humanoid_defs/SetJointVelocity "849c7d5675e0a15566e7a31f1fcf93be")


