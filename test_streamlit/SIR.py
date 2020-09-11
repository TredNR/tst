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
    st.title("Example of an interactive model")
    st.text("In the process of revision")

    st.subheader("Mathematical formulas")
    r'''
    $$\frac{dS}{dt} = -\beta*I*\frac{S}{N}$$
    
    $$\frac{dE}{dt} = \beta * I * \frac{S}{N} - \delta * E$$

    $$\frac{dI}{dt} = \delta * E - (1 - \alpha) * \gamma * \rho * I$$

    $$\frac{dR}{dt} = (1 - \alpha) * \gamma*I$$
    
    $$\frac{dD}{dt} = \alpha * \rho * I$$
    '''

# Используемые уравнения при построении
    def SEIRD(y, t, N, beta, gamma, delta, alpha_opt, rho):
        S, E, I, R, D = y

        def alpha(t):
            return s * I / N + alpha_opt

        dSdt = -beta(t) * S * I / N
        dEdt = beta(t) * S * I / N - delta * E
        dIdt = delta * E - (1 - alpha(t)) * gamma * I - alpha(t) * rho * I
        dRdt = (1 - alpha(t)) * gamma * I
        dDdt = alpha(t) * rho * I
        return dSdt, dEdt, dIdt, dRdt, dDdt

# Настройка параметров системы
    st.subheader("System parameters")

    D = st.slider('[D] Number of days an infected person has and can spread the disease', min_value=1.0, max_value=4.0, value=4.0, step=0.1)
    delta = 1.0 / st.slider('[δ] Incubation period', min_value=1, max_value=7, value=5, step=1)
    rho = 1 / st.slider('[ρ] Days from infection until death', min_value=1, max_value=10, value=9, step=1)
    gamma = 1.0 / D
    st.write("[γ]", gamma, " - the proportion of infected recovering per day (γ = 1/D)")
    #alpha = st.slider('Death rate (%)', min_value=0.1, max_value=1.0, value=0.2, step=0.1)

# Показатели возрастных групп и средний уровень смертности
    alpha_by_agegroup = {"0-29": 0.01, "30-59": 0.05, "60-89": 0.2, "89+": 0.3}
    proportion_of_agegroup = {"0-29": 0.1, "30-59": 0.3, "60-89": 0.4, "89+": 0.2}
    s = 0.01
    alpha_opt = sum(alpha_by_agegroup[i] * proportion_of_agegroup[i] for i in list(alpha_by_agegroup.keys()))

# Параметры условия "Когда лучше всего ввести карантин"
    R_0_start, k, x0, R_0_end = 5.0, 0.5, 50, 0.5
    def logistic_R_0(t):
        return (R_0_start-R_0_end) / (1 + np.exp(-k*(-t+x0))) + R_0_end

# Установка начальных условий
    st.subheader("Starting conditions")

    N = st.slider('Population', min_value=10, max_value=1000000, value=500000, step=1)
    S0 = st.slider('Number of people susceptible', min_value=1, max_value=(N - 1), value=(N - 1), step=1)
    I0 = st.slider('Number of people infected', min_value=1, max_value=(N - S0 - 1), value=1, step=1)
    R0 = st.slider('Number of people recovered', min_value=0, max_value=(N - S0 - I0 - 1), value=0, step=1)
    E0 = 0
    st.write("Number of people exposed", E0)
    D0 = 0
    st.write("Number of people dead", D0)

    y0 = S0, E0, I0, R0, D0

    st.subheader("Lockdown settings")

# Параметр карантина (через сколько дней его начать)
    L = st.slider('After days', min_value=0, max_value=100, value=40, step=1)

    def R_0(t):
        return 5.0 if t < L else 0.9
    def beta(t):
        return R_0(t) * gamma

# Установка даты
    st.subheader("Date settings")

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
    st.write("Period = ", days_full, " days")

# Установка array [0, 1, 2, ... days_full] из дней
    t = np.linspace(0, days_full-1, days_full)

    ret = odeint(SEIRD, y0, t, args=(N, beta, gamma, delta, alpha_opt, rho))
    S, E, I, R, D = ret.T

    R0_over_time = [logistic_R_0(i) for i in range(len(t))]
    Alpha_over_time = [s * I[i]/N + alpha_opt for i in range(len(t))]

    first_date = np.datetime64(start)
    x_ticks = pd.date_range(start=first_date, periods=days_full, freq="D")

# ----------------------------- Функция построения графиков ---------------------------------------
    def plotsir(S, E, I, R, D=None, t1=None, x_ticks=None, L=None, R0=None, Alpha=None):
        f, ax = plt.subplots(1, 1, figsize=(10, 4))

# Условие вывода графика с датой
        ax.plot(x_ticks, S, 'b', alpha=0.7, linewidth=2, label='Susceptible')
        ax.plot(x_ticks, E, 'y', alpha=0.7, linewidth=2, label='Exposed')
        ax.plot(x_ticks, I, 'r', alpha=0.7, linewidth=2, label='Infected')
        ax.plot(x_ticks, R, 'g', alpha=0.7, linewidth=2, label='Recovered')
        if D is not None:
            ax.plot(x_ticks, D, 'k', alpha=0.7, linewidth=2, label='Dead')
            ax.plot(x_ticks, S + E + I + R + D, 'c--', alpha=0.7, linewidth=2, label='Total')
        else:
            ax.plot(x_ticks, S + E + I + R, 'c--', alpha=0.7, linewidth=2, label='Total')
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
            #ax.set_xticks(x_ticks)
        f.autofmt_xdate()

        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)

# Условие простого карантина (введенного после определенного количества дней)
        if L is not None:
            plt.title("Lockdown after {} days".format(L))
        st.pyplot()

        if R0 is not None:
            ax1 = f.add_subplot()
            ax1.plot(t1, R0, 'b--', alpha=0.7, linewidth=2, label='R_0')

            ax1.set_xlabel('Time (days)')
            ax1.title.set_text('R_0 over time')
            ax1.yaxis.set_tick_params(length=0)
            ax1.xaxis.set_tick_params(length=0)
            ax1.yaxis.set_tick_params(length=0)
            ax1.xaxis.set_tick_params(length=0)
            ax1.grid(b=True, which='major', c='w', lw=2, ls='-')
            legend = ax1.legend()
            legend.get_frame().set_alpha(0.5)
            for spine in ('top', 'right', 'bottom', 'left'):
                ax.spines[spine].set_visible(False)
            st.pyplot()

        if Alpha is not None:
            ax2 = f.add_subplot()
            ax2.plot(t1, Alpha, 'r--', alpha=0.7, linewidth=2, label='alpha')
            ax2.set_xlabel('Time (days)')
            ax2.title.set_text('Fatality rate over time')
            ax2.yaxis.set_tick_params(length=0)
            ax2.xaxis.set_tick_params(length=0)
            ax2.grid(b=True, which='major', c='w', lw=2, ls='-')
            legend = ax2.legend()
            legend.get_frame().set_alpha(0.5)
            for spine in ('top', 'right', 'bottom', 'left'):
                ax.spines[spine].set_visible(False)
            st.pyplot()

    if st.button("Show plot`s", key=1):
        plotsir(S, E, I, R, x_ticks=x_ticks, t1=t, D=D, L=L, R0=R0_over_time, Alpha=Alpha_over_time)

    if st.button ("Show plot from altair", key=2):
        st.line_chart(Alpha_over_time)

# Ну тут и так понятно
if __name__ == '__main__':
    main()
