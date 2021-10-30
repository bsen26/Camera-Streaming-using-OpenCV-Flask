from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # Local Webcam

# Generating the frames for Streaming
def gen_frames():
    while True:
        success, frame = camera.read()  # Reading the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Webcam Streaming"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
