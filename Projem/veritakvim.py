import requests
import pandas as pd
from datetime import datetime
import streamlit as st

yıl=datetime.today().year

def veritakvim(yayım_durumu):
    try:
        url=f"https://www.tuik.gov.tr/Kurumsal/GetYillikHaberBulteniListesi?yil={yıl}"
        req=requests.get(url).json()[yayım_durumu]
        veri=pd.DataFrame(req)
        veri.rename(columns={"sorumluKurum":"Kurum","link":"Link","gTarih":"Gönderi Tarihi",
                             "donemi":"Veri Dönemi","adi":"Veri Adı"},inplace=True)
        veri.drop(columns=["sorumluKisaAd","dilId","birimi","id"],inplace=True)
        veri=veri[["Kurum","Veri Adı","Gönderi Tarihi","Veri Dönemi","Link"]]
        
        veri[["Tarih","Saat"]]=veri["Gönderi Tarihi"].str.split("T",expand=True)
        veri["Gönderi Tarihi"]=pd.to_datetime(veri["Tarih"] + ' ' + veri["Saat"])
        veri["Gönderi Tarihi"]=veri["Gönderi Tarihi"].dt.strftime('%d/%m/%Y %H:%M:%S')
        veri.drop(columns=["Tarih","Saat"],inplace=True)
        
        return veri
    except requests.exceptions.ConnectionError:
        st.error("Beklenmedik bir hata oluştu...")

secenekler={"Yayımlananlar":"yayindaOlanlarList","Yayımlanacaklar":"yayindaOlmayanlarList"}
st.markdown('<p style="font-weight:bold; color:black;">Yayımlanma Durumu Seçiniz:</p>', unsafe_allow_html=True)
secim=st.radio("", list(secenekler.keys()),index=0,horizontal=True)

veri=veritakvim(secenekler[secim])
st.dataframe(veri,hide_index=True,height=550,use_container_width=True,
             column_config={"Link": st.column_config.LinkColumn()})
