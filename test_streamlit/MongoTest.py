import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.title("Test with MongoDB")

#@st.cache(hash_funcs={MongoClient: id})
#def get_client():
#    return MongoClient("mongodb://127.0.0.1/admin")

enter = st.text_input("Address",'mongodb://localhost:27017')
if st.button("Enter", key=1):
    result = enter.title()
    st.success(result)

client = MongoClient(enter)

# ------------- Настройка выбора коллекции --------------

#client = get_client()

db = client.list_database_names()
c = st.write(db)
select1 = st.selectbox("Select a database", db)
selected_database = client[select1]

a = selected_database.list_collection_names()
b = st.write(a)
select = st.selectbox("Select a collection", a)
selected_filename = selected_database[select]

collection_select = pd.DataFrame(list(selected_filename.find()))

# ------------------ Превью коллекции ---------------------

if st.checkbox("Preview collection", key=1):
    number = st.number_input("Number of Rows to View",1, 200)
    st.dataframe(collection_select.head(number))

# --------------- Показать всю коллекцию -----------------

if st.checkbox("Show all collection", key=2):
    view = st.write(collection_select)

# ---------------------- Тип данных ------------------------

if st.checkbox("Data Types in the collection", key=3):
    st.write(collection_select.dtypes)

# --------- Общая информация о кол-ве стобцов/строк ---------

if st.checkbox("Shape of Dataset", key=4):
    st.text("Number of Rows")
    st.write(collection_select.shape[0])
    st.text("Number of Columns")
    st.write(collection_select.shape[1])

# --------------- Нарисуем какие-нибудь графики ---------------

if st.checkbox("Plot with select columns", key=5):
    st.text("Works extremely unstable, needs to be improved")
    type_of_plot = st.selectbox("Select Type of Plot", ["Area", "Bar", "Line", "Hist", "Box", "Kde"])

    all_columns_names = collection_select.columns.tolist()
    selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

    if st.button("Generate Plot"):
        st.success("Generating Customizable Plot of {} for {}".format(type_of_plot, selected_columns_names))

    if type_of_plot == 'Area':
        cust_data = collection_select[selected_columns_names]
        st.area_chart(cust_data)

    elif type_of_plot == 'Bar':
        cust_data = collection_select[selected_columns_names]
        st.bar_chart(cust_data)

    elif type_of_plot == 'Line':
        cust_data = collection_select[selected_columns_names]
        st.line_chart(cust_data)

    elif type_of_plot:
        cust_plot = collection_select[selected_columns_names].plot(kind=type_of_plot)
        st.write(cust_plot)
        st.pyplot()



