import streamlit as st
import evds as ev
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from urllib.error import HTTPError


evdsapi=ev.evdsAPI("Your Api Key")

def mbapi():
    kodlar=["TP.APIFON1.IHA","TP.APIFON1.KOT.A","TP.APIFON1.KOT.B","TP.APIFON1.KOT.C",
        "TP.APIFON1.KOT.T","TP.APIFON1.TOP","TP.APIFON2.IHA","TP.APIFON2.KOT",
        "TP.APIFON2.TOP","TP.APIFON3","TP.APIFON4"]
    
    start="02-01-2019"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
    veri.dropna(axis=0,inplace=True)
    veri.columns=["Tarih","İhale Yoluyla Fonlama","Bist O/N","Depo","GLP","Toplam Kotasyon",
                  "Toplam Fonlama","İhale Yoluyla Sterilizasyon","Kotasyon Yoluyla Sterilizasyon",
                  "Toplam Sterilizasyon","Net Fonlama","AOFM"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y")
    veri["Tarih"]=veri["Tarih"].dt.strftime("%d-%m-%Y")             
    return veri

def on():
    url="https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb+tr/main+menu/temel+faaliyetler/para+politikasi/merkez+bankasi+faiz+oranlari/faiz-oranlari"
    tablo=pd.read_html(url)
    veri=tablo[0]
    veri.drop(veri.index[0],inplace=True)
    veri.columns=["Tarih","Borç Alma","Borç Verme"]
    veri["Tarih"]=veri["Tarih"].apply(lambda x: datetime.strptime(x,"%d.%m.%y"))
    veri2=pd.DataFrame(columns=veri.columns)
    veri2["Tarih"]=pd.date_range(veri["Tarih"].iloc[0],datetime.today()+pd.DateOffset(months=1),freq="ME")

    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri2["Tarih"]=veri2["Tarih"].dt.to_period("M")

    veri2=veri2.merge(veri,on='Tarih',how='left')
    veri2.drop(columns=["Borç Alma_x","Borç Verme_x"],inplace=True)
    veri2=veri2.ffill()
    veri2.columns=veri.columns
    veri2["Tarih"]=veri2["Tarih"].dt.strftime("%d-%m-%Y") 
    return veri2

def glp():
    url="https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/Gec+Likidite+Penceresi+%28LON%29"
    tablo=pd.read_html(url)
    veri=tablo[0]
    veri.drop(veri.index[0],inplace=True)
    veri.columns=["Tarih","Borç Alma","Borç Verme"]
    veri["Tarih"]=veri["Tarih"].apply(lambda x: datetime.strptime(x,"%d.%m.%y"))
    veri2=pd.DataFrame(columns=veri.columns)
    veri2["Tarih"]=pd.date_range(veri["Tarih"].iloc[0],datetime.today()+pd.DateOffset(months=1),freq="ME")

    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri2["Tarih"]=veri2["Tarih"].dt.to_period("M")

    veri2=veri2.merge(veri,on='Tarih',how='left')
    veri2.drop(columns=["Borç Alma_x","Borç Verme_x"],inplace=True)
    veri2=veri2.ffill()
    veri2.columns=veri.columns
    veri2["Tarih"]=veri2["Tarih"].dt.strftime("%d-%m-%Y") 
    return veri2


def repo():
    url="https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/1+Hafta+Repo"
    tablo=pd.read_html(url)
    veri=tablo[0]
    veri.drop(veri.index[0],inplace=True)
    veri.columns=["Tarih","Borç Alma","Borç Verme"]
    veri["Tarih"]=veri["Tarih"].apply(lambda x: datetime.strptime(x,"%d.%m.%Y"))
    veri2=pd.DataFrame(columns=veri.columns)
    veri2["Tarih"]=pd.date_range(veri["Tarih"].iloc[0],datetime.today()+pd.DateOffset(months=1),freq="ME")

    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri2["Tarih"]=veri2["Tarih"].dt.to_period("M")

    veri2=veri2.merge(veri,on='Tarih',how='left')
    veri2.drop(columns=["Borç Alma_x","Borç Verme_x"],inplace=True)
    veri2=veri2.ffill()
    veri2.columns=veri.columns
    veri2["Tarih"]=veri2["Tarih"].dt.strftime("%d-%m-%Y") 
    return veri2

def tlref():
    start="28-12-2018"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.BISTTLREF.ORAN"],startdate=start,enddate=end)
    veri.dropna(axis=0,inplace=True)
    veri.columns=["Tarih","TLREF"]
    return veri


##------------------------------------------------------------------------------------

st.markdown("""
    <style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }
    .title {
        color: red;
        border: 2px solid black;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Freestyle Script', cursive;
        font-size: 55px; 
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title">Via Anlaşılır Ekonomi</h1>',unsafe_allow_html=True)
st.sidebar.title("Göstergeler")

##-----------------------------------------------------------------------------

button1=st.sidebar.button("MB APİ Fonlama")
button2=st.sidebar.button("MB Faizler")
button3=st.sidebar.button("MB Kur Değerleri")

if button1:
    st.session_state["button1_clicked"]=True
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=False

if button2:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=True
    st.session_state["button3_clicked"]=False

if button3:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=True

##-----------------------------------------------------------------------------

if st.session_state.get("button1_clicked",False):
    st.dataframe(mbapi(),hide_index=True,width=1000)

    fig=go.Figure()
    fig.add_trace(go.Scatter(
    x=pd.to_datetime(mbapi()["Tarih"],format="%d-%m-%Y"),
    y=mbapi()["Net Fonlama"],
    mode="lines",
    name="Net Fonlama"))

    fig.update_layout(title={
        "text":"APİ Net Fonlama","x":0.5,"xanchor":"center"},
    xaxis_title="Tarih",
    yaxis_title="Net Fonlama",
    xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1"))
    fig.update_xaxes(tickangle=-45)

    fig2=go.Figure()
    fig2.add_trace(go.Scatter(
    x=pd.to_datetime(mbapi()["Tarih"], format="%d-%m-%Y"),
    y=mbapi()["AOFM"],
    mode="lines",
    line=dict(color="red"),
    name="AOFM"))

    fig2.update_layout(title={
        "text":"AOFM (%)","x": 0.5,"xanchor": "center"},
    xaxis_title="Tarih",
    yaxis_title="AOFM",
    xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1"))
    fig2.update_xaxes(tickangle=-45)
    
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

##--------------------------------------------------------------------------

if st.session_state.get("button2_clicked",False):
    secenek=["O/N","GLP","1 Haftalık Repo","TLREF"]
    st.markdown('<p style="font-weight:bold; color:black;">Faiz Türünü Seçin:</p>',unsafe_allow_html=True)
    faiz_secim=st.radio("",secenek,index=None,horizontal=True)
    
    if faiz_secim=="O/N":
        st.markdown('<p style="font-weight:bold; color:black;">O/N (%)</p>',unsafe_allow_html=True)
        st.dataframe(on(),hide_index=True,width=1000)

        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(on()["Tarih"],format="%d-%m-%Y"),
        y=on()["Borç Alma"],
        mode="lines",
        name="Borç Alma",
        line=dict(color="red")))

        fig.add_trace(go.Scatter(
        x=pd.to_datetime(on()["Tarih"], format="%d-%m-%Y"),
        y=on()["Borç Verme"],
        mode="lines",
        name="Borç Verme",
        line=dict(color="Blue")))

        fig.update_layout(title={
            "text":"O/N (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Faiz",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M3"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)

    elif faiz_secim=="GLP":
        st.markdown('<p style="font-weight:bold; color:black;">GLP (%)</p>',unsafe_allow_html=True)
        st.dataframe(glp(),hide_index=True,width=1000)

        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(glp()["Tarih"],format="%d-%m-%Y"),
        y=glp()["Borç Alma"],
        mode="lines",
        name="Borç Alma",
        line=dict(color="red")))

        fig.add_trace(go.Scatter(
        x=pd.to_datetime(glp()["Tarih"], format="%d-%m-%Y"),
        y=glp()["Borç Verme"],
        mode="lines",
        name="Borç Verme",
        line=dict(color="Blue")))

        fig.update_layout(title={
            "text":"GLP (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Faiz",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M3"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)

    elif faiz_secim=="1 Haftalık Repo":
        st.markdown('<p style="font-weight:bold; color:black;">1 Haftalık Repo (%)</p>',unsafe_allow_html=True)
        st.dataframe(repo(),hide_index=True,width=1000)

        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(repo()["Tarih"], format="%d-%m-%Y"),
        y=repo()["Borç Verme"],
        mode="lines",
        name="Borç Verme",
        line=dict(color="Red")))

        fig.update_layout(title={
            "text":"1 Haftalık Repo (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Faiz",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M3"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)
    
    elif faiz_secim=="TLREF":
        st.markdown('<p style="font-weight:bold; color:black;">TLREF (%)</p>',unsafe_allow_html=True)
        st.dataframe(tlref(),hide_index=True,width=1000)

        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(tlref()["Tarih"], format="%d-%m-%Y"),
        y=tlref()["TLREF"],
        mode="lines",
        name="TLREF",
        line=dict(color="Red")))

        fig.update_layout(title={
            "text":"TLREF (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Faiz",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)

##---------------------------------------------------------------------------------

if st.session_state.get("button3_clicked",False):
    st.markdown("<h4><strong>Lütfen Tarih Seçiniz...</strong></h4>",unsafe_allow_html=True)
    tarih=st.date_input("",format="DD/MM/YYYY",max_value=datetime.today().date())
    gun=str(tarih.day).zfill(2)
    ay=str(tarih.month).zfill(2)
    yıl=str(tarih.year).zfill(2)

    url=f'https://www.tcmb.gov.tr/kurlar/{yıl+ay}/{gun+ay+yıl}.xml?_=1726480314217'

    try:
        veri=pd.read_xml(url)
        veri.drop(columns=["CrossOrder","Kod","CurrencyName","CrossRateUSD","CrossRateOther"],inplace=True)
        veri.columns=["Döviz Kodu","Birim","İsim","Döviz Alış","Döviz Satış","Efektif Alış","Efektif Satış"]
        veri["Döviz Kodu"]=veri["Döviz Kodu"].apply(lambda x: f"{x}/TRY")
        veri.drop(veri.index[-1],inplace=True)
        veri=veri.fillna("-")
        st.dataframe(veri,hide_index=True,width=1000)
    except HTTPError as e:
        st.markdown("<p style='color:red; font-weight:bold;'>Girdiğiniz tarihte kur bilgisi yoktur. Lütfen tarihleri kontrol ediniz...</p>", unsafe_allow_html=True)

##---------------------------------------------------------------------------------- 


