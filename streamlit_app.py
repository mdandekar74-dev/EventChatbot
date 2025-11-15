import streamlit as st
from openai import OpenAI
import os
from openai.types.responses import ResponseOutputMessage

#######################

########################

def find_ticketmaster_events(input_text):
  print("In find_ticketmaster_events")
  
  # Call the OpenAI API with the MCP tool to get Ticketmaster events
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

###############
def get_hotel_info(input_prompt):

    st.write("Getting hotel info...")
    
    resp = client.responses.create(
       model="gpt-4.1-mini",
       input=input_prompt
       )

    user_texts = []
    for item in resp.output:
         if isinstance(item, ResponseOutputMessage):
          for c in item.content:
              if hasattr(c, "text"):
                  user_texts.append(c.text)

       # Join them for display
    st.write("\n\n".join(user_texts))

    user_response = st.text_input("would you like to search for some sightseeing places in the city? yes/no ")

    if user_response=="yes":
        info_prompt = "find sightseeing places in " + user_destination_city
        st.write("Getting more info...")
    
        resp = client.responses.create(
           model="gpt-4.1-mini",
           input=info_prompt
           )

        user_texts = []
        for item in resp.output:
             if isinstance(item, ResponseOutputMessage):
              for c in item.content:
                  if hasattr(c, "text"):
                      user_texts.append(c.text)

         # Join them for display
        st.write("\n\n".join(user_texts))

###############
def get_flight_info(input_prompt):
    st.write("Getting flight info...")
    print(input_prompt)
    resp=client.responses.create( model="gpt-4.1-mini",
    input=input_prompt)

    user_texts=[]
    for item in resp.output:
      if isinstance(item, ResponseOutputMessage):
          for c in item.content:
              if hasattr(c, "text"):
                  user_texts.append(c.text)

    # Join them for display
    st.write("\n\n".join(user_texts))
    

##########
print("At the start")
os.environ['OPENAI_API_KEY']=st.secrets['OPENAI_API_KEY']
client = OpenAI()

# Show title and description.
st.title("Smart Event Planner Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-4.1-mini model to generate responses. "    
    "It can help you find music events and nearby hotels based on your preferences." 
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
user_destination_city = st.text_input("Enter the city for music events:", key="city")
user_timeline = st.text_input("Enter the month and year:", key="timeline")
user_music_genre = st.text_input("Enter a genre (or 'any'):", key="genre")


if user_destination_city and user_timeline and user_music_genre:
  tm_input = "Find music events in city " + user_destination_city + " for genre " + user_music_genre + " for " + user_timeline
  print(f"user prompt is {tm_input}")
   
  st.write("Initiating music event search...")
  find_ticketmaster_events(tm_input)

  #user_eventDate = st.text_input("Please enter the date for the music event you would like to attend ")
  #if user_eventDate:
  user_eventVenue = st.text_input("Please enter the venue for the music event you would like to attend")
  if user_eventVenue:      
    input_prompt = "find hotels for city " + user_destination_city + " near " + user_eventVenue
    print(input_prompt)
    get_hotel_info(input_prompt)
 
       



