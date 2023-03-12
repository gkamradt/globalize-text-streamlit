import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
I want you to act as an English translator, spelling corrector and improver. 

I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. 

I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. 

Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations.

Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    JOBS: {jobs}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "jobs", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title='Better Grammar Ally', layout="wide", page_icon='✍️')

st.markdown("# Better thoughts with AI ✨")

with st.container():
   st.markdown("Improve your thoughts, messages, and emails by 10X with OpenAI. \n\n Made by [Prithvi](https://twitter.com/iprithvitharun).")

st.markdown("## Your message")

def get_api_key():
    input_text = st.text_input(label="OpenAI API key ", placeholder="sk-XXXXXXXXXXXXXXXXXXX", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2, col3 = st.columns(3)
with col1:
    option_tone = st.selectbox(
        'Select the tone you want the message to be?',
        ('Formal', 'Casual', 'Sad', 'Funny'))

with col2:
    option_jobs = st.selectbox(
        'Character',
        ('Product Manager', 'UX Writer', 'Designer', 'Developer', 'Law officer'))

with col3:
    option_dialect = st.selectbox(
        'Dialect',
        ('American English', 'British English'))                        

def get_text():
    input_text = st.text_area(label="Your thoughts", label_visibility='visible', placeholder='Enter your thoughts here.', key="email_input")
    return input_text

email_input = get_text()


if len(email_input.split(" ")) > 700:
    st.write("The maximum length is 700 words.")
    st.stop()


# def update_text_with_example():
#    print ("in updated")
#    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

# st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Improved message:")

if email_input:
    if not openai_api_key:
        st.error('Enter your OpenAI API key to continue. [Find API key](https://platform.openai.com/account/api-keys)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, jobs=option_jobs, dialect=option_dialect, email=email_input)
    
    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)