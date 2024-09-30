import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def rezerv(frekans):
    start="01-01-2000"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.REZVARPD.K1","TP.REZVARPD.K2","TP.REZVARPD.K8","TP.REZVARPD.K9",
            "TP.REZVARPD.K10","TP.REZVARPD.K12"]
    sütunad=["Tarih","Toplam Rezerv","Döviz","IMF","SDR","Altın","Diğer"]
    
    if frekans=="Aylık":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end)
        veri.columns=sütunad
        veri.dropna(axis=0,inplace=True)
    elif frekans=="Yıllık":
        veri=evdsapi.get_data(kodlar,startdate=start,enddate=end,frequency=8)
        veri.columns=sütunad
    return veri

secenek=["Aylık","Yıllık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri=rezerv(secim)

st.markdown("<h4 style='font-size:20px;'>MB Rezervler</h4>",unsafe_allow_html=True)
st.dataframe(veri,hide_index=True,use_container_width=True)

tarih_formatı="%m-%Y" if secim=="Aylık" else "%Y"
dtick="M5" if secim=="Aylık" else "M12"

veri["Tarih"]=pd.to_datetime(veri["Tarih"],dayfirst=True,errors="coerce")

fig=go.Figure()

for sütun in veri.columns[1:]: 
    fig.add_trace(go.Scatter(x=veri["Tarih"],y=veri[sütun],mode="lines",name=sütun))

fig.update_layout(title="Rezervler",xaxis_title="Tarih",yaxis_title="Milyon ABD $",
                  xaxis=dict(tickformat=tarih_formatı,dtick=dtick,
                             rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))

fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))

fig.update_xaxes(tickangle=-45)
st.plotly_chart(fig,use_container_width=True)

