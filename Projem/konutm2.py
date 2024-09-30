import evds as ev
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

with open("evdsapi.txt","r") as dosya:
    api = dosya.read()

evdsapi=ev.evdsAPI(api)

def get_konut_data(seri):
    veri=evdsapi.get_series(seri).drop(columns=["START_DATE"])
    veri[["Şehir","b","c","d"]]=veri["SERIE_NAME"].str.split(" ",expand=True)
    veri.drop(columns=["b","c","d","SERIE_NAME"],inplace=True)
    return veri

konutid=["bie_birimfiyat"]
konutveri=[get_konut_data(konut_id) for konut_id in konutid]

secenek=["Çeyreklik","Yıllık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>', unsafe_allow_html=True)
frekans=st.radio("",secenek,index=0,horizontal=True)

def get_veri(konut_data):
    start="01-01-2010"
    end=datetime.today().strftime("%d-%m-%Y")
    if frekans=="Çeyreklik":
        veri=evdsapi.get_data(konut_data["SERIE_CODE"].to_list(),startdate=start,enddate=end)
        veri.columns=["Tarih"]+konut_data["Şehir"].to_list()
        veri=veri.reindex(sorted(veri.columns),axis=1)
        sütunsıra=["Tarih","Türkiye"]+[col for col in veri.columns if col not in ["Tarih","Türkiye"]]
        veri.fillna(0,inplace=True)
        return veri[sütunsıra]
    elif frekans=="Yıllık":
        veri=evdsapi.get_data(konut_data["SERIE_CODE"].to_list(),startdate=start,enddate=end,frequency=8)
        veri.columns=["Tarih"]+konut_data["Şehir"].to_list()
        veri=veri.reindex(sorted(veri.columns),axis=1)
        sütunsıra=["Tarih","Türkiye"]+[col for col in veri.columns if col not in ["Tarih","Türkiye"]]
        veri.fillna(0,inplace=True)
        return veri[sütunsıra]


veriler=[get_veri(konut_data) for konut_data in konutveri][0]

st.markdown("<h4 style='font-size:20px;'>Konut Birim Fiyatları</h4>",unsafe_allow_html=True)
st.dataframe(veriler,hide_index=True,use_container_width=True)

liste=veriler.columns[1:].tolist()
veriler["Tarih"]=pd.to_datetime(veriler["Tarih"])

default_il="Türkiye"
secim=st.selectbox("İl Seçin:",options=liste,index=0)

if secim:
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=veriler["Tarih"],y=veriler[secim],mode="lines",name=secim,
                            line=dict(width=2,color="red")))

    if frekans=="Çeyreklik":
        tickformat="%Y-Q%q"
        dtick="M3"
    elif frekans=="Yıllık":
        tickformat="%Y" 
        dtick="M12"

    fig.update_layout(
        title=f"{secim}",xaxis_title="Tarih",yaxis_title="TL",legend_title="İller",
        xaxis=dict(tickformat=tickformat,dtick=dtick,
            rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
    
    fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig)