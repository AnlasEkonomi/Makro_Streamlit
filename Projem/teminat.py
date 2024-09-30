import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime,timedelta
import streamlit as st
from concurrent.futures import ThreadPoolExecutor
import plotly.graph_objects as go

def li(ilk,son):
    try:
        url=f"https://www.takasbank.com.tr/tr/istatistikler/vadeli-islem-ve-opsiyon-piyasasi-viop/teminat-tamamlama-cagrisi-raporu?page=1&startDate={ilk}&endDate={son}&reportNumber=0"
        response=requests.get(url)
        soup=BeautifulSoup(response.content, "html.parser")
        li=soup.find("ul",class_="pagination flat-list lm-xs-b10").find_all("li")
        return int(li[-2].text)
    except (AttributeError):
        st.error("Girdiğiniz tarih aralığında veri yoktur. Lütfen kontrol ediniz!")
    
def vericek(sayfa,ilk,son):
    url=f"https://www.takasbank.com.tr/tr/istatistikler/vadeli-islem-ve-opsiyon-piyasasi-viop/teminat-tamamlama-cagrisi-raporu?page={sayfa}&startDate={ilk}&endDate={son}&reportNumber=0"
    veri=pd.read_html(url,decimal=',',thousands='.')[0]
    return veri

def teminat(ilk,son):
    try:
        toplam_sayfa=li(ilk,son)
        sayfalar=[]

        with ThreadPoolExecutor() as executor:
            futures=[executor.submit(vericek,i,ilk,son) for i in range(1,toplam_sayfa+1)]
            for future in futures:
                sayfalar.append(future.result())

        tumveri=pd.concat(sayfalar,ignore_index=True)
        tumveri["Tarih"]=tumveri["Tarih"].astype(str)
        tumveri["Tarih"]=tumveri["Tarih"].str.replace(",", ".")
        tumveri["Tarih"]=tumveri["Tarih"].astype(str).str.zfill(8)
        tumveri["Tarih"]=pd.to_datetime(tumveri["Tarih"],format="%d%m%Y").dt.strftime("%d-%m-%Y")
        return tumveri
    except TypeError:
        st.write("")

st.markdown("<h4><strong>Lütfen Tarih Aralığı Seçiniz...</strong></h4>", unsafe_allow_html=True)
tarih1=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date()-timedelta(days=32),max_value=datetime.today().date(),key="Giriş")
tarih2=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date(),max_value=datetime.today().date(),min_value=tarih1,key="Çıkış")

st.session_state["ilk_tarih"]=tarih1.strftime("%Y-%m-%d")
st.session_state["son_tarih"]=tarih2.strftime("%Y-%m-%d")

veri=teminat(st.session_state["ilk_tarih"],st.session_state["son_tarih"])
st.markdown("<h4 style='font-size:20px;'>Teminat Tamamlama İşlem Özeti</h4>",unsafe_allow_html=True)
st.dataframe(veri,hide_index=True,use_container_width=True)

fig=go.Figure()
fig.add_trace(go.Scatter(x=veri["Tarih"],y=veri["Teminat Tamamlama Çağrısı"],mode="lines+markers",name="Tutar (TL)"))

fig.update_layout(
    title='Günlük Teminat Tutarları',xaxis_title="İşlem Tarihi",yaxis_title="Tutar (TL)",
    xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))

fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_xaxes(tickangle=-45)
st.plotly_chart(fig)