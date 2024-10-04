import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def osd(frekans):
    start="01-01-1974"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.UR.S08","TP.UR.S09","TP.UR.S10","TP.UR.S11","TP.UR.S12","TP.UR.S13",
            "TP.UR.S14","TP.UR.S31"]
    sütunad=["Tarih","Binek","Çekici","Kamyon","Kamyonet","Midibüs","Minibüs",
             "Otobüs","Traktör"]
    
    if frekans=="Aylık (Adet)":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
        veri.columns=sütunad
        veri['Tarih']=pd.to_datetime(veri["Tarih"],dayfirst=True,errors="coerce").dt.strftime("%m-%Y")
    elif frekans=="Yıllık (Adet)":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end,frequency=8)
        veri.columns=sütunad
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y",errors="coerce").dt.year.astype(str)
    
    return veri

secenek=["Aylık (Adet)","Yıllık (Adet)"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=osd(secim)

st.markdown(f"<h4 style='font-size:20px;'>OSD Üretim İstatistikleri ({secim})</h4>",unsafe_allow_html=True)
st.dataframe(veri,hide_index=True,use_container_width=True)

fig=go.Figure()

if secim=="Aylık (Adet)":
    for col in veri.columns[1:]:
        fig.add_trace(go.Scatter(x=veri["Tarih"],y=veri[col],mode="lines",name=col))
    grafik_baslik="OSD Üretim (Aylık)"
else:
    for col in veri.columns[1:]:
        fig.add_trace(go.Bar(x=veri["Tarih"],y=veri[col],name=col))
    grafik_baslik = "OSD Üretim (Yıllık)"
    fig.update_layout(barmode="stack")

fig.update_layout(title=grafik_baslik,xaxis_title="Tarih",yaxis_title="Adet",
    template="plotly_white",
    xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))

fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_xaxes(tickangle=-45)

st.plotly_chart(fig)