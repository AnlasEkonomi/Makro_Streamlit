import pandas as pd
import requests
import streamlit as st
from datetime import datetime,timedelta
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from io import StringIO
import numpy as np

def opetil():
    urlil="https://api.opet.com.tr/api/fuelprices/provinces"
    il=pd.DataFrame(requests.get(urlil).json())
    return il

def poil():
    urlil="https://www.petrolofisi.com.tr/arsiv-fiyatlari"
    req=requests.get(urlil)
    soup=BeautifulSoup(req.content,"html.parser")
    id=soup.find("select",{"id":"filterCity"})
    kod=[]
    il=[]

    for i in id:
        if i and i.name=="option":
            kod.append(i.get("value"))
            il.append(i.text)
    veri=pd.DataFrame({"Kod":kod,"İl":il})
    veri=veri.iloc[1:].reset_index(drop=True)
    return veri


def opetilce(ilkod):
    urlilce=f"https://api.opet.com.tr/api/fuelprices/provinces/{ilkod}/districts"
    ilce=pd.DataFrame(requests.get(urlilce).json())
    ilce.drop(columns=["latitude","longitude","isCenter"],inplace=True)
    return ilce

def poilce(ilkod):
    urlilce="https://www.petrolofisi.com.tr/District/Search"
    yuk={"cityId": ilkod}
    req=requests.post(urlilce,data=yuk)
    soup=BeautifulSoup(req.text,"html.parser")
    options=soup.find_all("option")

    kod=[]
    ilce=[]
    for option in options:
        kod.append(option.get('value'))
        ilce.append(option.text.strip())
    veri=pd.DataFrame({"Kod":kod,"İlçe":ilce})
    return veri

def opetfiyat(ilcekod,ilktarih,sontarih):
    try:
        urlfiyat=f"https://api.opet.com.tr/api/fuelprices/prices/archive?DistrictCode={ilcekod}&StartDate={ilktarih}T20:57:41.180Z&EndDate={sontarih}T20:57:41.180Z&IncludeAllProducts=true"
        fiyat=pd.DataFrame(requests.get(urlfiyat).json())["prices"]
        ayır=pd.DataFrame(fiyat.explode("prices"))
        fiyat=ayır["prices"].apply(pd.Series) 
        fiyat[["priceDate1","2"]]=fiyat["priceDate"].str.split("T",expand=True)
        fiyat.drop(columns=["priceDate","productShortName","productCode","2"],inplace=True)
        fiyat["priceDate1"]=pd.to_datetime(fiyat["priceDate1"]).dt.strftime("%d-%m-%Y")
        fiyat=fiyat[["priceDate1","productName","amount"]]
        fiyat.columns=["Tarih","Ürün","Fiyat"]
        fiyat['Tarih']=pd.to_datetime(fiyat['Tarih'], format='%d-%m-%Y')
        fiyat=fiyat.pivot(index='Tarih',columns='Ürün',values='Fiyat')
        fiyat.reset_index(inplace=True)
        fiyat["Tarih"]=fiyat["Tarih"].dt.strftime("%d-%m-%Y")
        return fiyat
    except (ValueError,KeyError,AttributeError):
        st.error("Aradığınız Tarihler Arasında Veri Bulunamadı...")
    
def pofiyat(ilcekod,ilktarih,sontarih):
    urlfiyat="https://www.petrolofisi.com.tr/Fuel/Search"
    yuk={"template": 3,
         "cityId":ilkod,
         "districtId":ilcekod,
         "startDate":ilktarih,
         "endDate":sontarih}
    req=requests.post(urlfiyat,data=yuk)
    html= StringIO(req.text)
    veri=pd.read_html(html)[0]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"],dayfirst=True,format="%d.%m.%Y")
    veri.sort_values(by="Tarih",inplace=True)
    veri["Tarih"]=veri["Tarih"].dt.strftime("%d-%m-%Y")
    
    for i in veri.columns[1:]:
        veri[i]=veri[i].str.split().str[0]
    
    sütunad=["Tarih","V/Max Kurşunsuz 95 (LT)","V/Pro Diesel (LT)","V/Max Diesel (LT)",
             "Gazyağı (LT)","Kalorifer Yakıtı (KG)","%1 Kükürtlü Fuel Oil (KG)",
             "PO/gaz Otogaz (LT)"]
    veri.columns=sütunad
    veri.replace("-",np.nan,inplace=True)
    veri.fillna(method="ffill",inplace=True)
    return veri


