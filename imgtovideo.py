import cv2
import numpy as np
import re
import os
from flask import Flask, render_template, Response
from flask_restful import Api,Resource,reqparse, abort


app=Flask(__name__,static_folder='./ims/2/gan')


def gen_frames():  
    path = "./ims/2/"
    paths = [os.path.join(path , i ) for i in os.listdir(path) if re.search(".jpg$", i )]
    ## 정렬 작업
    store1 = []
    store2 = []
    for i in paths :
        if len(i) == 19 :
            store2.append(i)
        else :
            store1.append(i)

    paths = list(np.sort(store1)) + list(np.sort(store2))

    pathIn= './ims/2/'
    pathOut = './ims/2/gan/gan.mp4'
    fps = 30
    frame_array = []
    for idx , path in enumerate(paths) : 
        if (idx % 2 == 0) | (idx % 5 == 0) :
            continue
        img = cv2.imread(path)
        height, width, layers = img.shape
        size = (width,height)
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()

    cap = cv2.VideoCapture('./ims/2/gan/gan.mp4')
    while True:
        success, img = cap.read()  # read the mp4 frame
        if not success:
            break
        else:
            # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            # edge = cv2.Canny(gray, 10,200,apertureSize=3) # 윤곽선
            # vis= img.copy()
            # vis = np.trunc(vis / 2)
            # vis[edge != 0] = (0, 255, 0) 
            # merge = np.concatenate((img, vis), axis=1)
            # cv2.imwrite('out.png', merge) # 프레임 받아서 저장
            cv2.imwrite('out.png', img) # 프레임 받아서 저장
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
    app.run(host='0.0.0.0',debug=True)
   