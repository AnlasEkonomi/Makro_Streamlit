import streamlit as st
import evds as ev
import pandas as pd
from datetime import datetime,timedelta
import plotly.graph_objects as go
from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup
import plotly.express as px
from io import StringIO
from yahooquery import Ticker
from lxml import etree
import cloudscraper


evdsapi=ev.evdsAPI("Your Api Key")

def mbapi():
    kodlar=["TP.APIFON1.IHA","TP.APIFON1.KOT.A","TP.APIFON1.KOT.B","TP.APIFON1.KOT.C",
        "TP.APIFON1.KOT.T","TP.APIFON1.TOP","TP.APIFON2.IHA","TP.APIFON2.KOT",
        "TP.APIFON2.TOP","TP.APIFON3","TP.APIFON4"]
    
    start="02-01-2019"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
    veri.dropna(axis=0,inplace=True)
    veri.columns=["Tarih","İhale Yoluyla Fonlama","Bist O/N","Depo","GLP","Toplam Kotasyon",
                  "Toplam Fonlama","İhale Yoluyla Sterilizasyon","Kotasyon Yoluyla Sterilizasyon",
                  "Toplam Sterilizasyon","Net Fonlama","AOFM"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y")
    veri["Tarih"]=veri["Tarih"].dt.strftime("%d-%m-%Y")             
    return veri

def on():
    url="https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb+tr/main+menu/temel+faaliyetler/para+politikasi/merkez+bankasi+faiz+oranlari/faiz-oranlari"
    tablo=pd.read_html(url)
    veri=tablo[0]
    veri.drop(veri.index[0],inplace=True)
    veri.columns=["Tarih","Borç Alma","Borç Verme"]
    veri["Tarih"]=veri["Tarih"].apply(lambda x: datetime.strptime(x,"%d.%m.%y"))
    veri2=pd.DataFrame(columns=veri.columns)
    veri2["Tarih"]=pd.date_range(veri["Tarih"].iloc[0],datetime.today()+pd.DateOffset(months=1),freq="ME")

    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri2["Tarih"]=veri2["Tarih"].dt.to_period("M")

    veri2=veri2.merge(veri,on='Tarih',how='left')
    veri2.drop(columns=["Borç Alma_x","Borç Verme_x"],inplace=True)
    veri2=veri2.ffill()
    veri2.columns=veri.columns
    veri2["Tarih"]=veri2["Tarih"].dt.strftime("%d-%m-%Y") 
    return veri2

def glp():
    url="https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/Gec+Likidite+Penceresi+%28LON%29"
    tablo=pd.read_html(url)
    veri=tablo[0]
    veri.drop(veri.index[0],inplace=True)
    veri.columns=["Tarih","Borç Alma","Borç Verme"]
    veri["Tarih"]=veri["Tarih"].apply(lambda x: datetime.strptime(x,"%d.%m.%y"))
    veri2=pd.DataFrame(columns=veri.columns)
    veri2["Tarih"]=pd.date_range(veri["Tarih"].iloc[0],datetime.today()+pd.DateOffset(months=1),freq="ME")

    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri2["Tarih"]=veri2["Tarih"].dt.to_period("M")

    veri2=veri2.merge(veri,on='Tarih',how='left')
    veri2.drop(columns=["Borç Alma_x","Borç Verme_x"],inplace=True)
    veri2=veri2.ffill()
    veri2.columns=veri.columns
    veri2["Tarih"]=veri2["Tarih"].dt.strftime("%d-%m-%Y") 
    return veri2

def repo():
    url="https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/1+Hafta+Repo"
    tablo=pd.read_html(url)
    veri=tablo[0]
    veri.drop(veri.index[0],inplace=True)
    veri.columns=["Tarih","Borç Alma","Borç Verme"]
    veri["Tarih"]=veri["Tarih"].apply(lambda x: datetime.strptime(x,"%d.%m.%Y"))
    veri2=pd.DataFrame(columns=veri.columns)
    veri2["Tarih"]=pd.date_range(veri["Tarih"].iloc[0],datetime.today()+pd.DateOffset(months=1),freq="ME")

    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri2["Tarih"]=veri2["Tarih"].dt.to_period("M")

    veri2=veri2.merge(veri,on="Tarih",how="left")
    veri2.drop(columns=["Borç Alma_x","Borç Verme_x"],inplace=True)
    veri2=veri2.ffill()
    veri2.columns=veri.columns
    veri2["Tarih"]=veri2["Tarih"].dt.strftime("%d-%m-%Y") 
    return veri2

def tlref():
    start="28-12-2018"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.BISTTLREF.ORAN"],startdate=start,enddate=end)
    veri.dropna(axis=0,inplace=True)
    veri.columns=["Tarih","TLREF"]
    return veri

def mevfaiz():
    start="04-01-2002"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.TRY.MT01","TP.TRY.MT02","TP.TRY.MT03",
                           "TP.TRY.MT04","TP.TRY.MT05"],startdate=start,enddate=end)
    veri.drop(columns=["YEARWEEK"],inplace=True)
    veri.columns=["Tarih","1 Aya Kadar","3 Aya Kadar","6 Aya Kadar","1 Yıla Kadar","1 Yıl ve Üzeri"]
    return veri

