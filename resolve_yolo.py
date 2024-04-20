import cv2
import ffmpeg
import subprocess
import numpy as np
from ultralytics import YOLO

# 人脸检测器
class FaceDetector:
    def __init__(self, module_file):
        self.module_file = module_file
        self.face_cascade = cv2.CascadeClassifier(self.module_file)

    def detectFace(self, gray_img):
        face_rect = self.face_cascade.detectMultiScale(gray_img, 1.3, 5)
        return face_rect
# 推流器
class StreamPusher:
    def __init__(self, rtmp_url):
        # 创建FFmpeg命令行参数
        ffmpeg_cmd = ['ffmpeg',
                      '-y',  # 覆盖已存在的文件
                      '-f', 'rawvideo',
                      '-pixel_format', 'bgr24',
                      '-video_size', '640x480',
                      '-i', '-',  # 从标准输入读取数据
                      '-c:v', 'libx264',
                      '-preset', 'ultrafast',
                      '-tune', 'zerolatency',
                      '-pix_fmt', 'yuv420p',
                      '-f', 'rtsp',
                      rtmp_url]
                      
        print('ffmpeg_cmd:', ffmpeg_cmd)
        # 启动 ffmpeg
        self.ffmepg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    def streamPush(self, frame):
        self.ffmepg_process.stdin.write(frame.tobytes())

# 人脸检测器模型文件路径
module_file = 'D:/programs/anaconda/pkgs/libopencv-4.0.1-hbb9e17c_0/Library/etc/haarcascades/haarcascade_frontalface_default.xml'
rtmp_server = 'rtsp://127.0.0.1:9554/live/test'

class Worker():
    def __init__(self):
        self.streamable = True
        self.model = YOLO('flaskr/yolov8n.pt')
        
    def main_worker(self, control_code='', model_path='', source=0, module_file='yolov8n', polygon=[0.0443,0.1005,0.2815,0.1005,0.2815,0.2998,0.0443,0.2998]):
        if module_file == 'yolov8n':
            self.model = YOLO('flaskr/yolov8n.pt')
        elif module_file == 'yolov8m':
            self.model = YOLO('flaskr/yolov8m.pt')
        dectector = FaceDetector(module_file)
        pusher = StreamPusher(rtmp_server)
        # 打开摄像头
        cap = cv2.VideoCapture(0)
        while self.streamable:
            # 读取一帧
            ret, frame = cap.read()
            results = self.model(frame)
            current_result = results[0]
            for i in range(len(polygon)):
                if i%2 == 0:
                    polygon[i] = int(polygon[i]*frame.shape[1])
                else:
                    polygon[i] = int(polygon[i]*frame.shape[0])
            cv2.polylines(img, polygon, isClosed=True, color=(255, 255, 0), thickness=1)
            for box in current_result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            pusher.streamPush(frame)
        # 释放摄像头
        cap.release()
        
    def stop_stream(self):
        self.streamable = False

# program entry
if __name__ == '__main__':
    polygon=[0.0443,0.1005,0.2815,0.1005,0.2815,0.2998,0.0443,0.2998]
    for i in range(len(polygon)):
        if i%2 == 0:
            polygon[i] = int(polygon[i]*640)
        else:
            polygon[i] = int(polygon[i]*480)
    pts = np.array([[polygon[0], polygon[1]], [polygon[2], polygon[3]], 
                [polygon[4], polygon[5]], [polygon[6], polygon[7]]], np.int32)
    pts = pts.reshape((-1, 1, 2))
        
    model = YOLO('yolov8n.pt')  # load an official model
    dectector = FaceDetector(module_file)
    pusher = StreamPusher(rtmp_server)
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    while True:
        # 读取一帧
        ret, frame = cap.read()
        results = model(frame)
        current_result = results[0]
        
        cv2.polylines(frame, [pts], isClosed=True, color=(255, 255, 0), thickness=2)
        
        for box in current_result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.imshow('frame',frame)
#         如果按下Esc键，退出循环
        if cv2.waitKey(1) & 0xFF == 27:
            print("Press Esc, to exit.")
            break
#        pusher.streamPush(frame)
    # 释放摄像头
    cap.release()
    # 关闭所有窗口
    cv2.destroyAllWindows()