secenek=["Opet","Petrol Ofisi","Shell","BP","TP"]
st.markdown('<p style="font-weight:bold; color:black;">Firma Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)

if secim=="Opet":
    if secim=="Opet":
        il_df=opetil()
        il=st.selectbox("İl Seçiniz:",options=il_df["name"])
        ilkod=il_df.loc[il_df["name"]==il,"code"].values[0]
        ilce_df=opetilce(ilkod)
        ilce=st.selectbox("İlçe Seçiniz:",options=ilce_df["name"])
        ilcekod=ilce_df.loc[ilce_df["name"]==ilce,"code"].values[0]
        fiyat=opetfiyat(ilcekod,st.session_state["ilk_tarih"],st.session_state["son_tarih"])
        
        st.markdown("<h4><strong>Lütfen Tarih Aralığı Seçiniz...</strong></h4>",unsafe_allow_html=True)
        tarih1=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date()-timedelta(days=32),max_value=datetime.today().date()-timedelta(days=1),key="Giriş")
        tarih2=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date()-timedelta(days=1),max_value=datetime.today().date()-timedelta(days=1),min_value=tarih1,key="Çıkış")
        
        st.session_state["ilk_tarih"]=tarih1.strftime("%Y-%m-%d")
        st.session_state["son_tarih"]=tarih2.strftime("%Y-%m-%d")

        st.markdown(f"<h4 style='font-size:20px;'>{secim} Ürün Fiyat Arşivi ({str(il).capitalize()}-{str(ilce).capitalize()}) </h4>",unsafe_allow_html=True)
        st.dataframe(fiyat,hide_index=True,use_container_width=True)

        fig=go.Figure()
        for col in fiyat.columns[1:]:
            fig.add_trace(go.Scatter(x=fiyat["Tarih"],y=fiyat[col],mode="lines",name=col))
            grafik_baslik=f"{secim} Fiyat ({str(il).capitalize()}-{str(ilce).capitalize()})"
        fig.update_layout(barmode="stack")

        fig.update_layout(title=grafik_baslik,xaxis_title="Tarih",yaxis_title="Fiyat",
        template="plotly_white",
        xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))

        fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)

if secim=="Petrol Ofisi":
    if secim=="Petrol Ofisi":
        il_df=poil()
        il=st.selectbox("İl Seçiniz:",options=il_df["İl"])
        ilkod=il_df.loc[il_df["İl"]==il,"Kod"].values[0]
        ilce_df=poilce(ilkod)
        ilce=st.selectbox("İlçe Seçiniz:",options=ilce_df["İlçe"])
        ilcekod=ilce_df.loc[ilce_df["İlçe"]==ilce,"Kod"].values[0]
        fiyat=pofiyat(ilcekod,st.session_state["ilk_tarih"],st.session_state["son_tarih"])

        st.markdown("<h4><strong>Lütfen Tarih Aralığı Seçiniz...</strong></h4>",unsafe_allow_html=True)
        tarih1=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date()-timedelta(days=32),max_value=datetime.today().date()-timedelta(days=1),key="Giriş")
        tarih2=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date()-timedelta(days=1),max_value=datetime.today().date()-timedelta(days=1),min_value=tarih1,key="Çıkış")
        
        st.session_state["ilk_tarih"]=tarih1.strftime("%d-%m-%Y")
        st.session_state["son_tarih"]=tarih2.strftime("%d-%m-%Y")

        st.markdown(f"<h4 style='font-size:20px;'>{secim} Ürün Fiyat Arşivi ({str(il).capitalize()}-{str(ilce).capitalize()}) </h4>",unsafe_allow_html=True)
        st.dataframe(fiyat,hide_index=True,use_container_width=True)

        fig=go.Figure()
        for col in fiyat.columns[1:]:
            fig.add_trace(go.Scatter(x=fiyat["Tarih"],y=fiyat[col],mode="lines",name=col))
            grafik_baslik=f"{secim} Fiyat ({str(il).capitalize()}-{str(ilce).capitalize()})"
        fig.update_layout(barmode="stack")

        fig.update_layout(title=grafik_baslik,xaxis_title="Tarih",yaxis_title="Fiyat",
        template="plotly_white",
        xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))

        fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)
