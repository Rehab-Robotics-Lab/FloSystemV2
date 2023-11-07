
(cl:in-package :asdf)

(defsystem "dynamixel_sdk_examples-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "BulkGetItem" :depends-on ("_package_BulkGetItem"))
    (:file "_package_BulkGetItem" :depends-on ("_package"))
    (:file "GetPosition" :depends-on ("_package_GetPosition"))
    (:file "_package_GetPosition" :depends-on ("_package"))
    (:file "SyncGetPosition" :depends-on ("_package_SyncGetPosition"))
    (:file "_package_SyncGetPosition" :depends-on ("_package"))
  ))