import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def döviz(frekans):
    kodlar=["USDTRY=X","EURTRY=X","DX-Y.NYB"]
    sütunad=["Tarih","DXY","EuroTL","DolarTL"]
    if frekans=="Günlük":
        veri=pd.DataFrame(yf.download(kodlar,start="2005-01-01")["Adj Close"]).dropna().reset_index()
        veri.columns=sütunad
        veri["Sepet Kur"]=(veri["DolarTL"]+veri["EuroTL"])/2
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y").dt.strftime("%d-%m-%Y")
    if frekans=="Aylık":
        veri=pd.DataFrame(yf.download(kodlar,start="2005-01-01",interval="1mo")["Adj Close"]).dropna().reset_index()
        veri.columns=sütunad
        veri["Sepet Kur"]=(veri["DolarTL"]+veri["EuroTL"])/2
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y").dt.strftime("%m-%Y")
    return veri

secenek=["Günlük","Aylık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=döviz(secim)

st.markdown("<h4 style='font-size:20px;'>Döviz Verileri</h4>",unsafe_allow_html=True)
st.dataframe(veri,hide_index=True,use_container_width=True)

fig=make_subplots(specs=[[{"secondary_y":True}]])
columns=["DXY","EuroTL","DolarTL","Sepet Kur"]
renkler=["Red","Blue","Green","Black"]

tarih_formatı="%d-%m-%Y" if secim=="Günlük" else "%m-%Y"

for col,color in zip(columns,renkler):
    fig.add_trace(
        go.Scatter(x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),
            y=veri[col],mode="lines",name=col,line=dict(color=color)),
            secondary_y=(col=="DXY"))

fig.update_layout(
    title={"text":"Döviz","x":0.5,"xanchor":"center"},
    xaxis_title="Tarih",yaxis_title="Döviz",
    xaxis=dict(tickformat=tarih_formatı,tickmode="linear",dtick="M3",
               rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)),
    yaxis=dict(title="EuroTL / DolarTL / Sepet Kur"),yaxis2=dict(title="DXY"))

fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_xaxes(tickangle=-45)

st.plotly_chart(fig)