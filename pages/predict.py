import streamlit as st
import joblib
import numpy as np
# Page configuration
st.set_page_config(page_title='Betta Ai', page_icon='📈', layout="wide", initial_sidebar_state="collapsed")
st.sidebar.title("Hi There!")
st.sidebar.markdown("Take a look at my website :shark:")
# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'prediction_steps' not in st.session_state:
    st.session_state.prediction_steps = 'first_phase'
if 'user_details' not in st.session_state:
    st.session_state.user_details = []

# Predefined chats
chats = {
    ('wake up', 'wake', 'betta', 'are you there', 'listen'): [
        'Hello, do you need any help?',
        'Hi there, how can I help you today, sir?',
        'Huh, did you call for me?',
        'I hear you sir. Any help needed?'
    ],
    ('what is your name', 'what can I call you', 'name'): [
        'Hi, my name is Betta, I am your assistant.',
        'My name is Betta, what is yours?',
        'Betta, how can I help you today?'
    ],
    ('can do', 'abilities'): [
        'I can help you predict the price of a house.',
        'I can also predict the size of your house, sir.'
    ],
}

# Function to get a response based on prompt
def get_value(prompt):
    for keys in chats.keys():
        for key in keys:
            if prompt in key or key in prompt:
                return random.choice(chats[keys])
    return 'Unknown command due to limited information right now 😄..'

def predict(prompt):
    if st.session_state.prediction_steps == 'first_phase':
        st.session_state.prediction_steps = 'second_phase'
        return '''Now, please provide details to predict the price of your house 😊. Ordered in (category -- area --title_deed -- repair --room_number -- floor_house -- total_floors -- title_length -- floor_status -- price_1m2)'''
    elif st.session_state.prediction_steps == 'second_phase':
        try:
            data =[]
            details = prompt.split(',')
            for detail in details:
                data.append(float(detail.strip()))
            data[-1] = np.log1p(data[-1])
            st.session_state.user_details.append(data)

            st.session_state.prediction_steps = 'third_phase'
            return f'Details received. Please confirm or add more.{data}'
        except:
            return 'Data in wrong shape'
    elif st.session_state.prediction_steps == 'third_phase':
        if prompt =='confirm':
            message = process_details(st.session_state.user_details)
            st.session_state.prediction_steps = 'first_phase'
            return message
        else:
            st.session_state.prediction_steps = 'second_phase'
            return 'Please provide details'
    elif st.session_state.prediction_steps == 'final_phase':
        # All details collected, call the processing function
        process_details(st.session_state.user_details)
        message = 'Details processed and prediction is being made...'
        st.session_state.prediction_steps = 'first_phase'
        return message

# ex1 : 0,51.5,0,1,1.0,4.0,8.0,49,2,5050.0
# ex2   1,100.0,1,1,4.0,2.0,2.0,52,3,2370.0
# ex3   0,82.0,1,1,2.0,15.0,16.0,51,3,1780.0
# ex4   1,52.0,1,1,2.0,8.0,9.0,46,3,1670.0

def process_details(details):
    model = joblib.load('Models/regression/pipeline_model1.joblib')
    pred = model.predict(details)
    st.session_state.user_details.clear()
    return np.expm1(pred)

# Chat input field
prompt = st.chat_input("Ask what you need?")

# If there is input, add it to the conversation history
if prompt:
    st.session_state.messages.append({"name": "User", "avatar": 'images/user.png', "message": f"{prompt}"})
    if 'predict' in prompt or st.session_state.prediction_steps in ['second_phase','third_phase','final_phase']:
        response = predict(prompt)
    else:
        response = get_value(prompt)
    st.session_state.messages.append({"name": "Deep Ai", "avatar": 'images/robot.png', "message": response})

# Display the conversation history
for chat in st.session_state.messages:
    st.chat_message(name=chat["name"], avatar=chat["avatar"]).write(chat["message"])
