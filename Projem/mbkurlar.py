import streamlit as st
from datetime import datetime
from urllib.error import HTTPError
import pandas as pd

st.markdown("<h4><strong>Lütfen Tarih Seçiniz...</strong></h4>",unsafe_allow_html=True)
tarih=st.date_input("",format="DD/MM/YYYY",value=datetime.today().date(),max_value=datetime.today().date())
url=f'https://www.tcmb.gov.tr/kurlar/{tarih.year:02d}{tarih.month:02d}/{tarih.day:02d}{tarih.month:02d}{tarih.year}.xml?_=1726480314217'

try:
    veri=pd.read_xml(url).drop(columns=["CrossOrder","Kod","CurrencyName","CrossRateUSD","CrossRateOther"])
    veri.columns=["Döviz Kodu","Birim","İsim","Döviz Alış","Döviz Satış","Efektif Alış","Efektif Satış"]
    veri["Döviz Kodu"]=veri["Döviz Kodu"].apply(lambda x: f"{x}/TRY")
    veri.drop(veri.index[-1],inplace=True)
    veri=veri.fillna("-")
    st.dataframe(veri,hide_index=True,width=1000)
except HTTPError as e:
    st.markdown("<p style='color:red; font-weight:bold;'>Girdiğiniz tarihte kur bilgisi yoktur. Lütfen tarihleri kontrol ediniz...</p>", unsafe_allow_html=True)