def kredifaiz():
    start="04-01-2002"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.KTF10","TP.KTF11","TP.KTF12","TP.KTF17",
                           "TP.KTFTUK"],startdate=start,enddate=end)
    veri.drop(columns=["YEARWEEK"],inplace=True)
    veri.columns=["Tarih","İhtiyaç","Taşıt","Konut","Ticari","Tüketici (İhtiyaç+Taşıt+Konut)"]
    return veri


def hissead():
    hisseler=[]
    url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=ACSEL"
    r=requests.get(url)
    s=BeautifulSoup(r.text,"html.parser")
    s1=s.find("select",id="ddlAddCompare")
    c1=s1.findChild("optgroup").findAll("option")

    for a in c1:
        hisseler.append(a.string)
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

    for _ in range(7):
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

def hissefiyat(hisse,ilk,son):
    try:
        url=f'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse={hisse}&startdate={ilk}&enddate={son}'
        response=requests.get(url)
        json_data=response.json()
        veri=pd.DataFrame(json_data)["value"]
        veri=pd.json_normalize(veri)
        veri.drop(columns=["HGDG_HS_KODU","END_ENDEKS_KODU","END_TARIH","END_SEANS",
                    "END_DEGER","DD_DOVIZ_KODU","DD_DT_KODU","DD_TARIH","ENDEKS_BAZLI_FIYAT",
                    "DOLAR_HACIM","HG_KAPANIS","HG_AOF","HG_MIN","HG_MAX",
                    "HAO_PD","HAO_PD_USD","HG_HACIM"],inplace=True)
        veri.columns=["Tarih","Kapanış","AOF","Min","Max","Hacim","DolarTL","Dolar Bazlı Fiyat",
                "Sermaye","PD","PD Dolar","Dolar Bazlı Min","Dolar Bazlı Max","Dolar Bazlı AOF"]
        
        return veri
    except KeyError as e:
        veri2=pd.DataFrame(columns=veri.columns)
        return veri2

def bisttreemap():
    url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx#page-1"
    r=requests.get(url).text
    tablo=pd.read_html(StringIO(r))[2]
    sektor=pd.DataFrame({"Hisse": tablo["Kod"], "Sektör": tablo["Sektör"], "Piyasa Değeri (mn $)": tablo["Piyasa Değeri (mn $)"]})
    tablo2=pd.read_html(StringIO(r))[7]
    getiri=pd.DataFrame({"Hisse": tablo2["Kod"], "Getiri (%)": tablo2["Günlük Getiri (%)"]/100})

    df=pd.merge(sektor,getiri,on="Hisse")
    df["Piyasa Değeri (mn $)"]=df["Piyasa Değeri (mn $)"].str.replace('.', '').str.replace(',', '.').astype("float64")

    renk_aralik=[-10,-5,-0.01,0,0.01,5,10]
    df["Renk"]=pd.cut(df["Getiri (%)"],bins=renk_aralik,labels=["red","indianred","lightpink","lightgreen","lime","green"])

    fig=px.treemap(df,path=[px.Constant("Borsa İstanbul"),"Sektör","Hisse"],values="Piyasa Değeri (mn $)",
                    color="Renk",custom_data=["Getiri (%)","Sektör"],
                    color_discrete_map={"(?)":"#262931","red":"red","indianred":"indianred", 
                                        "lightpink":"lightpink","lightgreen":"lightgreen","lime":"lime","green":"green"})
    fig.update_layout(width=2000,height=1600)
    fig.update_traces(
        hovertemplate="<br>".join([
            "Hisse: %{label}",
            "Piyasa Değeri (mn $): %{value}",
            "Getiri: %{customdata[0]}",
            "Sektör: %{customdata[1]}"]))
    fig.data[0].texttemplate="<b>%{label}</b><br>%{customdata[0]} %"
    st.plotly_chart(fig)

