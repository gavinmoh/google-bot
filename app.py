from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationBufferMemory
from langchain.agents import  load_tools, initialize_agent


def main():
    load_dotenv()
    st.set_page_config(page_title='Google Bot 🤖', page_icon="🤖")
    st.header("ChatGPT + Google = 🚀")
    

    if "memory" not in st.session_state:
            st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []   

  
    query = st.text_input(
        "Your wish is my command...",
        placeholder="How may I assist you?",
    )
    if query:
        with st.spinner("Thinking...🤔"):
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
            tools = load_tools(['google-serper', 'wikipedia'])
            memory = ConversationBufferMemory(memory_key="chat_history")
            agent = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory, verbose=True)

            with get_openai_callback() as callback:
                result = agent.run(query)
                print(callback)
                st.success(result, icon="🤖")

            st.session_state.messages.append("🐵: {}".format(query))
            st.session_state.messages.append("🤖: {}".format(result))
        
    with st.expander("Show chat history"):
        if st.session_state.messages != []:
            for message in reversed(st.session_state.messages):
                st.write(message)    

if __name__ == '__main__':
    main()