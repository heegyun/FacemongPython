from flask import Flask, render_template, Response
from flask_restful import Api,Resource,reqparse, abort


import cv2
import numpy


app=Flask(__name__)

# VideoCapture () 객체를 만들어 카메라를 트리거하고 
# 비디오의 첫 번째 이미지 / 프레임을 읽는다. 
# 비디오 파일의 경로를 제공하거나 숫자를 사용하여 로컬 웹캠 사용을 지정할 수 있다
# 1. 웹캠을 트리거하기 위해 '0'을 인수로 전달

# camera = cv2.VideoCapture(0)
'''
2. for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
for local webcam use cv2.VideoCapture(0)
'''


# def gen_frames():  
#    
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:

#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


# 3. 로컬 mp4 파일을 읽어 비디오 프레임 추출 및 스트리밍

def gen_frames():  
    cap = cv2.VideoCapture('./movie/dog.mp4')
    while True:
        success, img = cap.read()  # read the mp4 frame
        if not success:
            break
        else:
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            edge = cv2.Canny(gray, 10,200,apertureSize=3)
            vis= img.copy()
            vis = numpy.trunc(vis / 2)
            vis[edge != 0] = (0, 255, 0) # 테두리 감지
            merge = numpy.concatenate((img, vis), axis=1)
            cv2.imwrite('out.png', merge)
            frame = open('out.png', 'rb').read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)