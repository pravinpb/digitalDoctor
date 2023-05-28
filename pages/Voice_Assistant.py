import streamlit as st
import pickle,keras,random,datetime
import speech_recognition as sr
import pyttsx3
import numpy as np
from tensorflow import keras

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.title("Welcome")

 # load all pickle files for mdoel 
data = pickle.load(open(r"model_files\bot files\all_data_medical.pickle",'rb'))

model = keras.models.load_model(r'model_files\bot files\chatbot_model_new.h5')

with open(r'model_files\bot files\tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
    
with open(r'model_files\bot files\label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)
 
 

# Initialize the recognizer
r = sr.Recognizer()
 
# Function to convert text to
# speech
def SpeakText(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
     
     
def stt():
      
    try:
        
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.1)
            
            #listens for the user's input
            audio2 = r.listen(source2)
            
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            
            return MyText
     
    except sr.RequestError as e:
        return ("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        return ("unknown error occurred")
  
          
# user_list.append(user_input)
                
# bot_list.append(output_data)
        
# add_data(today_date=datetime.datetime.today().date(),today_time= str(datetime.datetime.today().time()),User_messages=user_input,Bot_messages=output_data)   


c1,c2 = st.columns(2)

for i in range(10):
    
    SpeakText("Say any thing")
    text = stt()
    
    with c1:st.info(text)
    
    SpeakText(text)
    
    if text == "stop":
        break
    
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([text]),truncating='post', maxlen=20))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])
    for i in data['intents']:
        if i['tag'] == tag:
            output_data =  random.choice(list(i['responses']))
            
            with c2: st.success(output_data)
            SpeakText(output_data)  
            
    
    