def hedef_fiyat_yahoo():
    def hisseler():
        url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?endeks=01#page-1"
        html_text=requests.get(url).text
        html_io=StringIO(html_text)
        tablo=pd.read_html(html_io)[2]["Kod"]
        for i in range(len(tablo)):
            tablo[i] += ".IS"
        hissekod=tablo.to_list()
        return hissekod
    hisse=Ticker(hisseler())
    hisse_dict=hisse.financial_data
    veri=pd.DataFrame.from_dict(hisse_dict,orient="index").iloc[:,1:6].reset_index()
    veri.columns=["Hisse Adı","Güncel Fiyat","En Yüksek Tahmin","En Düşük Tahmin",
            "Ortalama Tahmin","Medyan Tahmin"]
    veri["Hisse Adı"]=veri["Hisse Adı"].str.replace(".IS","",regex=False)
    veri.dropna(axis=0,inplace=True)
    veri.reset_index(drop=True,inplace=True)
    return veri

def cnbcpro():
    url=st.text_input("**Lütfen URL Giriniz:**") 
    if url:
        try:
            res=requests.get(url)
            soup=BeautifulSoup(res.text,"html.parser")
            doc=etree.HTML(str(soup))
            doc2=doc.xpath("//*[@id='RegularArticle-ArticleBody-5']/span[1]/span/span")

            st.write(doc2[0].text)
        except Exception as e:
             st.error("**Hatalı URL. Lütfen tekrar giriniz...**")

def cds():
    scraper=cloudscraper.CloudScraper()
    url="https://en.macromicro.me/charts/data/68256"

    headers={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Authorization": "Bearer 8096cd3a67d6b9d10e0785239a58390a",
        "Cookie": "PHPSESSID=r2f4losopnom9dt5kjq486boss; _gid=GA1.2.1302961084.1726567296; _fbp=fb.1.1726567296378.35347350480971742; aiExplainOn=off; _hjSession_1543609=eyJpZCI6ImMzYzk3NDRmLTJiOGYtNGQ5NC04ODFlLTIzNDU2MDUwYTM0ZSIsImMiOjE3MjY1NjcyOTcwOTEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=; __lt__cid=147f0834-02cb-4b05-bd97-a9c12ba4c803; __lt__sid=d30c02d1-c4f0aeef; reminder=1726567309; _hjSessionUser_1543609=eyJpZCI6IjE4NzgzZjIxLWE2ODItNTA3Yi04MjVjLWJiYzcxZjg2ZGJjOSIsImNyZWF0ZWQiOjE3MjY1NjcyOTcwOTAsImV4aXN0aW5nIjp0cnVlfQ==; prime7dfomc=1726567532; app_ui_support_btn=5; mm_sess_pages=5; _ga_4CS94JJY2M=GS1.1.1726567296.1.1.1726568202.0.0.0; cf_clearance=DKVck3.Q2OFHp1_Mh6juT.SKiYpRuJbbit9SR1xlWu0-1726568202-1.2.1.1-LL6qtwtUyCeqsVSsz8b6U4m9.n0nFLATCrrSA8Q.a8SRPYmpfx6asGt_ZbbvmSuzDehCJ0x3HdABmz3IAqa1xOKzIvA0Swmn1xF.fuTYHiCtwSx6Qr2.GrtD3mQrPQjnozc7_GlnpHdjl33huAOgVpAjo9z2_Vc3qKNsf4B5qWQB8n.Q2fxku6haJey0BsJMiauDYrPL_zwqa8ylFpWjvjkRwIiFLCKc7Ivb.oGrKJMqMl6e5KLqv89u7BtC3chKqVG_zrTfR7muhL.qBPp_WOTbN3FQ0tD_afaKFrY7GGQeKjyCMzc1aTEW5KGuWJ6iY7DAWfG9j1TM.cNUfKabKqzXn9qvg8CIOmYUtocfUIF3y5OpFsH2iHtadIn9btCG9vWm37Bah.4zd0e0P4oWjw; _ga=GA1.2.1196831987.1726567296; _gat_gtag_UA_66285376_3=1",
        "Referer": "https://en.macromicro.me/charts/68256/turkey-5year-cds",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}

    response=scraper.get(url,headers=headers)
    veri=response.json()["data"]["c:68256"]["series"]
    veri=pd.DataFrame(veri[0],columns=["Tarih","CDS"])
    veri["Tarih"]=pd.to_datetime(veri["Tarih"])
    veri["Tarih"]=veri["Tarih"].dt.strftime('%d-%m-%Y')
    return veri


