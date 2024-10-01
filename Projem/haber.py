import requests
import pandas as pd
from io import StringIO
import streamlit as st
from bs4 import BeautifulSoup
import bs4

def yerli():
    url="https://www.matriksdata.com/website/matriks-haberler/"
    req=requests.get(url)
    html=StringIO(req.text)
    table=pd.read_html(html)[0]
    link=BeautifulSoup(req.text,"html.parser")
    link=link.find("div",{"id":"ContentPlaceHolder1_divTable"}).find("tbody")

    linkler=[]

    for i in link:
        if isinstance(i,bs4.element.Tag):
            onclick_attr=i.get("onclick")
            if onclick_attr and "document.location=" in onclick_attr:
                start_idx=onclick_attr.find("'") + 1
                end_idx=onclick_attr.rfind("'")
                link=onclick_attr[start_idx:end_idx]
                linkler.append(link)
    table["Link"]=linkler
    return table

def yabancı():
    url="https://finviz.com/news.ashx"
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}

    req=requests.get(url,headers=headers)
    html=StringIO(req.text)
    table=pd.read_html(html)[4]
    table.columns=["0","Tarih","Konu"]
    table.drop(columns=["0"],inplace=True)
    link=BeautifulSoup(req.text,"html.parser")

    linkler=[]

    for row in link.find_all("tr"):
        onclick_attr=row.get("onclick")
        if onclick_attr and "trackAndOpenNews" in onclick_attr:
            start_idx=onclick_attr.find("'") + 1
            end_idx=onclick_attr.rfind("'")
            link=onclick_attr[start_idx:end_idx]
            linkler.append(link)
            linkler=linkler[:90]
    table["Link"]=linkler
    return table

secenek=["Yerli (Matriks Haber)","Uluslararası"]
st.markdown('<p style="font-weight:bold; color:black;">Haber Kaynağı Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)

if secim=="Yerli (Matriks Haber)":
    veri=yerli()
    st.dataframe(veri,hide_index=True,height=600,use_container_width=True,
                 column_config={"Link": st.column_config.LinkColumn(label="Link",display_text="🔗")})
if secim=="Uluslararası":
    veri=yabancı()
    st.dataframe(veri,hide_index=True,height=600,use_container_width=True,
                 column_config={"Link": st.column_config.LinkColumn(label="Link",display_text="🔗")})

