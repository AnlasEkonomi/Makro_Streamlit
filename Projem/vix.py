import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

def vix(frekans):
    kodlar=["^VIX"]
    sütunad=["Tarih","VIX"]
    if frekans=="Günlük":
        veri=pd.DataFrame(yf.download(kodlar,start="1991-01-01")["Adj Close"]).dropna().reset_index()
        veri.columns=sütunad
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y").dt.strftime("%d-%m-%Y")
    elif frekans=="Aylık":
        veri=pd.DataFrame(yf.download(kodlar,start="1991-01-01",interval="1mo")["Adj Close"]).dropna().reset_index()
        veri.columns=sütunad
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%m-%Y").dt.strftime("%m-%Y")
    return veri

secenek=["Günlük","Aylık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=vix(secim)

st.dataframe(veri,hide_index=True,use_container_width=True)

tarih_formatı="%d-%m-%Y" if secim=="Günlük" else "%m-%Y"

fig=go.Figure()
fig.add_trace(go.Scatter(x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),y=veri["VIX"],mode="lines",name="VIX"))

fig.update_layout(
    title={"text":"CBOE Volatility Index","x": 0.5,"xanchor":"center"},
    xaxis_title="Tarih",
    yaxis_title="VIX",
    xaxis=dict(tickmode="linear",dtick="M3",tickformat=tarih_formatı,
               rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))

fig.update_xaxes(tickangle=-45)
st.plotly_chart(fig)