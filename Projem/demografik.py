import requests
import pandas as pd
from io import StringIO
import streamlit as st
import locale
import plotly.graph_objects as go

def ilduzey():
    url="https://cip.tuik.gov.tr/assets/geometri/nuts3.json"
    veri=requests.get(url).json()
    veri=veri["features"]

    iller=[]
    for i in veri:
        properties=i["properties"]
        iller.append(properties)

    veri=pd.DataFrame(iller)
    veri.drop(columns=["name","bolgeKodu","nutsKodu"],inplace=True)
    return veri


def cinsiyetnufus(il):
    url="https://nip.tuik.gov.tr/Home/GetInformation"

    yuk={"status":"1",
        "name":"CinsiyeteGoreNufus",
        "value":str(il)}
    
    req=requests.get(url,data=yuk)
    html=StringIO(req.text)
    veri=pd.read_html(html,decimal=",",thousands=".")[0]
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    veri.sort_values(by="Yıl",inplace=True)
    veri.drop(columns=["Düzey"],inplace=True)
    return veri

iller=list(ilduzey()["ad"])
locale.setlocale(locale.LC_COLLATE,"tr_TR.UTF-8")
iller=sorted(iller,key=locale.strxfrm)
indeks=iller.index("KAYSERI")
iller[indeks]="KAYSERİ"
iller.insert(0,"TÜRKİYE")

with st.expander("Cinsiyete Göre Nüfus"):
    secim=st.selectbox(label="İl Seçiniz:",options=iller)
    veri=cinsiyetnufus(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)
    
    bar_trace=go.Bar(
    x=veri["Yıl"],y=veri["Toplam Nüfus"],name='Toplam Nüfus',marker=dict(color='lightblue'))

    erkek=go.Scatter(x=veri["Yıl"],y=veri["Erkek Nüfus"],name="Erkek Nüfusu",
        mode="lines+markers",marker=dict(color="blue"))

    kadın=go.Scatter(x=veri["Yıl"],y=veri["Kadın Nüfus"],name="Kadın Nüfusu",
        mode="lines+markers",marker=dict(color="red"))

    fig=go.Figure(data=[bar_trace,erkek,kadın])

    fig.update_layout(
        title=f"Yıllara Göre Nüfus ({str(secim).capitalize()})",xaxis_title='Yıllar',
        yaxis_title="Nüfus",barmode="group")
    
    fig.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig)
