import evds as ev
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def gsyhharcama(frekans):
    start="01-01-1998"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.GSYIH20.HY.CF","TP.GSYIH27.HY.CF","TP.GSYIH21.HY.CF","TP.GSYIH22.HY.CF",
            "TP.GSYIH23.HY.CF","TP.GSYIH24.HY.CF","TP.GSYIH25.HY.CF","TP.GSYIH26.HY.CF"]          
    sütunad=["Tarih","Hanehalkı Tüketim","Kurum Tüketimi","Kamu Harcamaları",
             "Yatırım","Stok Değişimi","İhracat","İthalat (-)","GSYH"] 
    if frekans=="Çeyreklik":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
        veri.columns=sütunad
        sütunlar=veri.columns.tolist()
        sütunlar.insert(1,sütunlar.pop(sütunlar.index("GSYH")))
        veri=veri[sütunlar]
        return veri
    elif frekans=="Yıllık":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end,frequency=8)
        veri.columns=sütunad
        sütunlar=veri.columns.tolist()
        sütunlar.insert(1,sütunlar.pop(sütunlar.index("GSYH")))
        veri=veri[sütunlar]
        return veri

def gsyhgelir(frekans):
    start="01-01-1998"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.GSYIH14.GY.CF","TP.GSYIH15.GY.CF","TP.GSYIH17.GY.CF",
            "TP.GSYIH18.GY.CF","TP.GSYIH19.GY.CF","TP.GSYIH26.GY.CF"]          
    sütunad=["Tarih","Toplam İşgücü Ödemeleri","Üretim Net Vergi",
             "Sabit Sermaye Tüketimi","Net İşletme Artığı","Ürün Sübvansiyon","GSYH"] 
    if frekans=="Çeyreklik":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
        veri.columns=sütunad
        sütunlar=veri.columns.tolist()
        sütunlar.insert(1,sütunlar.pop(sütunlar.index("GSYH")))
        veri=veri[sütunlar]
        return veri
    elif frekans=="Yıllık":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end,frequency=8)
        veri.columns=sütunad
        sütunlar=veri.columns.tolist()
        sütunlar.insert(1,sütunlar.pop(sütunlar.index("GSYH")))
        veri=veri[sütunlar]
        return veri

def gsyhuretim(frekans):
    start="01-01-1998"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.GSYIH01.IFK.CF","TP.GSYIH02.IFK.CF","TP.GSYIH04.IFK.CF",
            "TP.GSYIH05.IFK.CF","TP.GSYIH06.IFK.CF","TP.GSYIH07.IFK.CF",
            "TP.GSYIH08.IFK.CF","TP.GSYIH09.IFK.CF","TP.GSYIH10.IFK.CF",
            "TP.GSYIH11.IFK.CF","TP.GSYIH12.IFK.CF","TP.GSYIH13.IFK.CF",
            "TP.GSYIH26.IFK.CF"]        
    sütunad=["Tarih","Tarım-Ormancılık-Balıkçılık","Sanayi","İnşaat","Hizmetler",
             "Bilgi ve İletişim","Finans ve Sigorta","Gayrimenkul","Mesleki Hizmet",
             "Kamu Yönetimi-Sağlık-Sosyal Hiz","Diğer Hizmetler","Toplam Sektörler",
             "Vergi-Sübvansiyon","GSYH"] 
    if frekans=="Çeyreklik":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
        veri.columns=sütunad
        sütunlar=veri.columns.tolist()
        sütunlar.insert(1,sütunlar.pop(sütunlar.index("GSYH")))
        veri=veri[sütunlar]
        return veri
    elif frekans=="Yıllık":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end,frequency=8)
        veri.columns=sütunad
        sütunlar=veri.columns.tolist()
        sütunlar.insert(1,sütunlar.pop(sütunlar.index("GSYH")))
        veri=veri[sütunlar]
        return veri


tur=st.selectbox("GSYH Hesaplama Türü:",options=["Gelir Yöntemi","Harcama Yöntemi","Üretim Yöntemi"])

if tur=="Gelir Yöntemi":
    secenek=["Çeyreklik","Yıllık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>', unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)

    veri=gsyhgelir(secim)
    oran=veri.copy()

    for sütun in veri.columns[1:]:
        oran[sütun]=(veri[sütun]/veri["GSYH"]).apply(lambda x: f"{x*100 :.2f}%")

    st.subheader("GSYH Tutar")
    st.dataframe(veri,hide_index=True,use_container_width=True)
    st.subheader("GSYH Katkı Oranları")
    st.dataframe(oran,hide_index=True, use_container_width=True)

elif tur=="Harcama Yöntemi":
    secenek=["Çeyreklik","Yıllık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>', unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)

    veri=gsyhharcama(secim)
    oran=veri.copy()

    for sütun in veri.columns[1:]:
        oran[sütun]=(veri[sütun]/veri["GSYH"]).apply(lambda x: f"{x*100 :.2f}%")

    st.subheader("GSYH Tutar")
    st.dataframe(veri,hide_index=True,use_container_width=True)
    st.subheader("GSYH Katkı Oranları")
    st.dataframe(oran,hide_index=True, use_container_width=True)

elif tur=="Üretim Yöntemi":
    secenek=["Çeyreklik","Yıllık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>', unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)

    veri=gsyhuretim(secim)
    oran=veri.copy()

    for sütun in veri.columns[1:]:
        oran[sütun]=(veri[sütun]/veri["GSYH"]).apply(lambda x: f"{x*100 :.2f}%")

    st.subheader("GSYH Tutar")
    st.dataframe(veri,hide_index=True,use_container_width=True)
    st.subheader("GSYH Katkı Oranları")
    st.dataframe(oran,hide_index=True, use_container_width=True)
