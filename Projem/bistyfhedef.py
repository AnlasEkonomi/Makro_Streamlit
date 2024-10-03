import requests
import pandas as pd
from io import StringIO
from yahooquery import Ticker
import streamlit as st

def hedef_fiyat_yahoo():    
    def hisseler():
        url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?endeks=01#page-1"
        html_text=requests.get(url).text
        html_io=StringIO(html_text)
        tablo=pd.read_html(html_io)[2]["Kod"]
        for i in range(len(tablo)):
            tablo[i] += ".IS"
        hissekod=tablo.to_list()
        return hissekod
    hisse=Ticker(hisseler())
    hisse_dict=hisse.financial_data
    veri=pd.DataFrame.from_dict(hisse_dict).T.reset_index().iloc[:,[0,2,24,25,26,27]]
    veri.columns=["Hisse Adı","Güncel Fiyat","En Yüksek Tahmin","En Düşük Tahmin",
            "Ortalama Tahmin","Medyan Tahmin"]
    veri["Hisse Adı"]=veri["Hisse Adı"].str.replace(".IS","",regex=False)
    veri.dropna(axis=0,inplace=True)
    veri.reset_index(drop=True,inplace=True)
    return veri

st.markdown("<h4 style='font-size:20px;'>Yahoo Hedef Fiyat</h4>",unsafe_allow_html=True)
st.dataframe(hedef_fiyat_yahoo(),hide_index=True,use_container_width=True,width=1200,height=600)