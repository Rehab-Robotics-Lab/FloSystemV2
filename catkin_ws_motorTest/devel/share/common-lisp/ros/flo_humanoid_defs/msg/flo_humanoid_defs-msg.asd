
(cl:in-package :asdf)

(defsystem "flo_humanoid_defs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "SetJointPosition" :depends-on ("_package_SetJointPosition"))
    (:file "_package_SetJointPosition" :depends-on ("_package"))
    (:file "SetJointPositions" :depends-on ("_package_SetJointPositions"))
    (:file "_package_SetJointPositions" :depends-on ("_package"))
    (:file "SetJointVelocity" :depends-on ("_package_SetJointVelocity"))
    (:file "_package_SetJointVelocity" :depends-on ("_package"))
  ))