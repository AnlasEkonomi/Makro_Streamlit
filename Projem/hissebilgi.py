import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from io import StringIO

def hissead():
    hisseler=[]
    url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=ACSEL"
    r=requests.get(url)
    s=BeautifulSoup(r.text,"html.parser")
    hisseler=[a.string for a in s.find("select",id="ddlAddCompare").find("optgroup").find_all("option")]
    return hisseler

def info(hisse):
    url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+hisse
    bilgi=pd.read_html(url)[4]
    unvan=str(bilgi.iloc[:,1][0])
    kurulustarih=str(bilgi.iloc[:,1][1])
    faaliyet=str(bilgi.iloc[:,1][2])
    telefon=str(bilgi.iloc[:,1][3])
    faks=str(bilgi.iloc[:,1][4])
    adres=str(bilgi.iloc[:,1][5])
    endeks=pd.DataFrame(pd.read_html(url,decimal=',',thousands='.')[3].iloc[0]).reset_index().sort_index(ascending=False)

    return unvan,kurulustarih,faaliyet,telefon,faks,adres,endeks

st.markdown("**Hisse Senedi Seçin:**")
hisse_secim = st.selectbox('', hissead())

unvan,kurulustarih,faaliyet,telefon,faks,adres,endeks=info(hisse_secim)

st.markdown("<h3 style='font-size: 30px;'>Şirket Künyesi</h3>",unsafe_allow_html=True)
st.markdown("""
<style>
.readonly {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 5px;
    color: black; 
    font-weight: bold;
    padding: 16px; 
    font-size: 16px;
    margin-bottom: 11px; 
}
</style>
""", unsafe_allow_html=True)

html_content = "<div class='readonly'>"
for index, row in endeks.iterrows():
    html_content += f"{row['index']}: {row[0]}<br>"
html_content += "</div>"

st.markdown(f'<div class="readonly">Şirket Unvanı: {unvan}</div>',unsafe_allow_html=True)
st.markdown(f'<div class="readonly">Kuruluş Tarihi: {kurulustarih}</div>',unsafe_allow_html=True)
st.markdown(f'<div class="readonly">Faaliyet Alanı: {faaliyet}</div>',unsafe_allow_html=True)
st.markdown(f'<div class="readonly">Telefon: {telefon}</div>',unsafe_allow_html=True)
st.markdown(f'<div class="readonly">Faks: {faks}</div>',unsafe_allow_html=True)
st.markdown(f'<div class="readonly">Adres: {adres}</div>',unsafe_allow_html=True)
st.markdown(html_content,unsafe_allow_html=True)

def info2(hisse,tür):
    link=f"https://analizim.halkyatirim.com.tr/Financial/ScoreCardDetail?hisseKod={hisse}"
    r=requests.get(link,headers={'User-Agent': 'XYZ/3.0'})
    soup=BeautifulSoup(r.content,"html.parser")

    if tür==secenek[0]:
        tablo=soup.find("div",{"id":"pazar-endeskleri"})
        tablo=pd.read_html(StringIO(str(tablo)),flavor="bs4")[0]
        tablo.columns=["Özellikler","Bilgiler"]
        tablo.drop(axis=0,index=1,inplace=True)
        tablo.fillna("-",inplace=True)
    elif tür==secenek[1]:
        tablo=soup.find("div",{"id":"fiyat-performansi"})
        tablo=pd.read_html(StringIO(str(tablo)),flavor="bs4")[0]
        tablo.columns.values[0]=""
        tablo.fillna("-",inplace=True)
    elif tür==secenek[2]:
        tablo=soup.find("div",{"id":"piyasa-degeri"})
        tablo=pd.read_html(StringIO(str(tablo)),flavor="bs4")[0]
        tablo.columns=[""," "]
        tablo.fillna("-",inplace=True)
    elif tür==secenek[3]:
        tablo=soup.find("div",{"id":"teknik-veriler"})
        tablo=pd.read_html(StringIO(str(tablo)),flavor="bs4")[0]
        tablo.columns=["Teknik","Değer","Sonuç"]
        tablo.fillna("-",inplace=True)
    elif tür==secenek[4]:
        tablo=soup.find("div",{"id":"temel-veri-analizleri"})
        tablo=pd.read_html(StringIO(str(tablo)),flavor="bs4")[0]
        tablo.columns=["Kalemler","Değerler"]
        tablo.fillna("-",inplace=True)
    elif tür==secenek[5]:
        tablo=soup.find("div",{"id":"fiyat-ozeti"})
        tablo=pd.read_html(StringIO(str(tablo)),flavor="bs4")[0]
        tablo.columns=["Kalemler","Değerler"]
        tablo.fillna("-",inplace=True)
    elif tür==secenek[6]:
        tablo=soup.find("div",{"id":"finanslar"})
        tablo=pd.read_html(StringIO(str(tablo)),flavor="bs4")[0]
        tablo.fillna("-",inplace=True)
    elif tür==secenek[7]:
        tablo=soup.find("div",{"id":"karlilik"})
        tablo=pd.read_html(StringIO(str(tablo)),flavor="bs4")[0]
        tablo.fillna("-",inplace=True)
    elif tür==secenek[8]:
        tablo=soup.find("div",{"id":"carpanlar"})
        tablo=pd.read_html(StringIO(str(tablo)),flavor="bs4")[0]
        tablo.fillna("-",inplace=True)

    return tablo

secenek=["Pazar Endeksleri","Fiyat Performans","Piyasa Değeri","Teknik Veriler",
         "Temel Verileri","Fiyat Özeti","Finansallar","Karlılık","Çarpanlar"]
st.markdown('<p style="font-weight:bold; color:black;">İşlem Seçiniz:</p>',unsafe_allow_html=True)
tur_secim=st.radio("",secenek,index=0,horizontal=True)

if hisse_secim and tur_secim:
    tablo=info2(hisse_secim,tur_secim)
    st.dataframe(tablo,hide_index=True,use_container_width=True)
