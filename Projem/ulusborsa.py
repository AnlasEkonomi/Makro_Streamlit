import pandas as pd
from io import StringIO
import cloudscraper
from bs4 import BeautifulSoup
import streamlit as st

def borsa():
    scraper=cloudscraper.CloudScraper()
    url="https://www.investing.com/indices/world-indices"

    headers={
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://tr.investing.com",
            "Referer": "https://tr.investing.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Domain-ID": "tr"}
    
    veri=scraper.post(url,headers=headers)
    html=StringIO(veri.text)
    tablo=pd.read_html(html)
    soup=BeautifulSoup(html,"html.parser").find("section",{"id":"leftColumn"}).find_all("h2")

    ülkeler=[]
    for i in soup:
        ülkeler.append(i.text)

    for i in range(0,91):
        tablo[i].drop(columns=["Unnamed: 0","Unnamed: 8"],inplace=True)  
        tablo[i].columns=["Endeks","Son","Yüksek","Düşük","Değişim","Değişim (%)",
                          "Saat-Tarih"]
    return tablo,ülkeler

tablo=borsa()[0]
ülke=borsa()[1]


st.markdown("<h4 style='font-size:20px;'>Ülkeler</h4>",unsafe_allow_html=True)
for i in range(len(ülke)):
    with st.expander(str(ülke[i])):
        st.dataframe(tablo[i],hide_index=True,use_container_width=True)
