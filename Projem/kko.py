import evds as ev
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

kko=evdsapi.get_series("bie_kko2")
kko.drop(columns=["START_DATE"],inplace=True)

def ikko(frekans):
    start="01-01-2007"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=kko["SERIE_CODE"].to_list()
    sütunad=kko["SERIE_NAME"].to_list()

    if frekans=="Aylık":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
        veri.columns=["Tarih"]+sütunad
        return veri

    elif frekans=="Yıllık":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end,frequency=8)
        veri.columns=["Tarih"]+sütunad
        return veri

secenek=["Aylık","Yıllık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)

veri=ikko(secim)
st.markdown("<h4 style='font-size:20px;'>İmalat Sanayi Kapasite Kullanım Oranı (%)</h4>",unsafe_allow_html=True)
st.dataframe(veri,hide_index=True,use_container_width=True)

ilk="İmalat Sanayi Kapasite Kullanım Oranı"
secim=st.multiselect(
    "Grafikte göstermek istediğiniz sütunları seçin:", 
    veri.columns[1:], 
    default=[ilk] if ilk in veri.columns else None)

if secim:
    fig=go.Figure()

    for i,column in enumerate(secim):
        fig.add_trace(go.Scatter(
            x=veri["Tarih"],y=veri[column],mode="lines",name=column))

    fig.update_xaxes(range=[veri["Tarih"].min(),veri["Tarih"].max()])

    if "Yıllık" in secim:
        fig.update_xaxes(dtick="M12",tickformat="%Y")
    else:
        fig.update_xaxes(dtick="M3",tickformat="%m-%Y")

    fig.update_layout(
        title="İmalat Sanayi Kapasite Kullanım Oranı (%)",
        xaxis_title="Tarih",yaxis_title="",
        xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))

    fig.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig)
else:
    st.warning("Lütfen grafikte göstermek için en az veri seçin.")

