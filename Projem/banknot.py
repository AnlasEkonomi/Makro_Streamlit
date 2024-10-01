import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def banknot(frekans):
    start="01-01-2009"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlartutar=["TP.TEDAVULTUT.T200","TP.TEDAVULTUT.T100","TP.TEDAVULTUT.T50",
                "TP.TEDAVULTUT.T20","TP.TEDAVULTUT.T10","TP.TEDAVULTUT.T5"]
    kodlaradet=["TP.TEDAVULADT.T200","TP.TEDAVULADT.T100","TP.TEDAVULADT.T50",
                "TP.TEDAVULADT.T20","TP.TEDAVULADT.T10","TP.TEDAVULADT.T5"]
    sütunad=["Tarih","200 TL","100 TL","50 TL","20 TL","10 TL","5 TL"]
    
    if frekans=="Aylık (Tutar)":
        veri=evdsapi.get_data(kodlartutar,startdate=start,enddate=end,frequency=5,aggregation_types="last")
    elif frekans=="Yıllık (Tutar)":
        veri=evdsapi.get_data(kodlartutar,startdate=start,enddate=end,frequency=8,aggregation_types="last")
    elif frekans=="Aylık (Adet)":
        veri=evdsapi.get_data(kodlaradet,startdate=start,enddate=end,frequency=5,aggregation_types="last")
    elif frekans=="Yıllık (Adet)":
        veri=evdsapi.get_data(kodlaradet,startdate=start,enddate=end,frequency=8,aggregation_types="last")
    
    veri.columns=sütunad
    return veri

secenek=["Aylık (Tutar)","Yıllık (Tutar)","Aylık (Adet)","Yıllık (Adet)"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem ve Tür Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=banknot(secim)

st.markdown("<h4 style='font-size:20px;'>Banknot Dağılımı</h4>",unsafe_allow_html=True)
st.dataframe(veri,hide_index=True,use_container_width=True)

veri["Tarih"]=pd.to_datetime(veri["Tarih"],dayfirst=False,errors="coerce")

if "Tutar" in secim:
    baslik=f"{secim}"
else:
    baslik=f"{secim}"

fig = go.Figure()
for column in veri.columns[1:]:
    fig.add_trace(go.Scatter(x=veri["Tarih"],y=veri[column],
                            mode="lines+markers",name=column))

fig.update_xaxes(range=[veri["Tarih"].min(),veri["Tarih"].max()])

if "Yıllık" in secim:
    fig.update_xaxes(dtick="M12",tickformat="%Y")
else:
    fig.update_xaxes(dtick="M3",tickformat="%m-%Y")

fig.update_layout(title=baslik,xaxis_title="Tarih",yaxis_title="",
                  xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))

fig.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_xaxes(tickangle=-45)

st.plotly_chart(fig)