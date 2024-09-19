import streamlit as st
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from packaging.version import Version
import re



nltk.download('punkt_tab') 
responses = {
    "hello": "Hi there! How can I help you today?",
    "how are you": "I'm just a program, but thanks for asking!",
    "bye": "Goodbye! Have a great day!",
    "what is your name": "I am a speech-enabled chatbot.",
}

def generate_response(user_input):
    """Generate a response based on user input."""
    # Normalize the input: lower case and remove punctuation
    normalized_input = re.sub(r'[^\w\s]', '', user_input.lower())
    
    if normalized_input in responses:
        return responses[normalized_input]
    
    return "I'm sorry, I don't understand that."

def transcribe_speech():
    """Transcribe speech input into text using speech recognition."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio_text = r.listen(source)
        st.info("Transcribing... Please wait.")

        try:
            text = r.recognize_google(audio_text)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Error with the speech recognition service: {e}"

def main():
    """Main function to run the Streamlit app."""
    st.title("Speech-Enabled Chatbot")

    user_input_option = st.radio("Choose input method:", ["Text Input", "Speech Input"])

    if user_input_option == "Text Input":
        user_input = st.text_input("You: ")
        if st.button("Send"):
            response = generate_response(user_input)
            st.success(f"Bot: {response}")

    elif user_input_option == "Speech Input":
        if st.button("Start Recording"):
            text = transcribe_speech()
            if text:
                response = generate_response(text)
                st.success(f"You said: {text}")
                st.success(f"Bot: {response}")

if __name__ == "__main__":
    main()
    