import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def mbbilanco():
    start="01-01-1985"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.AB.A01","TP.AB.A02","TP.AB.A08","TP.AB.A09","TP.AB.A10",
            "TP.AB.A15"]
    sütunad=["Tarih","Aktif","Dış Varlık","İç Varlık","Pasif",
             "Toplam Döviz Yükümlülükleri","MB Parası"]
    veri=evdsapi.get_data(kodlar,startdate=start,enddate=end,frequency=5)
    veri.columns=sütunad
    veri["İç Varlık/Dış Varlık"]=veri["İç Varlık"]/veri["Dış Varlık"]
    veri["İç Varlık/Aktif"]=veri["İç Varlık"]/veri["Aktif"]
    veri["Dış Varlık/Aktif"]=veri["Dış Varlık"]/veri["Aktif"]
    veri["Döviz Yükümlülüğü/Pasif"]=veri["Toplam Döviz Yükümlülükleri"]/veri["Pasif"]
    veri["MB Parası/Pasif"]=veri["MB Parası"]/veri["Pasif"]
    veri["Dış Varlık/Döviz Yükümlülüğü"]=veri["Dış Varlık"]/veri["Toplam Döviz Yükümlülükleri"]
    return veri

veri=mbbilanco()
st.dataframe(veri,hide_index=True,use_container_width=True)

fig=go.Figure()
fig.add_trace(go.Scatter(x=veri["Tarih"],y=veri["Aktif"],mode="lines",name="Aktif"))
fig.update_layout(title={"text":"MB Aktif Büyüklüğü","x":0.5,"xanchor":"center"},
                    xaxis_title="Tarih", yaxis_title="Aktif",
                    xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M6",
                               rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))
fig.update_xaxes(tickangle=-45)
st.plotly_chart(fig)


fig2=go.Figure()

fig2.add_trace(go.Scatter(x=veri["Tarih"],y=veri["İç Varlık/Dış Varlık"], mode="lines", name="İç Varlık/Dış Varlık"))
fig2.add_trace(go.Scatter(x=veri["Tarih"],y=veri["İç Varlık/Aktif"], mode="lines", name="İç Varlık/Aktif"))
fig2.add_trace(go.Scatter(x=veri["Tarih"],y=veri["Dış Varlık/Aktif"], mode="lines", name="Dış Varlık/Aktif"))
fig2.add_trace(go.Scatter(x=veri["Tarih"],y=veri["Döviz Yükümlülüğü/Pasif"], mode="lines", name="Döviz Yükümlülüğü/Pasif"))
fig2.add_trace(go.Scatter(x=veri["Tarih"],y=veri["MB Parası/Pasif"], mode="lines", name="MB Parası/Pasif"))
fig2.add_trace(go.Scatter(x=veri["Tarih"],y=veri["Dış Varlık/Döviz Yükümlülüğü"], mode="lines", name="Dış Varlık/Döviz Yükümlülüğü"))

fig2.update_layout(title={"text":"MB Bilanço Rasyoları","x":0.5,"xanchor":"center"},
                  xaxis_title="Tarih",yaxis_title="Oran",
                  xaxis=dict(tickformat="%m-%Y",tickmode="linear",dtick="M6",
                             rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))
fig2.update_xaxes(tickangle=-45)
st.plotly_chart(fig2)
