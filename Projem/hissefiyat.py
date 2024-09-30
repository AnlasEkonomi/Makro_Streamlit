import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import plotly.graph_objects as go

def hissead():
    hisseler=[]
    url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=ACSEL"
    r=requests.get(url)
    s=BeautifulSoup(r.text,"html.parser")
    hisseler=[a.string for a in s.find("select",id="ddlAddCompare").find("optgroup").find_all("option")]
    return hisseler

def hissefiyat(hisse,ilk,son):
    try:
        url=f'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse={hisse}&startdate={ilk}&enddate={son}'
        json_data=requests.get(url).json()
        veri=pd.DataFrame(json_data)["value"]
        veri=pd.json_normalize(veri)
        sütunad=["Tarih","Kapanış","AOF","Min","Max","Hacim","DolarTL","Dolar Bazlı Fiyat",
                "Sermaye","PD","PD Dolar","Dolar Bazlı Min","Dolar Bazlı Max","Dolar Bazlı AOF"]
        veri.drop(columns=["HGDG_HS_KODU","END_ENDEKS_KODU","END_TARIH","END_SEANS",
                    "END_DEGER","DD_DOVIZ_KODU","DD_DT_KODU","DD_TARIH","ENDEKS_BAZLI_FIYAT",
                    "DOLAR_HACIM","HG_KAPANIS","HG_AOF","HG_MIN","HG_MAX",
                    "HAO_PD","HAO_PD_USD","HG_HACIM"],inplace=True)
        veri.columns=sütunad       
        return veri
    except (KeyError,ValueError,UnboundLocalError) as e:
        veri2=pd.DataFrame(columns=sütunad)
        return veri2

st.markdown("<h4><strong>Lütfen Tarih Aralığı Seçiniz...</strong></h4>",unsafe_allow_html=True)
tarih1=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date()-timedelta(days=365),max_value=datetime.today().date(),key="Giriş")
tarih2=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date(),max_value=datetime.today().date(),min_value=tarih1,key="Çıkış")
    
st.session_state["ilk_tarih"]=tarih1.strftime("%d-%m-%Y")
st.session_state["son_tarih"]=tarih2.strftime("%d-%m-%Y")

seçenekler=hissead()
st.markdown("**Hisse Senedi Seçin:**")
seçim=st.selectbox('', seçenekler)
st.session_state["seçilen_hisse"]=seçim

if "seçilen_hisse" in st.session_state:
    veri=hissefiyat(seçim,st.session_state["ilk_tarih"],st.session_state["son_tarih"])
    st.dataframe(veri,hide_index=True,use_container_width=True)

    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),y=veri["Kapanış"],
        mode="lines",
        name="Fiyat",
        line=dict(color="Red")))

    fig.update_layout(title={"text":"Hisse Kapanış Fiyatı","x":0.5,"xanchor":"center"},
                        xaxis_title="Tarih",yaxis_title="Fiyat",
                        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1",
                                   rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
    
    fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig)