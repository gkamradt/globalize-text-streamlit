import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI


template = """
Act as UX Writer with extensive knowledge about Nielsan Norman Group content + Carbon Design System content style guides + Mailchimp content style guide + Intuit's Content design system. You should not mention Nielsen Norman Group’s or Carbon Design System’s content style guide in the response.

You will help me with multiple examples based on the requests. You will list the examples in a list.

    Below is the message:
    MESSAGE: {message}
    
    YOUR {message} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["message"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title='AI placeholder text generator', layout="wide", page_icon='✍️')

def get_api_key():
    input_text = st.text_input(label="Your OpenAI API key", type="password", placeholder="sk-XXXXXXXXXXXXXXXXXXX", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()
                 
def get_text():
    input_text = st.text_area(label="What do you need?", label_visibility='visible', placeholder='Ask and you shall receive.', key="message_input")
    return input_text

message_input = get_text()

if len(message_input.split(" ")) < 2:
    st.write("Try explaining a bit more.")
    st.stop()


if len(message_input.split(" ")) > 100:
    st.write("Make sure your word count is less than 100 and try again.")
    st.stop()




# def update_text_with_example():
#    print ("in updated")
#    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

# st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Examples:")

if message_input:
    if not openai_api_key:
        st.error('Enter your OpenAI API key to continue. [Find API key](https://platform.openai.com/account/api-keys)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_message = prompt.format(message=message_input)
    
    formatted_message = llm(prompt_with_message)

    st.write(formatted_message)

st.button('Try again', type="secondary")