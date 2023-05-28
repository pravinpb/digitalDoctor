import streamlit as st
from PIL import Image
import cv2
import mediapipe as mp
import pyttsx3
import math
import os
import statistics
from st_clickable_images import clickable_images
import pandas as pd

st.set_page_config(page_title="psychotherapy_doctor",page_icon="🏥")

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


import sqlite3
conn = sqlite3.connect('psychotherapy_doctor_database.db',check_same_thread=False)
c = conn.cursor()

def create_table(db_table_name):
    	c.execute('CREATE TABLE IF NOT EXISTS ' + db_table_name + '(pose_name TEXT,hands_distance INT,right_hand_angle2_ellow INT,left_hand_angle1_ellow INT,right_hand_angle4_shoulder INT,left_hand_angle3_shoulder INT,right_hip INT,left_hip INT,right_knee INT,left_knee INT)')

def add_data(db_table_name,pose_name,hands_distance,right_hand_angle2_ellow,left_hand_angle1_ellow,right_hand_angle4_shoulder,left_hand_angle3_shoulder,right_hip,left_hip,right_knee,left_knee):
	c.execute('INSERT INTO '+db_table_name+'(pose_name,hands_distance,right_hand_angle2_ellow,left_hand_angle1_ellow,right_hand_angle4_shoulder,left_hand_angle3_shoulder,right_hip,left_hip,right_knee,left_knee) VALUES (?,?,?,?,?,?,?,?,?,?)',(pose_name,hands_distance,right_hand_angle2_ellow,left_hand_angle1_ellow,right_hand_angle4_shoulder,left_hand_angle3_shoulder,right_hip,left_hip,right_knee,left_knee))
	conn.commit()
 
def Drop_table(db_table_name):
    	c.execute("DROP TABLE "+db_table_name)


def view_all_data(db_table_name):
    c.execute('SELECT * FROM '+db_table_name)
    data = c.fetchall()
    return data


# def get_task(db_table_name,task):
#     c.execute('SELECT * FROM '+db_table_name+ ' WHERE test="{}"'.format(task))
#     data = c.fetchall()
#     return data

# def delete_data(db_table_name,task):
#     c.execute('DELETE FROM '+db_table_name+' WHERE test="{}"'.format(task))
#     conn.commit()
    

st.title("welcome !!!")

def calculate_angle(landmark1,landmark2,landmark3):
    
            global angle
            x1,y1 = landmark1
            x2,y2 = landmark2
            x3,y3 = landmark3
            angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
            if angle < 0 :
                angle *= -1
            if angle > 180:
                angle = 360 - angle
            # cv2.circle(frame,(round(x1*width_frame),round(y1*height_frame)),radius=20,color=(180,20,40),thickness=3)
            return round(angle)
 
 
c1,c2,c3 = st.columns([1,1,1])

with c1: st.subheader("Right elbow pain 💪")
with c2: st.subheader("Surya Namascaram 🧘")
with c3: st.subheader("Train your own model 🚶‍♂️")

clicked = clickable_images(
    [
        "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTguJbDxnaMEYCtktAWyGQ2tFpfkg-HfHWU4F0lsrTRFFnPKx85",
        "https://img.freepik.com/premium-vector/yoga-surya-namaskar-sequence-sun-salutating-woman-morning-yoga-flow-with-all-steps_499431-1098.jpg?w=2000",
        "https://static.vecteezy.com/system/resources/previews/001/915/369/original/people-doing-stretching-and-strength-exercise-free-vector.jpg",

        ],
    titles=[f"Image #{str(i)}" for i in range(5)],
    
    div_style={"display": "flex","flex": "33.33%","padding": "5px"},
    img_style={"margin": "5px", "max-width":"30%","height":"200px","width": "50%"},
)


select_condition = str(clicked)

# --------------------------------------- Right hand ellow pain --------------------------------------------------------------#

