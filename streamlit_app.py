import streamlit as st
from openai import OpenAI

import os

from openai import OpenAI
from openai.types.responses import ResponseOutputMessage

def find_ticketmaster_events(input_text):
  print("In find_ticketmaster_events")
  client = OpenAI()

  resp = client.responses.create(
      model="gpt-4.1-mini",
      tools=[
          {
              "type": "mcp",
              "server_label": "weird-red-beetle",
              "server_url": "https://weird-red-beetle.fastmcp.app/mcp",
              "require_approval": "never",
          },
      ],
      input=input_text,
  )

  user_texts = []
  for item in resp.output:
      if isinstance(item, ResponseOutputMessage):
          for c in item.content:
              if hasattr(c, "text"):
                  user_texts.append(c.text)

  # Join them for display
  st.write("\n\n".join(user_texts))


print("At the start")
os.environ['OPENAI_API_KEY']=st.secrets['OPENAI_API_KEY']



# Show title and description.
st.title("Smart Event Planner Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
user_city = st.text_input("Enter the city for music events:", key="city")
user_timeline = st.text_input("Enter the month and year:", key="timeline")
user_music_genre = st.text_input("Enter a genre (or 'none'):", key="genre")
if user_city:
    print(f"user city is {user_city}")

if user_timeline:
    print(f"user timeline is {user_timeline}")
if user_music_genre:
    print(f"user music genre is {user_music_genre}")
tm_input = "Find music events in city " + user_city + " for genre " + user_music_genre + " for " + user_timeline
print(f"user prompt is {tm_input}")

if user_city and user_timeline and user_music_genre:
    st.write("Initiating event search...")
    find_ticketmaster_events(tm_input)
    
