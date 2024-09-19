import streamlit as st
import evds as ev
import pandas as pd
from datetime import datetime,timedelta
import plotly.graph_objects as go
from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup
import plotly.express as px
from plotly.subplots import make_subplots
from io import StringIO
from yahooquery import Ticker
from lxml import etree
import cloudscraper
import yfinance as yf 


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
    except (KeyError,ValueError,UnboundLocalError) as e:
        veri2=pd.DataFrame(columns=["Tarih","Kapanış","AOF","Min","Max","Hacim","DolarTL","Dolar Bazlı Fiyat",
                "Sermaye","PD","PD Dolar","Dolar Bazlı Min","Dolar Bazlı Max","Dolar Bazlı AOF"])
        return veri2

def bisttreemap():
    url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx#page-1"
    r=requests.get(url).text
    tablo=pd.read_html(StringIO(r))[2]
    sektor=pd.DataFrame({"Hisse": tablo["Kod"], "Sektör": tablo["Sektör"], "Piyasa Değeri (mn $)": tablo["Piyasa Değeri (mn $)"]})
    tablo2=pd.read_html(StringIO(r))[7]
    ##tablo2["Günlük Getiri (%)"]=pd.to_numeric(tablo2["Günlük Getiri (%)"].str.replace('%', '').str.replace(',', '.'),errors='coerce')
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
            metin=doc2[0].text 
            st.markdown(f"""
<style>
     .arial {{
        font-family: Arial, sans-serif;;
    }}
</style>
<div class="arial">
    {metin}
</div>
""", unsafe_allow_html=True)
        except Exception as e:
             st.error("**Hatalı URL. Lütfen tekrar giriniz...**")

