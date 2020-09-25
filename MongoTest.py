import streamlit as st
from pymongo import MongoClient
import pandas as pd
import altair as alt
import datetime
import pydeck as pdk
import time

def main():
    st.title("Test with MongoDB")

#@st.cache(hash_funcs={MongoClient: id})
#def get_client():
#    return MongoClient("mongodb://127.0.0.1/admin")

    enter = st.sidebar.text_input("Address database",'mongodb://localhost:27017')
    if st.sidebar.button("Enter", key=1):
        result = enter.title()
        st.sidebar.success(result)

    client = MongoClient(enter)

# ------------- Настройка выбора коллекции --------------

    db = client.list_database_names()
    select1 = st.sidebar.selectbox("Select a database", db)
    selected_database = client[select1]

    a = selected_database.list_collection_names()
    select = st.sidebar.selectbox("Select a collection", a)
    selected_filename = selected_database[select]
    collection_select = pd.DataFrame(list(selected_filename.find()))

# ------------------ Превью коллекции ---------------------

    if st.checkbox("Preview selected collection", key=1):
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

# ---------------------- Altair ----------------------------
    st.subheader("Altair")
    db = client.CovidModel3
    select = st.selectbox("Select request", ["Confirmed global", "Deaths global", "Recover global"], key = 20)
    if select == "Confirmed global":
        collection1 = db.Confirmed_global_narrow
    elif select == "Deaths global":
        collection1 = db.Deaths_global_narrow
    elif select == "Recover global":
        collection1 = db.Recovered_global_narrow

    collection = pd.DataFrame(list(collection1.find()))
    collection['Date'] = pd.to_datetime(collection['Date'], format='%Y/%m/%d').dt.strftime('%Y-%m-%d')
    country_name_input = st.multiselect('Country name (leave blank to see all results)',
                                        collection.groupby('Country/Region').count().reset_index()['Country/Region'].tolist())

    if len(country_name_input) > 0:
        collection = collection[collection['Country/Region'].isin(country_name_input)]
    if st.checkbox ("Show altair graph"):
        total_cases_graph = alt.Chart(collection).transform_filter(
            alt.datum.Value > 0
        ).mark_line().encode(
            x=alt.X('Date:T', title='Date'),
            y=alt.Y('sum(Value)', title='Value'),
            color='Country/Region',
            tooltip='sum(Value)',
        ).properties(
            width=1500,
            height=800
        ).configure_axis(
            labelFontSize=17,
            titleFontSize=20
        ).interactive()
        st.altair_chart(total_cases_graph)

# --------------------------- Map -----------------------------

    collect_map = db.covid2
    collect_map_list = pd.DataFrame(list(collect_map.find()))
    #collect_map_list = collect_map_list.to_dict()

    metrics = ['total_cases', 'new_cases', 'total_deaths']
    if metrics == 'total_cases':
        metrics == collect_map_list["total_cases"]
    elif metrics == 'new_cases':
        metrics == collect_map_list['new_cases']
    elif metrics == 'total_deaths':
        metrics == collect_map_list['total_deaths']

    cols = st.selectbox('Covid metric to view', metrics)
    if cols in metrics:
        metric_to_show_in_covid_Layer = cols

    a12 = dict(collect_map_list["Longitude"])
    b12 = dict(collect_map_list["Latitude"])
    #st.write(a12)

    date = datetime.date(2020, 1, 1)
    view2 = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)
    covidLayer = pdk.Layer(
            "ScatterplotLayer",
            dir(collect_map_list),
            pickable=False,
            opacity=0.3,
            stroked=True,
            filled=True,
            radius_scale=10,
            radius_min_pixels=5,
            radius_max_pixels=60,
            line_width_min_pixels=1,
            get_position=[a12, b12],
            get_radius=metric_to_show_in_covid_Layer,
            get_fill_color=[252, 136, 3],
            get_line_color=[255, 0, 0],
            tooltip="test test",
        )

    r = pdk.Deck(
        layers=[covidLayer],
        initial_view_state=view2,
        map_style="mapbox://styles/mapbox/light-v10",
    )

    subheading = st.subheader("")

    map = st.pydeck_chart(r)

    for i in range(0, 120, 1):

        date += datetime.timedelta(days=1)
        covidLayer.data = collect_map_list[collect_map_list["date"] == date.isoformat()]
        r.update()
        map.pydeck_chart(r)

        subheading.subheader("%s on : %s" % (metric_to_show_in_covid_Layer, date.strftime("%B %d, %Y")))

        time.sleep(1)

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

if __name__ == '__main__':
    main()

