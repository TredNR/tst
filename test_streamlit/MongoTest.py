import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.title("Test with MongoDB")

@st.cache(hash_funcs={MongoClient: id})
def get_client():
    return MongoClient("mongodb://127.0.0.1/admin")

# ------------- Настройка выбора коллекции --------------

client = get_client()

db = client.CovidModel3
a = db.list_collection_names()
b = st.write(a)

select = st.selectbox("Select a collection", a)
selected_filename = db[select]

collection_select = pd.DataFrame(list(selected_filename.find()))

# ------------------ Превью коллекции ---------------------

if st.button("PREVIEW", key=1):
    number = st.number_input("Number of Rows to View",1, 200)
    st.dataframe(collection_select.head(number))

# --------------- Показать всю коллекцию -----------------

if st.checkbox("All collection"):
    view = st.write(collection_select)

# ---------------------- Тип данных ------------------------

if st.checkbox("Data Types"):
    st.write(collection_select.dtypes)

# --------- Общая информация о кол-ве стобцов/строк ---------

if st.checkbox("Shape of Dataset"):
    st.write(collection_select.shape)
    data_dim = st.radio("Show Dimension By ",("Rows", "Columns"))
    if data_dim == 'Rows':
        st.text("Number of Rows")
        st.write(collection_select.shape[0])
    elif data_dim == 'Columns':
        st.text("Number of Columns")
        st.write(collection_select.shape[1])
    else:
        st.write(collection_select.shape)

# --------------- Нарисуем какие-нибудь графики ---------------

if st.checkbox("Plot"):
    st.write(collection_select.describe().T)
    st.subheader("Data Visualization")
    all_columns_names = collection_select.columns.tolist()
    type_of_plot = st.selectbox("Select Type of Plot", ["Area", "Bar", "Line", "Hist", "Box", "Kde"])
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

