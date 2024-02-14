import streamlit as st
import openai
#from config import OPEN_API_KEY
import json
#OPEN_API_KEY='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'
openai.api_key=OPEN_API_KEY



if 'key' not in st.session_state:

    st.session_state.key={
   
    '0': 'Ask the questions in this format "what Position are you  hiring for?"',
    '1':'Ask the questions in this format"what are the skills required for this position"',
    '2': 'Ask the questions in this format"How many years of experience is needed ?"',
    '3': 'Ask the questions in this format"What is the minimum education requirement ?"',
     '4':'Ask the questions in this format"What location is the position based in ?"',
    '5':'Ask the questions in this format"Ask Is this position remote (Yes/no)" ?',
    
    }


st.title("Hiring Recruitement Chatbot")
page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://mcdn.wallpapersafari.com/335/73/76/VbjnPw.jpg");
  background-size: cover;
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  
if bool(st.session_state.key) == False:
    st.session_state.messages.append({'role':'system','content':"Return summary of all details as a dictionary.For keys as 'Postion','Skills','Experience level' new line'Education' new line'Remote'.Display all in new line on after another"})
    resp=openai.ChatCompletion.create(
                                model='gpt-3.5-turbo',
                                messages=st.session_state.messages,
                                temperature=0.7)
    response=resp['choices'][0]['message']['content']    
    st.subheader("Summary of collected requirements!")
    for i in response:
        st.markdown(response[i])
        
    with st.chat_message("Assistant"):
        st.write("Your requirements have been saved succesfully!")

# Display chat messages from history on app rerun
else:
    for message in st.session_state.messages:
        if message["role"] == 'assistant':
           
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if message["role"] == 'user':
            
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        

# React to user input

    for key in  dict(st.session_state.key):
        
        i=st.session_state.key[key]
       
        st.session_state.messages.append({'role':'system','content':f"{i}"})
        
        resp=openai.ChatCompletion.create(
                            model='gpt-3.5-turbo',
                            messages=st.session_state.messages,temperature=0.7)
        response=resp['choices'][0]['message']['content']
        #st.write(response)

        
        with st.chat_message('Assistant'):
            st.markdown(response)
        
        if prompt := st.chat_input("here",key=''):
        # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.messages.append({"role": "user", "content": prompt})

            del st.session_state.key[key]

        else:
            break
        st.rerun()

    