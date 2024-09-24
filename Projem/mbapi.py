import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def mbapi():
    start="02-01-2019"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.APIFON1.IHA","TP.APIFON1.KOT.A","TP.APIFON1.KOT.B","TP.APIFON1.KOT.C",
        "TP.APIFON1.KOT.T","TP.APIFON1.TOP","TP.APIFON2.IHA","TP.APIFON2.KOT",
        "TP.APIFON2.TOP","TP.APIFON3","TP.APIFON4"]
    sütunad=["Tarih","İhale Yoluyla Fonlama","Bist O/N","Depo","GLP","Toplam Kotasyon",
                  "Toplam Fonlama","İhale Yoluyla Sterilizasyon","Kotasyon Yoluyla Sterilizasyon",
                  "Toplam Sterilizasyon","Net Fonlama","AOFM"]  
    veri=evdsapi.get_data(kodlar,startdate=start,enddate=end).dropna()
    veri.columns=sütunad
    veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y").dt.strftime("%d-%m-%Y")         
    st.dataframe(veri,hide_index=True,width=1000)
    
    for y_column, title, color in [("Net Fonlama","APİ Net Fonlama","blue"),("AOFM", "AOFM (%)", "red")]:
        fig=go.Figure()
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),
            y=veri[y_column],
            mode="lines",
            line=dict(color=color),
            name=y_column))
        
        fig.update_layout(
            title={"text":title,"x": 0.5,"xanchor":"center"},
            xaxis_title="Tarih",
            yaxis_title=y_column,
            xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1",
                       rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
        fig.update_xaxes(tickangle=-45)
        
        st.plotly_chart(fig)

    return veri

mbapi()