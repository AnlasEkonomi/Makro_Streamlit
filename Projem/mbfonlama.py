import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from requests.exceptions import ReadTimeout
import tabula

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def mbapi():
    try:
        start="02-01-2019"
        end=datetime.today().strftime("%d-%m-%Y")
        kodlar=["TP.APIFON1.IHA","TP.APIFON1.KOT.A","TP.APIFON1.KOT.B","TP.APIFON1.KOT.C",
            "TP.APIFON1.KOT.T","TP.APIFON1.TOP","TP.APIFON2.IHA","TP.APIFON2.KOT",
            "TP.APIFON2.TOP","TP.APIFON3","TP.APIFON4"]
        sütunad=["Tarih","İhale Yoluyla Fonlama","Bist O/N","Depo","GLP","Toplam Kotasyon",
                    "Toplam Fonlama","İhale Yoluyla Sterilizasyon","Kotasyon Yoluyla Sterilizasyon",
                    "Toplam Sterilizasyon","Net Fonlama","AOFM (%)"]  
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end).dropna()
        veri.columns=sütunad
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y").dt.strftime("%d-%m-%Y")         
        return veri
    except ReadTimeout:
        st.warning("Sunucuya ulaşılamadı. Lütfen tekrar deneyiniz...")

def ihale():
    try:
        bugun=datetime.today()
        url="https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb+tr/main+page+site+area/acik+piyasa+islemleri/ihale+ile+gerceklestirilen+repo+islemleri+verileri"
        veri=pd.read_html(url)[0]
        veri=veri.iloc[:,[2,3,4,5,6,7,9,12]]
        sütunad=["Tür","Valör","Vade","Gün","Teklif","Kazanan","Basit Faiz","Bileşik Faiz"]
        veri.columns=sütunad
        veri.drop(veri.index[:5],inplace=True)
        veri["Valör"]=pd.to_datetime(veri["Valör"],format="%d.%m.%Y")
        veri["Vade"]=pd.to_datetime(veri["Vade"],format="%d.%m.%Y")
        veri=veri[veri["Vade"]>bugun]
        veri["Teklif"]=pd.to_numeric(veri["Teklif"].str.replace(".", "").str.replace(",", "."))
        veri["Kazanan"]=pd.to_numeric(veri["Kazanan"].str.replace(".", "").str.replace(",", "."))
        veri["Valör"]=veri["Valör"].dt.strftime("%d-%m-%Y")
        veri["Vade"]=veri["Vade"].dt.strftime("%d-%m-%Y")
        return veri
    except ReadTimeout:
        st.warning("Sunucuya ulaşılamadı. Lütfen tekrar deneyiniz...")

def swap():
    try:
        url="https://www.tcmb.gov.tr/wps/wcm/connect/a6ffdb2f-47d9-4ae9-8c39-5075867aaec3/TCMB+Tarafl%C4%B1+Swap+%C4%B0%C5%9Flemleri.pdf?MOD=AJPERES"
        veriler=tabula.read_pdf(url,pages="all",multiple_tables=False)

        sütunad=["Valör Tarihi","Döviz Karşılığı TL Swap","Döviz Karşılığı TL Swap Stok","Bist Swap",
        "Bist Swap Stok","TL Karşılığı Altın Swap","TL Karşılığı Altın Swap Stok",
        "Döviz Karşılığı TL Swap Geleneksel İhale (Alım)","Döviz Karşılığı TL Swap Geleneksel İhale (Alım) Stok",
        "Döviz Karşılığı TL Swap Geleneksel İhale (Satım)","Döviz Karşılığı TL Swap Geleneksel İhale (Satım) Stok",
        "Döviz Karşılığı TL Swap Miktar İhale","Döviz Karşılığı TL Swap Miktar İhale Stok",
        "Altın Karşılığı TL Swap Geleneksel İhale (Alım)","Altın Karşılığı TL Swap Geleneksel İhale (Alım) Stok",
        "Altın Karşılığı TL Swap Geleneksel İhale (Satım)","Altın Karşılığı TL Swap Geleneksel İhale (Satım) Stok",
        "Döviz Karşılığı Altın Swap","Döviz Karşılığı Altın Swap Stok","Toplam Stok (Alım)","Toplam Stok (Satım)",
        "Döviz Karşılığı TL Swap-Depo İşlemleri","Döviz Karşılığı TL Swap-Depo İşlemleri Stok"]

        birlestir=pd.DataFrame(columns=sütunad)

        for i,df in enumerate(veriler):
            if i==0:
                df.columns=sütunad
            else:
                df=df.iloc[1:]
            
            df.reset_index(drop=True,inplace=True)
            birlestir=pd.concat([birlestir,df],ignore_index=True)

        birlestir.fillna("-",inplace=True)
        veri=birlestir[1:].reset_index(drop=True)
        veri=veri.iloc[:-11].reset_index(drop=True)
        istenmeyen=veri.loc[[39,40],"Valör Tarihi"].tolist()
        veri=veri[~veri["Valör Tarihi"].isin(istenmeyen)]
        veri.reset_index(drop=True,inplace=True)
        veri["Valör Tarihi"]=pd.to_datetime(veri["Valör Tarihi"],format="%d.%m.%Y")
        veri["Valör Tarihi"]=veri["Valör Tarihi"].dt.strftime("%d-%m-%Y")

        for i in veri.columns[1:]:
            veri[i]=veri[i].apply(lambda x: x.replace('.', '').replace(',', '.') if x != '-' else x)
            veri[i]=pd.to_numeric(veri[i],errors="coerce")
        veri.fillna(0,inplace=True)
        return veri
    except ReadTimeout:
        st.warning("Sunucuya ulaşılamadı. Lütfen tekrar deneyiniz...")

