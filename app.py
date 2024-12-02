import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import os

# Configure your Google API key for Gemini
Google_api_key = "AIzaSyCdjIsQuCU9J9hJKVZdUh4ATgnQNIIYvm4"
genai.configure(api_key=Google_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to generate response using Gemini
def generate_response(input_text):
    try:
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

# Speech to Text function
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Reduce noise
        print("Listening for your speech...")

        try:
            # Capture the audio
            audio = recognizer.listen(source, timeout=5)  # 5 seconds timeout
            print("Processing your speech...")

            # Convert speech to text
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text

        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
            return None

        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None

        except sr.RequestError as e:
            print(f"Error with the recognition service: {e}")
            return None

# Text to Speech function
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")  # Save the response as an mp3 file
    os.system("start response.mp3")  # Play the audio on Windows (use 'open' on macOS or 'xdg-open' on Linux)

# Streamlit UI and Logic

# Streamlit page setup
st.title("Speech to Text with Gemini Response")
st.write("Click 'Record' to start recording your voice. Once finished, click 'Stop'.")

# Button to record
record_button = st.button("Record")

if record_button:
    st.write("Recording started...")

    # Call the speech to text function
    recognized_text = speech_to_text()

    if recognized_text:
        st.write(f"You said: {recognized_text}")
        
        # Get response from Gemini API
        response_text = generate_response(recognized_text)
        st.write(f"Gemini Response: {response_text}")
        
        # Convert response text to speech
        text_to_speech(response_text)
    else:
        st.write("No recognized speech. Try again.")
    
    st.write("Recording stopped.")

