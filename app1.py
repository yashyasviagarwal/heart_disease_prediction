import streamlit as st
import sqlite3
from io import BytesIO
import base64
import pickle
import numpy as np
import bcrypt
import pandas as pd
from PIL import Image
conn = sqlite3.connect('data.db')
c = conn.cursor()


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def dropUserInfoTable():
    c.execute('DROP TABLE usersInfoTable')


def dropUserTable():
    c.execute('DROP TABLE userstable')


def create_userInfoTable():
    c.execute('CREATE TABLE IF NOT EXISTS usersInfoTable(username TEXT, age INTEGER, sex TEXT, cp REAL, trestbps REAL, chol REAL, fbs REAL, ecg REAL,hrt REAL, exg  REAL, op INTEGER,slp REAL, ca REAL, thal REAL, risk REAL)')


def view_allUserInfo():
    c.execute('SELECT * FROM usersInfoTable')
    data = c.fetchall()
    return data


def view_userInfo(username):
    c.execute('SELECT * FROM usersInfoTable WHERE username=?', (username,))
    data = c.fetchall()
    return data


def add_userdetails(db_lst):
    c.execute('INSERT INTO usersInfoTable(username,age,sex,cp,trestbps,chol,fbs,ecg,hrt,exg,op,slp,ca,thal,risk ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
              tuple(db_lst))
    conn.commit()


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',
              (username, password))
    conn.commit()