def mbkur():
    tarih=pd.to_datetime(swap()["Valör Tarihi"],format="%d-%m-%Y")
    start=tarih[0].strftime("%d-%m-%Y")
    end=tarih.iloc[-1].strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.DK.USD.A.YTL"],startdate=start,enddate=end)
    veri.columns=["Tarih","DolarTL Alış"]
    veri.dropna(axis=0,inplace=True)
    return veri


st.markdown("<h4 style='font-size:20px;'>TCMB APİ Fonlama Yapısı (Milyon TL)</h4>",unsafe_allow_html=True)
veri=mbapi()
st.dataframe(veri,hide_index=True,width=1000)

veri2=ihale()
st.markdown("<h4 style='font-size:20px;'>TCMB APİ Açık İhale Yapısı (Milyon TL)</h4>",unsafe_allow_html=True)
st.dataframe(veri2,hide_index=True,width=1000)

veri3=swap()
st.markdown("<h4 style='font-size:20px;'>TCMB Swap Fonlama Yapısı (Milyon $)</h4>",unsafe_allow_html=True)
st.dataframe(veri3,hide_index=True,width=1000)


tswap=pd.merge(swap(),mbkur()[["Tarih","DolarTL Alış"]],left_on="Valör Tarihi",right_on="Tarih",how="left")
tswap["TL Değer"]=(tswap["Toplam Stok (Alım)"]-tswap["Döviz Karşılığı TL Swap-Depo İşlemleri Stok"])*tswap["DolarTL Alış"]


fig=go.Figure()
fig.add_trace(go.Scatter(x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),
                y=veri["Net Fonlama"],mode="lines",line=dict(color="red"),
                name="APİ Net Fonlama"))

fig.add_trace(go.Scatter(x=pd.to_datetime(tswap["Tarih"],format="%d-%m-%Y"),
                             y=tswap["TL Değer"],mode="lines",line=dict(color="blue"),
                             name="Swap Fonlama (TL)"))

fig.update_layout(title={"text":"Net Fonlama (Api-Swap)","x": 0.5,"xanchor":"center"},
                xaxis_title="Tarih",yaxis_title="Milyon TL",
                xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1",
                        rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))

fig.update_yaxes(showline=True,zeroline=True,zerolinecolor="black",zerolinewidth=2)
fig.update_xaxes(tickangle=-45)
fig.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black")) 


fig2=go.Figure()
fig2.add_trace(go.Scatter(x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),
                y=veri["AOFM (%)"],mode="lines",line=dict(color="red"),name="AOFM (%)"))
fig2.update_layout(title={"text":"AOFM (%)","x": 0.5,"xanchor":"center"},
                xaxis_title="Tarih",yaxis_title="AOFM (%)",
                xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1",
                        rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
fig2.update_yaxes(showline=True,zeroline=True,zerolinecolor="black",zerolinewidth=2)
fig2.update_xaxes(tickangle=-45)
fig2.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig2.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black")) 

fig3=go.Figure()
fig3.add_trace(go.Scatter(x=pd.to_datetime(veri3["Valör Tarihi"],format="%d-%m-%Y"),
                          y=veri3["Toplam Stok (Alım)"],mode="lines",name="Toplam Stok (Alım)",
                          line=dict(color="blue")))

fig3.add_trace(go.Scatter(x=pd.to_datetime(veri3["Valör Tarihi"],format="%d-%m-%Y"),
                          y=veri3["Toplam Stok (Satım)"],mode="lines",name="Toplam Stok (Satım)",
                          line=dict(color="red")))

fig3.update_layout(title={"text":"Toplam Swap Stok (Milyon $)","x":0.5,"xanchor":"center"},
                   xaxis_title="Valör Tarihi",yaxis_title="Milyon $",
                   xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M1",
                   rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
fig3.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig3.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"),showline=True,linecolor="black")
fig3.update_xaxes(tickangle=-45)

st.plotly_chart(fig)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
