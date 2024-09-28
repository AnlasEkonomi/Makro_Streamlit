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
    veri[["a", "Şehir", "b"]]=veri["SERIE_NAME"].str.split('_',expand=True)
    veri.drop(columns=["a","b","SERIE_NAME"],inplace=True)
    return veri

konutid=["bie_akonutsat1","bie_akonutsat2","bie_akonutsat3","bie_akonutsat4"]
konutveri=[get_konut_data(konut_id) for konut_id in konutid]

def get_veri(konut_data):
    start="01-01-2013"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(konut_data["SERIE_CODE"].to_list(),startdate=start,enddate=end)
    veri.columns=["Tarih"]+konut_data["Şehir"].to_list()
    veri=veri.reindex(sorted(veri.columns),axis=1)
    sütunsıra=["Tarih"," Türkiye "]+[col for col in veri.columns if col not in ["Tarih"," Türkiye "]]
    return veri[sütunsıra]

veriler=[get_veri(konut_data) for konut_data in konutveri]

secenek=["Toplam","İpotekli","İlk El","İkinci El"]
st.markdown('<p style="font-weight:bold; color:black;">Tür Seçiniz:</p>', unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)

if secim=="Toplam":
    secilen=veriler[0]
elif secim=="İpotekli":
    secilen=veriler[1]
elif secim=="İlk El":
    secilen=veriler[2]
elif secim=="İkinci El":
    secilen=veriler[3]

st.dataframe(secilen,hide_index=True,use_container_width=True)
liste=secilen.columns[1:].tolist()
secilen["Tarih"]=pd.to_datetime(secilen["Tarih"])

default_il=" Türkiye "
secim=st.selectbox("İl Seçin:",options=liste,index=0)

if secim:
    fig=go.Figure()

    fig.add_trace(go.Scatter(x=secilen["Tarih"],y=secilen[secim],mode="lines",
        name=secim,line=dict(width=2,color="red")))

    fig.update_layout(title=f"{secim}",xaxis_title="Tarih",yaxis_title="Değer",
        legend_title="İller",
        xaxis=dict(tickformat="%m-%Y",dtick="M3",
                   rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig)