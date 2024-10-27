import streamlit as st
import easyocr
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

reader = easyocr.Reader(['en'])

st.title("Text from Image Extractor")
st.write("Upload an image, and the app will display detected text with bounding boxes.")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    result = reader.readtext(img_array)

    for detection in result:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        text = detection[1]
        
        img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        
        img = cv2.putText(img, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 5, 155), 1)

    st.image(img, caption="Detected text with bounding boxes", use_column_width=True)

    st.subheader("Extracted Text")
    extracted_text = "\n".join([detection[1] for detection in result])
    st.text_area("Text found in the image:", extracted_text, height=200)