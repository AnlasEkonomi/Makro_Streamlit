import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def hissead():
    hisseler=[]
    url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=ACSEL"
    r=requests.get(url)
    s=BeautifulSoup(r.text,"html.parser")
    hisseler=[a.string for a in s.find("select",id="ddlAddCompare").find("optgroup").find_all("option")]
    return hisseler


def bilanco(hisse,para_birim):
    tarihler=[]
    yıllar=[]
    donemler=[]
    grup=[]

    url1="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=" + hisse
    r1=requests.get(url1)
    soup=BeautifulSoup(r1.text,"html.parser")
    secim=soup.find("select",id="ddlMaliTabloFirst")
    secim2=soup.find("select",id="ddlMaliTabloGroup")

    try:
        cocuklar=secim.findChildren("option")
        grup=secim2.find("option")["value"]

        for i in cocuklar:
            tarihler.append(i.string.rsplit("/"))
        for j in tarihler:
            yıllar.append(j[0])
            donemler.append(j[1])

        if len(tarihler) >= 4:
            parametreler = (
                ("companyCode",hisse),
                ("exchange",para_birim),
                ("financialGroup",grup),
                ("year1",yıllar[0]),
                ("period1",donemler[0]),
                ("year2",yıllar[1]),
                ("period2",donemler[1]),
                ("year3",yıllar[2]),
                ("period3",donemler[2]),
                ("year4",yıllar[3]),
                ("period4",donemler[3])
            )
            url2="https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
            r2=requests.get(url2,params=parametreler).json()["value"]
            veri=pd.DataFrame.from_dict(r2)
            veri.drop(columns=["itemCode","itemDescEng"], inplace=True)
        else:
            return pd.DataFrame()

    except AttributeError:
        return pd.DataFrame() 

    del tarihler[0:4]
    tumveri=[veri]

    for _ in range(12):
        if len(tarihler)==len(yıllar):
            del tarihler[0:4]
        else:
            yıllar=[]
            donemler=[]
            for j in tarihler:
                yıllar.append(j[0])
                donemler.append(j[1])

            if len(tarihler) >= 4:
                parametreler2 = (
                    ("companyCode",hisse),
                    ("exchange",para_birim),
                    ("financialGroup",grup),
                    ("year1",yıllar[0]),
                    ("period1",donemler[0]),
                    ("year2",yıllar[1]),
                    ("period2",donemler[1]),
                    ("year3",yıllar[2]),
                    ("period3",donemler[2]),
                    ("year4",yıllar[3]),
                    ("period4",donemler[3])
                )
                r3=requests.get(url2,params=parametreler2).json()["value"]
                veri2=pd.DataFrame.from_dict(r3)
                try:
                    veri2.drop(columns=["itemCode","itemDescTr","itemDescEng"],inplace=True)
                    tumveri.append(veri2)
                except KeyError:
                    continue

    veri3=pd.concat(tumveri, axis=1)
    başlık=["Bilanço"]
    for i in cocuklar:
        başlık.append(i.string)

    başlıkfark=len(başlık)-len(veri3.columns)

    if başlıkfark !=0:
        del başlık[-başlıkfark:]

    veri3=veri3.set_axis(başlık, axis=1)
    veri3[başlık[1:]] = veri3[başlık[1:]].astype(float)
    veri3=veri3.fillna(0)
    return veri3


st.markdown("**Hisse Senedi Seçin:**")
st.session_state["seçilen_hisse"]=seçim=st.selectbox('', hissead())

st.markdown("**Para birimini seçin:**") 
st.session_state["seçilen_para_birimi"]=para_birimi=st.radio("", ("TRY", "USD"))

if all(key in st.session_state for key in ["seçilen_hisse","seçilen_para_birimi"]):
    st.dataframe(bilanco(seçim,para_birimi),hide_index=True,use_container_width=True)
