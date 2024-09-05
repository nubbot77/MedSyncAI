import streamlit as st
import pandas as pd
import hashlib
from streamlit_option_menu import option_menu
from db import get_database
from model import response

st.set_page_config(layout='wide',page_title='MedSyncAI')

hide_st_style = """
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility:hidden;}
            header {visibility:hidden;}
            </style>
"""

st.markdown(hide_st_style,unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options = ['Home',"Profile"],
    icons=['pencil-fill','bar-chart-fill'],
    orientation='horizontal',
)

if selected=='Home':



    st.title("MedSyncAI ---- Integrated Medical Adherence and Management Platform")

    st.text("A comprehensive platform designed to enhance patient adherence to medical treatments and streamline healthcare management processes.")


    db = get_database()

    class User:
        def __init__(self, username, password, email):
            self.username = username
            self.password = password  # Hash password for security
            self.email = email

    def user_exists(username):
        collection = db["registered_users"]

        user = collection.find_one({"username": username})

        return user is not None

    def store_user(user):
        # Replace with your actual database or file storage logic
        collection = db["registered_users"]

        user_data = user.__dict__
        result = collection.insert_one(user_data)

        if result.inserted_id:
            print("User has been successfully registered")
        else:
            print("Error in registering")
    def get_user(username, password):
        collection = db["registered_users"]

        

        user = collection.find_one({"username": username, "password": password})
        if user:
            return user["username"]
        else:
            print("Couldn't retrieve user")
            return None

    def get_session_user_id():
        if "user_id" in st.session_state:
            return st.session_state.user_id
        else:
            return None

    def get_current_user():
        collection = db["registered_users"]
        current_user_id = get_session_user_id()
        user = collection.find_one({"_id": current_user_id})
        return user

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def signup():
        st.title("Signup")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")

        if st.button("Signup"):
            if username and password and email:
                # Check if username already exists
                if not user_exists(username):
                    
                    user = User(username, password, email)
                    store_user(user)
                    st.success("Signup successful!")
                else:
                    st.error("Username already exists.")
            else:
                st.error("Please fill in all fields.")
    def login():
        st.title("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username and password:
                # Retrieve user data from database or file (replace with appropriate retrieval)
                user = get_user(username, password)
                if user:
                    st.success("Login successful!")
                    # Redirect to user profile or other pages
                else:
                    st.error("Invalid username or password.")
            else:
                st.error("Please fill in all fields.")  

    def profile(user):
        st.title("Profile")
        st.write(f"Username: {user.username}")
        st.write(f"Email: {user.email}")
        # Add more profile fields as needed

    def is_user_logged_in():
        if "user_id" in st.session_state:
            return True
        else:
            return False

    def main():
        st.title("User Management")

        option = st.radio("Choose an option", ["Signup", "Login"])
    
        if option == "Signup":
            signup()
        elif option == "Login":
            login()

        # Assuming you have a way to get the current logged-in user
        
        # Replace with appropriate logic
        # current_user = get_current_user()  # Replace with appropriate logic
        # if current_user:
        #     profile(current_user)
        # if is_user_logged_in():
        #     st.sidebar.markdown(f"**[Profile](/profile)**", unsafe_allow_html=True)
        # else:
        #     st.sidebar.markdown(f"**[Login](/login)**", unsafe_allow_html=True)
        


    if __name__ == "__main__":
        main()                      

if selected=='Profile':
    col1,col2 = st.columns(2,gap='medium')
    with col1:


        db = get_database()

        class User_Info: 
            def __init__(self,fullname, age, sex, medical_history, prescribed_medicines, symptoms, phone_number):
                self.fullname = fullname
                self.age = age
                self.sex = sex 
                self.medical_history = medical_history
                self.prescribed_medicines = prescribed_medicines
                self.symptoms = symptoms 
                self.phone_number = phone_number


        def go_to_model():
            st.title("Welcome to the model page!")
            st.write("Here we go")


        def store_data(user):
            collection = db["user_data"]
            user = user.__dict__
            
            existing_user = collection.find_one(user)

            if not existing_user:
                result = collection.insert_one(user)
                if result:
                    return True
                else:
                    return False
            else:
                st.text("Your detailed profile has already been created")
                st.button("Click here to be redirected further!", on_click=go_to_model)



        st.title("MedSyncAI")
        st.text("Hello, ")
        st.text("Please the following information so we can get to know more about you!")

        col3,col4 = st.columns(2,gap='large')
        with col3:
            full_name  = st.text_input("Enter your Full name")
            sex = st.text_input("Please enter your sex")
        with col4:
            age = st.number_input("Please enter your age")
            phone_numbe = st.number_input("Please enter your phone number: ")
            # symptoms = ""
            # prescribed_medicines = ""
            # if medical_history:
            #     prescribed_medicines = st.text_input("Please enter the medicines you take: ")
            # else:
            #     st.text("Are you experiencing any symptoms")    
            #     symptoms = st.text_input("Please input your symptoms: ")
            
        def fetch_med_info():
            collection = db["user_data"]

            # Get the current user's full name from the input fields
            current_user_name = full_name

            # Define the projection to include only desired fields
            projection = {"_id": 0, "medical_history": 1, "symptoms": 1, "prescribed_medicines": 1}

            # Find the current user's document based on full name
            user_data = collection.find_one({"fullname": current_user_name}, projection=projection)

            if user_data:
                # Extract the desired fields from the user data
                medical_history_fetched = user_data["medical_history"]
                symptoms_fetched = user_data["symptoms"]
                prescribed_medicines_fetched = user_data["prescribed_medicines"]
                print("Data Fetched and sent ofc")  
                # Return the fetched information
                return medical_history_fetched, symptoms_fetched, prescribed_medicines_fetched
            
            else:
                st.text("No user found with that name. Please check the entered name.")
            
        submit = st.button("Submit")
        # if submit:

        #     user = User_Info(full_name, age, sex, medical_history, prescribed_medicines, symptoms, phone_numbe)
        #     data = store_data(user)
        #     if data:
        #         print("Successfully stored data")
        #         st.markdown(f"[Get Results](model.py)")
        #         fetch_med_info()

        #     else:
        #         print("Data not stored")

    with col2:
        st.subheader("Your health level")
        with st.form(key='my_form'):
            hist = st.text_input('Please enter your medical history (If any)')
            symp = st.text_input('Are you experiencing any symptoms:')
            bp = st.number_input('what is your Blood Pressure Levels:')
            sugar = st.number_input('what is your Sugar Levels:')
            pluse = st.number_input('what is your Pulse rate:')
            oxg = st.number_input('what is your SpO2 Levels:')

            submit_button = st.form_submit_button(label='Submit')
            print(submit_button)

            if submit_button:
                question=f'''
                According to vitals, is Patient is taking medicines or not?
                blood pressure = {bp}, patient history = {hist}, patient symptoms = {symp}, sugar level = {sugar}, pulse rate = {pluse}, SpO2 = {oxg}'''
                st.write(response(question))
                st.write("___")

            



