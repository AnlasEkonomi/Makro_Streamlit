import requests
import pandas as pd
from io import StringIO
import plotly.express as px
import streamlit as st

def bisttreemap():
    url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx#page-1"
    r=requests.get(url).text
    tablo=pd.read_html(StringIO(r))[2]
    sektor=pd.DataFrame({"Hisse":tablo["Kod"],"Sektör":tablo["Sektör"],"Piyasa Değeri (mn $)":tablo["Piyasa Değeri (mn $)"]})
    tablo2=pd.read_html(StringIO(r))[6]
    
    try:
        getiri=pd.DataFrame({"Hisse":tablo2["Kod"],"Getiri (%)":tablo2["Günlük Getiri (%)"]/100})
    except TypeError:
        tablo2["Günlük Getiri (%)"]=pd.to_numeric(tablo2["Günlük Getiri (%)"].str.replace('%', '').str.replace(',', '.'),errors='coerce')
        getiri=pd.DataFrame({"Hisse":tablo2["Kod"],"Getiri (%)":tablo2["Günlük Getiri (%)"]/100})
    
    df=pd.merge(sektor,getiri,on="Hisse")
    df["Piyasa Değeri (mn $)"]=df["Piyasa Değeri (mn $)"].str.replace('.', '').str.replace(',', '.').astype("float64")
    
    renk_aralik=[-10,-5,-0.01,0,0.01,5,10]
    df["Renk"]=pd.cut(df["Getiri (%)"],bins=renk_aralik,labels=["red","indianred","lightpink","lightgreen","lime","green"])

    fig=px.treemap(df,path=[px.Constant("Borsa İstanbul"),"Sektör","Hisse"],values="Piyasa Değeri (mn $)",
                    color="Renk",custom_data=["Getiri (%)","Sektör"],
                    color_discrete_map={"(?)":"#262931","red":"red","indianred":"indianred", 
                                        "lightpink":"lightpink","lightgreen":"lightgreen","lime":"lime","green":"green"})
    fig.update_layout(width=2000,height=1600)
    fig.update_traces(
        hovertemplate="<br>".join([
            "Hisse: %{label}",
            "Piyasa Değeri (mn $): %{value}",
            "Getiri: %{customdata[0]}",
            "Sektör: %{customdata[1]}"]))
    fig.data[0].texttemplate="<b>%{label}</b><br>%{customdata[0]} %"
    st.plotly_chart(fig)

bisttreemap()
