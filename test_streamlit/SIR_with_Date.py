import streamlit as st
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd


def main():
    """ Test Dataset (3) """
    st.title("Second test with database")
    st.text("I hope everything works out")

    st.subheader("Mathematical formulas")
    r'''
    $$\frac{dS}{dt} = -\beta*I*\frac{S}{N}$$

    $$\frac{dI}{dt} = -\beta*I*\frac{S}{N}-\gamma*I$$

    $$\frac{dR}{dt} = \gamma*I$$
    '''

    def SIR(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    st.subheader("System parameters")

    N = st.slider('Population', min_value=10, max_value=10000, value=1000, step=1)
    beta = st.slider('Beta (expected amount of people an infected person infects per day)', min_value=0.5,
                     max_value=2.0, value=1.0, step=0.1)
    D = st.slider('D (number of days an infected person has and can spread the disease)', min_value=1.0, max_value=4.0,
                  value=4.0, step=0.1)
    gamma = 1.0 / D

    st.subheader("Starting conditions")

    S0 = st.slider('Number of people susceptible', min_value=1, max_value=(N - 1), value=(N - 1), step=1)
    I0 = st.slider('Number of people infected', min_value=1, max_value=(S0 - 1), value=1, step=1)
    R0 = st.slider('Number of people recovered', min_value=0, max_value=I0, value=0, step=1)
    y0 = S0, I0, R0

    st.subheader("Date parameters")

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    one_day = tomorrow - datetime.timedelta(days=1)
    start = st.date_input('Start date', today)
    end = st.date_input('End date', tomorrow)
    last = st.date_input('Last date', one_day)

    if start < end:
        st.success('Start date: `%s`\n\nEnd date: `%s`\n\n' % (start, end))
    else:
        st.error('Error: End date must fall after start date.')

    if last < end:
        st.success('Last date: `%s`\n\nEnd date: `%s`\n\n' % (last, end))
    else:
        st.error('Error: End date must fall after last date.')

    t = pd.date_range(start=np.datetime64(start), end=np.datetime64(last), freq="D")

    ret = odeint(SIR, y0, t, args=(N, beta, gamma))

    S, I, R = ret.T

    def plotsir(t, S, I, R):
        f, ax = plt.subplots(1, 1, figsize=(10, 4))
        ax.plot(t, S, 'b', alpha=0.7, linewidth=2, label='Susceptible')
        ax.plot(t, I, 'y', alpha=0.7, linewidth=2, label='Infected')
        ax.plot(t, R, 'g', alpha=0.7, linewidth=2, label='Recovered')

        ax.set_xlabel('Time (days)')

        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
            st.pyplot()

    if st.button("Show Plot SIR"):
        st.text("Enjoy")
        plotsir(t, S, I, R)

if __name__ == '__main__':
    main()