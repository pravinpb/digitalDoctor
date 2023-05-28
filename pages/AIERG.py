import streamlit as st
from gtts import gTTS
import pickle
from translate import Translator
import pandas as pd
from  PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import datetime
import base64
from st_clickable_images import clickable_images
from bs4 import BeautifulSoup
import requests
import sqlite3
import webbrowser 
import people_also_ask as paa
import random
from playsound import playsound
import numpy as np 
from tensorflow import keras


st.set_page_config(page_title="medical report generator",page_icon="🎭")

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# def get_img_as_base64(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
# img = get_img_as_base64(r"D:\Downloads\chat-bot-messages-smart-chatbot-assistant-conversation-online-customer-support-robot-talking-to-machine-bots-message-answering-134553809.jpg")

# page_bg_img = f"""
# <style>
# .stApp {{
# background-image: url('data:image/jpg;base64,{img}');
# background-size: cover;
# }} 
# </style>
# """
           
# st.markdown(page_bg_img, unsafe_allow_html=True)




st.title("CareBot")

df = pd.read_csv(r"D:\DigitalDoctor\csv_files\symptoms_chatbot.csv")
df.drop("Unnamed: 133",axis=1,inplace=True)

#--------------------------------------------------------- medical_database_table ---------------------------------------------#

conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def create_table():
    	c.execute('CREATE TABLE IF NOT EXISTS medical_database_table(today_date DATE,today_time TEXT ,User_messages TEXT, Bot_messages TEXT)')
create_table()
    

def add_data(today_date,today_time,User_messages,Bot_messages):
	c.execute('INSERT INTO medical_database_table(today_date,today_time,User_messages,Bot_messages) VALUES (?,?,?,?)',(today_date,today_time,User_messages,Bot_messages))
	conn.commit()
 
create_table()

def view_all_data():
    c.execute('SELECT * FROM medical_database_table')
    data = c.fetchall()
    return data

def get_task(task):
    c.execute('SELECT * FROM medical_database_table WHERE test="{}"'.format(task))
    data = c.fetchall()
    return data

def delete_data(task):
    c.execute('DELETE FROM medical_database_table WHERE test="{}"'.format(task))
    conn.commit()
    
#--------------------------------------------------------- medical_database_table ---------------------------------------------#


column_1_1,column_1_2 = st.columns(2)
column_2_1,column_2_2 = st.columns(2)
column_3_1,column_3_2 = st.columns(2)
column_4_1,column_4_2 = st.columns(2)
column_5_1,column_5_2 = st.columns(2)
column_6_1,column_6_2 = st.columns(2)
column_7_1,column_7_2 = st.columns(2)
column_8_1,column_8_2 = st.columns(2)
column_9_1,column_9_2 = st.columns(2)
column_10_1,column_10_2 = st.columns(2)
column_11_1,column_11_2 = st.columns(2)
column_12_1,column_12_2 = st.columns(2)
column_13_1,column_13_2 = st.columns(2)
column_14_1,column_14_2 = st.columns(2)
column_15_1,column_15_2 = st.columns(2)
column_16_1,column_16_2 = st.columns(2)
column_17_1,column_17_2 = st.columns(2)
column_18_1,column_18_2 = st.columns(2)
column_19_1,column_19_2 = st.columns(2)
column_20_1,column_20_2 = st.columns(2)
column_21_1,column_21_2 = st.columns(2)
column_22_1,column_22_2 = st.columns(2)
column_23_1,column_23_2 = st.columns(2)
column_24_1,column_24_2 = st.columns(2)
column_25_1,column_25_2 = st.columns(2)
column_26_1,column_26_2 = st.columns(2)


