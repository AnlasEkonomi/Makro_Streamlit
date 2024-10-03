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


def tüfe():
    start="01-01-2015"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.FG.J0"]
    sütunad=["Tarih","TÜFE"]
    veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
    veri.columns=sütunad
    veri["Enflasyon"]=round(veri["TÜFE"].pct_change(12)*100,2)
    veri.dropna(axis=0,inplace=True)
    veri.drop(columns=["Tarih","TÜFE"],inplace=True)
    veri.reset_index(inplace=True,drop=True)
    return veri


veri=enfanket()
veri2=tüfe()

veri["12 Sonraki Enflasyon"]=veri2["Enflasyon"]
veri["PK Sapma"]=veri["Piyasa Katılımcıları"]-veri["12 Sonraki Enflasyon"]
veri["RS Sapma"]=veri["Reel Sektör"]-veri["12 Sonraki Enflasyon"]
veri["HH Sapma"]=veri["Hanehalkı"]-veri["12 Sonraki Enflasyon"]
veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y-%m").dt.strftime("%Y-%m")

st.markdown("<h4 style='font-size:20px;'>12 Ay Sonrası Yıllık Enflasyon Beklentisi</h4>",unsafe_allow_html=True)
st.dataframe(veri,hide_index=True,use_container_width=True)

fig=go.Figure()
fig2=go.Figure()

for sütun in veri.columns[1:4]:
    fig.add_trace(go.Scatter(x=veri["Tarih"],y=veri[sütun],mode="lines",name=sütun))

renkler=["red","blue","green"]

for idx,sütun in enumerate(veri.columns[5:]):
    fig2.add_trace(go.Bar(
        x=veri["Tarih"],
        y=veri[sütun],
        name=sütun,
        marker=dict(color=renkler[idx % len(renkler)],opacity=1)))

fig.update_layout(title="Enflasyon Anketi",xaxis_title="Tarih",yaxis_title="Enflasyon",
                  xaxis=dict(tickformat="%m-%Y",dtick="M1",
                rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))

fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_xaxes(tickangle=-45)

fig2.update_layout(title="Anket Sapma",xaxis_title="Tarih",yaxis_title="Sapma Puan",
                  xaxis=dict(tickformat="%m-%Y",dtick="M1",
                rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))

fig2.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
fig2.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig2.update_xaxes(tickangle=-45)

st.plotly_chart(fig,use_container_width=True)
st.plotly_chart(fig2,use_container_width=True)