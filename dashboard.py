import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests

from apis import apod_generator

st.title("Water Quality Dashboard")
st.header("Internship Ready Software Development")
st.subheader("Prof. Gregory Reis")
st.divider()

df = pd.read_csv("biscayneBay_waterquality.csv")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Descriptive Statistics",
     "2d Plots",
     "3d Plots",
     "NASA's APOD"]
)

with tab1:
    st.dataframe(df)
    st.caption("Raw Data")
    st.divider()
    st.dataframe(df.describe())
    st.caption("Descriptive Statistics")

with tab2:
    temp_limit = st.slider(
        "Minimum Temperature (°C)",
        min_value=float(df["Temperature (c)"].min()),
        max_value=float(df["Temperature (c)"].max()),
        value=float(df["Temperature (c)"].min())
    )

    filtered_df = df[df["Temperature (c)"] >= temp_limit]

    fig1 = px.line(filtered_df, x="Time", y="Temperature (c)")
    st.plotly_chart(fig1)


with tab3:
    fig3 = px.scatter_3d(df,
                         x="Longitude",
                         y="Latitude",
                         z="Total Water Column (m)",
                         color="Temperature (c)")
    fig3.update_scenes(zaxis_autorange="reversed")
    st.plotly_chart(fig3)


def apod_generator(api_key: str):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url).json()
    return response

with tab4:
    st.header("NASA's Astronomy Picture of the Day")
    api_key = os.getenv("NASA_API_KEY")
    if api_key:
        apod_data = apod_generator(api_key)
        st.subheader(apod_data.get("title", "No title"))
        st.image(apod_data.get("url"), caption=apod_data.get("explanation", ""), use_column_width=True)
        st.caption(f"Date: {apod_data.get('date', '')}")
    else:
        st.error("NASA API key not found. Please set NASA_API_KEY in your .env file.")