if True:
    # ----------------------------------------- columns 1 ---------------------------------------------------------#
    # bot
    with column_1_1:
        q1_c1 = "Welcome to CareBot "
        st.info("hi i am artificial intelligent bot, how can i help you?",icon="🤖")
        st.info("Do you have any problem?",icon="🤖")

    # ----------------------------------------- columns 2 ---------------------------------------------------------#
    # user   
    with column_2_2:
        # problem_result = ""
        
        s1,s2 = st.columns(2)
        with s1:problem = st.button("I have a problem")
        with s2:not_problem = st.button("No,I not have a problem")
        
        if problem:
            problem_result = "problem"
            st.success("I have a problem")
            # if 'problem_result' not in st.session_state:
            st.session_state['problem_result'] = problem_result
        if not_problem:
            problem_result = "not_problem"
            st.success("No,I not have a problem")
             
            # if 'problem_result' not in st.session_state:
            st.session_state['problem_result'] = problem_result

    # ----------------------------------------- columns 3 ---------------------------------------------------------#
    # bot  
    problem_result = str(st.session_state.problem_result)

    if problem_result == "problem":
        with column_3_1:
            st.info("plese give some general information")
            st.info("upload your photo")
            
        # user columns 4
        with column_4_2:
            your_photo = st.file_uploader("upload your photo")
            if your_photo != None:
                if 'your_photo' not in st.session_state:
                    st.session_state['your_photo'] = "your_photo_uploaded"
                
                
        your_photo_ = str(st.session_state.your_photo)
            
        
        # bot columns 5
        if your_photo_ == "your_photo_uploaded":
            with column_5_1:
                st.info("what is your name?")

            # user columns 6
            with column_6_2:
                my_name = st.text_input("enter your name:")
                if my_name != "":
                    if 'my_name' not in st.session_state:
                        st.session_state['my_name'] = my_name
                
            my_name = str(st.session_state.my_name)
            
        # bot columns 7
        if my_name != "":
            with column_7_1:
                st.info("what is your age and D.O.B?")
            
            # user columns 8
            with column_8_2:
                my_age = st.number_input("enter your age",0,100)
                my_dob = st.date_input("Date of birth")
                if my_age != 0:
                    if 'my_age' not in st.session_state:
                            st.session_state['my_age'] = my_age
                
            my_age = int(st.session_state.my_age)

           
        # bot columns 9
        if int(my_age) != 0:
            with column_9_1:
                st.info("what is your sex?")
            
            # user columns 10
            with column_10_2:
                g5,g6 = st.columns(2)
                
                with g5: male = st.button("male")
                with g6: female = st.button("female")
                
                if male:
                    result_sex = "male"
                    st.success("male")
                    if 'result_sex' not in st.session_state:
                            st.session_state['result_sex'] = result_sex
                if female:
                    result_sex = "female"
                    st.success("female")
                    if 'result_sex' not in st.session_state:
                            st.session_state['result_sex'] = result_sex
                    
                    
            my_gender = str(st.session_state.result_sex)
        
        # bot columns 11
        if my_gender != "":
            with column_11_1:
                st.info("what is your blood group?")

            # user columns 12
            with column_12_2:
                my_blood_group = st.selectbox("enter your blood group:",["None","A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                if my_blood_group != "None":
                    if 'my_blood_group' not in st.session_state:
                            st.session_state['my_blood_group'] = my_blood_group
                            
            my_blood_group = str(st.session_state.my_blood_group)
        
        
        # bot columns 13
        if my_blood_group != "None":
            with column_13_1:
                st.info("what are symptoms you suffering right now?")
            
            # user columns 14
            with column_14_2:
                my_symptoms = st.multiselect("select your symptoms",list(df.columns))
                if len(my_symptoms) != 0:
                    if 'my_symptoms' not in st.session_state:
                            st.session_state['my_symptoms'] = my_symptoms
                        
            my_symptoms_for_condition = st.session_state.my_symptoms
            
            
        # bot columns 15
        if len(my_symptoms_for_condition) != 0:
            with column_15_1:
                st.info("how many days have this kind of symptoms like ")
                
            # user columns 16
            with column_16_2:
                symptoms_days = st.text_input("")
                if symptoms_days != "":
                    if 'symptoms_days' not in st.session_state:
                            st.session_state['symptoms_days'] = symptoms_days
                            
            symptoms_days =  str(st.session_state.symptoms_days)
            
        # bot columns 17
        if symptoms_days != "":
            with column_17_1:
                st.info("how severe this all symptoms?")
            
            # user columns 18
            with column_18_2:
                severe_list = []
                for i in my_symptoms:
                    severe_st =  st.select_slider(i,[1,2,3,4,5])
                    severe_list.append(severe_st)
            
        if symptoms_days != "":
            with column_19_1:
                st.info("Do you have others problems or symptoms")
                

            # user columns 18
            with column_20_2:
                s3,s4 = st.columns(2)
                with s3: condi_yes = st.button("YES")
                with s4: condi_no = st.button("NO")
                if condi_no:
                    st.success("genarating report.......")
                    condi_resu = "no"
                    # if 'condi_resu' not in st.session_state:
                    st.session_state['condi_resu'] = condi_resu
                    
                if condi_yes:
                    condi_resu = "yes"
                    st.success("please add your others symptom in previous symptom container")
                    
                    # if 'condi_resu' not in st.session_state:
                    st.session_state['condi_resu'] = condi_resu
                   
            condi_resu = str(st.session_state.condi_resu)
            
                

        if condi_resu == "no":
            
            with column_22_2:

                # generate_report_ = st.button("GENERATE REPORT")
                generate_report_ = True
                if generate_report_:
                    
                    # to take all rows relatrd to symptom
                    all_dataframe = pd.DataFrame()
                    for i in my_symptoms:
                        predicted_symptom = df[ (df[i] == 1)]
                        all_dataframe =  pd.concat([all_dataframe,predicted_symptom])
                    
                    # to filter main content in full dataframe
                    find_list = []
                    for i in all_dataframe.to_numpy():
                        i = list(i)
                        find_list.append([i[:len(my_symptoms)], i[-1], i[3:].count(0)])

                    # to sort the data 
                    h = find_list
                    def sor(e):
                        return sum(e[0]),e[2]
                    h.sort(key=sor,reverse=True)
                    
                    # to append diesease from sorted dataframe
                    z = []
                    for i in h:
                        z.append(i[1]) 
                    
                    # to remove reduntanancy
                    res = []
                    for x in z:
                        if x not in res:
                            res.append(x)
                    
                    st.subheader("There are predicted disease in priority order for your symptoms") 
                    disease_in_order_df = pd.DataFrame(data=res,columns=["Disease"])   
                    st.dataframe(disease_in_order_df,width=600) 
                
                
                    report_result = "you may have change of " + res[0] + " disease"
                    st.success(report_result)
                    if report_result != "":
                        if 'report_result' not in st.session_state:
                                st.session_state['report_result'] = report_result
                    
        report_result = str(st.session_state.report_result)
            
        if report_result != "":
                    
            with column_23_1:
                
                st.info("Do you want us to refer you to near by specialist near by you?")
                st.info("give your district")
                
                
            # user columns 18
            with column_24_2:
                
                ques1_near_specialist = st.selectbox("*",["None","Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore", "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kanchipuram", "Kanyakumari", "Karur", "Krishnagiri", "Madurai", "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai", "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi", "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore", "Viluppuram", "Virudhunagar"])
                if ques1_near_specialist != "None":
    
                    search_text = "https://www.lybrate.com/" + ques1_near_specialist + "/treatment-for-" + report_result.split(" ")[5]
                    
                    content = BeautifulSoup(requests.get(search_text).text)
                    all_con = content.find_all("a")
                    text_list = []
                    for i in all_con:
                        text_list.append(i.text)
                    
                    for n,i in enumerate(text_list):
                        f_in = n 
                        if "Dr." in i.strip().split():
                            break 
                    for n,i in enumerate(text_list):
                        if "Dr." in i.strip().split():
                            s_in = n 
                    
                    text_list = text_list[f_in:s_in]
                    
                    
                    doctor_list = [ i.strip().replace("\xa0","") for i in text_list if i != ""]
                    
                    st.dataframe(pd.DataFrame(data=doctor_list,columns=["specialist"]),width=600)
                    
                    if ques1_near_specialist != "":
                        if 'ques1_near_specialist' not in st.session_state:
                                st.session_state['ques1_near_specialist'] = ques1_near_specialist
                                
                    
            ques1_near_specialist_ = str(st.session_state.ques1_near_specialist)
            
                
        if ques1_near_specialist_ != "None":
            
            with column_25_1:
                
                st.info("Do you want book appointment in near by hospital?")
            
                    
            with column_26_2:
              
                    
                st.success("Are you need book appointment in near by hospital")
                s5,s6,s7 = st.columns(3)
                with s5: book_yes = st.button("YES!!!")
                with s6: book_no = st.button("NO!!!")
                with s7: report_button = st.button("Download report")
                
           
                
                if book_no:
                    st.success("okay thank you")
                    final_con = "yes"
                    if 'final_con' not in st.session_state:
                            st.session_state['final_con'] = final_con
                    
                if book_yes:
                    
                    url = "https://www.lybrate.com/"+ ques1_near_specialist  +"/treatment-for-" + report_result.replace("you may have change of ","").replace("disease","").replace(" ","")
                    webbrowser.open_new(url)
                    
                    final_con = "yes"
                    if 'final_con' not in st.session_state:
                            st.session_state['final_con'] = final_con
                            
                                       
                if report_button:
                    
                    try:
                        diabatics_list_data_user = st.session_state.diabatics_list_data_user
                        diabatics_list_data_user = [197,70,45,543,30.5,0.158,53]
                        
                    except:
                        diabatics_list_data_user = [197,70,45,543,30.5,0.158,53]
                     
                        
                    bg_image = Image.open(r"images\png_20230515_155225_0000.png")
         
                    my_pho_ima = Image.open(your_photo)
                    my_pho_ima = my_pho_ima.resize((270,270))
                    Image.Image.paste(bg_image,my_pho_ima,(1100,230))
                    
                    title_font = ImageFont.truetype(r"fonts\Poppins-Medium.otf",35)
                    d1 = ImageDraw.Draw(bg_image)
                    
                    d1.text((450,160),my_name,font = title_font,fill= (0,0,0))
                    d1.text((450,216),str(my_age),font = title_font,fill= (0,0,0))
                    d1.text((450,267),my_gender,font = title_font,fill= (0,0,0))
                    d1.text((450,328),str(my_dob),font = title_font,fill= (0,0,0))
                    d1.text((830,275),ques1_near_specialist_,font = title_font,fill= (0,0,0))
                    d1.text((830,330),my_blood_group,font = title_font,fill= (0,0,0))
                    
                    x1 = 580
                    for i in my_symptoms:
                        d1.text((50,x1),i,font = title_font,fill= (0,0,0))
                        x1 += 60
                     
                    x2 = 580
                    for i in severe_list:
                        d1.text((600,x2)," * "*i+"  " + str(i),font = title_font,fill= (0,0,0))
                        x2 += 60   
                    
                    x3 = 1030
                    for i,j in enumerate(disease_in_order_df["Disease"][:5]):
                        d1.text((50,x3),str(i+1) + ")  " + j ,font = title_font,fill= (0,0,0))
                        x3 += 60 
                    
                    d1.text((500,1150),"you may have change of " +disease_in_order_df["Disease"][0]+ " disease" ,font = title_font,fill= (0,0,0))
                    
                    # BMI
                    d1.text((830,170),str(diabatics_list_data_user[5]),font = title_font,fill= (0,0,0))
                    # Insulin
                    d1.text((200,1630),str(diabatics_list_data_user[4]),font = title_font,fill= (0,0,0))
                    # Glucose
                    d1.text((200,1710),str(diabatics_list_data_user[1]),font = title_font,fill= (0,0,0))
                    # BloodPressure
                    d1.text((200,1780),str(diabatics_list_data_user[2]),font = title_font,fill= (0,0,0))
                    # diabatics_ result
                    d1.text((1170,1620),"yes",font = title_font,fill= (0,0,0))
                    
                    bg_image.show()
                    
                    bg_image.save("report.png")
                    
                    with open("report.png", "rb") as file:

                        btn = st.download_button(

                                label="Download image",

                                data=file,

                                file_name="report.png",

                                mime="image/png"

                            )
                        
                        if btn:
                            st.balloons()
                    
                    
            final_con = str(st.session_state.final_con)
        
#-----------------------------------------chat bot--------------------------------------------------------------------------#        
        
        if final_con != "":
            with open('user_list.pickle', 'rb') as handle:
                user_list = pickle.load(handle)

            with open('bot_list.pickle', 'rb') as handle:
                    bot_list = pickle.load(handle)

            # load all pickle files for mdoel 
            data = pickle.load(open(r"model_files\bot files\all_data_medical.pickle",'rb'))

            model = keras.models.load_model(r'model_files\bot files\chatbot_model_new.h5')

            with open(r'model_files\bot files\tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)
                
            with open(r'model_files\bot files\label_encoder.pickle', 'rb') as enc:
                lbl_encoder = pickle.load(enc)

          
            input_ques_columns1,input_ques_columns2 = st.columns(2)
            with input_ques_columns1:
                user_input =  st.text_input("Query :")
            with input_ques_columns2:
                st.markdown("")
                st.markdown("")
                submit_button_bot = st.button("Submit!!!!")
                


            if submit_button_bot == True:
                
                
                user_list.append(user_input)
                
                result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([user_input]),truncating='post', maxlen=20))
                tag = lbl_encoder.inverse_transform([np.argmax(result)])
                for i in data['intents']:
                    if i['tag'] == tag:
                        output_data =  random.choice(list(i['responses']))
                        
                        bot_list.append(output_data)
                        
                add_data(today_date=datetime.datetime.today().date(),today_time= str(datetime.datetime.today().time()),User_messages=user_input,Bot_messages=output_data)   
                
                    
                # else:
                #     # to get answer for user input 
                #     paa_result = paa.get_simple_answer(user_input)
                
                    # generated_ans =  paa.generate_answer(user_input)
                    # for i in generated_ans:
                    #     predict_res = i.values()
                    #     predict_res = list(predict_res)
                    #     break
                    # res1_val = predict_res[3]
                    # if res1_val == "":
                    #     res1_val = predict_res[-1]
                    
                    # result_from_join = res1_val + "\n\n" + predict_res[-1]
                   
                    # user_list.append(user_input)
                    # bot_list.append(result_from_join)
            
            
                        
            with open('user_list.pickle', 'wb') as handle:
                pickle.dump(user_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

            with open('bot_list.pickle', 'wb') as handle:
                pickle.dump(bot_list, handle, protocol=pickle.HIGHEST_PROTOCOL)  


            for i,j in enumerate(zip(user_list,bot_list)):
                col1, col2 = st.columns(2)
                col11, col22 = st.columns(2)
                
                
                
                
                with col1:
                    selected_col1 = st.info(j[0],icon="🧊")
                with col22:
                    selected_col2 = st.success(j[1],icon="🤖")
                    
                    c1,c2,c3 = st.columns(3)
                    with c1:
                        say = st.button("Say"+str(i)+"🔊",use_container_width=True)
                    with c2:
                        extra_information_button = st.button("See extra"+str(i),use_container_width=True)
                    with c3:
                        translate_button = st.button("Translate"+str(i),use_container_width=True)
                        
                    
                    if say:
                        
                        tts = gTTS(text=j[1], lang="en", slow=False)
                        tts.save("sound.mp3")
                        
                        playsound("sound.mp3",True)
                        
                    if extra_information_button:
                        paa_result = paa.get_simple_answer(j[0])
                        
                        with st.expander("View"):
                            st.markdown(paa_result)
                            
                    if translate_button:
                        translator= Translator( from_lang='en', to_lang="ta")
                        translation = translator.translate(j[1])  
                        st.warning(translation)
                    

            if len(bot_list) > 1:
                end_button_conservation = st.button("End Conversation")
                if end_button_conservation:
                    user_list = []
                    bot_list = []
                    with open('user_list.pickle', 'wb') as handle:
                        pickle.dump(user_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

                    with open('bot_list.pickle', 'wb') as handle:
                        pickle.dump(bot_list, handle, protocol=pickle.HIGHEST_PROTOCOL) 

          

# except:
#     pass
    
    
