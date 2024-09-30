from datetime import datetime,timedelta
import requests
import pandas as pd
import streamlit as st

def ekonomiktakvim():
    bugün=datetime.today()
    haftanınilkgünü=(bugün-timedelta(days=bugün.weekday())).strftime("%Y%m%d")
    haftanınsongünü=(bugün-timedelta(days=bugün.weekday())+timedelta(days=6)).strftime("%Y%m%d")

    url=f'https://yatirim.akbank.com/_vti_bin/AkbankYatirimciPortali/Hisse/Service.svc/EkonomikTakvimForList/{haftanınilkgünü+"000000"}/{haftanınsongünü+"235900"}'
    data=requests.get(url).json()

    deger=[]
    for i in data["Data"]:
        key=i["Key"]
        for value in i["Value"]:
            value["Key"]=key
            deger.append(value)

    df=pd.DataFrame(deger)
    veri=df[["Key","Tsi","Country","Event","Actual","Forecast","Previous"]]
    veri.columns=["Tarih","Saat (TSİ)","Ülke","Olay","Açıklanan","Tahmin","Önceki"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d/%m/%Y")
    bugün=datetime.today().date()
    veri=veri[veri["Tarih"].dt.date >= bugün]
    veri["Tarih"]=veri["Tarih"].dt.strftime("%d-%m-%Y")
    veri["Saat (TSİ)"]=pd.to_datetime(veri["Saat (TSİ)"],format="%H%M").dt.strftime("%H:%M")
    veri.sort_values(by=["Tarih","Saat (TSİ)"],ascending=True,inplace=True)
    return veri

st.markdown("<h4 style='font-size:20px;'>Bu Hafta Takvimi</h4>",unsafe_allow_html=True)
st.dataframe(ekonomiktakvim(),hide_index=True,use_container_width=True,height=700)