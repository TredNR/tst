import os
import streamlit as st
import matplotlib
import pandas as pd
import seaborn as sns
matplotlib.use('Agg')

def main():
    """ Test Dataset """
    st.title("First test with data (csv)")
    st.header("I hope everything works out")

    html_temp = """ <div style = "background-color:orange"><p align="center" style ="color:white;font_size:30px">(´･ᴗ･ )</p></div>"""
    st.markdown(html_temp, unsafe_allow_html=True)

    def file_selector(folder_path ='C:/Users/tred1/Desktop/infectious_disease_modelling-master/data'):
        filenames = os.listdir(folder_path)
        selected_filename = st.selectbox("Select a file", filenames)
        return os.path.join(folder_path, selected_filename)

    filename = file_selector()
    st.info("You Selected {}".format(filename))

# ---------------------- Чтение из файла ---------------------

    df = pd.read_csv(filename)

# --------------------- Показать данные ---------------------

# ------ Вывод определенного количества ячеек таблицы -------
    if st.checkbox("Show Dataset"):
        number = st.number_input("Number of Rows to View",1, 200)
        st.dataframe(df.head(number))

# ---------- Вывод наименований полей таблицы ---------------
    if st.button ("Column Names"):
        st.write(df.columns)

# --------- Общая информация о кол-ве стобцов/строк ---------
    if st.checkbox("Shape of Dataset"):
        st.write(df.shape)
        data_dim = st.radio("Show Dimension By ",("Rows", "Columns"))
        if data_dim == 'Rows':
            st.text("Number of Rows")
            st.write(df.shape[0])
        elif data_dim == 'Columns':
            st.text("Number of Columns")
            st.write(df.shape[1])
        else:
            st.write(df.shape)

# ---------------- Выбор стобца базы данных ---------------
    if st.checkbox("Select Columns to Show"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select", all_columns)
        new_df = df[selected_columns]
        st.dataframe(new_df)

# ------- Определение количества повторений в столбце -------
    if st.button("Value Counts"):
        st.text("Value Counts By Target/Class")
        st.write(df.iloc[:, 1].value_counts())

# ---------------- Какой тип данных у поля -----------------
    if st.button("Data Types"):
        st.write(df.dtypes)

    if st.checkbox("Summary"):
        st.write(df.describe().T)

        st.subheader("Data Visualization")
        st.subheader("Customizable Plot")
        all_columns_names = df.columns.tolist()
        type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
        selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

    if st.button("Generate Plot"):
        st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

        if type_of_plot == 'area':
            cust_data = df[selected_columns_names]
            st.area_chart(cust_data)

        elif type_of_plot == 'bar':
            cust_data = df[selected_columns_names]
            st.bar_chart(cust_data)

        elif type_of_plot == 'line':
            cust_data = df[selected_columns_names]
            st.line_chart(cust_data)

        elif type_of_plot:
            cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
            st.write(cust_plot)
            st.pyplot()

# ---------------- Pie Plot -------------------
    if st.checkbox("Pie Plot"):
        all_columns_names = df.columns.tolist()
        if st.button("Generate Pie Plot", key=1):
            st.success("Generating A Pie Plot")
            st.write(df.iloc[:, 1]. value_counts(). plot. pie(autopct ="%1.1f%%"))
            st.pyplot()

# ---------------- Seaborn -------------------
    if st.checkbox("Correlation Plot[Seaborn]"):
        st.write(sns.heatmap(df.corr(), annot=True))
        st.pyplot()

# --------------- Count Plot ------------------
    if st.checkbox("Plot of Value Counts"):
        st.text("Value Counts By Target")
        all_columns_names = df.columns.tolist()
        primary_col = st.selectbox("Primary Column to GroupBy", all_columns_names)
        selected_columns_names = st.multiselect("Select Columns", all_columns_names)
        if st.button("Plot", key=2):
            st.text("Generate Plot")
            if selected_columns_names:
                vc_plot = df.groupby(primary_col)[selected_columns_names].count()
            else:
                vc_plot = df.iloc[:, 1].value_counts()
            st.write(vc_plot.plot(kind="bar"))
            st.pyplot()

    if st.button("Шарики"):
        st.balloons()

if __name__ == '__main__':
    main()



