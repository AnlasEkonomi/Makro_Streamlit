import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def bist(frekans):
    start="01-01-1987"
    end=datetime.today().strftime("%d-%m-%Y")
    if frekans=="Günlük":
        veri=evdsapi.get_data(["TP.MK.F.BILESIK"],startdate=start,enddate=end)
        veri.dropna(axis=0,inplace=True)
        veri.columns=["Tarih","XU100"]
        veri["Getiri Nominal (%)"]=veri["XU100"]/veri["XU100"].shift(1)-1
        veri["Getiri Nominal (%)"]=veri["Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%d-%m-%Y")
        veri=veri.iloc[1:]
    if frekans=="Aylık":
        veri=evdsapi.get_data(["TP.MK.F.BILESIK"],frequency=5,aggregation_types="last",startdate=start,enddate=end)
        veri.dropna(axis=0,inplace=True)
        veri.columns=["Tarih","XU100"]
        veri["Getiri Nominal (%)"]=veri["XU100"].pct_change()
        veri["Getiri Nominal (%)"]=veri["Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y-%m")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%m-%Y")
        veri=veri.iloc[1:]
    if frekans=="Yıllık":
        veri=evdsapi.get_data(["TP.MK.F.BILESIK","TP.FG.J0"],frequency=8,aggregation_types="last",startdate=start,enddate=end)
        veri.columns=["Tarih","XU100","TÜFE"]
        veri["TÜFE Değişim"]=veri["TÜFE"].pct_change()
        eski=[0.5505,0.7521,0.6877,0.6041,0.7114,0.6597,0.7108,1.2549,
              0.7892,0.7976,0.9909,0.6973,0.6879,0.3903,0.6853,0.2975,0.1836,0.0932]
        veri["TÜFE Değişim"].loc[:len(eski)-1]=[value for value in eski]
        veri["Getiri Nominal (%)"]=veri["XU100"].pct_change()
        veri["Getiri Reel (%)"]=((1+veri["Getiri Nominal (%)"])/(1+veri["TÜFE Değişim"])-1)
        veri["Getiri Reel (%)"]=veri["Getiri Reel (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%Y")
        veri["Getiri Nominal (%)"]=veri["Getiri Nominal (%)"]
        veri["Getiri Nominal (%)"]=veri["Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri.drop(columns=["TÜFE","TÜFE Değişim"],inplace=True)
        veri=veri.iloc[1:]
    return veri

secenek=["Günlük","Aylık","Yıllık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=bist(secim)
st.dataframe(veri,hide_index=True,use_container_width=True)

fig=go.Figure()
fig2=go.Figure()

if secim=="Günlük":
    tarih_formatı="%d-%m-%Y"
    dtick="M5"
elif secim=="Aylık":
    tarih_formatı="%m-%Y"
    dtick="M5"
else: 
    tarih_formatı="%Y"
    dtick="M12"

fig.add_trace(go.Scatter(
    x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),
    y=veri["XU100"],
    mode="lines",
    name="XU100",
    line=dict(color="Red")))

fig.update_layout(title={"text":"XU100","x": 0.5,"xanchor":"center"},
                    xaxis_title="Tarih",yaxis_title="Endeks",
                    xaxis=dict(tickformat=tarih_formatı, tickmode="linear", dtick=dtick))
fig.update_xaxes(tickangle=-45)

if secim=="Yıllık":
    fig2.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),
        y=veri["Getiri Nominal (%)"], name="Nominal Getiri",marker_color="Red"))
    fig2.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),
        y=veri["Getiri Reel (%)"],
        name="Reel Getiri",
        marker_color="Blue"))
else:
    fig2.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),
        y=veri["Getiri Nominal (%)"],mode="lines",name="Getiri",
        line=dict(color="Blue")))

fig2.update_layout(title={"text":"XU100 Getiri (%)","x":0.5,"xanchor":"center"},
                    xaxis_title="Tarih",yaxis_title="Getiri",
                    xaxis=dict(tickformat=tarih_formatı, tickmode="linear", dtick=dtick))
fig2.update_xaxes(tickangle=-45)

st.plotly_chart(fig)
st.plotly_chart(fig2)