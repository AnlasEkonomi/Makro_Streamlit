import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def dısticaret(frekans):
    start="01-01-2013"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlarihracat=["TP.IHRACATBEC.9999","TP.IHRACATBEC.1","TP.IHRACATBEC.2","TP.IHRACATBEC.3",
            "TP.IHRACATBEC.4"]
    kodlarithalat=["TP.ITHALATBEC.9999","TP.ITHALATBEC.1","TP.ITHALATBEC.2","TP.ITHALATBEC.3",
            "TP.ITHALATBEC.4"]
    sütunad=["Tarih","Toplam","Yatırım Malları","Ara Mallar","Tüketim Malları","Diğer"]

    if frekans=="Aylık":
        veri1=evdsapi.get_data(kodlarihracat,startdate=start,enddate=end)
        veri2=evdsapi.get_data(kodlarithalat,startdate=start,enddate=end)
    elif frekans=="Yıllık":
        veri1=evdsapi.get_data(kodlarihracat,startdate=start,enddate=end,frequency=8)
        veri2=evdsapi.get_data(kodlarithalat,startdate=start,enddate=end,frequency=8)
    
    veri1.columns=sütunad
    veri2.columns=sütunad
   
    for column in sütunad[1:]:
        if column !="Toplam":
            veri1[f"{column} Oranı (%)"]=(veri1[column]/veri1["Toplam"]).map(lambda x: f"{x:.2%}")
            veri2[f"{column} Oranı (%)"]=(veri2[column]/veri2["Toplam"]).map(lambda x: f"{x:.2%}")
    return veri1,veri2

secenek=["Aylık","Yıllık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri1,veri2=dısticaret(secim)

st.subheader("İhracat Verileri")
st.dataframe(veri1,hide_index=True,use_container_width=True)

st.subheader("İthalat Verileri")
st.dataframe(veri2,hide_index=True,use_container_width=True)

fig_total=go.Figure()
fig_total.add_trace(go.Scatter(x=veri1["Tarih"],y=veri1["Toplam"],mode="lines",name="İhracat Toplam"))
fig_total.add_trace(go.Scatter(x=veri2["Tarih"],y=veri2["Toplam"],mode="lines",name="İthalat Toplam"))

fig_total.update_xaxes(range=[min(veri1["Tarih"].min(),veri2["Tarih"].min()), 
                               max(veri1["Tarih"].max(),veri2["Tarih"].max())])
fig_total.update_layout(title=f"İhracat ve İthalat Toplam ({secim})",xaxis_title="Tarih",yaxis_title="Değer")
fig_total.update_xaxes(tickangle=-45)

if "Yıllık" in secim:
    fig_total.update_xaxes(dtick="M12",tickformat="%Y")
else:
    fig_total.update_xaxes(dtick="M3",tickformat="%m-%Y")

st.plotly_chart(fig_total,use_container_width=True)

renkler=["blue","black","green","red","purple"]

fig_ihracat=go.Figure()
for i, column in enumerate(veri1.columns):
    if "Oranı (%)" in column:
        fig_ihracat.add_trace(go.Bar(x=veri1["Tarih"],y=veri1[column],name=column,marker_color=renkler[i % len(renkler)]))

fig_ihracat.update_layout(title=f"İhracat Oranları ({secim})",xaxis_title="Tarih",yaxis_title="Oran (%)", xaxis_tickangle=-45)
if "Yıllık" in secim:
    fig_ihracat.update_xaxes(dtick="M12",tickformat="%Y")
else:
    fig_ihracat.update_xaxes(dtick="M3",tickformat="%m-%Y")

st.plotly_chart(fig_ihracat,use_container_width=True)

fig_ithalat=go.Figure()
for i, column in enumerate(veri2.columns):
    if "Oranı (%)" in column:
        fig_ithalat.add_trace(go.Bar(x=veri2["Tarih"],y=veri2[column],name=column,marker_color=renkler[i % len(renkler)]))

fig_ithalat.update_layout(title=f"İthalat Oranları ({secim})",xaxis_title="Tarih",yaxis_title="Oran (%)",xaxis_tickangle=-45)
if "Yıllık" in secim:
    fig_ithalat.update_xaxes(dtick="M12",tickformat="%Y")
else:
    fig_ithalat.update_xaxes(dtick="M3",tickformat="%m-%Y")

st.plotly_chart(fig_ithalat,use_container_width=True)