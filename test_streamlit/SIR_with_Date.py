# http://localhost:8501/

import streamlit as st
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd

def main():

# Заголовок
    """ Test Dataset (3) """
    st.title("Second test with database")
    st.text("I hope everything works out")

    st.subheader("Mathematical formulas")
    r'''
    $$\frac{dS}{dt} = -\beta*I*\frac{S}{N}$$

    $$\frac{dI}{dt} = -\beta*I*\frac{S}{N}-\gamma*I$$

    $$\frac{dR}{dt} = \gamma*I$$
    '''

# Используемые уравнения при построении
    def SIR(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt


# Настройка параметров системы
    st.subheader("System parameters")

    N = st.slider('Population', min_value=10, max_value=10000, value=1000, step=1)
    beta = st.slider('Beta (expected amount of people an infected person infects per day)', min_value=0.5,
                     max_value=2.0, value=1.0, step=0.1)
    D = st.slider('D (number of days an infected person has and can spread the disease)', min_value=1.0, max_value=4.0,
                  value=4.0, step=0.1)
    gamma = 1.0 / D

# Установка начальных условий
    st.subheader("Starting conditions")

    S0 = st.slider('Number of people susceptible', min_value=1, max_value=(N - 1), value=(N - 1), step=1)
    I0 = st.slider('Number of people infected', min_value=1, max_value=(S0 - 1), value=1, step=1)
    R0 = st.slider('Number of people recovered', min_value=0, max_value=I0, value=0, step=1)
    y0 = S0, I0, R0

# Установка даты
    today = datetime.today()
    start_day = datetime.strptime('2020-08-01', '%Y-%m-%d')
    start = st.date_input('Start date', start_day)
    end = st.date_input('End date', today)
    last = end - timedelta(days=1)

# Проверка условия согласованности
    if start < end:
        st.success('Start date: `%s`\n\nEnd date: `%s`\n\n' % (start, end))
    else:
        st.error('Error: End date must fall after start date.')

    if start < last:
        st.success('Start date: `%s`\n\nLast date: `%s`\n\n' % (start, last))
    else:
        st.error('Error: Last date must fall after start date.')

# Определение периода дней
    period = end - start
    days_full = period.days
    st.write("Period = ", days_full)

# Установка array [0, 1, 2, ... days_full]
    t = np.linspace(0, days_full-1, days_full)

    ret = odeint(SIR, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    first_date = np.datetime64(start)
    x_ticks = pd.date_range(start=first_date, periods=days_full, freq="D")

# Функция построения графиков
    def plotsir(S, I, R, t1=None, x_ticks=None):
        f, ax = plt.subplots(1, 1, figsize=(10, 4))

# Условие вывода простого графика
        if x_ticks is None:
            ax.plot(t1, S, 'b', alpha=0.7, linewidth=2, label='Susceptible')
            ax.plot(t1, I, 'y', alpha=0.7, linewidth=2, label='Infected')
            ax.plot(t1, R, 'g', alpha=0.7, linewidth=2, label='Recovered')

# Условие для вывода графика по датам
        else:
            ax.plot(x_ticks, S, 'b', alpha=0.7, linewidth=2, label='Susceptible')
            ax.plot(x_ticks, I, 'y', alpha=0.7, linewidth=2, label='Infected')
            ax.plot(x_ticks, R, 'g', alpha=0.7, linewidth=2, label='Recovered')
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
            #ax.set_xticks(x_ticks)
            f.autofmt_xdate()

        ax.title.set_text('Extended SIR-Model')

        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        st.pyplot()

# Кнопка вывода простого графика по периоду дней
    if st.button("Show Plot SIR", key=1):
        st.text("Enjoy")
        plotsir(S, I, R, x_ticks=None, t1=t)

# Кнопка вывода графика по датам
    if st.button("Show Plot SIR with date format", key=2):
        st.text("Enjoy")
        plotsir(S, I, R, x_ticks=x_ticks, t1=None)

# Тест вывода данных средством Streamlit, пока плачевно
    if st.button("Test line plot", key=4):
        df = pd.DataFrame(R)
        st.line_chart(df)

# Ну тут и так понятно
if __name__ == '__main__':
    main()
