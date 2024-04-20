import cv2
import ffmpeg
import subprocess

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

# program entry
if __name__ == '__main__':
    dectector = FaceDetector(module_file)
    pusher = StreamPusher(rtmp_server)
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    while True:
        # 读取一帧
        ret, frame = cap.read()
        # 将图片转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测人脸
        faces = dectector.detectFace(gray)
        # 在检测到的每张人脸周围画一个矩形
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        # 显示帧
#        cv2.imshow('frame',frame)
#         如果按下Esc键，退出循环
#        if cv2.waitKey(1) & 0xFF == 27:
#            print("Press Esc, to exit.")
#            break
        pusher.streamPush(frame)
    # 释放摄像头
    cap.release()
    # 关闭所有窗口
    cv2.destroyAllWindows()