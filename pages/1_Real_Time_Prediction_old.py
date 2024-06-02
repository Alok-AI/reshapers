import streamlit as st 
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time


st.subheader('Real-Time Prediction Attendance System')


# Retrive the data from Redis Database
with st.spinner('Retriving Data from Redis DB ...'):    
    redis_face_db = face_rec.retrive_data2(name='contact1:register')
    st.dataframe(redis_face_db)
    
st.success("Data sucessfully retrived from Redis")

# time 
waitTime = 30 # time in sec
setTime = time.time()
realtimepred = face_rec.RealTimePred() # real time prediction class

# Real Time Prediction
# streamlit webrtc
# callback function
def video_frame_callback(frame):
    global setTime
    
    img = frame.to_ndarray(format="bgr24") # 3 dimension numpy array
    # operation that you can perform on the array
    pred_img = realtimepred.face_prediction(img,redis_face_db,
                                        'facial_features',['Name','Role'],thresh=0.5)
    rtsp_url = "rtsp://admin:ab@123456@122.160.10.254:554/Streaming/Channels/101"
    realtimepred = face_rec.RealTimePred(rtsp_url)
    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time() # reset time        
        print('Save Data to redis database')
    

    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback,
    rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        }
    )