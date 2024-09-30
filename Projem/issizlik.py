import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)


def issizlik(tür):
    start="01-01-2014"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar1=["TP.YISGUCU2.G1","TP.YISGUCU2.G2","TP.YISGUCU2.G3","TP.YISGUCU2.G4","TP.YISGUCU2.G5",
             "TP.YISGUCU2.G6","TP.YISGUCU2.G7","TP.YISGUCU2.G8"]
    kodlar2=["TP.TIG01","TP.TIG02","TP.TIG03","TP.TIG04","TP.TIG05","TP.TIG06","TP.TIG07",
             "TP.TIG08"]
    sütunad=["Tarih","Nüfus","İş Gücü","İstihdam","İşsiz","İş Gücüne Dahil Olmayan",
             "İş Gücüne Katılım (%)","İstihdam (%)","İşsizlik (%)"]
    
    if tür=="Mevsimsellikten Arındırılmamış İş Gücü 15+ Nüfus":
        veri=evdsapi.get_data(kodlar1,startdate=start,enddate=end)
        veri.columns=sütunad
        veri["İş Gücüne Katılım (%)"]=veri["İş Gücüne Katılım (%)"].apply(lambda x: f"{x :.2f}%")
        veri["İstihdam (%)"]=veri["İstihdam (%)"].apply(lambda x: f"{x :.2f}%")
        veri["İşsizlik (%)"]=veri["İşsizlik (%)"].apply(lambda x: f"{x :.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y-%m").dt.strftime("%m-%Y")
    
    if tür=="Mevsimsellikten Arındırılmış İş Gücü 15+ Nüfus":
        veri=evdsapi.get_data(kodlar2,startdate=start,enddate=end)
        veri.columns=sütunad
        veri["İş Gücüne Katılım (%)"]=veri["İş Gücüne Katılım (%)"].apply(lambda x: f"{x :.2f}%")
        veri["İstihdam (%)"]=veri["İstihdam (%)"].apply(lambda x: f"{x :.2f}%")
        veri["İşsizlik (%)"]=veri["İşsizlik (%)"].apply(lambda x: f"{x :.2f}%")
        veri["Tarih"]=pd.to_datetime(veri["Tarih"],format="%Y-%m").dt.strftime("%m-%Y")
    return veri

secenek=["Mevsimsellikten Arındırılmamış İş Gücü 15+ Nüfus",
             "Mevsimsellikten Arındırılmış İş Gücü 15+ Nüfus"]
st.markdown('<p style="font-weight:bold; color:black;">Veri Türü Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=issizlik(secim)

st.markdown("<h4 style='font-size:20px;'>İşsizlik Verileri</h4>",unsafe_allow_html=True)
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
    xaxis=dict(tickformat="%Y-%m",tickmode="linear",
               rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)),
    yaxis=dict(tickformat="d"))
    
    fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
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
    xaxis=dict(tickformat="%Y-%m",tickmode="linear",
               rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)),
    yaxis=dict(tickformat="d"))
    
    fig2.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
    fig2.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
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
    xaxis=dict(tickformat="%Y-%m",tickmode="linear",
               rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)),
    yaxis=dict(tickformat="d"))
    
    fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
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
    xaxis=dict(tickformat="%Y-%m",tickmode="linear",
               rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)),
    yaxis=dict(tickformat="d"))
    
    fig2.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
    fig2.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig2.update_xaxes(tickangle=-45)

    st.plotly_chart(fig)
    st.plotly_chart(fig2)