##------------------------------------------------------------------------------------

st.markdown("""
    <style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }
    .title {
        color: red;
        border: 2px solid black;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Freestyle Script', cursive;
        font-size: 55px; 
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title">Via Anlaşılır Ekonomi</h1>',unsafe_allow_html=True)
st.sidebar.title("Göstergeler")

##-----------------------------------------------------------------------------

button1=st.sidebar.button("MB APİ Fonlama")
button2=st.sidebar.button("MB Faizler")
button3=st.sidebar.button("MB Kur Değerleri")
button4=st.sidebar.button("Bilançolar")
button5=st.sidebar.button("Geçmiş Fiyat")
button6=st.sidebar.button("Bist Tree Map")
button7=st.sidebar.button("Bist YF Hedef Fiyat")
button8=st.sidebar.button("CNBC Pro Makaleler")
button9=st.sidebar.button("CDS")

if button1:
    st.session_state["button1_clicked"]=True
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=False
    st.session_state["button4_clicked"]=False
    st.session_state["button5_clicked"]=False
    st.session_state["button6_clicked"]=False
    st.session_state["button7_clicked"]=False
    st.session_state["button8_clicked"]=False
    st.session_state["button9_clicked"]=False

if button2:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=True
    st.session_state["button3_clicked"]=False
    st.session_state["button4_clicked"]=False
    st.session_state["button5_clicked"]=False
    st.session_state["button6_clicked"]=False
    st.session_state["button7_clicked"]=False
    st.session_state["button8_clicked"]=False
    st.session_state["button9_clicked"]=False

if button3:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=True
    st.session_state["button4_clicked"]=False
    st.session_state["button5_clicked"]=False
    st.session_state["button6_clicked"]=False
    st.session_state["button7_clicked"]=False
    st.session_state["button8_clicked"]=False
    st.session_state["button9_clicked"]=False

if button4:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=False
    st.session_state["button4_clicked"]=True
    st.session_state["button5_clicked"]=False
    st.session_state["button6_clicked"]=False
    st.session_state["button7_clicked"]=False
    st.session_state["button8_clicked"]=False
    st.session_state["button9_clicked"]=False

if button5:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=False
    st.session_state["button4_clicked"]=False
    st.session_state["button5_clicked"]=True
    st.session_state["button6_clicked"]=False
    st.session_state["button7_clicked"]=False
    st.session_state["button8_clicked"]=False
    st.session_state["button9_clicked"]=False

if button6:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=False
    st.session_state["button4_clicked"]=False
    st.session_state["button5_clicked"]=False
    st.session_state["button6_clicked"]=True
    st.session_state["button7_clicked"]=False
    st.session_state["button8_clicked"]=False
    st.session_state["button9_clicked"]=False

if button7:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=False
    st.session_state["button4_clicked"]=False
    st.session_state["button5_clicked"]=False
    st.session_state["button6_clicked"]=False
    st.session_state["button7_clicked"]=True
    st.session_state["button8_clicked"]=False
    st.session_state["button9_clicked"]=False

if button8:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=False
    st.session_state["button4_clicked"]=False
    st.session_state["button5_clicked"]=False
    st.session_state["button6_clicked"]=False
    st.session_state["button7_clicked"]=False
    st.session_state["button8_clicked"]=True
    st.session_state["button9_clicked"]=False

if button9:
    st.session_state["button1_clicked"]=False
    st.session_state["button2_clicked"]=False
    st.session_state["button3_clicked"]=False
    st.session_state["button4_clicked"]=False
    st.session_state["button5_clicked"]=False
    st.session_state["button6_clicked"]=False
    st.session_state["button7_clicked"]=False
    st.session_state["button8_clicked"]=False
    st.session_state["button9_clicked"]=True

##-----------------------------------------------------------------------------

if st.session_state.get("button1_clicked",False):
    st.dataframe(mbapi(),hide_index=True,width=1000)

    fig=go.Figure()
    fig.add_trace(go.Scatter(
    x=pd.to_datetime(mbapi()["Tarih"],format="%d-%m-%Y"),
    y=mbapi()["Net Fonlama"],
    mode="lines",
    name="Net Fonlama"))

    fig.update_layout(title={
        "text":"APİ Net Fonlama","x":0.5,"xanchor":"center"},
    xaxis_title="Tarih",
    yaxis_title="Net Fonlama",
    xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1"))
    fig.update_xaxes(tickangle=-45)

    fig2=go.Figure()
    fig2.add_trace(go.Scatter(
    x=pd.to_datetime(mbapi()["Tarih"], format="%d-%m-%Y"),
    y=mbapi()["AOFM"],
    mode="lines",
    line=dict(color="red"),
    name="AOFM"))

    fig2.update_layout(title={
        "text":"AOFM (%)","x": 0.5,"xanchor": "center"},
    xaxis_title="Tarih",
    yaxis_title="AOFM",
    xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1"))
    fig2.update_xaxes(tickangle=-45)
    
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

##--------------------------------------------------------------------------

if st.session_state.get("button2_clicked",False):
    secenek=["O/N","GLP","1 Haftalık Repo","TLREF","Mevduat Faizleri (TL)","Kredi Faizleri (TL)"]
    st.markdown('<p style="font-weight:bold; color:black;">Faiz Türünü Seçin:</p>',unsafe_allow_html=True)
    faiz_secim=st.radio("",secenek,index=None,horizontal=True)
    
    if faiz_secim=="O/N":
        st.markdown('<p style="font-weight:bold; color:black;">O/N (%)</p>',unsafe_allow_html=True)
        st.dataframe(on(),hide_index=True,width=1000)

        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(on()["Tarih"],format="%d-%m-%Y"),
        y=on()["Borç Alma"],
        mode="lines",
        name="Borç Alma",
        line=dict(color="red")))

        fig.add_trace(go.Scatter(
        x=pd.to_datetime(on()["Tarih"], format="%d-%m-%Y"),
        y=on()["Borç Verme"],
        mode="lines",
        name="Borç Verme",
        line=dict(color="Blue")))

        fig.update_layout(title={
            "text":"O/N (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Faiz",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M3"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)

    elif faiz_secim=="GLP":
        st.markdown('<p style="font-weight:bold; color:black;">GLP (%)</p>',unsafe_allow_html=True)
        st.dataframe(glp(),hide_index=True,width=1000)

        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(glp()["Tarih"],format="%d-%m-%Y"),
        y=glp()["Borç Alma"],
        mode="lines",
        name="Borç Alma",
        line=dict(color="red")))

        fig.add_trace(go.Scatter(
        x=pd.to_datetime(glp()["Tarih"], format="%d-%m-%Y"),
        y=glp()["Borç Verme"],
        mode="lines",
        name="Borç Verme",
        line=dict(color="Blue")))

        fig.update_layout(title={
            "text":"GLP (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Faiz",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M3"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)

    elif faiz_secim=="1 Haftalık Repo":
        st.markdown('<p style="font-weight:bold; color:black;">1 Haftalık Repo (%)</p>',unsafe_allow_html=True)
        st.dataframe(repo(),hide_index=True,width=1000)

        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(repo()["Tarih"], format="%d-%m-%Y"),
        y=repo()["Borç Verme"],
        mode="lines",
        name="Borç Verme",
        line=dict(color="Red")))

        fig.update_layout(title={
            "text":"1 Haftalık Repo (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Faiz",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M3"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)
    
    elif faiz_secim=="TLREF":
        st.markdown('<p style="font-weight:bold; color:black;">TLREF (%)</p>',unsafe_allow_html=True)
        st.dataframe(tlref(),hide_index=True,width=1000)

        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(tlref()["Tarih"], format="%d-%m-%Y"),
        y=tlref()["TLREF"],
        mode="lines",
        name="TLREF",
        line=dict(color="Red")))

        fig.update_layout(title={
            "text":"TLREF (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Faiz",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)
    
    elif faiz_secim=="Mevduat Faizleri (TL)":
        st.markdown('<p style="font-weight:bold; color:black;">Mevduat Faizleri (%)</p>',unsafe_allow_html=True)
        st.dataframe(mevfaiz(),hide_index=True,width=1000)

        fig=go.Figure()
        columns=["1 Aya Kadar","3 Aya Kadar","6 Aya Kadar","1 Yıla Kadar","1 Yıl ve Üzeri"]
        renkler=["Red","Blue","Green","Orange","Purple"]

        for col,color in zip(columns,renkler):
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(mevfaiz()["Tarih"],format="%d-%m-%Y"),
                y=mevfaiz()[col],
                mode="lines",
                name=col,
                line=dict(color=color)))

        fig.update_layout(
            title={"text": "Mevduat Faizleri (%)", "x": 0.5, "xanchor": "center"},
            xaxis_title="Tarih",
            yaxis_title="Faiz",
            xaxis=dict(tickformat="%d-%m-%Y", tickmode="linear", dtick="M3"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)
    
    elif faiz_secim=="Kredi Faizleri (TL)":
        st.markdown('<p style="font-weight:bold; color:black;">Kredi Faizleri (%)</p>',unsafe_allow_html=True)
        st.dataframe(kredifaiz(),hide_index=True,width=1000)

        fig=go.Figure()
        columns=["İhtiyaç","Taşıt","Konut","Ticari",
                  "Tüketici (İhtiyaç+Taşıt+Konut)"]
        renkler=["Red","Blue","Green","Orange","Purple","Black"]

        for col,color in zip(columns,renkler):
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(kredifaiz()["Tarih"],format="%d-%m-%Y"),
                y=kredifaiz()[col],
                mode="lines",
                name=col,
                line=dict(color=color)))

        fig.update_layout(
            title={"text": "Kredi Faizleri (%)", "x": 0.5, "xanchor": "center"},
            xaxis_title="Tarih",
            yaxis_title="Faiz",
            xaxis=dict(tickformat="%d-%m-%Y", tickmode="linear", dtick="M3"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)

##---------------------------------------------------------------------------------

if st.session_state.get("button3_clicked",False):
    st.markdown("<h4><strong>Lütfen Tarih Seçiniz...</strong></h4>",unsafe_allow_html=True)
    tarih=st.date_input("",format="DD/MM/YYYY",value=datetime.today().date(),max_value=datetime.today().date())
    gun=str(tarih.day).zfill(2)
    ay=str(tarih.month).zfill(2)
    yıl=str(tarih.year).zfill(2)

    url=f'https://www.tcmb.gov.tr/kurlar/{yıl+ay}/{gun+ay+yıl}.xml?_=1726480314217'

    try:
        veri=pd.read_xml(url)
        veri.drop(columns=["CrossOrder","Kod","CurrencyName","CrossRateUSD","CrossRateOther"],inplace=True)
        veri.columns=["Döviz Kodu","Birim","İsim","Döviz Alış","Döviz Satış","Efektif Alış","Efektif Satış"]
        veri["Döviz Kodu"]=veri["Döviz Kodu"].apply(lambda x: f"{x}/TRY")
        veri.drop(veri.index[-1],inplace=True)
        veri=veri.fillna("-")
        st.dataframe(veri,hide_index=True,width=1000)
    except HTTPError as e:
        st.markdown("<p style='color:red; font-weight:bold;'>Girdiğiniz tarihte kur bilgisi yoktur. Lütfen tarihleri kontrol ediniz...</p>", unsafe_allow_html=True)

##---------------------------------------------------------------------------------- 

if st.session_state.get("button4_clicked",False):
    seçenekler=hissead()
    st.markdown("**Hisse Senedi Seçin:**")
    seçim = st.selectbox('', seçenekler)
    st.session_state["seçilen_hisse"]=seçim

    st.markdown("**Para birimini seçin:**") 
    para_birimi = st.radio("", ("TRY", "USD"))
    st.session_state["seçilen_para_birimi"]=para_birimi

    if "seçilen_hisse" in st.session_state and "seçilen_para_birimi" in st.session_state:
        veri=bilanco(st.session_state["seçilen_hisse"],st.session_state["seçilen_para_birimi"])
        st.dataframe(veri,hide_index=True,use_container_width=True)

##--------------------------------------------------------------------------------

if st.session_state.get("button5_clicked",False):
    st.markdown("<h4><strong>Lütfen Tarih Aralığı Seçiniz...</strong></h4>",unsafe_allow_html=True)
    tarih1=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date()-timedelta(days=365),max_value=datetime.today().date(),key="Giriş")
    tarih2=st.date_input("",format="DD-MM-YYYY",value=datetime.today().date(),max_value=datetime.today().date(),key="Çıkış")
    
    gun1=str(tarih1.day).zfill(2)
    ay1=str(tarih1.month).zfill(2)
    yıl1=str(tarih1.year).zfill(2)
    son1=gun1+"-"+ay1+"-"+yıl1
    st.session_state["ilk_tarih"]=son1

    gun2=str(tarih2.day).zfill(2)
    ay2=str(tarih2.month).zfill(2)
    yıl2=str(tarih2.year).zfill(2)
    son2=gun2+"-"+ay2+"-"+yıl2
    st.session_state["son_tarih"]=son2

    seçenekler=hissead()
    st.markdown("**Hisse Senedi Seçin:**")
    seçim=st.selectbox('',seçenekler)
    st.session_state["seçilen_hisse"]=seçim

    if "seçilen_hisse" in st.session_state:
        veri=hissefiyat(st.session_state["seçilen_hisse"],st.session_state["ilk_tarih"],
                        st.session_state["son_tarih"])
        st.dataframe(veri,hide_index=True,use_container_width=True)

    fig=go.Figure()
    fig.add_trace(go.Scatter(
    x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),
    y=veri["Kapanış"],
    mode="lines",
    name="Fiyat",
    line=dict(color="Red")))

    fig.update_layout(title={
        "text":"Hisse Kapanış Fiyatı","x":0.5,"xanchor":"center"},
    xaxis_title="Tarih",
    yaxis_title="Fiyat",
    xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1"))
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig)

##--------------------------------------------------------------------------------------

if st.session_state.get("button6_clicked",False):
    bisttreemap()

##---------------------------------------------------------------------------------------

if st.session_state.get("button7_clicked",False):
   veri=hedef_fiyat_yahoo()
   st.dataframe(veri,hide_index=True,use_container_width=True,width=1200,height=600)

##--------------------------------------------------------------------------------------

if st.session_state.get("button8_clicked",False):
    st.error("Burası planda yoktu ama süpriz yapayım dedim :)))")
    cnbcpro()

##-----------------------------------------------------------------------------------------

if st.session_state.get("button9_clicked",False):
    veri=cds()
    st.dataframe(veri,hide_index=True,use_container_width=True)

    fig=go.Figure()
    fig.add_trace(go.Scatter(
    x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),
    y=veri["CDS"],
    mode="lines",
    name="CDS",
    line=dict(color="Red")))

    fig.update_layout(title={
        "text":"Türkiye CDS 5 Yıl","x":0.5,"xanchor":"center"},
    xaxis_title="Tarih",
    yaxis_title="CDS",
    xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M2"))
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig)

##----------------------------------------------------------------------------------