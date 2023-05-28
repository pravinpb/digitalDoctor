import streamlit as st
import numpy as np
from tensorflow import keras
from keras.utils import img_to_array
from PIL import Image
import cv2
from ultralytics import YOLO
import shutil


st.set_page_config(page_title="X-ray image analysis",page_icon="❄️")

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("To analysis X-ray images")

def predict_image(path):
    
    read =  Image.open(path)
    resize_image = read.resize((180,180))
    ima_array = img_to_array(resize_image)
    
    resize_image = ima_array / 255

    return resize_image.reshape(1,180,180,3)
        

select_type_of_disease = st.radio("Enter the disease :",["brain_tumour","Tuberculosis"],horizontal=True)



if select_type_of_disease == "brain_tumour":
    # title of page
    st.title("Brain tumour")
    
    #  image upload 
    uploaded_show_img = st.image([])
    image  = st.file_uploader("Upload a CT scan")
    

    
    
    
    if image is not None: 
        uploaded_show_img.image(image,use_column_width=True)
    
    labels_result = ["glioma_tumor","meningioma_tumor","no_tumor","pituitary_tumor"]
    button_tumour = st.button("Submit",use_container_width=True)
    
    if button_tumour:

             
            model_segment = YOLO(r"E:\vs code projects\Digital Docter\model_files\yolov8_segment_models\yolov8_segment_brain_tumor_model.pt") 
            
            image = Image.open(image).save("x-ray.png")
            
            model_segment.predict("x-ray.png",save=True,conf=0.20)
                        
            
            st.subheader("disease segmented result")
            st.image(cv2.imread(r"runs\segment\predict\x-ray.png"),use_column_width=True)
            
            shutil.rmtree(r"runs")
            
            model = keras.models.load_model(r'E:\vs code projects\Digital Docter\model_files\all models files\brain_tumor.h5')
            result = model.predict([predict_image("x-ray.png")])
            result = str(labels_result[np.argmax(result)])
            
            
            st.success("Result : " + result ,icon="✅")
            
            if result != "no_tumor":
                
                st.subheader("Description:")
                st.success("A brain tumor, known as an intracranial tumor, is an abnormal mass of tissue in which cells grow and multiply uncontrollably, seemingly unchecked by the mechanisms that control normal cells.")  
                st.subheader("Causes:")
                st.success(" Brain tumors can be caused by genetic mutations, exposure to radiation, age, gender, family history, immune system disorders, and environmental factors. Genetic mutations, radiation, age, gender, family history, immune system disorders, and environmental factors can all increase the risk of developing brain tumors.   ")
                st.success("Brain tumors can be caused by genetic mutations, exposure to radiation, age, gender, family history, immune system disorders, and environmental factors. Genetic mutations, radiation, age, gender, family history, immune system disorders, and environmental factors can all increase the risk of developing brain tumors.   ")
                st.subheader("Precaution:")
                st.success("  Regular check-ups with a primary care physician or a neurologist are important to monitor brain health and detect potential issues early. To protect your head, wear helmets and seatbelts when biking, skateboarding, or participating in other sports. Eat a healthy diet rich in fruits, vegetables, and whole grains. Exercise regularly to improve overall health and reduce the risk of many diseases. Limit exposure to radiation to reduce the risk of developing brain tumors.")
                
                st.subheader("Symptoms:")
            else:
                st.info("You are safe")
            
if select_type_of_disease == "Tuberculosis":
    # title of page
    st.title("Tuberculosis")
    
    #  image upload 
    uploaded_show_img = st.image([])
    image  = st.file_uploader("Upload a CT scan")
    
    
    if image is not None: 
        uploaded_show_img.image(image,use_column_width=True)
    
    labels_result = ["normal","Tuberculosis"]
    button_tumour = st.button("Submit",use_container_width=True)
    
    if button_tumour:

             
            model_segment = YOLO(r"model_files\yolov8_segment_models\tuberculosis_yolov8.pt") 
            
            image = Image.open(image).save("x-ray.png")
            
            results = model_segment.predict("x-ray.png",save=True,conf=0.30)
            

            st.subheader("disease segmented result")
            st.image(cv2.imread(r"runs\detect\predict\x-ray.png"),use_column_width=True)
            
            shutil.rmtree(r"runs")
            
            for i in results:
                results = i.boxes.cls.tolist()
            
            if 4 not in results:
                
                st.subheader("Description:")
                st.subheader("Causes:")
                st.subheader("Precaution:")
                st.subheader("Symptoms:")
            else:
                st.info("You are safe")
  

st.title("Generating X-ray images")

generate_button = st.button("Generate")
# Saves
if generate_button:
    c1,c2= st.columns(2)
    img = Image.open(image)
    img = img.save("img.jpg")
    # OpenCv Read
    img = cv2.imread("img.jpg")
    im1 = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
    im2 = cv2.applyColorMap(img, cv2.COLORMAP_BONE)
    im3 = cv2.applyColorMap(img, cv2.COLORMAP_JET)
    im4 = cv2.applyColorMap(img, cv2.COLORMAP_WINTER)
    im5 = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
    im6 = cv2.applyColorMap(img, cv2.COLORMAP_OCEAN)
    im7 = cv2.applyColorMap(img, cv2.COLORMAP_SUMMER)
    im8 = cv2.applyColorMap(img, cv2.COLORMAP_SPRING)
    im9 = cv2.applyColorMap(img, cv2.COLORMAP_COOL)
    im10 = cv2.applyColorMap(img, cv2.COLORMAP_HSV)
    im11 = cv2.applyColorMap(img, cv2.COLORMAP_PINK)
    im12 = cv2.applyColorMap(img, cv2.COLORMAP_HOT)

    with c1:
        st.image(im1,use_column_width=True)
        st.image(im2,use_column_width=True)
        st.image(im3,use_column_width=True)
        st.image(im4,use_column_width=True)
        st.image(im5,use_column_width=True)
        st.image(im6,use_column_width=True)
        
    with c2:
        st.image(im7,use_column_width=True)
        st.image(im8,use_column_width=True)
        st.image(im9,use_column_width=True)
        st.image(im10,use_column_width=True)
        st.image(im11,use_column_width=True)
        st.image(im12,use_column_width=True)
        

        
        
        
        
        