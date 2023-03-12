import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
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

st.markdown("## Your thoughts")

def get_api_key():
    input_text = st.text_input(label="OpenAI API key ", placeholder="sk-XXXXXXXXXXXXXXXXXXX", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Tone',
        ('Formal', 'Casual', 'Sad', 'Funny'))
    
with col2:
    option_dialect = st.selectbox(
        'Dialect',
        ('American', 'British', 'Indian'))        

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

st.markdown("### Your improved thoughts 👇")

if email_input:
    if not openai_api_key:
        st.error('Enter your OpenAI API key to continue. [Find API key](https://platform.openai.com/account/api-keys)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)
    
    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)