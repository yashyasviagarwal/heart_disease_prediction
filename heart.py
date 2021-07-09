

import pickle
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df):

    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download File</a>'


def get_sex(n):
    if n == "Male":
        return 1
    else:
        return 0


def get_cp(n):
    if n == '1':
        return 1.0
    elif n == '2':
        return 2.0
    elif n == '3':
        return 3.0
    elif n == '4':
        return 4.0


def get_exg(n):
    if n == '0':
        return 0.0
    elif n == '1':
        return 1.0

    elif n == '2':
        return 2.0


def get_op(n):
    if n == '1':
        return 1
    else:
        return 0


def get_ca(n):
    if n == '0':
        return 0.0
    elif n == '1':
        return 1.0

    elif n == '2':
        return 2.0
    elif n == '3':
        return 3.0


def main():

    st.markdown('<div style=background-color:powderblue;</div>',
                unsafe_allow_html=True)
    activity = ['Home', 'Prediction']

    st.sidebar.markdown(
        '<div style=color:#006080;font-size:20px;font-family:courier;font-weight:bold>MENU</div>', unsafe_allow_html=True)
    choice = st.sidebar.radio("        ", activity)

    img = Image.open('hb3.png')

    st.sidebar.image(img, width=300)

    if choice == 'Prediction':
        # df1=pd.read_csv("stent.csv")

        st.sidebar.markdown(
            '<div style=color:#006080;font-size:20px;font-family:courier;font-weight:bold>ENTER PATIENT DETAILS:</div>', unsafe_allow_html=True)
        st.markdown('<div style=color:#001866;text-align:center;font-size:40px;font-family:courier;font-weight:bold>PREDICTION SESSION</div>', unsafe_allow_html=True)
        # st.markdown('<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Graphical Representation Of The Dataset:</div>',unsafe_allow_html=True)
        #sns.catplot(x='stent',data=df1,palette='Blues',kind='violin',  height=2, aspect=3)
        #df1['stent'].value_counts().plot(kind='pie', figsize=(20,10),palette='Blues')
        # st.pyplot(figsize=(5,5))
        img = Image.open('cg.png')

        st.image(img, width=700)
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Age:</div>', unsafe_allow_html=True)
        age = st.sidebar.number_input(" ", value=1)
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Sex:</div>', unsafe_allow_html=True)

        sex = st.sidebar.radio(' ', ['Male', 'Female'], index=0)
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Chest Pain:</div>', unsafe_allow_html=True)
        cp = st.sidebar.radio('   ', ['1', '2', '3', '4'], index=0)
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Resting blood pressure:</div>', unsafe_allow_html=True)
        tresbps = st.sidebar.number_input("           ")
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Cholestrol:</div>', unsafe_allow_html=True)
        chol = st.sidebar.number_input(" ")
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Fasting blood sugar:</div>', unsafe_allow_html=True)
        fbs = st.sidebar.number_input("                     ")
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Resting electrocardiographic results:</div>', unsafe_allow_html=True)
        ecg = st.sidebar.number_input("                  ")

        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Maximum Heart Rate:</div>', unsafe_allow_html=True)
        hrt = st.sidebar.number_input("  ")
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Exercise Induced Angina:</div>', unsafe_allow_html=True)

        exg = st.sidebar.radio("     ", ["0", "1", "2"], index=0)

        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>ST Depression Induced By Exercise Relative To Rest:</div>', unsafe_allow_html=True)
        op = st.sidebar.number_input("                           ")
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Slope Of The Peak Exercise ST Segment:</div>', unsafe_allow_html=True)
        slp = st.sidebar.number_input("    ")
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Number of major vessels colored:</div>', unsafe_allow_html=True)

        ca = st.sidebar.radio("             ", ["0", "1", "2", "3"], index=0)
        st.sidebar.markdown(
            '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>thalium stress result:</div>', unsafe_allow_html=True)
        thal = st.sidebar.number_input("                 ")

        sex1 = get_sex(sex)
        cp1 = get_cp(cp)
        # op1=get_op(op)

        ca1 = get_ca(ca)
        exg1 = get_exg(exg)
        lst = [age, sex1, cp1, tresbps, chol, fbs,
               ecg, hrt, exg1, op, slp, ca1, thal]
        # st.write(lst)
        # img=Image.open('hb5.jpg')

        # st.image(img,width=300)

        sample_data = np.array(lst).reshape(1, -1)
        # st.write(sample_data)
        if st.sidebar.button("Predict"):

            #st.markdown('<div style=color:black;font-size:22px;font-family:courier>Data Encrypted As:</div>',unsafe_allow_html=True)
            # st.write(lst)
            model = pickle.load(open('heart_disease.sav', 'rb'))
            # model=joblib.load(open(os.path.join("dtree_model.pkl"),"rb"))
            Prediction = model.predict(sample_data)
            if Prediction == 0.:
                st.markdown(
                    '<div style=color:black;font-size:22px;font-family:courier>Heart disease not detected</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style=color:black;font-size:22px;font-family:courier>Heart disease detected</div>', unsafe_allow_html=True)

            img = Image.open('hb3.png')

            st.image(img, width=700)

    if choice == 'Home':
        st.markdown('<div style=color:#001866;text-align:center;font-size:40px;font-family:courier;font-weight:bold>HEART DISEASE PREDICTION</div>', unsafe_allow_html=True)
        img = Image.open('rb.jpg')

        st.image(img, width=120)
        st.markdown('<div style=color:black;font-size:16px;font-family:times>A little prediction goes a long way and this is what we tried implementing Where data is the new science, Machine Learning holds all the answers.With all data piled up, Machine Learning accomplishes the task of developing new capabilities from these data.This automation is the source of our model for building its predictive power</div>', unsafe_allow_html=True)
        st.write(" ")
        img = Image.open('cg.png')

        st.image(img, width=700)
        st.markdown('<div style=color:black;font-size:16px;font-family:times>In this app,in order to predict the risk of having a heart disease, user needs to enter the values of various parameters on the basis of which the calculation will be made. From the given measurements,our app will evaluate whether the person suuffers from heart disease like blockage.</div>', unsafe_allow_html=True)
        st.write(" ")
        img = Image.open('hb3.png')

        st.image(img, width=700)

    st.sidebar.markdown(
        '<div style=color:#006080;font-size:20px;font-family:courier;font-weight:bold>ABOUT US</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div style=color:black;font-size:12px;font-family:times>Every year a large amount of data is generated in the healthcare industry but they are not used effectively.So here is a system that will be able to communicate with people’s mind and help them in getting prepared based on their medical history.By using patient’s input features such as sex, cholesterol, blood pressure and much more the prediction of the presence of heart disease. So this model depicts whether or not a person is at a risk of having a heart disease.</div>', unsafe_allow_html=True)
    # img=Image.open('bulb.png')
    # img=Image.open('bub.png')

    # st.sidebar.image(img,width=300)
    # img=Image.open('cg.png')

    # st.image(img,width=700)

    Image.open('bulb3.jpg').convert('RGB').save('new2.png')
    st.sidebar.image('new2.png', width=40)

    st.sidebar.markdown(
        '<div style=color:black;font-size:12px;font-family:courier>Use the values from the dataset to see different results.</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
