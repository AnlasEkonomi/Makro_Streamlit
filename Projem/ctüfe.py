import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def ctüfe(frekans):
    start="01-01-2003"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.FE.OKTG01","TP.FE.OKTG02","TP.FE.OKTG03","TP.FE.OKTG04","TP.FE.OKTG05",
            "TP.FE.OKTG27","TP.FE.OKTG28"]
    sütunad=["Tarih","TÜFE","Mevsimlik Ürünler Hariç",
             "İşlenmemiş Gıda, Enerji, Alkollü İçkiler ve Tütün ile Altın Hariç",
            "Enerji, Gıda ve Alkolsüz İçecekler, Alkollü İçkiler ile Tütün Ürünleri ve Altın Hariç",
            "İşlenmemiş Gıda, Alkollü İçecekler ve Tütün Ürünleri Hariç",
            "Alkollü İçecekler ve Tütün Hariç","Yönetilen Yönlendirilen Fiyatlar Hariç"]
    veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
    veri.columns=sütunad
    veri["Tarih"]=pd.to_datetime(veri["Tarih"]).dt.to_period("M")
    veri.set_index("Tarih",inplace=True)

    if frekans=="Aylık":
        veri=veri.pct_change()*100
    elif frekans=="Yıllık":
        veri=veri.pct_change(12)*100

    veri=veri.round(2).reset_index()
    veri.dropna(axis=0,inplace=True)
    return veri

secenek=["Aylık","Yıllık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=ctüfe(secim)

st.markdown("<h4 style='font-size:20px;'>Çekirdek TÜFE Enflasyonu</h4>",unsafe_allow_html=True)
st.dataframe(veri,hide_index=True,use_container_width=True)

veri["Tarih"]=veri["Tarih"].dt.to_timestamp()

columns=["TÜFE", "Mevsimlik Ürünler Hariç", 
        "İşlenmemiş Gıda, Enerji, Alkollü İçkiler ve Tütün ile Altın Hariç",
        "Enerji, Gıda ve Alkolsüz İçecekler, Alkollü İçkiler ile Tütün Ürünleri ve Altın Hariç",
        "İşlenmemiş Gıda, Alkollü İçecekler ve Tütün Ürünleri Hariç",
        "Alkollü İçecekler ve Tütün Hariç","Yönetilen Yönlendirilen Fiyatlar Hariç"]
renkler=["Red","Blue","Green","Orange","Black","Cyan","Magenta","Salmon","Gray"]

fig=go.Figure()
for col,color in zip(columns,renkler):
    fig.add_trace(go.Scatter(x=veri["Tarih"],y=veri[col],mode="lines",
                                name=col,line=dict(color=color)))

fig.update_layout(
    title={"text":"Çekirdek Enflasyon 2003=100 (%)","x":0.5,"xanchor":"center"},
    xaxis_title="Tarih",yaxis_title="Enflasyon",
    xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M3",
               rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))

fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_xaxes(tickangle=-45)

son_satir=veri.tail(1).iloc[0]
sıralı_sütun=son_satir[columns].sort_values(ascending=False).index
sıralı_deger=son_satir[columns].sort_values(ascending=False).values
sıralı_renkler=[renkler[columns.index(col)] for col in sıralı_sütun]

fig2=go.Figure()
fig2.add_trace(go.Bar(x=sıralı_deger,y=sıralı_sütun,marker_color=sıralı_renkler,
    orientation="h", text=sıralı_deger, textposition="outside"))

fig2.update_layout(
    title={"text":"Çekirdek TÜFE 2003=100 (%)","x":0.5,"xanchor":"center"},
    xaxis_title="Enflasyon",yaxis_title="Kategori",xaxis=dict(tickangle=-45))

st.plotly_chart(fig)
st.plotly_chart(fig2)