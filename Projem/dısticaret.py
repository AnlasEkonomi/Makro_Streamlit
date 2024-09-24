import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def dısticaret(frekans):
    start="01-01-2013"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlarihracat=["TP.IHRACATBEC.9999","TP.IHRACATBEC.1","TP.IHRACATBEC.2","TP.IHRACATBEC.3",
            "TP.IHRACATBEC.4"]
    kodlarithalat=["TP.ITHALATBEC.9999","TP.ITHALATBEC.1","TP.ITHALATBEC.2","TP.ITHALATBEC.3",
            "TP.ITHALATBEC.4"]
    sütunad=["Tarih","Toplam","Yatırım Malları","Ara Mallar","Tüketim Malları","Diğer"]

    if frekans=="Aylık":
        veri1=evdsapi.get_data(kodlarihracat,startdate=start,enddate=end)
        veri2=evdsapi.get_data(kodlarithalat,startdate=start,enddate=end)
    elif frekans=="Yıllık":
        veri1=evdsapi.get_data(kodlarihracat,startdate=start,enddate=end,frequency=8)
        veri2=evdsapi.get_data(kodlarithalat,startdate=start,enddate=end,frequency=8)
    
    veri1.columns=sütunad
    veri2.columns=sütunad
   
    for column in sütunad[1:]:
        if column !="Toplam":
            veri1[f"{column} Oranı (%)"]=(veri1[column]/veri1["Toplam"]).map(lambda x: f"{x:.2%}")
            veri2[f"{column} Oranı (%)"]=(veri2[column]/veri2["Toplam"]).map(lambda x: f"{x:.2%}")
    
    veri3=pd.DataFrame(columns=["Tarih","İhracat","İthalat","Dış Ticaret Hacmi",
                                "Dış Ticaret Dengesi","İhracatın İthalatı Karşılama Oranı"])
    veri3["Tarih"]=veri1["Tarih"]
    veri3["İhracat"]=veri1["Toplam"]
    veri3["İthalat"]=veri2["Toplam"]
    veri3["Dış Ticaret Hacmi"]=veri3["İhracat"]+veri3["İthalat"]
    veri3["Dış Ticaret Dengesi"]=veri3["İhracat"]-veri3["İthalat"]
    veri3["İhracatın İthalatı Karşılama Oranı"]=(veri3["İhracat"]/veri3["İthalat"]).map(lambda x: f"{x:.2%}")
    
    return veri1,veri2,veri3

secenek=["Aylık","Yıllık"]
st.markdown('<p style="font-weight:bold; color:black;">Dönem Seçiniz:</p>',unsafe_allow_html=True)
secim=st.radio("",secenek,index=0,horizontal=True)
veri1,veri2,veri3=dısticaret(secim)

st.subheader("İhracat Verileri")
st.dataframe(veri1,hide_index=True,use_container_width=True)

st.subheader("İthalat Verileri")
st.dataframe(veri2,hide_index=True,use_container_width=True)

st.subheader("Dış Ticaret Dengesi")
st.dataframe(veri3,hide_index=True,use_container_width=True)

fig_total=go.Figure()
fig_total.add_trace(go.Scatter(x=veri1["Tarih"],y=veri1["Toplam"], 
                               mode="lines",name="İhracat", 
                               line=dict(color="red",width=2)))
fig_total.add_trace(go.Scatter(x=veri2["Tarih"],y=veri2["Toplam"], 
                               mode="lines",name="İthalat", 
                               line=dict(color="green",width=2)))
fig_total.add_trace(go.Bar(x=veri3["Tarih"],y=veri3["Dış Ticaret Dengesi"], 
                           name="Dış Ticaret Dengesi", 
                           marker=dict(color="blue",opacity=0.8)))

max_eks=max(veri1["Toplam"].max(),veri2["Toplam"].max())
min_eks=min(veri3["Dış Ticaret Dengesi"].min(), -5000000)

fig_total.update_layout(
    title=f"Dış Ticaret Dengesi ({secim})",
    xaxis=dict(showgrid=False,tickangle=-45,
               rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)),
    yaxis=dict(title="Değer",range=[min_eks,max_eks],zeroline=True,zerolinewidth=2,zerolinecolor="gray"),
    barmode="overlay",
    showlegend=True)

if "Yıllık" in secim:
    fig_total.update_xaxes(dtick="M12",tickformat="%Y")
else:
    fig_total.update_xaxes(dtick="M3",tickformat="%m-%Y")

st.plotly_chart(fig_total,use_container_width=True)


fig_total2=go.Figure()

veri3["İhracatın İthalatı Karşılama Oranı"]=(veri3["İhracatın İthalatı Karşılama Oranı"]
    .str.replace("%", "")
    .astype(float)/100)

veri3["Dış Ticaret Hacmi"]=veri3["Dış Ticaret Hacmi"].astype(float)

fig_total2.add_trace(go.Bar(
    x=veri3["Tarih"],y=veri3["Dış Ticaret Hacmi"],name="Dış Ticaret Hacmi", 
    marker=dict(color="green")))

fig_total2.add_trace(go.Scatter(
    x=veri3["Tarih"],y=veri3["İhracatın İthalatı Karşılama Oranı"], 
    mode="lines",name="İhracatın İthalatı Karşılama Oranı", 
    line=dict(color="blue",width=2),yaxis="y2"))

fig_total2.update_layout(
    title=f"Hacim ve Karşılama Oranı ({secim})",
    xaxis=dict(showgrid=False,tickangle=-45,
               rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)),
    yaxis=dict(title="Dış Ticaret Hacmi",zeroline=True,zerolinewidth=2,zerolinecolor="gray"),
    yaxis2=dict(title="İhracatın İthalatı Karşılama Oranı",overlaying='y',side='right'),
    showlegend=True)

if "Yıllık" in secim:
    fig_total2.update_xaxes(dtick="M12", tickformat="%Y")
else:
    fig_total2.update_xaxes(dtick="M3", tickformat="%m-%Y")

st.plotly_chart(fig_total2, use_container_width=True)


renkler=["blue","black","green","red","purple"]

fig_ihracat=go.Figure()
for i, column in enumerate(veri1.columns):
    if "Oranı (%)" in column:
        fig_ihracat.add_trace(go.Bar(x=veri1["Tarih"],y=veri1[column],name=column,marker_color=renkler[i % len(renkler)]))

fig_ihracat.update_layout(title=f"İhracat Oranları ({secim})",xaxis_title="Tarih",yaxis_title="Oran (%)",xaxis_tickangle=-45,
                          xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))
if "Yıllık" in secim:
    fig_ihracat.update_xaxes(dtick="M12",tickformat="%Y")
else:
    fig_ihracat.update_xaxes(dtick="M3",tickformat="%m-%Y")

st.plotly_chart(fig_ihracat,use_container_width=True)

fig_ithalat=go.Figure()
for i, column in enumerate(veri2.columns):
    if "Oranı (%)" in column:
        fig_ithalat.add_trace(go.Bar(x=veri2["Tarih"],y=veri2[column],name=column,marker_color=renkler[i % len(renkler)]))

fig_ithalat.update_layout(title=f"İthalat Oranları ({secim})",xaxis_title="Tarih",yaxis_title="Oran (%)",xaxis_tickangle=-45,
                          xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))
if "Yıllık" in secim:
    fig_ithalat.update_xaxes(dtick="M12",tickformat="%Y")
else:
    fig_ithalat.update_xaxes(dtick="M3",tickformat="%m-%Y")

st.plotly_chart(fig_ithalat,use_container_width=True)