def login_user(username):
    c.execute('SELECT * FROM userstable WHERE username=?',
              (username,))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


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
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download File </a>'


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
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

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
    elif(choice == "Login"):
        st.markdown(
            '<div style=color:#001866;text-align:center;font-size:40px;font-family:courier;font-weight:bold>HEART DISEASE PREDICTOR</div>', unsafe_allow_html=True)
        img = Image.open('cg.png')
        st.image(img, width=700)

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input(
            "Password", type="password").encode('utf-8')
        if st.sidebar.checkbox("Login/Logout"):
            create_usertable()
            data = login_user(username)
            if data:
                data = data[0]
                if bcrypt.checkpw(password, data[1]):
                    st.success("Logged In as {}".format(username))
                    logged_in_user = data[0]
                    if(logged_in_user == 'admin'):
                        st.subheader("Welcome to the Admin Portal")
                        admin_menu = ["ViewUsers", "ViewUserDetails"]
                        admin_choice = st.selectbox("Menu", admin_menu)
                        if(admin_choice == "ViewUsers"):
                            user_result = view_all_users()
                            clean_db = pd.DataFrame(user_result, columns=[
                                                    "Username", "Password"])
                            st.dataframe(clean_db)
                        elif(admin_choice == "ViewUserDetails"):
                            create_userInfoTable()
                            user_details_result = view_allUserInfo()
                            clean_db = pd.DataFrame(user_details_result, columns=[
                                                    "Username", "Age", "Sex", "Chest Pain", "Resting Blood Pressure", "Cholestrol", "Fasting Blood Sugar", "ECG", "Maximum Heart Rate", "Exercise incuced Angina", "ST Depression", "Slope Of The Peak Exercise", "vessels colored", "thalium stress", "Heart Disease Risk"])
                            st.dataframe(clean_db)

                    else:
                        login_menu = ["Predict", "My Profile"]
                        login_choice = st.sidebar.selectbox(
                            "Login Menu", login_menu)
                        if(login_choice == "Predict"):
                            st.sidebar.markdown(
                                '<div style=color:#006080;font-size:20px;font-family:courier;font-weight:bold>ENTER PATIENT DETAILS:</div>', unsafe_allow_html=True)
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Age:</div>', unsafe_allow_html=True)
                            age = st.sidebar.number_input(" ", value=1)
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Sex:</div>', unsafe_allow_html=True)

                            sex = st.sidebar.radio(
                                ' ', ['Male', 'Female'], index=0)
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Chest Pain:</div>', unsafe_allow_html=True)
                            cp = st.sidebar.radio(
                                '   ', ['1', '2', '3', '4'], index=0)
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Resting blood pressure:</div>', unsafe_allow_html=True)
                            tresbps = st.sidebar.number_input("           ")
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Cholestrol:</div>', unsafe_allow_html=True)
                            chol = st.sidebar.number_input(" ")
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Fasting blood sugar:</div>', unsafe_allow_html=True)
                            fbs = st.sidebar.number_input(
                                "                     ")
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Resting electrocardiographic results:</div>', unsafe_allow_html=True)
                            ecg = st.sidebar.number_input("                  ")

                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Maximum Heart Rate:</div>', unsafe_allow_html=True)
                            hrt = st.sidebar.number_input("  ")
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Exercise Induced Angina:</div>', unsafe_allow_html=True)

                            exg = st.sidebar.radio(
                                "     ", ["0", "1", "2"], index=0)

                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>ST Depression Induced By Exercise Relative To Rest:</div>', unsafe_allow_html=True)
                            op = st.sidebar.number_input(
                                "                           ")
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Slope Of The Peak Exercise ST Segment:</div>', unsafe_allow_html=True)
                            slp = st.sidebar.number_input("    ")
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>Number of major vessels colored:</div>', unsafe_allow_html=True)

                            ca = st.sidebar.radio(
                                "             ", ["0", "1", "2", "3"], index=0)
                            st.sidebar.markdown(
                                '<div style=color:#3973ac;font-size:16px;font-weight:bold;font-family:courier>thalium stress result:</div>', unsafe_allow_html=True)
                            thal = st.sidebar.number_input("                 ")

                            sex1 = get_sex(sex)
                            cp1 = get_cp(cp)

                            ca1 = get_ca(ca)
                            exg1 = get_exg(exg)
                            db_lst = [username, age, sex, cp1, tresbps, chol, fbs,
                                      ecg, hrt, exg1, op, slp, ca1, thal]
                            lst = [age, sex1, cp1, tresbps, chol, fbs,
                                   ecg, hrt, exg1, op, slp, ca1, thal]

                            sample_data = np.array(lst).reshape(1, -1)
                            if st.sidebar.button("Predict"):

                                model = pickle.load(
                                    open('heart_disease.sav', 'rb'))
                                Prediction = model.predict(sample_data)
                                if Prediction == 0.:
                                    st.markdown(
                                        '<div style=color:black;font-size:22px;font-family:courier>Heart disease not detected</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(
                                        '<div style=color:black;font-size:22px;font-family:courier>Heart disease detected</div>', unsafe_allow_html=True)

                                img = Image.open('hb3.png')

                                st.image(img, width=700)
                                create_userInfoTable()
                                db_lst.append(int(Prediction[0]))
                                add_userdetails(db_lst)
                        else:
                            create_userInfoTable()
                            user_details_result = view_userInfo(username)
                            clean_db = pd.DataFrame(user_details_result, columns=[
                                                    "Username", "Age", "Sex", "Chest Pain", "Resting Blood Pressure", "Cholestrol", "Fasting Blood Sugar", "ECG", "Maximum Heart Rate", "Exercise incuced Angina", "ST Depression", "Slope Of The Peak Exercise", "vessels colored", "thalium stress", "Heart Disease Risk"])
                            st.subheader("My Past Medical Records")
                            st.dataframe(clean_db)
            else:
                st.warning("Invalid Credentials!")
    else:
        st.subheader("SignUp")
        new_user = st.text_input("Username")
        new_password = st.text_input(
            "Password", type="password").encode('utf-8')

        if st.button("SignUp"):
            create_usertable()
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(new_password, salt)
            add_userdata(new_user, hashed)
            st.success("registered")
            st.info("go to login")
    st.sidebar.markdown(
        '<div style=color:#006080;font-size:20px;font-family:courier;font-weight:bold>ABOUT US</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div style=color:black;font-size:12px;font-family:times>Every year a large amount of data is generated in the healthcare industry but they are not used effectively.So here is a system that will be able to communicate with people’s mind and help them in getting prepared based on their medical history.By using patient’s input features such as sex, cholesterol, blood pressure and much more the prediction of the presence of heart disease. So this model depicts whether or not a person is at a risk of having a heart disease.</div>', unsafe_allow_html=True)

    Image.open('bulb3.jpg').convert('RGB').save('new2.png')
    st.sidebar.image('new2.png', width=40)

    st.sidebar.markdown(
        '<div style=color:black;font-size:12px;font-family:courier>Use the values from the dataset to see different results.</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