def cds():
    bugün=datetime.today()
    gün=str(bugün.strftime("%d"))
    ay=str(bugün.strftime("%m"))
    yıl=str(bugün.year)

    scraper=cloudscraper.CloudScraper()
    url=f'https://api.investing.com/api/financialdata/historical/1096486?start-date=2008-02-01&end-date={yıl+"-"+ay+"-"+gün}&time-frame=Daily&add-missing-rows=false'

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://tr.investing.com",
        "Referer": "https://tr.investing.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Domain-ID": "tr"}

    response=scraper.get(url,headers=headers)
    veri=response.json()["data"]
    veri=[{"rowDate": item["rowDate"],"last_close": item["last_close"]} for item in veri]
    veri=pd.DataFrame(veri)
    veri.columns=["Tarih","CDS"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"],format='%d.%m.%Y')
    veri.sort_values(by="Tarih",ascending=True,inplace=True)
    veri["Tarih"]=veri["Tarih"].dt.strftime('%d-%m-%Y')
    veri["CDS"]=veri["CDS"].str.replace(',', '.').astype(float)
    veri["CDS Oynaklık"]=veri["CDS"].pct_change()
    return veri

def ekonomiktakvim():
    bugün=datetime.today()
    haftanınilkgünü=bugün-timedelta(days=bugün.weekday())
    haftanınsongünü=haftanınilkgünü+timedelta(days=6)
    gün1=str(haftanınilkgünü.strftime("%d"))
    ay1=str(haftanınilkgünü.strftime("%m"))
    yıl1=str(haftanınilkgünü.year)
    gün2=str(haftanınsongünü.strftime("%d"))
    ay2=str(haftanınsongünü.strftime("%m"))
    yıl2=str(haftanınsongünü.year)

    url=f'https://yatirim.akbank.com/_vti_bin/AkbankYatirimciPortali/Hisse/Service.svc/EkonomikTakvimForList/{yıl1+ay1+gün1+"000000"}/{yıl2+ay2+gün2+"235900"}'
    res=requests.get(url)
    data=res.json()

    deger=[]
    for i in data["Data"]:
        key = i["Key"]
        for value in i["Value"]:
            value["Key"]=key
            deger.append(value)

    df=pd.DataFrame(deger)
    veri=df[["Key","Tsi","Country","Event","Actual","Forecast","Previous"]]
    veri.columns=["Tarih","Saat (TSİ)","Ülke","Olay","Açıklanan","Tahmin","Önceki"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d/%m/%Y")
    bugün=datetime.today().date()
    veri=veri[veri['Tarih'].dt.date >= bugün]
    veri["Tarih"]=veri["Tarih"].dt.strftime("%d-%m-%Y")
    veri["Saat (TSİ)"]=pd.to_datetime(veri["Saat (TSİ)"],format="%H%M").dt.strftime("%H:%M")
    veri.sort_values(by=["Tarih","Saat (TSİ)"],ascending=True,inplace=True)
    return veri

def tüfe(frekans):
    start="01-01-2003"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.FG.J0","TP.FG.J01","TP.FG.J02","TP.FG.J03","TP.FG.J04",
                           "TP.FG.J05","TP.FG.J06","TP.FG.J07","TP.FG.J08","TP.FG.J09",
                           "TP.FG.J10","TP.FG.J11","TP.FG.J12"],startdate=start,enddate=end)
    veri.columns=["Tarih","TÜFE","Gıda ve Alkolsüz İçecekler","Alkollü İçecekler ve Tütün",
                  "Giyim ve Ayakkabı","Konut,","Ev Eşyası","Sağlık","Ulaştırma","Haberleşme",
                  "Eğlence ve Kültür","Eğitim","Lokanta ve Oteller","Çeşitli Mal ve Hizmetler"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"])
    veri["Tarih"] = veri["Tarih"].dt.to_period("M")
    veri.set_index("Tarih",inplace=True)

    if frekans=="Aylık":
        veri=veri.pct_change()*100
    elif frekans=="Yıllık":
        veri=veri.pct_change(12)*100

    veri=veri.round(2)
    veri=veri.reset_index()
    veri.dropna(axis=0,inplace=True)
    return veri

def üfe(frekans):
    start="01-01-2003"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.TUFE1YI.T1","TP.TUFE1YI.T2","TP.TUFE1YI.T15","TP.TUFE1YI.T118",
                           "TP.TUFE1YI.T124"],startdate=start,enddate=end)
    veri.columns=["Tarih","ÜFE","Madencilik ve Taş Ocaklığı","İmalat",
                  "Elektrik Gaz Buhar ve İklimlendirme",
                  "Su Temini Kanalizasyon Atık Yönetimi"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"])
    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri.set_index("Tarih",inplace=True)

    if frekans=="Aylık":
        veri=veri.pct_change()*100
    elif frekans=="Yıllık":
        veri=veri.pct_change(12)*100

    veri=veri.round(2)
    veri=veri.reset_index()
    veri.dropna(axis=0,inplace=True)
    return veri

def ctüfe(frekans):
    start="01-01-2003"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.FE.OKTG01","TP.FE.OKTG02","TP.FE.OKTG03","TP.FE.OKTG04",
                           "TP.FE.OKTG05","TP.FE.OKTG27","TP.FE.OKTG28"],startdate=start,enddate=end)
    veri.columns=["Tarih","TÜFE","Mevsimlik Ürünler Hariç","İşlenmemiş Gıda, Enerji, Alkollü İçkiler ve Tütün ile Altın Hariç",
                  "Enerji, Gıda ve Alkolsüz İçecekler, Alkollü İçkiler ile Tütün Ürünleri ve Altın Hariç",
                  "İşlenmemiş Gıda, Alkollü İçecekler ve Tütün Ürünleri Hariç",
                  "Alkollü İçecekler ve Tütün Hariç","Yönetilen Yönlendirilen Fiyatlar Hariç"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"])
    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri.set_index("Tarih",inplace=True)

    if frekans=="Aylık":
        veri=veri.pct_change()*100
    elif frekans=="Yıllık":
        veri=veri.pct_change(12)*100

    veri=veri.round(2)
    veri=veri.reset_index()
    veri.dropna(axis=0,inplace=True)
    return veri

def ito(frekans):
    start="01-01-2003"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.FE.OKTG01","TP.FG.B01.95","TP.FG.B02.95",
                           "TP.FG.B03.95","TP.FG.B04.95","TP.FG.B05.95",
                           "TP.FG.B06.95","TP.FG.B07.95","TP.FG.B08.95",
                           "TP.FG.B09.95"],startdate=start,enddate=end)
    veri.columns=["Tarih","TÜFE","İTO","Gıda","Konut","Ev Eşyası","Giyim",
                  "Sağlık","Ulaştırma","Kültür-Eğitim","Diğer"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"])
    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri.set_index("Tarih",inplace=True)

    if frekans=="Aylık":
        veri=veri.pct_change()*100
    elif frekans=="Yıllık":
        veri=veri.pct_change(12)*100

    veri=veri.round(2)
    veri=veri.reset_index()
    veri.dropna(axis=0,inplace=True)
    return veri

def döviz(frekans):
    if frekans=="Günlük":
        veri=pd.DataFrame(yf.download(["USDTRY=X","EURTRY=X","DX-Y.NYB"],start="2005-01-01")["Adj Close"])
        veri.dropna(axis=0,inplace=True)
        veri.reset_index(inplace=True)
        veri.columns=["Tarih","DXY","EuroTL","DolarTL"]
        veri["Sepet Kur"]=(veri["DolarTL"]+veri["EuroTL"])/2
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%d-%m-%Y")
    if frekans=="Aylık":
        veri=pd.DataFrame(yf.download(["USDTRY=X","EURTRY=X","DX-Y.NYB"],start="2005-01-01",
                                      interval="1mo")["Adj Close"])
        veri.dropna(axis=0,inplace=True)
        veri.reset_index(inplace=True)
        veri.columns=["Tarih","DXY","EuroTL","DolarTL"]
        veri["Sepet Kur"]=(veri["DolarTL"]+veri["EuroTL"])/2
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%m-%Y")
    return veri

def bist(frekans):
    start="01-01-1987"
    end=datetime.today().strftime("%d-%m-%Y")
    if frekans=="Günlük":
        veri=evdsapi.get_data(["TP.MK.F.BILESIK"],startdate=start,enddate=end)
        veri.dropna(axis=0,inplace=True)
        veri.columns=["Tarih","XU100"]
        veri["Getiri Nominal (%)"]=veri["XU100"]/veri["XU100"].shift(1)-1
        veri["Getiri Nominal (%)"]=veri["Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%d-%m-%Y")
        veri=veri.iloc[1:]
    if frekans=="Aylık":
        veri=evdsapi.get_data(["TP.MK.F.BILESIK"],frequency=5,aggregation_types="last",startdate=start,enddate=end)
        veri.dropna(axis=0,inplace=True)
        veri.columns=["Tarih","XU100"]
        veri["Getiri Nominal (%)"]=veri["XU100"].pct_change()
        veri["Getiri Nominal (%)"]=veri["Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y-%m")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%m-%Y")
        veri=veri.iloc[1:]
    if frekans=="Yıllık":
        veri=evdsapi.get_data(["TP.MK.F.BILESIK","TP.FG.J0"],frequency=8,aggregation_types="last",startdate=start,enddate=end)
        veri.columns=["Tarih","XU100","TÜFE"]
        veri["TÜFE Değişim"]=veri["TÜFE"].pct_change()
        eski=[0.5505,0.7521,0.6877,0.6041,0.7114,0.6597,0.7108,1.2549,
              0.7892,0.7976,0.9909,0.6973,0.6879,0.3903,0.6853,0.2975,0.1836,0.0932]
        veri["TÜFE Değişim"].loc[:len(eski)-1]=[value for value in eski]
        veri["Getiri Nominal (%)"]=veri["XU100"].pct_change()
        veri["Getiri Reel (%)"]=((1+veri["Getiri Nominal (%)"])/(1+veri["TÜFE Değişim"])-1)
        veri["Getiri Reel (%)"]=veri["Getiri Reel (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%Y")
        veri["Getiri Nominal (%)"]=veri["Getiri Nominal (%)"]
        veri["Getiri Nominal (%)"]=veri["Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri.drop(columns=["TÜFE","TÜFE Değişim"],inplace=True)
        veri=veri.iloc[1:]
    return veri

def altın(frekans):
    start="01-01-1987"
    end=datetime.today().strftime("%d-%m-%Y")
    if frekans=="Aylık":
        veri=evdsapi.get_data(["TP.MK.LON.YTL","TP.MK.KUL.YTL"],frequency=5,aggregation_types="last",startdate=start,enddate=end)
        veri.dropna(axis=0,inplace=True)
        veri.columns=["Tarih","Ons Altın ($)","Gram Altın (TL)"]
        veri["Ons Getiri Nominal (%)"]=veri["Ons Altın ($)"].pct_change()
        veri["Ons Getiri Nominal (%)"]=veri["Ons Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Gram Getiri Nominal (%)"]=veri["Gram Altın (TL)"].pct_change()
        veri["Gram Getiri Nominal (%)"]=veri["Gram Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y-%m")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%m-%Y")
        veri=veri.iloc[1:]
    if frekans=="Yıllık":
        veri=evdsapi.get_data(["TP.MK.LON.YTL","TP.MK.KUL.YTL","TP.FG.J0"],frequency=8,aggregation_types="last",startdate=start,enddate=end)
        veri.columns=["Tarih","Ons Altın ($)","Gram Altın (TL)","TÜFE"]
        veri["TÜFE Değişim"]=veri["TÜFE"].pct_change()
        eski=[0.5505,0.7521,0.6877,0.6041,0.7114,0.6597,0.7108,1.2549,
              0.7892,0.7976,0.9909,0.6973,0.6879,0.3903,0.6853,0.2975,0.1836,0.0932]
        veri["TÜFE Değişim"].loc[:len(eski)-1]=[value for value in eski]
        veri["Ons Getiri Nominal (%)"]=veri["Ons Altın ($)"].pct_change()
        veri["Ons Getiri Nominal (%)"]=veri["Ons Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Gram Getiri Nominal (%)"]=veri["Gram Altın (TL)"].pct_change()
        veri["Gram Getiri Reel (%)"]=((1+veri["Gram Getiri Nominal (%)"])/(1+veri["TÜFE Değişim"])-1)
        veri["Gram Getiri Reel (%)"]=veri["Gram Getiri Reel (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Gram Getiri Nominal (%)"]=veri["Gram Getiri Nominal (%)"].apply(lambda x: f"{x * 100:.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%Y")
        veri.drop(columns=["TÜFE","TÜFE Değişim"],inplace=True)
        veri=veri.iloc[1:]
    return veri

def issizlik(tür):
    start="01-01-2014"
    end=datetime.today().strftime("%d-%m-%Y")
    if tür=="Mevsimsellikten Arındırılmamış İş Gücü 15+ Nüfus":
        veri=evdsapi.get_data(["TP.YISGUCU2.G1","TP.YISGUCU2.G2","TP.YISGUCU2.G3",
                               "TP.YISGUCU2.G4","TP.YISGUCU2.G5","TP.YISGUCU2.G6",
                               "TP.YISGUCU2.G7","TP.YISGUCU2.G8"],startdate=start,enddate=end)
        veri.columns=["Tarih","Nüfus","İş Gücü","İstihdam","İşsiz","İş Gücüne Dahil Olmayan",
                      "İş Gücüne Katılım (%)","İstihdam (%)","İşsizlik (%)"]
        veri["İş Gücüne Katılım (%)"]=veri["İş Gücüne Katılım (%)"].apply(lambda x: f"{x :.2f}%")
        veri["İstihdam (%)"]=veri["İstihdam (%)"].apply(lambda x: f"{x :.2f}%")
        veri["İşsizlik (%)"]=veri["İşsizlik (%)"].apply(lambda x: f"{x :.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y-%m")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%m-%Y")
    if tür=="Mevsimsellikten Arındırılmış İş Gücü 15+ Nüfus":
        veri=evdsapi.get_data(["TP.TIG01","TP.TIG02","TP.TIG03","TP.TIG04","TP.TIG05",
                               "TP.TIG06","TP.TIG07","TP.TIG08"],startdate=start,enddate=end)
        veri.columns=["Tarih","Nüfus","İş Gücü","İstihdam","İşsiz","İş Gücüne Dahil Olmayan",
                      "İş Gücüne Katılım (%)","İstihdam (%)","İşsizlik (%)"]
        veri["İş Gücüne Katılım (%)"]=veri["İş Gücüne Katılım (%)"].apply(lambda x: f"{x :.2f}%")
        veri["İstihdam (%)"]=veri["İstihdam (%)"].apply(lambda x: f"{x :.2f}%")
        veri["İşsizlik (%)"]=veri["İşsizlik (%)"].apply(lambda x: f"{x :.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y-%m")
        veri["Tarih"]=veri["Tarih"].dt.strftime("%m-%Y")
    return veri

##------------------------------------------------------------------------------------

st.markdown("""
    <style>
    body {
        background-color: white;
    }
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        position: relative;
    }
    .title {
        color: red;
        border: 2px solid black;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Freestyle Script', cursive;
        font-size: 55px;
        position: relative;
    }
    .time-box {
        position: absolute;
        bottom: 10px;
        right: 10px;
        padding: 5px 10px;
        background-color: #ffffff;
        font-family: 'Freestyle Script', cursive;;
        font-size: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title">Via Anlaşılır Ekonomi</h1>',unsafe_allow_html=True)
tarihbugün=datetime.now().strftime('%d/%m/%Y')
st.markdown(f'<div class="time-box">{tarihbugün}</div>',unsafe_allow_html=True)
st.sidebar.title("Göstergeler")

##-----------------------------------------------------------------------------

buttons=[
    ("MB APİ Fonlama","button1_clicked"),
    ("MB Faizler","button2_clicked"),
    ("MB Kur Değerleri","button3_clicked"),
    ("Bilançolar","button4_clicked"),
    ("Geçmiş Fiyat","button5_clicked"),
    ("Bist Tree Map","button6_clicked"),
    ("Bist YF Hedef Fiyat","button7_clicked"),
    ("CNBC Pro Makaleler","button8_clicked"),
    ("CDS","button9_clicked"),
    ("Ekonomik Takvim","button10_clicked"),
    ("TÜFE","button11_clicked"),
    ("ÜFE","button12_clicked"),
    ("TÜFE Çekirdek","button13_clicked"),
    ("İTO","button14_clicked"),
    ("Döviz","button15_clicked"),
    ("BİST","button16_clicked"),
    ("Altın","button17_clicked"),
    ("İşsizlik","button18_clicked")]

def reset_buttons():
    for _, key in buttons:
        st.session_state[key]=False

for label, key in buttons:
    if st.sidebar.button(label):
        reset_buttons() 
        st.session_state[key]=True

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
    x=pd.to_datetime(mbapi()["Tarih"],format="%d-%m-%Y"),
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
        "text":"Türkiye CDS 5 Year","x":0.5,"xanchor":"center"},
    xaxis_title="Tarih",
    yaxis_title="CDS",
    xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M2"))
    fig.update_xaxes(tickangle=-45)

    fig2=go.Figure()
    fig2.add_trace(go.Scatter(
    x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),
    y=veri["CDS Oynaklık"],
    mode="lines",
    name="CDS Oynaklık",
    line=dict(color="Blue")))

    fig2.update_layout(title={
        "text":"Türkiye CDS 5 Year Oynaklık","x":0.5,"xanchor":"center"},
    xaxis_title="Tarih",
    yaxis_title="Oynaklık",
    xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M2"))
    fig2.update_xaxes(tickangle=-45)
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

##----------------------------------------------------------------------------------

if st.session_state.get("button10_clicked",False):
    veri=ekonomiktakvim()
    st.markdown("### **Bu Hafta Takvimi**",unsafe_allow_html=True)
    st.dataframe(veri,hide_index=True,use_container_width=True,height=700)

##----------------------------------------------------------------------------------

if st.session_state.get("button11_clicked",False):
    secenek=["Aylık","Yıllık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)
    veri=tüfe(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)

    veri["Tarih"]=veri["Tarih"].dt.to_timestamp()
    fig=go.Figure()
    columns=["TÜFE","Gıda ve Alkolsüz İçecekler","Alkollü İçecekler ve Tütün",
                  "Giyim ve Ayakkabı","Konut,","Ev Eşyası","Sağlık","Ulaştırma","Haberleşme",
                  "Eğlence ve Kültür","Eğitim","Lokanta ve Oteller","Çeşitli Mal ve Hizmetler"]
    renkler=["Red","Blue","Green","Orange","Purple","Black","Cyan","Magenta","Salmon","Gray",
               "Brown","Pink","Crimson"]

    for col,color in zip(columns,renkler):
        fig.add_trace(go.Scatter(
            x=veri["Tarih"],
            y=veri[col],
            mode="lines",
            name=col,
            line=dict(color=color)))

    fig.update_layout(
        title={"text": "Tüketici Enflasyonu 2003=100 (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Enflasyon",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M3"))

    fig.update_xaxes(tickangle=-45)
    
    son_satir=veri.tail(1).iloc[0]
    sıralı_sütun=son_satir[columns].sort_values(ascending=False).index
    sıralı_deger=son_satir[columns].sort_values(ascending=False).values
    sıralı_renkler=[renkler[columns.index(col)] for col in sıralı_sütun]

    fig2=go.Figure()
    fig2.add_trace(go.Bar(
    x=sıralı_deger,
    y=sıralı_sütun,
    marker_color=sıralı_renkler,
    orientation="h",
    text=sıralı_deger,
    textposition="outside"))

    fig2.update_layout(
        title={"text": "TÜFE 2003=100 (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Enflasyon",
        yaxis_title="Kategori",
        xaxis=dict(tickangle=-45))
    
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

##-------------------------------------------------------------------------------------------

if st.session_state.get("button12_clicked",False):
    secenek=["Aylık","Yıllık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)
    veri=üfe(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)

    veri["Tarih"]=veri["Tarih"].dt.to_timestamp()
    fig=go.Figure()
    columns=["ÜFE","Madencilik ve Taş Ocaklığı","İmalat","Elektrik Gaz Buhar ve İklimlendirme",
            "Su Temini Kanalizasyon Atık Yönetimi"]
    renkler=["Red","Blue","Green","Orange","Black"]

    for col, color in zip(columns, renkler):
        fig.add_trace(go.Scatter(
            x=veri["Tarih"],
            y=veri[col],
            mode="lines",
            name=col,
            line=dict(color=color)))

    fig.update_layout(
        title={"text": "Üretici Enflasyonu 2003=100 (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Enflasyon",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M3"))

    fig.update_xaxes(tickangle=-45)
    
    son_satir=veri.tail(1).iloc[0]
    sıralı_sütun=son_satir[columns].sort_values(ascending=False).index
    sıralı_deger=son_satir[columns].sort_values(ascending=False).values
    sıralı_renkler=[renkler[columns.index(col)] for col in sıralı_sütun]

    fig2=go.Figure()
    fig2.add_trace(go.Bar(
    x=sıralı_deger,
    y=sıralı_sütun,
    marker_color=sıralı_renkler,
    orientation="h",
    text=sıralı_deger,
    textposition="outside"))

    fig2.update_layout(
        title={"text": "ÜFE 2003=100 (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Enflasyon",
        yaxis_title="Kategori",
        xaxis=dict(tickangle=-45))
    
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

##---------------------------------------------------------------------------------------

if st.session_state.get("button13_clicked",False):
    secenek=["Aylık","Yıllık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)
    veri=ctüfe(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)

    veri["Tarih"]=veri["Tarih"].dt.to_timestamp()
    fig=go.Figure()
    columns=["TÜFE","Mevsimlik Ürünler Hariç","İşlenmemiş Gıda, Enerji, Alkollü İçkiler ve Tütün ile Altın Hariç",
            "Enerji, Gıda ve Alkolsüz İçecekler, Alkollü İçkiler ile Tütün Ürünleri ve Altın Hariç",
            "İşlenmemiş Gıda, Alkollü İçecekler ve Tütün Ürünleri Hariç",
            "Alkollü İçecekler ve Tütün Hariç","Yönetilen Yönlendirilen Fiyatlar Hariç"]
    renkler=["Red","Blue","Green","Orange","Black","Cyan","Magenta","Salmon","Gray"]

    for col, color in zip(columns,renkler):
        fig.add_trace(go.Scatter(
            x=veri["Tarih"],
            y=veri[col],
            mode="lines",
            name=col,
            line=dict(color=color)))

    fig.update_layout(
        title={"text": "Çekirdek Enflasyon 2003=100 (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Enflasyon",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M3"))

    fig.update_xaxes(tickangle=-45)
    
    son_satir=veri.tail(1).iloc[0]
    sıralı_sütun=son_satir[columns].sort_values(ascending=False).index
    sıralı_deger=son_satir[columns].sort_values(ascending=False).values
    sıralı_renkler=[renkler[columns.index(col)] for col in sıralı_sütun]

    fig2=go.Figure()
    fig2.add_trace(go.Bar(
    x=sıralı_deger,
    y=sıralı_sütun,
    marker_color=sıralı_renkler,
    orientation="h",
    text=sıralı_deger,
    textposition="outside"))

    fig2.update_layout(
        title={"text": "Çekirdek TÜFE 2003=100 (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Enflasyon",
        yaxis_title="Kategori",
        xaxis=dict(tickangle=-45))
    
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

##-----------------------------------------------------------------------------------------
if st.session_state.get("button14_clicked",False):
    secenek=["Aylık","Yıllık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)
    veri=ito(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)

    veri["Tarih"]=veri["Tarih"].dt.to_timestamp()
    fig=go.Figure()
    columns=["TÜFE","İTO","Gıda","Konut","Ev Eşyası","Giyim",
            "Sağlık","Ulaştırma","Kültür-Eğitim","Diğer"]
    renkler=["Red","Blue","Green","Orange","Black","Pink","Magenta","Salmon","Gray",
             "Brown"]

    for col, color in zip(columns,renkler):
        fig.add_trace(go.Scatter(
            x=veri["Tarih"],
            y=veri[col],
            mode="lines",
            name=col,
            line=dict(color=color)))

    fig.update_layout(
        title={"text": "İTO Enflasyon 1995=100 (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Enflasyon",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M3"))

    fig.update_xaxes(tickangle=-45)
    
    son_satir=veri.tail(1).iloc[0]
    sıralı_sütun=son_satir[columns].sort_values(ascending=False).index
    sıralı_deger=son_satir[columns].sort_values(ascending=False).values
    sıralı_renkler=[renkler[columns.index(col)] for col in sıralı_sütun]

    fig2=go.Figure()
    fig2.add_trace(go.Bar(
    x=sıralı_deger,
    y=sıralı_sütun,
    marker_color=sıralı_renkler,
    orientation="h",
    text=sıralı_deger,
    textposition="outside"))

    fig2.update_layout(
        title={"text": "İTO 1995=100 (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Enflasyon",
        yaxis_title="Kategori",
        xaxis=dict(tickangle=-45))
    
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

##--------------------------------------------------------------------------------------

if st.session_state.get("button15_clicked",False):
    secenek=["Günlük","Aylık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)
    veri=döviz(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)

    fig=make_subplots(specs=[[{"secondary_y":True}]])
    columns=["DXY","EuroTL","DolarTL","Sepet Kur"]
    renkler=["Red","Blue","Green","Black"]

    if secim=="Günlük":
        tarih_formatı="%d-%m-%Y"
    else:
        tarih_formatı="%m-%Y"

    for col,color in zip(columns, renkler):
        if col=="DXY":
            fig.add_trace(
                go.Scatter(
                    x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),
                    y=veri[col],
                    mode="lines",
                    name=col,
                    line=dict(color=color)),
                secondary_y=True)
        else:
            fig.add_trace(
                go.Scatter(
                    x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),
                    y=veri[col],
                    mode="lines",
                    name=col,
                    line=dict(color=color)),
                secondary_y=False)
    fig.update_layout(
        title={"text": "Döviz","x": 0.5,"xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Döviz",
        xaxis=dict(tickformat=tarih_formatı,tickmode="linear",dtick="M3"),
        yaxis=dict(title="EuroTL / DolarTL / Sepet Kur"), 
        yaxis2=dict(title="DXY"))
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig)

##---------------------------------------------------------------------------------------

if st.session_state.get("button16_clicked",False):
    secenek=["Günlük","Aylık","Yıllık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)
    veri=bist(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)

    if secim=="Günlük":
        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),
        y=veri["XU100"],
        mode="lines",
        name="XU100",
        line=dict(color="Red")))

        fig.update_layout(title={
            "text":"XU100","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Endeks",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M5"))
        fig.update_xaxes(tickangle=-45)

        fig2=go.Figure()
        fig2.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),
        y=veri["Getiri Nominal (%)"],
        mode="lines",
        name="Getiri",
        line=dict(color="Blue")))

        fig2.update_layout(title={
        "text":"XU100 Getiri Nominal (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Getiri",
        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M5"))
        fig2.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)
        st.plotly_chart(fig2)
    
    if secim=="Aylık":
        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%m-%Y"),
        y=veri["XU100"],
        mode="lines",
        name="XU100",
        line=dict(color="Red")))

        fig.update_layout(title={
            "text":"XU100","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Endeks",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M5"))
        fig.update_xaxes(tickangle=-45)

        fig2=go.Figure()
        fig2.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%m-%Y"),
        y=veri["Getiri Nominal (%)"],
        mode="lines",
        name="Getiri",
        line=dict(color="Blue")))

        fig2.update_layout(title={
        "text":"XU100 Getiri Nominal (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Getiri",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M5"))
        fig2.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)
        st.plotly_chart(fig2)
    
    if secim=="Yıllık":
        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%Y"),
        y=veri["XU100"],
        mode="lines",
        name="XU100",
        line=dict(color="Red")))

        fig.update_layout(title={
            "text":"XU100","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Endeks",
        xaxis=dict(tickformat="%Y",tickmode="linear",dtick="M12"))
        fig.update_xaxes(tickangle=-45)

        fig2=go.Figure()
        fig2.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"], format="%Y"),
        y=veri["Getiri Nominal (%)"],
        name="Nominal Getiri",
        marker_color="Red"))

        fig2.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"], format="%Y"),
        y=veri["Getiri Reel (%)"],
        name="Reel Getiri",
        marker_color="Blue"))

        fig2.update_layout(
        title={
            "text": "XU100 Getiri Nominal ve Reel (%)",
            "x": 0.5,
            "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Getiri",
        xaxis=dict(
            tickformat="%Y",
            tickmode="linear",
            dtick="M12"),
            barmode="group")
        fig2.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)
        st.plotly_chart(fig2)

##-----------------------------------------------------------------------------------------

if st.session_state.get("button17_clicked",False):
    secenek=["Aylık","Yıllık"]
    st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)
    veri=altın(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)

    if secim=="Aylık":
        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%m-%Y"),
        y=veri["Ons Altın ($)"],
        mode="lines",
        name="Ons Altın ($)",
        line=dict(color="Red")))

        fig.update_layout(title={
            "text":"Ons Altın ($)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Fiyat",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M5"))
        fig.update_xaxes(tickangle=-45)

        fig2=go.Figure()
        fig2.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"],format="%m-%Y"),
        y=veri["Ons Getiri Nominal (%)"],
        name="Getiri",
        marker=dict(color="Blue")))

        fig2.update_layout(title={
        "text": "Ons Altın Getiri Nominal (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Getiri",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M5"))
        fig2.update_xaxes(tickangle=-45)
        

        fig3=go.Figure()
        fig3.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%m-%Y"),
        y=veri["Gram Altın (TL)"],
        mode="lines",
        name="Gram Altın (TL)",
        line=dict(color="Red")))

        fig3.update_layout(title={
            "text":"Gram Altın (TL)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Fiyat",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M5"))
        fig3.update_xaxes(tickangle=-45)

        fig4=go.Figure()
        fig4.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"],format="%m-%Y"),
        y=veri["Gram Getiri Nominal (%)"],
        name="Getiri",
        marker=dict(color="Blue")))

        fig4.update_layout(title={
        "text": "Gram Altın Getiri Nominal (%)", "x": 0.5, "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Getiri",
        xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M5"))
        fig4.update_xaxes(tickangle=-45)

        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)
    
    if secim=="Yıllık":
        fig=go.Figure()
        fig.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%Y"),
        y=veri["Ons Altın ($)"],
        mode="lines",
        name="Ons Altın ($)",
        line=dict(color="Red")))

        fig.update_layout(title={
            "text":"Ons Altın ($)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Fiyat",
        xaxis=dict(tickformat="%Y",tickmode="linear",dtick="M5"))
        fig.update_xaxes(tickangle=-45)


        fig2=go.Figure()
        fig2.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%Y"),
        y=veri["Gram Altın (TL)"],
        mode="lines",
        name="Gram Altın (TL)",
        line=dict(color="Red")))

        fig2.update_layout(title={
            "text":"Gram Altın (TL)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Fiyat",
        xaxis=dict(tickformat="%Y",tickmode="linear",dtick="M5"))
        fig2.update_xaxes(tickangle=-45)

        fig3=go.Figure()
        fig3.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"], format="%Y"),
        y=veri["Gram Getiri Nominal (%)"],
        name="Nominal Getiri",
        marker_color="Red"))

        fig3.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"], format="%Y"),
        y=veri["Gram Getiri Reel (%)"],
        name="Reel Getiri",
        marker_color="Blue"))

        fig3.update_layout(
        title={
            "text": "Gram Altın Getiri Nominal ve Reel (%)",
            "x": 0.5,
            "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Getiri",
        xaxis=dict(
            tickformat="%Y",
            tickmode="linear",
            dtick="M12"),
            barmode="group")
        fig3.update_xaxes(tickangle=-45)

        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)

##--------------------------------------------------------------------------------------

if st.session_state.get("button18_clicked",False):
    secenek=["Mevsimsellikten Arındırılmamış İş Gücü 15+ Nüfus",
             "Mevsimsellikten Arındırılmış İş Gücü 15+ Nüfus"]
    st.markdown('<p style="font-weight:bold; color:black;">Veri Türü Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)
    veri=issizlik(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)
    if secim=="Mevsimsellikten Arındırılmamış İş Gücü 15+ Nüfus":
        fig=go.Figure()
        for column in veri.columns[1:6]:
            fig.add_trace(go.Scatter(
                x=veri["Tarih"],
                y=veri[column],
                mode="lines",
                name=column,
                fill="tozeroy"))

        fig.update_layout(
            title={
                "text": "İş Gücü","x": 0.5, "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Değer",
        xaxis=dict(tickformat="%Y-%m",tickmode="linear"),
        yaxis=dict(tickformat="d"))
        fig.update_xaxes(tickangle=-45)

        fig2=go.Figure()
        for column in veri.columns[6:]:
            fig2.add_trace(go.Bar(
                x=veri["Tarih"],
                y=veri[column],
                name=column))
        fig2.update_layout(
            title={
                "text": "İş Gücü (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Değer",
        xaxis=dict(tickformat="%Y-%m",tickmode="linear"),
        yaxis=dict(tickformat="d"))
        fig2.update_xaxes(tickangle=-45)

        st.plotly_chart(fig)
        st.plotly_chart(fig2)

    if secim=="Mevsimsellikten Arındırılmış İş Gücü 15+ Nüfus":
        fig=go.Figure()
        for column in veri.columns[1:6]:
            fig.add_trace(go.Scatter(
                x=veri["Tarih"],
                y=veri[column],
                mode="lines",
                name=column,
                fill="tozeroy"))

        fig.update_layout(
            title={
                "text": "İş Gücü","x": 0.5, "xanchor": "center"},
        xaxis_title="Tarih",
        yaxis_title="Değer",
        xaxis=dict(tickformat="%Y-%m",tickmode="linear"),
        yaxis=dict(tickformat="d"))
        fig.update_xaxes(tickangle=-45)

        fig2=go.Figure()
        for column in veri.columns[6:]:
            fig2.add_trace(go.Bar(
                x=veri["Tarih"],
                y=veri[column],
                name=column))
        fig2.update_layout(
            title={
                "text": "İş Gücü (%)","x":0.5,"xanchor":"center"},
        xaxis_title="Tarih",
        yaxis_title="Değer",
        xaxis=dict(tickformat="%Y-%m",tickmode="linear"),
        yaxis=dict(tickformat="d"))
        fig2.update_xaxes(tickangle=-45)

        st.plotly_chart(fig)
        st.plotly_chart(fig2)

##--------------------------------------------------------------------------------------
     