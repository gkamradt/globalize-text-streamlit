import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI


template = """
    Below is an message that may be poorly worded.
    Your goal is to:
    - Improve the meaning of the message, fix grammatical errors, and retain text formatting used
    - Convert the input text to a specified tone
    - Convert the input text from the point of view of the specified character

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Casual: Went to Barcelona for the weekend. Lots to tell you.

    Here are some information about the different characters:
    - Technical Writer: As a tech writer, you write technical documentation, manuals, and guides for software, hardware, and technology products.
    - Designer: As a graphic designer, you design graphics and visual materials for various media such as websites, advertisements, and branding. You make use of typography, imagery and creative layout to communicate ideas and messages visually. Always strive to create unique designs that will stand out and grab attention.
    - Product Manager: As a product manager, you oversee the development and marketing of a product, identify customer needs, and work with engineers and designers to create a product roadmap.
    - Marketer: As a marketing expert, you help the user develop marketing strategies and campaigns, conduct market research, and provide branding and advertising advice.
    - Frontend developer: As a Senior Frontend developer, you will rewrite the input message with your extensive knowledge in frontend development.
    - UX Writer: As a UX writer, you have extensive knowledge about the Nielsan Norman group content and will improve messages that will be most effective in grabbing users' attention and encouraging them to learn more about the product.
    
    Below is the message, tone, and dialect:
    MESSAGE: {message}
    TONE: {tone}
    CHARACTER: {character}
    
    YOUR {character} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "character", "message"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title='Better Grammar Ally', layout="wide", page_icon='✍️')

st.markdown("# Thoughts made better with AI ✨")

with st.container():
   st.markdown("Fix typos, grammar issues, improve sentence structure to make your messages more readable and understandable. \n\n Made with OpenAI and LangChain by **Prithvi**.")

st.markdown("## Your message")

def get_api_key():
    input_text = st.text_input(label="OpenAI API key", type="password", placeholder="sk-XXXXXXXXXXXXXXXXXXX", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Select the tone you want the message to be?',
        ('Formal', 'Casual', 'Sad', 'Funny'))

with col2:
    option_character = st.selectbox(
        'Character',

        ('Product Manager', 'Technical Writer', 'Designer', 'Marketer', 'Frontend developer', 'UX Writer' ))                   
def get_text():
    input_text = st.text_area(label="Your message", label_visibility='visible', placeholder='Enter your thoughts here.', key="message_input")
    return input_text

message_input = get_text()


if len(message_input.split(" ")) > 700:
    st.write("The maximum length is 700 words.")
    st.stop()


# def update_text_with_example():
#    print ("in updated")
#    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

# st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Improved message:")

if message_input:
    if not openai_api_key:
        st.error('Enter your OpenAI API key to continue. [Find API key](https://platform.openai.com/account/api-keys)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_message = prompt.format(tone=option_tone, character=option_character, message=message_input)
    
    formatted_message = llm(prompt_with_message)

    st.write(formatted_message)