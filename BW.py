import time
from flask import Flask, render_template
from flask_socketio import SocketIO
import speedtest

app = Flask(_name_)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('usage.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def get_bandwidth_data():
    st = speedtest.Speedtest()
    
    while True:
        upload_speed = st.upload()
        download_speed = st.download()

        print(f'Upload Speed: {upload_speed} bits/s, Download Speed: {download_speed} bits/s')

        
        socketio.emit('bandwidth_data', {'upload_speed': upload_speed, 'download_speed': download_speed}, namespace='/')

        time.sleep(1)  #sleeep for a sec.

if _name_ == '_main_':
    import threading
    threading.Thread(target=get_bandwidth_data).start()

    socketio.run(app, debug=True)