if select_condition == "0":
    
    # st.image(Image.open(r"C:\Users\USER\OneDrive - Kumaraguru College of Technology\Documents\2346200.jpeg"),use_column_width=True)
    col1,col2 = st.columns(2)
    with col1:
        execises = st.radio("Select the step",["Exercise 1","Exercise 2"],horizontal=True)
    with col2:
        no_of_step = st.number_input("No of step",min_value=1,max_value=100)
        
    start_button = st.button("START",use_container_width=True)
    
    
    c1_right,c2_right = st.columns(2)
   
    if start_button == True:

            with c1_right: st.image(Image.open(r"C:\Users\USER\OneDrive - Kumaraguru College of Technology\Documents\2346200.jpeg"),use_column_width=True)
            with c2_right:image_show =  st.image([],use_column_width=True)
        
            mp_draw = mp.solutions.drawing_utils
            mp_styles = mp.solutions.drawing_styles
            my_pose = mp.solutions.pose
            pose = my_pose.Pose()
            video = cv2.VideoCapture(0)
        
            count = 0
            correct = False

            if start_button:
                STOP = st.button("STOP")
                while True:
                    
                    ret,frame = video.read()
                    height_frame , width_frame,_ = frame.shape
                    frame = cv2.flip(frame,1)
                
                    results = pose.process(frame)
            
                    if results.pose_landmarks:
                        
                        mp_draw.draw_landmarks(frame,results.pose_landmarks,my_pose.POSE_CONNECTIONS,
                                            landmark_drawing_spec=mp_draw.DrawingSpec(color=(255,255,255),thickness=4, circle_radius=4),
                                            connection_drawing_spec=mp_draw.DrawingSpec(color=(49,125,237) ,thickness=3, circle_radius=3))
                        body_landmarks = results.pose_landmarks.landmark
                        
                        left_hand_angle1_ellow = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].y])
                    
                        right_hand_angle2_ellow = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].y])
                        
                        left_hand_angle3_shoulder = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y])
                                                    
                        right_hand_angle4_shoulder = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                                            [body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                            [body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y])

                        if execises == "Exercise 1":
                        
                        
                            cv2.line(frame,pt1=(round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y*height_frame)),pt2=(round(body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y *height_frame)),color=(255,0,0),thickness=10)
                            cv2.line(frame,pt1=(round(body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y *height_frame)),pt2=(round(body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].y*height_frame)),color=(255,0,0),thickness=10)
                            cv2.line(frame,pt1=(round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y*height_frame)),pt2=(round(body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].y*height_frame)),color=(0,140,0),thickness=10)                            
                            
                            
                            if not correct:
                                if right_hand_angle2_ellow in [ i for i in range(20,50)] and  right_hand_angle4_shoulder in [ i for i in range(26,90)] :
                                    count += 1
                                    correct = True 
                            if correct:
                                if right_hand_angle2_ellow not in [ i for i in range(20,50)] or right_hand_angle4_shoulder not  in [ i for i in range(26,90)]:
                                    correct = False
                                        
                            if count == no_of_step :
                                st.success("You have successfully completed the execise for right hand ")
                                break
                                
                        if execises == "Exercise 2":
                            if not correct:
                                if right_hand_angle2_ellow in [ i for i in range(160,190)] and  right_hand_angle4_shoulder in [ i for i in range(160,190)] :
                                    count += 1
                                    correct = True 
                            if correct:
                                if right_hand_angle2_ellow not in [ i for i in range(160,190)] or right_hand_angle4_shoulder not  in [ i for i in range(160,190)]:
                                    correct = False
                                        
                            if count == no_of_step :
                                st.success("You have successfully completed the execise for right hand ")
                                break
                        
                        
                        cv2.putText(frame,"count :" + str(count),(100,450),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3,cv2.LINE_AA)
                    
                    image_show.image(frame,channels="RBG")
                    if cv2.waitKey(1) == 81 or STOP == True :
                        break
                video.release()
                cv2.destroyAllWindows()
    
#-------------------------------------------------yogo code------------------------------------------------------------------#            


