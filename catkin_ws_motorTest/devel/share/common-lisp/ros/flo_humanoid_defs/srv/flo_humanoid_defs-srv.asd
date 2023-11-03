
(cl:in-package :asdf)

(defsystem "flo_humanoid_defs-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "GetJointPosition" :depends-on ("_package_GetJointPosition"))
    (:file "_package_GetJointPosition" :depends-on ("_package"))
    (:file "GetJointPositions" :depends-on ("_package_GetJointPositions"))
    (:file "_package_GetJointPositions" :depends-on ("_package"))
    (:file "GetJointVelocity" :depends-on ("_package_GetJointVelocity"))
    (:file "_package_GetJointVelocity" :depends-on ("_package"))
  ))