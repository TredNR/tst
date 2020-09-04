import streamlit as st
import datetime

st.title ("Test using different possibilities")

st.header ("some text")

st. subheader ("littel text")

st.text ('text')

st.markdown ("### Bolt")

st.success ("Successful")

st.info("Information")

st.warning("This is a warning")

st.error ("This is an error")

st.exception ("NameError ('name three not defined')")

st.help(range)

st.write("Test with write")

st.write(range(10))

from PIL import Image
img = Image.open("C:/Users/tred1/PycharmProjects/pythonProject2/image.jpg")
st.image(img, width=300, caption="Simple Image")

if st.checkbox ("Show/Hide"):
    st.text("Showing of Hiding Widget")

status = st.radio ("What is your status", ("Active", "Inactive"))
if status =='Active':
    st.success("You are Active")
else:
    st.warning("Inactive, Active")

occupation = st.selectbox("Your Occupation", ["Programmer", "DataScientist", "Doctor", "Businessman"])
st.write("You selected this option ", occupation)

location = st.multiselect("Where do you work?", ('London', 'New York', 'Moscow', 'Kiev'))
st.write("You selected", len(location), 'location')

level = st.slider('What is your level?', 1.0,5.0)

st.button("Simple Button")

if st.button("About"):
    st.text("Maybe... streamlit is coll")

firstname = st.text_input("Enter Your Firstname", "Type Here")
if st.button("Submit", key=1):
    result = firstname.title()
    st.success(result)

massage =st.text_area("Enter Your massage", "Type Here")
if st.button("Submit", key=2):
    result = massage.title()
    st.success(result)

today = st.date_input("Today is ", datetime.datetime.now())

the_time = st.time_input("The time is", datetime.datetime.now())

st.text ("Display JSON")
st.json({'name': 'Konstantin', 'gender': 'male'})

st.text("Display Raw Code")
st. code ("import numpy as np")

with st.echo():
    #Funny comment
    import pandas as pd
    df = pd.DataFrame()


import time
my_bar = st.progress(0)
for p in range(1):
    my_bar.progress(p+1)
    time.sleep(0)

with st.spinner ("Waiting"):
    time.sleep(0)
st.success("Finished :3")

#st.balloons()

st.sidebar.header("About")
st.sidebar.text("This is Streamlit tut")

@st.cache
def run_fxn():
    return range(100)

st.write(run_fxn())


