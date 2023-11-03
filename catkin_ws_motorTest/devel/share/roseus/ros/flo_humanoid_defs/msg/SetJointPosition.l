;; Auto-generated. Do not edit!


(when (boundp 'flo_humanoid_defs::SetJointPosition)
  (if (not (find-package "FLO_HUMANOID_DEFS"))
    (make-package "FLO_HUMANOID_DEFS"))
  (shadow 'SetJointPosition (find-package "FLO_HUMANOID_DEFS")))
(unless (find-package "FLO_HUMANOID_DEFS::SETJOINTPOSITION")
  (make-package "FLO_HUMANOID_DEFS::SETJOINTPOSITION"))

(in-package "ROS")
;;//! \htmlinclude SetJointPosition.msg.html


(defclass flo_humanoid_defs::SetJointPosition
  :super ros::object
  :slots (_id _position ))

(defmethod flo_humanoid_defs::SetJointPosition
  (:init
   (&key
    ((:id __id) 0)
    ((:position __position) 0)
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _position (round __position))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:position
   (&optional __position)
   (if __position (setq _position __position)) _position)
  (:serialization-length
   ()
   (+
    ;; uint8 _id
    1
    ;; int32 _position
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _id
       (write-byte _id s)
     ;; int32 _position
       (write-long _position s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _id
     (setq _id (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; int32 _position
     (setq _position (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get flo_humanoid_defs::SetJointPosition :md5sum-) "0a775458729eb3272bc88b4f5f764cc8")
(setf (get flo_humanoid_defs::SetJointPosition :datatype-) "flo_humanoid_defs/SetJointPosition")
(setf (get flo_humanoid_defs::SetJointPosition :definition-)
      "#message definition to set the positon of one joint of the humanoid robot
uint8 id
int32 position
")



(provide :flo_humanoid_defs/SetJointPosition "0a775458729eb3272bc88b4f5f764cc8")


