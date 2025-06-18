import cv2
import time

def test_camera(camera_index):
    print(f"测试摄像头 {camera_index}...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"摄像头 {camera_index} 无法打开")
        return False
    
    ret, frame = cap.read()
    if ret:
        print(f"摄像头 {camera_index} 成功打开并读取图像")
        # 显示摄像头图像
        cv2.imshow(f'Camera {camera_index}', frame)
        cv2.waitKey(2000)  # 显示2秒
        cv2.destroyAllWindows()
    else:
        print(f"摄像头 {camera_index} 打开但无法读取图像")
    
    cap.release()
    return ret

# # 测试摄像头 0
# test_camera(0)
# time.sleep(1)  # 等待1秒

# # 测试摄像头 1
# test_camera(1)