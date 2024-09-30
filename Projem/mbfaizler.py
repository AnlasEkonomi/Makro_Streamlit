import evds as ev
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

secenek=["O/N","GLP","1 Haftalık Repo","TLREF","Mevduat Faizleri (TL)","Kredi Faizleri (TL)"]
st.markdown('<p style="font-weight:bold; color:black;">Faiz Türünü Seçin:</p>',unsafe_allow_html=True)
faiz_secim=st.radio("",secenek,index=None,horizontal=True)

with open("evdsapi.txt","r") as dosya:
    api=dosya.read()

evdsapi=ev.evdsAPI(api)

def on():
    url="https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb+tr/main+menu/temel+faaliyetler/para+politikasi/merkez+bankasi+faiz+oranlari/faiz-oranlari"
    veri=pd.read_html(url)[0]
    veri.drop(veri.index[0],inplace=True)
    veri.columns=["Tarih","Borç Alma","Borç Verme"]
    veri["Tarih"]=veri["Tarih"].apply(lambda x: datetime.strptime(x,"%d.%m.%y"))
    veri2=pd.DataFrame(columns=veri.columns)
    veri2["Tarih"]=pd.date_range(veri["Tarih"].iloc[0],datetime.today()+pd.DateOffset(months=1),freq="ME")
    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri2["Tarih"]=veri2["Tarih"].dt.to_period("M")
    veri2=veri2.merge(veri,on="Tarih",how="left")
    veri2.drop(columns=["Borç Alma_x","Borç Verme_x"],inplace=True)
    veri2=veri2.ffill()
    veri2.columns=veri.columns
    veri2["Tarih"]=veri2["Tarih"].dt.strftime("%d-%m-%Y") 
    return veri2

def glp():
    url="https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/Gec+Likidite+Penceresi+%28LON%29"
    veri=pd.read_html(url)[0]
    veri.drop(veri.index[0],inplace=True)
    veri.columns=["Tarih","Borç Alma","Borç Verme"]
    veri["Tarih"]=veri["Tarih"].apply(lambda x: datetime.strptime(x,"%d.%m.%y"))
    veri2=pd.DataFrame(columns=veri.columns)
    veri2["Tarih"]=pd.date_range(veri["Tarih"].iloc[0],datetime.today()+pd.DateOffset(months=1),freq="ME")
    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri2["Tarih"]=veri2["Tarih"].dt.to_period("M")
    veri2=veri2.merge(veri,on='Tarih',how='left')
    veri2.drop(columns=["Borç Alma_x","Borç Verme_x"],inplace=True)
    veri2=veri2.ffill()
    veri2.columns=veri.columns
    veri2["Tarih"]=veri2["Tarih"].dt.strftime("%d-%m-%Y") 
    return veri2

def repo():
    url="https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/1+Hafta+Repo"
    veri=pd.read_html(url)[0]
    veri.drop(veri.index[0],inplace=True)
    veri.columns=["Tarih","Borç Alma","Borç Verme"]
    veri["Tarih"]=veri["Tarih"].apply(lambda x: datetime.strptime(x,"%d.%m.%Y"))
    veri2=pd.DataFrame(columns=veri.columns)
    veri2["Tarih"]=pd.date_range(veri["Tarih"].iloc[0],datetime.today()+pd.DateOffset(months=1),freq="ME")
    veri["Tarih"]=veri["Tarih"].dt.to_period("M")
    veri2["Tarih"]=veri2["Tarih"].dt.to_period("M")
    veri2=veri2.merge(veri,on="Tarih",how="left")
    veri2.drop(columns=["Borç Alma_x","Borç Verme_x"],inplace=True)
    veri2=veri2.ffill()
    veri2.columns=veri.columns
    veri2["Tarih"]=veri2["Tarih"].dt.strftime("%d-%m-%Y") 
    return veri2

def tlref():
    start="28-12-2018"
    end=datetime.today().strftime("%d-%m-%Y")
    veri=evdsapi.get_data(["TP.BISTTLREF.ORAN"],startdate=start,enddate=end).dropna()
    veri.columns=["Tarih","TLREF"]
    veri.dropna(axis=0,inplace=True)
    return veri

def mevfaiz():
    start="04-01-2002"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.TRY.MT01","TP.TRY.MT02","TP.TRY.MT03","TP.TRY.MT04","TP.TRY.MT05"]
    sütunad=["Tarih","1 Aya Kadar","3 Aya Kadar","6 Aya Kadar","1 Yıla Kadar","1 Yıl ve Üzeri"]
    veri=evdsapi.get_data(kodlar,startdate=start,enddate=end).drop(columns=["YEARWEEK"])
    veri.columns=sütunad
    veri.dropna(axis=0,inplace=True)
    return veri

def kredifaiz():
    start="04-01-2002"
    end=datetime.today().strftime("%d-%m-%Y")
    kodlar=["TP.KTF10","TP.KTF11","TP.KTF12","TP.KTF17","TP.KTFTUK"]
    sütunad=["Tarih","İhtiyaç","Taşıt","Konut","Ticari","Tüketici (İhtiyaç+Taşıt+Konut)"]
    veri=evdsapi.get_data(kodlar,startdate=start,enddate=end).drop(columns=["YEARWEEK"])
    veri.columns=sütunad
    veri.dropna(axis=0,inplace=True)
    return veri


veri_dict={
        "O/N":(on(),["Borç Alma","Borç Verme"],["red","blue"]),
        "GLP":(glp(),["Borç Alma","Borç Verme"],["red","blue"]),
        "1 Haftalık Repo":(repo(),["Borç Verme"],["red"]),
        "TLREF":(tlref(),["TLREF"],["red"]),
        "Mevduat Faizleri (TL)":(mevfaiz(),["1 Aya Kadar","3 Aya Kadar","6 Aya Kadar",
                                            "1 Yıla Kadar","1 Yıl ve Üzeri"], 
                                            ["red","blue","green","orange","purple"]),
        "Kredi Faizleri (TL)":(kredifaiz(),["İhtiyaç","Taşıt","Konut","Ticari", 
                                            "Tüketici (İhtiyaç+Taşıt+Konut)"],
                                            ["red","blue","green","orange","purple","black"])}

if faiz_secim in veri_dict:
        data,y_columns,colors=veri_dict[faiz_secim]
        st.markdown(f'<p style="font-weight:bold; color:black;">{faiz_secim} (%)</p>', unsafe_allow_html=True)
        st.dataframe(data,hide_index=True,width=1000)

        fig=go.Figure()
        for col,color in zip(y_columns,colors):
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(data["Tarih"],format="%d-%m-%Y"),y=data[col],
                mode="lines",
                name=col,
                line=dict(color=color)))

        fig.update_layout(
            title={"text": f"{faiz_secim} (%)", "x":0.5,"xanchor":"center"},
            xaxis_title="Tarih",yaxis_title="Faiz",
            xaxis=dict(tickformat="%d-%m-%Y", tickmode="linear",dtick="M3",
                       rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
        fig.update_xaxes(tickangle=-45,tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig)