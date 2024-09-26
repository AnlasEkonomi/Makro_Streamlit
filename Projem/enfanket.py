import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def enfanket():
    start="01-01-2015"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.ENFBEK.PKA12ENF","TP.ENFBEK.IYA12ENF","TP.ENFBEK.TEA12ENF"]
    sütunad=["Tarih","Piyasa Katılımcıları","Reel Sektör","Hanehalkı"]
    veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
    veri.columns=sütunad
    return veri

veri=enfanket()
st.header("12 Ay Sonrası Yıllık Enflasyon Beklentisi")
st.dataframe(veri,hide_index=True,use_container_width=True)
veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y-%m")

fig=go.Figure()

for sütun in veri.columns[1:]:
    fig.add_trace(go.Scatter(x=veri["Tarih"],y=veri[sütun],mode="lines",name=sütun))

fig.update_layout(xaxis_title="Tarih",yaxis_title="Enflasyon",
                  xaxis=dict(tickformat="%m-%Y",dtick="M1",
                rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
fig.update_xaxes(tickangle=-45)

st.plotly_chart(fig,use_container_width=True)