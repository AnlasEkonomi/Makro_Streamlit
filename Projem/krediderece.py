import requests
import pandas as pd
import streamlit as st

url="https://www.ttyatirimciiliskileri.com.tr/tr-tr/bono-tahvil/sayfalar/kredi-notlari"
url2="https://countryeconomy.com/ratings/turkey"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
response=requests.get(url,headers=headers)
response2=requests.get(url2,headers=headers)

aylar={
    "Ocak": "Jan",
    "Şubat": "Feb",
    "Mart": "Mar",
    "Nisan": "Apr",
    "Mayıs": "May",
    "Haziran": "Jun",
    "Temmuz": "Jul",
    "Ağustos": "Aug",
    "Eylül": "Sep",
    "Ekim": "Oct",
    "Kasım": "Nov",
    "Aralık": "Dec"}


fitch=pd.read_html(response.content,encoding="utf-8")[1]
fitch.columns=fitch.iloc[0]
fitch=fitch[1:].reset_index(drop=True)
for tray, enay in aylar.items():
    fitch["Tarih"]=fitch["Tarih"].str.replace(tray,enay)
fitch["Tarih"]=pd.to_datetime(fitch["Tarih"],format='%d %b %Y').dt.strftime("%d-%m-%Y")


sp=pd.read_html(response.content,encoding="utf-8")[2]
sp.columns=sp.iloc[0]
sp=sp[1:].reset_index(drop=True)
for tray, enay in aylar.items():
    sp["Tarih"]=sp["Tarih"].str.replace(tray,enay)
sp["Tarih"]=pd.to_datetime(sp["Tarih"],format='%d %b %Y').dt.strftime("%d-%m-%Y")

mod=pd.read_html(response2.content)[0]["Long term Rating"]["Foreign currency"]
mod[["Kredi Notu","Görünüm"]]=mod["Rating(Outlook)"].str.extract(r'([^ ]+) \(([^)]+)\)')
mod.drop(columns=["Rating(Outlook)"],inplace=True)
mod.rename(columns={"Date":"Tarih"},inplace=True)
mod["Tarih"]=pd.to_datetime(mod["Tarih"]).dt.strftime("%d-%m-%Y")

tr={
    "Positive":"Pozitif",
    "Negative":"Negatif",
    "Stable":"Durağan",
    "Under Review":"İnceleniyor"}
mod["Görünüm"]=mod["Görünüm"].map(tr)
mod.dropna(axis=0,inplace=True)


secenek=["Moody's","Fitch","S&P"] 
st.markdown('<p style="font-weight:bold; color:black;">Kurum Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)

resim="Resimler\kredi.jpg"

if secim=="Fitch":
    st.dataframe(fitch,hide_index=True,use_container_width=True)
    st.image(resim,use_column_width=True)
elif secim=="S&P":
    st.dataframe(sp,hide_index=True,use_container_width=True)
    st.image(resim,use_column_width=True)
elif secim=="Moody's":
    st.dataframe(mod,hide_index=True,use_container_width=True)
    st.image(resim,use_column_width=True)