if select_condition == "1":


    mp_draw = mp.solutions.drawing_utils
    mp_styles = mp.solutions.drawing_styles
    my_pose = mp.solutions.pose
    pose = my_pose.Pose()
    step_name = ""

    step1_count = 0
    step2_count = 0
    step3_count = 0
    step4_count = 0
    step5_count = 0
    step6_count = 0
    step7_count = 0
    step8_count = 0
    step9_count = 0
    step10_count = 0
    step11_count = 0
    step12_count = 0

    video = cv2.VideoCapture(0)


    #  for image input

    image_list_step = ["D:\DigitalDoctor\images\yoga\step1.jpg","D:\DigitalDoctor\images\yoga\step2.jpg","D:\DigitalDoctor\images\yoga\step3.jpg",
                    "D:\DigitalDoctor\images\yoga\step4.jpg","D:\DigitalDoctor\images\yoga\step5.jpgg","D:\DigitalDoctor\images\yoga\step6.jpg",
                    "D:\DigitalDoctor\images\yoga\step7.jpg","D:\DigitalDoctor\images\yoga\step8.jpg","D:\DigitalDoctor\images\yoga\step4.jpg",
                    "D:\DigitalDoctor\images\yoga\step3.jpg","D:\DigitalDoctor\images\yoga\step2.jpg","D:\DigitalDoctor\images\yoga\step1.jpg"]
    step_number = 0
    image_check = cv2.imread(r"D:\DigitalDoctor\images\yoga\step1.jpg")
    image_check =cv2.resize(image_check,(749, 720))
    results_image = pose.process(image_check)

    if results_image.pose_landmarks: 
        mp_draw.draw_landmarks(image_check,results_image.pose_landmarks,my_pose.POSE_CONNECTIONS,
                            landmark_drawing_spec=mp_draw.DrawingSpec(color=(255,255,255),thickness=3, circle_radius=3),
                            connection_drawing_spec=mp_draw.DrawingSpec(color=(49,125,237) ,thickness=2, circle_radius=2))

        
    body_landmarks_image = results_image.pose_landmarks.landmark

    def calculate_angle_image(landmark1_ima,landmark2_ima,landmark3_ima):
        global angle_image
        a1,b1 = landmark1_ima
        a2,b2 = landmark2_ima
        a3,b3 = landmark3_ima
        angle_image = math.degrees(math.atan2(b3-b2,a3-a2)-math.atan2(b1-b2,a1-a2))
        if angle_image < 0 :
            angle_image *= -1
        return round(angle_image)

        
    left_hand_angle_image = calculate_angle_image([body_landmarks_image[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                            [body_landmarks_image[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                            [body_landmarks_image[my_pose.PoseLandmark.RIGHT_WRIST.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_WRIST.value].y])
            
    right_hand_angle_imaga = calculate_angle_image([body_landmarks_image[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                    [body_landmarks_image[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                                    [body_landmarks_image[my_pose.PoseLandmark.LEFT_WRIST.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_WRIST.value].y])

    left_hand_angle3_shoulder_image = calculate_angle_image([body_landmarks_image[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                            [body_landmarks_image[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                            [body_landmarks_image[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_HIP.value].y])
                                            
            
    right_hand_angle4_shoulder_image = calculate_angle_image([body_landmarks_image[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                                [body_landmarks_image[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                [body_landmarks_image[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_HIP.value].y])

    left_hip_image = calculate_angle_image([body_landmarks_image[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                        [body_landmarks_image[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_HIP.value].y],
                                        [body_landmarks_image[my_pose.PoseLandmark.RIGHT_KNEE.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_KNEE.value].y])
            
    right_hip_image = calculate_angle_image([body_landmarks_image[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                [body_landmarks_image[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_HIP.value].y],
                                [body_landmarks_image[my_pose.PoseLandmark.LEFT_KNEE.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_KNEE.value].y])

    left_knee_image = calculate_angle_image([body_landmarks_image[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_HIP.value].y],
                                        [body_landmarks_image[my_pose.PoseLandmark.RIGHT_KNEE.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_KNEE.value].y],
                                        [body_landmarks_image[my_pose.PoseLandmark.RIGHT_ANKLE.value].x,body_landmarks_image[my_pose.PoseLandmark.RIGHT_ANKLE.value].y])
            
    right_knee_image = calculate_angle_image([body_landmarks_image[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_HIP.value].y],
                                        [body_landmarks_image[my_pose.PoseLandmark.LEFT_KNEE.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_KNEE.value].y],
                                        [body_landmarks_image[my_pose.PoseLandmark.LEFT_ANKLE.value].x,body_landmarks_image[my_pose.PoseLandmark.LEFT_ANKLE.value].y])

    y1,y2 = st.columns(2)
    with y1:demo_image_yoga = st.image([])
    with y2:live_image_yoga = st.image([])
    
    live_yoga_stop_button = st.button("STOP!!!")
    
    # cv2.imshow("image1",image_check)
    demo_image_yoga.image(image_check)
    
    def calculate_angle(landmark1,landmark2,landmark3):
                global angle
                x1,y1 = landmark1
                x2,y2 = landmark2
                x3,y3 = landmark3
                angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
                if angle < 0 :
                    angle *= -1
                if angle > 180:
                    angle = 360 - angle
                    
                # cv2.circle(frame,(round(x1*width_frame),round(y1*height_frame)),radius=20,color=(180,20,40),thickness=3)
                return round(angle)
            
    while True:
        
        image_check = cv2.imread(image_list_step[step_number])
        image_check =cv2.resize(image_check,(749, 720))
        
        # cv2.imshow("image1",image_check) 
        demo_image_yoga.image(image_check)
        

    # for video input

        cap,frame = video.read()
        frame=cv2.resize(frame,(749, 720))
        frame = cv2.flip(frame,1)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        height_frame , width_frame,_ = frame.shape
        results = pose.process(frame)
        
        if results.pose_landmarks:
            
            mp_draw.draw_landmarks(frame,results.pose_landmarks,my_pose.POSE_CONNECTIONS,
                                landmark_drawing_spec=mp_draw.DrawingSpec(color=(255,255,255),thickness=3, circle_radius=3),
                                connection_drawing_spec=mp_draw.DrawingSpec(color=(49,125,237) ,thickness=2, circle_radius=2))
            body_landmarks = results.pose_landmarks.landmark
            
            # for step 1 vanakkam angles
            
            left_hand_angle1_ellow = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                            [body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                            [body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].y])
            
            right_hand_angle2_ellow = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                            [body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                            [body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].y])
            
            left_hand_angle3_shoulder = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                            [body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                            [body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y])
                                            
            
            right_hand_angle4_shoulder = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y])
            
            right_pinky_cordi =  round(body_landmarks[my_pose.PoseLandmark.LEFT_PINKY.value].x*width_frame)
            left_pinky_cordi =  round(body_landmarks[my_pose.PoseLandmark.RIGHT_PINKY.value].x*width_frame)
            
            
            # for step 2 angles
            
            left_hip = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                        [body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y],
                                        [body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].y])
            
            right_hip = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                        [body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y],
                                        [body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].y])
            
            # for step 3 angles
            
            left_knee = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y],
                                        [body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].y],
                                        [body_landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].y])
            
            right_knee = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y],
                                        [body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].y],
                                        [body_landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].y])
            
            
            # condition checking for first step 
            
            if ( step_name == "" and (right_pinky_cordi-left_pinky_cordi) in [ i for i in range(-10,10)]  and  round(left_hand_angle1_ellow) in [ i for i in range(30,60)] and round(right_hand_angle2_ellow) in [ i for i in range(30,60)] and round(left_hand_angle3_shoulder) < 30 and round(right_hand_angle4_shoulder) < 30) : 
                # ((right_pinky_cordi-left_pinky_cordi) in [ i for i in range(-10,10)]  and round(left_hand_angle1_ellow) in [ i for i in range(30,60)] and round(left_hand_angle3_shoulder) < 30 and round(right_hand_angle4_shoulder) < 30)  or 
                # ((right_pinky_cordi-left_pinky_cordi) in [ i for i in range(-10,10)]  and round(right_hand_angle2_ellow) in [ i for i in range(30,60)] and round(right_hand_angle4_shoulder) < 30 and round(left_hand_angle3_shoulder) < 30)):
            
                
                step_name = "perfectly matched first step"
                step_number = 1
                step1_count += 1
                cv2.putText(frame,str(step1_count),(30,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                
                if step1_count > 40:
                
                    engine = pyttsx3.init()
                    engine.say("perfectly matched first step")
                    engine.runAndWait()
                    
                    cv2.putText(frame,step_name,(30,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
        
        
                
            
            # condition checking for second step

            if step_name == "perfectly matched first step" and (round(right_hip) in [i for i in range(140,170)] and round(left_hip) in [i for i in range(140,170)] and 
                round(right_hand_angle4_shoulder) in [i for i in range(140,170)] and round(left_hand_angle3_shoulder) in [i for i in range(140,170)] and 
                round(right_hand_angle2_ellow) in [i for i in range(140,170)] and round(left_hand_angle1_ellow) in [i for i in range(140,170)]):
                
                
                step_number = 2
                step_name = "perfectly matched second step"
                
                step2_count += 1
                if step2_count > 20:
                    engine = pyttsx3.init()
                    engine.say("perfectly matched second step")
                    engine.runAndWait()
                    
                    cv2.putText(frame,step_name,(50,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
            
            # condition checking for third step
            
            if  step_name == "perfectly matched second step" and  (round(right_hip) in [i for i in range(60,90)] and round(left_hip) in [i for i in range(60,90)] and 
                round(right_hand_angle2_ellow) in [i for i in range(150,180)] and round(left_hand_angle1_ellow) in [i for i in range(150,180)] and
                round(right_hand_angle4_shoulder) in [i for i in range(50,90)] and round(left_hand_angle3_shoulder) in [i for i in range(50,90)] and 
                round(right_knee) in [i for i in range(170,180)] and round(left_knee) in [i for i in range(170,180)]):
                
                step_number = 3
                step_name = "perfectly matched third step"
                step3_count += 1
                if step3_count > 40:
                    
                
                    engine = pyttsx3.init()
                    engine.say("perfectly matched third step")
                    engine.runAndWait()
                
                    cv2.putText(frame,step_name,(50,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                
            # condition checking for fourth step
            
            if step_name == "perfectly matched third step" and ((round(right_hip) in [i for i in range(20,60)] and round(left_hip) in [i for i in range(160,180)] and 
                round(right_hand_angle2_ellow) in [i for i in range(170,180)] and round(left_hand_angle1_ellow) in [i for i in range(170,180)] and
                round(right_hand_angle4_shoulder) in [i for i in range(20,45)] and round(left_hand_angle3_shoulder) in [i for i in range(25,50)] and 
                round(right_knee) in [i for i in range(60,90)] and round(left_knee) in [i for i in range(115,135)]) or 
                
                (round(right_hip) in [i for i in range(160,180)] and round(left_hip) in [i for i in range(20,60)] and 
                round(right_hand_angle2_ellow) in [i for i in range(170,180)] and round(left_hand_angle1_ellow) in [i for i in range(170,180)] and
                round(right_hand_angle4_shoulder) in [i for i in range(25,50)] and round(left_hand_angle3_shoulder) in [i for i in range(20,45)] and 
                round(right_knee) in [i for i in range(115,135)] and round(left_knee) in [i for i in range(60,90)])):
                
                step_number = 4
                step_name = "perfectly matched fourth step"
                step4_count += 1
                if step4_count > 30:
                    cv2.putText(frame,step_name,(50,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                
                    engine = pyttsx3.init()
                    engine.say("perfectly matched fourth step")
                    engine.runAndWait()
                
            # condition checking for fifth step  
            
            if step_name == "perfectly matched fourth step" and (round(right_hip) in [i for i in range(160,180)] and round(left_hip) in [i for i in range(160,180)] and 
                round(right_hand_angle2_ellow) in [i for i in range(150,180)] and round(left_hand_angle1_ellow) in [i for i in range(150,180)] and
                round(right_hand_angle4_shoulder) in [i for i in range(50,90)] and round(left_hand_angle3_shoulder) in [i for i in range(45,85)] and 
                round(right_knee) in [i for i in range(160,180)] and round(left_knee) in [i for i in range(160,180)]):
                
                step_name = "perfectly matched fifth step"
                step_number = 5
                step5_count += 1
                if step5_count > 40:
                    cv2.putText(frame,step_name,(30,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                
                    engine = pyttsx3.init()
                    engine.say("perfectly matched fourth step")
                    engine.runAndWait()
            
            # condition checking for sixth step
            
            if step_name == "perfectly matched fifth step" and ((round(right_hip) in [i for i in range(90,120)] and round(left_hip) in [i for i in range(90,120)] and 
                round(right_hand_angle2_ellow) in [i for i in range(10,40)] and round(left_hand_angle1_ellow) in [i for i in range(10,40)] and
                round(right_hand_angle4_shoulder) in [i for i in range(0,30)] and round(left_hand_angle3_shoulder) in [i for i in range(0,30)] and 
                round(right_knee) in [i for i in range(100,140)] and round(left_knee) in [i for i in range(100,140)])) :

                step_name = "perfectly matched sixth step"
                step_number = 6
                step5_count += 1
                if step5_count > 40:
                    
                    cv2.putText(frame,step_name,(30,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                
                    engine = pyttsx3.init()
                    engine.say("perfectly matched sixth step")
                    engine.runAndWait()

            #  condition checking for seventh step
            
            if step_name == "perfectly matched sixth step" and (round(right_hip) in [i for i in range(110,140)] and round(left_hip) in [i for i in range(110,140)] and 
                round(right_hand_angle2_ellow) in [i for i in range(155,175)] and round(left_hand_angle1_ellow) in [i for i in range(155,175)] and
                round(right_hand_angle4_shoulder) in [i for i in range(10,30)] and round(left_hand_angle3_shoulder) in [i for i in range(10,30)] and 
                round(right_knee) in [i for i in range(140,170)] and round(left_knee) in [i for i in range(140,170)]) :

                step_name = "perfectly matched seventh step"
                step_number = 7
                step7_count += 1
                if step7_count > 40:
                    cv2.putText(frame,step_name,(30,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                
                    engine = pyttsx3.init()
                    engine.say("perfectly matched seventh step")
                    engine.runAndWait()
                
            #  condition checking for eighth step
            
            if step_name == "perfectly matched seventh step" and ((round(right_hip) in [i for i in range(50,80)] and round(left_hip) in [i for i in range(50,80)] and 
                round(right_hand_angle2_ellow) in [i for i in range(160,180)] and round(left_hand_angle1_ellow) in [i for i in range(160,180)] and
                round(right_hand_angle4_shoulder) in [i for i in range(120,150)] and round(left_hand_angle3_shoulder) in [i for i in range(120,150)] and 
                round(right_knee) in [i for i in range(170,180)] and round(left_knee) in [i for i in range(170,180)])) :

                step_name = "perfectly matched eighth step"
                step_number = 8
                step8_count += 1
                if step8_count > 40:
                    cv2.putText(frame,step_name,(30,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                
                    engine = pyttsx3.init()
                    engine.say("perfectly matched eighth step")
                    engine.runAndWait()
            
            #  condition checking for nineth step
            
            if step_name == "perfectly matched eighth step" and ((round(right_hip) in [i for i in range(20,60)] and round(left_hip) in [i for i in range(160,180)] and 
                round(right_hand_angle2_ellow) in [i for i in range(170,180)] and round(left_hand_angle1_ellow) in [i for i in range(170,180)] and
                round(right_hand_angle4_shoulder) in [i for i in range(20,45)] and round(left_hand_angle3_shoulder) in [i for i in range(25,50)] and 
                round(right_knee) in [i for i in range(60,90)] and round(left_knee) in [i for i in range(115,135)]) or 
                
                (round(right_hip) in [i for i in range(160,180)] and round(left_hip) in [i for i in range(20,60)] and 
                round(right_hand_angle2_ellow) in [i for i in range(170,180)] and round(left_hand_angle1_ellow) in [i for i in range(170,180)] and
                round(right_hand_angle4_shoulder) in [i for i in range(25,50)] and round(left_hand_angle3_shoulder) in [i for i in range(20,45)] and 
                round(right_knee) in [i for i in range(115,135)] and round(left_knee) in [i for i in range(60,90)])):
                
                step_number = 9
                step_name = "perfectly matched nineth step"
                step9_count += 1
                if step9_count > 40:
                    cv2.putText(frame,step_name,(50,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                
                    engine = pyttsx3.init()
                    engine.say("perfectly matched nineth step")
                    engine.runAndWait()
            
            # condition checking for tenth step
            
            if  step_name == "perfectly matched nineth step" and  (round(right_hip) in [i for i in range(60,90)] and round(left_hip) in [i for i in range(60,90)] and 
                round(right_hand_angle2_ellow) in [i for i in range(150,180)] and round(left_hand_angle1_ellow) in [i for i in range(150,180)] and
                round(right_hand_angle4_shoulder) in [i for i in range(50,90)] and round(left_hand_angle3_shoulder) in [i for i in range(50,90)] and 
                round(right_knee) in [i for i in range(170,180)] and round(left_knee) in [i for i in range(170,180)]):
                
                step_number = 10
                step_name = "perfectly matched tenth step"
                step10_count += 1
                if step10_count > 40:
                    engine = pyttsx3.init()
                    engine.say("perfectly matched tenth step")
                    engine.runAndWait()
                
                    cv2.putText(frame,step_name,(50,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                
            # condition checking for eleventh step

            if step_name == "perfectly matched tenth step" and (round(right_hip) in [i for i in range(140,170)] and round(left_hip) in [i for i in range(140,170)] and 
                round(right_hand_angle4_shoulder) in [i for i in range(140,170)] and round(left_hand_angle3_shoulder) in [i for i in range(140,170)] and 
                round(right_hand_angle2_ellow) in [i for i in range(140,170)] and round(left_hand_angle1_ellow) in [i for i in range(140,170)]):
                
                
                step_number = 11
                step_name = "perfectly matched eleventh step"
                step11_count += 1
                if step11_count > 40:
                    engine = pyttsx3.init()
                    engine.say("perfectly matched eleventh step")
                    engine.runAndWait()
                    
                    cv2.putText(frame,step_name,(50,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
            
            # condition checking for twelveth step
            
            if ( step_name == "perfectly matched eleventh step" and (right_pinky_cordi-left_pinky_cordi) in [ i for i in range(-10,10)]   and  round(left_hand_angle1_ellow) in [ i for i in range(30,60)] and round(right_hand_angle2_ellow) in [ i for i in range(30,60)] and round(left_hand_angle3_shoulder) < 30 and round(right_hand_angle4_shoulder) < 30) : 
                # ((right_pinky_cordi-left_pinky_cordi) in [ i for i in range(-10,10)]  and round(left_hand_angle1_ellow) in [ i for i in range(30,60)] and round(left_hand_angle3_shoulder) < 30 and round(right_hand_angle4_shoulder) < 30)  or 
                # ((right_pinky_cordi-left_pinky_cordi) in [ i for i in range(-10,10)]  and round(right_hand_angle2_ellow) in [ i for i in range(30,60)] and round(right_hand_angle4_shoulder) < 30 and round(left_hand_angle3_shoulder) < 30)):
                
                
                step_name = "perfectly matched twelveth step"
                # step_number = 12
                step12_count += 1
                if step12_count > 40:
                    engine = pyttsx3.init()
                    engine.say("perfectly matched twelveth step")
                    engine.runAndWait()
                    
                    cv2.putText(frame,step_name,(30,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
            
                
        live_image_yoga.image(frame)
        # cv2.imshow("image",frame)
        key =  cv2.waitKey(1)
        if live_yoga_stop_button:
            break
    
    video.release()

    cv2.destroyAllWindows()


if select_condition == "2":
    
    select_test_train = st.radio("Select the test or train",["Prectise exercise","Train the exercise","Delete the pose from database"],horizontal=True)
    
    
#---------------------------------------------------- code for testing the pose------------------------------------------------#
    
    if select_test_train == "Prectise exercise":
        
        c.execute('SELECT name from sqlite_master where type= "table"')
        
      
        select_pose_name = st.selectbox("Select the pose name",[ i[0] for i in c.fetchall() ])
        
        c1_pra,c2_pra = st.columns(2)
        with c1_pra: 
            
            st.markdown("")
            test_submit_button = st.button("SUBMIT!",use_container_width=True)
        with c2_pra: count_pra = st.subheader([])
        
        tc1,tc2 = st.columns(2)
    # --------------------------------------- testing -------------------------------------------------#
        
        if test_submit_button:
             
            st.image( Image.open(r"psychotherapy_doctor_image"+ "/"+select_pose_name +"_image.png"))
            
            with tc1:test_live_frame  = st.image([],use_column_width=True)
            with tc2:test_live_frame_for_black  = st.image([],use_column_width=True)

            accuray_pose = st.success([])
            
            
            clean_df = pd.DataFrame(view_all_data(select_pose_name),columns=["pose_name","hands_distance","right_hand_angle2_ellow","left_hand_angle1_ellow","right_hand_angle4_shoulder","left_hand_angle3_shoulder","right_hip","left_hip","right_knee","left_knee"])

            st.dataframe(clean_df)

            df = clean_df
            ini_col = df.columns
            mode_list = []
            count_results = 0

            mp_draw = mp.solutions.drawing_utils
            mp_styles = mp.solutions.drawing_styles
            my_pose = mp.solutions.pose
            myhand = mp.solutions.hands
            hands = myhand.Hands(max_num_hands = 2)
            pose = my_pose.Pose()

            x = 0
            y = 10
            result_display = ""

            def calculate_angle(landmark1,landmark2,landmark3):
                        global angle
                        x1,y1 = landmark1
                        x2,y2 = landmark2
                        x3,y3 = landmark3
                        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
                        if angle < 0 :
                            angle *= -1
                        if angle > 180:
                            angle = 360 - angle
                            
                        return round(angle)

            def changing_colour(angle,dataset_column,codi1_x,codi1_y,codi2_x,codi2_y,codi3_x,codi3_y,pose_name_display):
                    if angle in dataset_column:
                        cv2.line(img=frame,pt1=(codi1_x,codi1_y),pt2=(codi2_x,codi2_y),color=(0,140,0),thickness=10)
                        cv2.line(img=frame,pt1=(codi2_x,codi2_y),pt2=(codi3_x,codi3_y),color=(0,140,0),thickness=10)
                    else:
                        cv2.line(img=frame,pt1=(codi1_x,codi1_y),pt2=(codi2_x,codi2_y),color=(255,255,255),thickness=10)
                        cv2.line(img=frame,pt1=(codi2_x,codi2_y),pt2=(codi3_x,codi3_y),color=(255,255,255),thickness=10)
                        # print("wrongly done part of your body :",pose_name_display)

            # to display pose in frame constant 
            pose_ima_display = cv2.imread("psychotherapy_doctor_image/" + select_pose_name + "_image.png")
            results_display = pose.process(pose_ima_display)
            
            if results_display.pose_landmarks:
                
                mp_draw.draw_landmarks(pose_ima_display,results_display.pose_landmarks,my_pose.POSE_CONNECTIONS,
                                    landmark_drawing_spec=mp_draw.DrawingSpec(color=(255,255,255),thickness=3, circle_radius=3),
                                    connection_drawing_spec=mp_draw.DrawingSpec(color=(49,125,237) ,thickness=2, circle_radius=2))


            video = cv2.VideoCapture(0)
            

            while True:
                
                cap,frame = video.read()
                frame = cv2.resize(frame,(500,500))
                frame = cv2.flip(frame,1)
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                height_frame , width_frame,_ = frame.shape
                results = pose.process(frame)
                results_hand = hands.process(frame)
                
                black_img_test = cv2.imread(r"images\plain_black.jpg")
                black_img_test = cv2.resize(black_img_test,(500,500))
                
                if results_hand.multi_hand_landmarks:
                    for hand_landmarks in results_hand.multi_hand_landmarks:
                        mp_draw.draw_landmarks(frame, hand_landmarks,myhand.HAND_CONNECTIONS,
                                            mp_styles.get_default_hand_landmarks_style(),
                                            mp_styles.get_default_hand_connections_style())
                        
                        
                        mp_draw.draw_landmarks(black_img_test, hand_landmarks,myhand.HAND_CONNECTIONS,
                                            mp_styles.get_default_hand_landmarks_style(),
                                            mp_styles.get_default_hand_connections_style())
                        # to display pose in frame constant        
                        
                if results.pose_landmarks:
                    
                    mp_draw.draw_landmarks(frame,results.pose_landmarks,my_pose.POSE_CONNECTIONS,
                                        landmark_drawing_spec=mp_draw.DrawingSpec(color=(255,255,255),thickness=3, circle_radius=3),
                                        connection_drawing_spec=mp_draw.DrawingSpec(color=(49,125,237) ,thickness=2, circle_radius=2))
                    
                    mp_draw.draw_landmarks(black_img_test,results.pose_landmarks,my_pose.POSE_CONNECTIONS,
                                            landmark_drawing_spec=mp_draw.DrawingSpec(color=(255,255,255),thickness=3, circle_radius=3),
                                            connection_drawing_spec=mp_draw.DrawingSpec(color=(49,125,237) ,thickness=2, circle_radius=2))

                    
                    body_landmarks = results.pose_landmarks.landmark
                    
                    # write the function find angle between three points
                    
                    # for angles in our body 8 angles !!!!!!!!!!!!!!!
                    
                    left_hand_angle1_ellow = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].y])
                    
                    right_hand_angle2_ellow = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].y])
                    
                    left_hand_angle3_shoulder = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y])
                                                    
                    right_hand_angle4_shoulder = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y])
                    
                    left_hip = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].y])
                    
                    right_hip = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].y])
                    
                    left_knee = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].y])
                    
                    right_knee = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].y],
                                                [body_landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].y])
                    
                    right_wrist_cordi =  round(body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x*width_frame)
                    left_wrist_cordi =  round(body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].x*width_frame)
                    two_hand_distance = right_wrist_cordi - left_wrist_cordi
                    if two_hand_distance < 0:
                        two_hand_distance *= -1
                        
                    # from total dataset spliting the each step dataset 
                    
                    each_step_data = df[df.columns[x:y]]
                    
                    print(each_step_data)

                    # columns of the each step dataset
                    each_columns = list(each_step_data.columns)
                    
                    for j in each_columns[1:]:
                        mode1 = statistics.mode(list(each_step_data[str(j)]))
                        mode_list.append(mode1)
                    sum_mode = sum(mode_list)
                
                    # condition for checking pose
                    if (round(two_hand_distance) in list(each_step_data[str(each_columns[1])]) and round(right_hand_angle2_ellow) in list(each_step_data[str(each_columns[2])]) and round(left_hand_angle1_ellow) in list(each_step_data[str(each_columns[3])]) and
                        round(right_hand_angle4_shoulder) in list(each_step_data[str(each_columns[4])]) and round(left_hand_angle3_shoulder) in list(each_step_data[str(each_columns[5])]) and 
                        round(right_hip) in list(each_step_data[str(each_columns[6])]) and round(left_hip) in list(each_step_data[str(each_columns[7])]) and 
                        round(right_knee) in list(each_step_data[str(each_columns[8])]) and round(left_knee) in list(each_step_data[str(each_columns[9])])):
                        sum_each_angle = right_hand_angle2_ellow + left_hand_angle1_ellow + right_hand_angle4_shoulder + left_hand_angle3_shoulder + right_hip + left_hip + right_knee + left_knee
                        accuracy = (sum_each_angle/sum_mode)*100
                        
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
                            
                        if accuracy > 100:
                            accuracy = accuracy - 100
                            accuracy = 100 - accuracy
                            accuray_pose.success("your accuracy of "+str(each_columns[0])+" is "+str(accuracy))
                        else:
                            
                            accuray_pose.success("your accuracy of "+str(each_columns[0])+" is "+str(accuracy))
                        count_results += 1

                        if count_results == 25:
                            result_display += "successfully done"
                            result_display += str(each_columns[0])
                            count_results = 0
                    
                    mode_list.clear()
                    
                    changing_colour(round(right_hand_angle2_ellow),list(each_step_data[str(each_columns[2])]),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y *height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].y*height_frame),
                                    each_columns[2])
                    
                    changing_colour(round(left_hand_angle1_ellow),list(each_step_data[str(each_columns[3])]),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y *height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].y*height_frame),
                                    each_columns[3])
                    
                    changing_colour(round(right_hand_angle4_shoulder),list(each_step_data[str(each_columns[4])]),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y *height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y*height_frame),
                                    each_columns[4])
                
                    changing_colour(round(left_hand_angle3_shoulder),list(each_step_data[str(each_columns[5])]),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y *height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y*height_frame),
                                    each_columns[5])
                    
                    changing_colour(round(right_hip),list(each_step_data[str(each_columns[6])]),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].y *height_frame),
                                    each_columns[6])
                    
                    changing_colour(round(left_hip),list(each_step_data[str(each_columns[7])]),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].y *height_frame),
                                    each_columns[7])
                                        
                    changing_colour(round(right_knee),list(each_step_data[str(each_columns[8])]),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].y *height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].y*height_frame),
                                    each_columns[8])
                    
                    changing_colour(round(left_knee),list(each_step_data[str(each_columns[9])]),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y*height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].y *height_frame),
                                    round(body_landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].x*width_frame),round(body_landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].y*height_frame),
                                    each_columns[9])
                    
                    #  x and y for changing each step dataset
                    x += 10
                    y += 10
                    if y > len(ini_col):
                        x = 0
                        y = 10
                    
                cv2.putText(frame,str(result_display),(50,600),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
                cv2.putText(frame,str(count_results),(50,60),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),4,cv2.LINE_AA)
                
                count_pra.title("Count : " + str(count_results) )

                
                test_live_frame.image(frame,use_column_width=True)
                test_live_frame_for_black.image(black_img_test,use_column_width=True)
                
                # cv2.imshow("image",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
                
                
                key =  cv2.waitKey(1)
                if key == 81:
                    break
            

            video.release()
            cv2.destroyAllWindows()


    # --------------------------------------- training -------------------------------------------------#

        
    if select_test_train == "Train the exercise":
        
        train_password = st.text_input("Enter the admin password",type="password")
            
        
        if train_password == "1234":
        
            
            name_of_step = st.text_input("Enter the pose name")
            
            c.execute('SELECT name from sqlite_master where type= "table"')
        
            
            
          
            train_password_submit_button = st.button("SUBMIT",use_container_width=True)
            
            if train_password_submit_button and name_of_step not in [i[0] for i in c.fetchall()]:
                
                create_table(name_of_step)
                
                train_live_frame = st.image([])
                
                
                mp_draw = mp.solutions.drawing_utils
                mp_styles = mp.solutions.drawing_styles
                my_pose = mp.solutions.pose
                pose = my_pose.Pose()
                close_count = 0

                # initial empty dataset 
                initial_dataset = pd.DataFrame()
                # 
                dataset_pose = pd.DataFrame(data={name_of_step:[],name_of_step+"_hands_distance":[],name_of_step+"_right_hand_angle2_ellow":[],
                                                name_of_step+"_left_hand_angle1_ellow":[],name_of_step+"_right_hand_angle4_shoulder":[],
                                                name_of_step+"_left_hand_angle3_shoulder":[],name_of_step+"_right_hip":[],name_of_step+"_left_hip":[],
                                                name_of_step+"_right_knee":[],name_of_step+"_left_knee":[]})

                # write the function find angle between three points  
                def calculate_angle(landmark1,landmark2,landmark3):
                            global angle
                            x1,y1 = landmark1
                            x2,y2 = landmark2
                            x3,y3 = landmark3
                            angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
                            if angle < 0 :
                                angle *= -1
                            if angle > 180:
                                angle = 360 - angle
                                
                            # cv2.circle(frame,(round(x1*width_frame),round(y1*height_frame)),radius=20,color=(180,20,40),thickness=3)
                            return round(angle)
                        
                video = cv2.VideoCapture(0)
                while True:
                    
                    cap,frame = video.read()
                    frame=cv2.resize(frame,(749, 720))
                    frame = cv2.flip(frame,1)
                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    height_frame , width_frame,_ = frame.shape
                    results = pose.process(frame)
                    
                    if results.pose_landmarks:
                        
                        mp_draw.draw_landmarks(frame,results.pose_landmarks,my_pose.POSE_CONNECTIONS,
                                            landmark_drawing_spec=mp_draw.DrawingSpec(color=(255,255,255),thickness=3, circle_radius=3),
                                            connection_drawing_spec=mp_draw.DrawingSpec(color=(49,125,237) ,thickness=2, circle_radius=2))
                        body_landmarks = results.pose_landmarks.landmark
                        
                        
                        
                        # for angles in our body 8 angles !!!!!!!!!!!!!!!
                        
                        left_hand_angle1_ellow = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].y])
                        
                        right_hand_angle2_ellow = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].y])
                        
                        left_hand_angle3_shoulder = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                                        [body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y])
                                                        
                        
                        right_hand_angle4_shoulder = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y],
                                                            [body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                            [body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y])
                        
                        left_hip = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].y])
                        
                        right_hip = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].y])
                        
                        left_knee = calculate_angle([body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].x,body_landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].y])
                        
                        right_knee = calculate_angle([body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].y],
                                                    [body_landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].x,body_landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].y])
                        
                        right_wrist_cordi =  round(body_landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x*width_frame)
                        left_wrist_cordi =  round(body_landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].x*width_frame)
                        two_hand_distance = right_wrist_cordi - left_wrist_cordi
                        if two_hand_distance < 0:
                            two_hand_distance *= -1
                            
                        check_list = { name_of_step:[name_of_step], name_of_step+"_hands_distance":[two_hand_distance],name_of_step+"_right_hand_angle2_ellow":[right_hand_angle2_ellow],name_of_step+"_left_hand_angle1_ellow":[left_hand_angle1_ellow],
                                    name_of_step+"_right_hand_angle4_shoulder":[right_hand_angle4_shoulder],name_of_step+"_left_hand_angle3_shoulder":[left_hand_angle3_shoulder],
                                    name_of_step+"_right_hip":[right_hip],name_of_step+"_left_hip":[left_hip],name_of_step+"_right_knee":[right_knee],name_of_step+"_left_knee":[left_knee]}
                        # to make each row into dataframe
                        
                    
                        
                        add_data(db_table_name=name_of_step,pose_name=name_of_step,hands_distance=two_hand_distance,
                                right_hand_angle2_ellow=right_hand_angle2_ellow ,left_hand_angle1_ellow = left_hand_angle1_ellow ,
                                right_hand_angle4_shoulder = right_hand_angle4_shoulder ,left_hand_angle3_shoulder = left_hand_angle3_shoulder,
                                right_hip = right_hip,left_hip = left_hip,right_knee = right_knee ,left_knee = left_knee )
                        
                    
                
                    train_live_frame.image(frame)
                    
                    close_count += 1
                    if close_count == 150:
                        cv2.imwrite("psychotherapy_doctor_image/"+str(name_of_step)+"_image.png",frame)
                    if close_count > 500:
                        
                        break

                    
                    key =  cv2.waitKey(1)
                    if key == 81:
                        break
                
                video.release()

                cv2.destroyAllWindows()

            c.execute('SELECT name from sqlite_master where type= "table"')
        
            if name_of_step in [i[0] for i in c.fetchall()]:            
                
                st.warning("entered pose is already in database")
    
    if select_test_train == "Delete the pose from database":
        
        delete_password = st.text_input("Enter the admin password",type="password")
        
        if delete_password == "1234":
            
            c.execute('SELECT name from sqlite_master where type= "table"')
        
            select_pose_name_delete = st.selectbox("Select the pose name",[ i[0] for i in c.fetchall() ])
            
            delete_button = st.button("DELETE!")
            
            if delete_button:
                
                Drop_table(select_pose_name_delete)
                os.remove("E:/vs code projects/Digital Docter/psychotherapy_doctor_image"+ "/"+select_pose_name_delete  +"_image.png")
                
                st.success("Successfully deleted pose")
        
    
    
