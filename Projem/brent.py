import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

def brent(frekans):
    sütunad=["Tarih","Brent"]
    if frekans=="Günlük":
        veri=pd.DataFrame(yf.download(["BZ=F"],start="2008-01-01"))["Adj Close"].dropna().reset_index()
        veri.columns=sütunad
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y").dt.strftime("%d-%m-%Y")
    elif frekans=="Aylık":
        veri=pd.DataFrame(yf.download(["BZ=F"],start="2008-01-01",interval="1mo"))["Adj Close"].dropna().reset_index()
        veri.columns=sütunad
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y").dt.strftime("%m-%Y")
    return veri

secenek=["Günlük","Aylık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=brent(secim)
st.dataframe(veri,hide_index=True,use_container_width=True)

fig=go.Figure()
fig.add_trace(go.Scatter(x=veri["Tarih"],y=veri["Brent"],mode="lines",
                         name="Brent",line=dict(color="red")))

fig.update_layout(title=f"Brent Petrol Fiyatları $ ({secim})",
                  xaxis_title="Tarih",
                  yaxis_title="Fiyat ($)",
                  xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)),
                  showlegend=True)
fig.update_xaxes(tickangle=-45)

st.plotly_chart(fig,use_container_width=True)
