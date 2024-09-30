import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime,timedelta
import streamlit as st
from concurrent.futures import ThreadPoolExecutor

def li(ilk,son):
    try:
        url=f"https://www.takasbank.com.tr/tr/istatistikler/takasbank-para-piyasasi-tpp/tpp-islem-ortalamalari-raporu?page=1&startDate={ilk}&endDate={son}"
        response=requests.get(url)
        soup=BeautifulSoup(response.content, "html.parser")
        li=soup.find("ul",class_="pagination flat-list lm-xs-b10").find_all("li")
        return int(li[-2].text)
    except AttributeError:
        st.error("Girdiğiniz tarih aralığında veri yoktur. Lütfen kontrol ediniz!")

def vericek(sayfa,ilk,son):
    url=f"https://www.takasbank.com.tr/tr/istatistikler/takasbank-para-piyasasi-tpp/tpp-islem-ortalamalari-raporu?page={sayfa}&startDate={ilk}&endDate={son}"
    veri=pd.read_html(url,decimal=',',thousands='.')[0]
    return veri

def tpp(ilk,son):
    try:
        toplam_sayfa=li(ilk,son)
        sayfalar=[]

        with ThreadPoolExecutor() as executor:
            futures=[executor.submit(vericek,i,ilk,son) for i in range(1,toplam_sayfa+1)]
            for future in futures:
                sayfalar.append(future.result())

        tumveri=pd.concat(sayfalar,ignore_index=True)
        tumveri["İşlem Tarihi"]=tumveri["İşlem Tarihi"].astype(str)
        tumveri["İşlem Tarihi"]=tumveri["İşlem Tarihi"].str.replace(",", ".")
        tumveri["İşlem Tarihi"]=tumveri["İşlem Tarihi"].astype(str).str.zfill(8)
        tumveri["İşlem Tarihi"]=pd.to_datetime(tumveri["İşlem Tarihi"],format="%d%m%Y").dt.strftime("%d-%m-%Y")
        return tumveri
    except TypeError:
        st.write("")

st.markdown("<h4><strong>Lütfen Tarih Aralığı Seçiniz...</strong></h4>", unsafe_allow_html=True)
tarih1=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date()-timedelta(days=5),max_value=datetime.today().date(),key="Giriş")
tarih2=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date(),max_value=datetime.today().date(),min_value=tarih1,key="Çıkış")

st.session_state["ilk_tarih"]=tarih1.strftime("%Y-%m-%d")
st.session_state["son_tarih"]=tarih2.strftime("%Y-%m-%d")

veri=tpp(st.session_state["ilk_tarih"],st.session_state["son_tarih"])
st.markdown("<h4 style='font-size:20px;'>TPP İşlem Özeti</h4>",unsafe_allow_html=True)
st.dataframe(veri,hide_index=True,use_container_width=True)