
(cl:in-package :asdf)

(defsystem "dynamixel_sdk_examples-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "BulkSetItem" :depends-on ("_package_BulkSetItem"))
    (:file "_package_BulkSetItem" :depends-on ("_package"))
    (:file "SetPosition" :depends-on ("_package_SetPosition"))
    (:file "_package_SetPosition" :depends-on ("_package"))
    (:file "SyncSetPosition" :depends-on ("_package_SyncSetPosition"))
    (:file "_package_SyncSetPosition" :depends-on ("_package"))
  ))