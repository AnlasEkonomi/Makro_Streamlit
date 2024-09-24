import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)


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

secenek=["Aylık","Yıllık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=altın(secim)
st.dataframe(veri,hide_index=True,use_container_width=True)

tarih_formatı="%m-%Y" if secim=="Aylık" else "%Y"
dtick="M5" if secim=="Aylık" else "M12"

fig1=go.Figure()
fig1.add_trace(go.Scatter(
    x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),
    y=veri["Ons Altın ($)"],mode="lines",name="Ons Altın ($)",
    line=dict(color="Red")))
fig1.update_layout(title={"text":"Ons Altın ($)","x": 0.5,"xanchor":"center"},
                    xaxis_title="Tarih", yaxis_title="Fiyat",
                    xaxis=dict(tickformat=tarih_formatı,tickmode="linear",dtick=dtick,
                               rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
fig1.update_xaxes(tickangle=-45)

fig2=go.Figure()
fig2.add_trace(go.Scatter(
    x=pd.to_datetime(veri["Tarih"], format=tarih_formatı),
    y=veri["Gram Altın (TL)"],mode="lines",name="Gram Altın (TL)",
    line=dict(color="Red")))
fig2.update_layout(title={"text":"Gram Altın (TL)","x": 0.5,"xanchor":"center"},
                    xaxis_title="Tarih", yaxis_title="Fiyat",
                    xaxis=dict(tickformat=tarih_formatı, tickmode="linear",dtick=dtick,
                               rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
fig2.update_xaxes(tickangle=-45)

if secim=="Aylık":
    fig3=go.Figure()
    fig3.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"], format=tarih_formatı),
        y=veri["Ons Getiri Nominal (%)"],name="Getiri",marker=dict(color="Blue")))
    fig3.update_layout(title={"text":"Ons Altın Getiri Nominal (%)","x": 0.5,"xanchor":"center"},
                        xaxis_title="Tarih", yaxis_title="Getiri",
                        xaxis=dict(tickformat=tarih_formatı,tickmode="linear",dtick=dtick,
                                   rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))
    fig3.update_xaxes(tickangle=-45)

    fig4=go.Figure()
    fig4.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"],format=tarih_formatı),
        y=veri["Gram Getiri Nominal (%)"],name="Getiri",marker=dict(color="Blue")))
    fig4.update_layout(title={"text":"Gram Altın Getiri Nominal (%)","x":0.5,"xanchor":"center"},
                        xaxis_title="Tarih", yaxis_title="Getiri",
                        xaxis=dict(tickformat=tarih_formatı,tickmode="linear",dtick=dtick,
                                   rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))
    fig4.update_xaxes(tickangle=-45)

    st.plotly_chart(fig1)
    st.plotly_chart(fig3)
    st.plotly_chart(fig2)
    st.plotly_chart(fig4)

else:
    fig3=go.Figure()
    fig3.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"], format="%Y"),
        y=veri["Gram Getiri Nominal (%)"],name="Nominal Getiri",marker_color="Red"))
    fig3.add_trace(go.Bar(
        x=pd.to_datetime(veri["Tarih"], format="%Y"),
        y=veri["Gram Getiri Reel (%)"],name="Reel Getiri",marker_color="Blue"))
    fig3.update_layout(title={"text": "Gram Altın Getiri Nominal ve Reel (%)", "x": 0.5, "xanchor": "center"},
                        xaxis_title="Tarih", yaxis_title="Getiri",
                        xaxis=dict(tickformat="%Y",tickmode="linear",dtick="M12",
                                   rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)),
                        barmode="group")
    fig3.update_xaxes(tickangle=-45)

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)