from datetime import datetime
import cloudscraper
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def cds():
    bugün=datetime.today().strftime("%Y-%m-%d")
    scraper=cloudscraper.CloudScraper()
    url=f'https://api.investing.com/api/financialdata/historical/1096486?start-date=2008-02-01&end-date={bugün}&time-frame=Daily&add-missing-rows=false'
    
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://tr.investing.com",
        "Referer": "https://tr.investing.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Domain-ID": "tr"}

    veri=scraper.get(url,headers=headers).json()["data"]
    veri=[{"rowDate":item["rowDate"],"last_close":item["last_close"]} for item in veri]
    veri=pd.DataFrame(veri)
    veri.columns=["Tarih","CDS"]
    veri["Tarih"]=pd.to_datetime(veri["Tarih"],format='%d.%m.%Y')
    veri.sort_values(by="Tarih",ascending=True,inplace=True)
    veri["Tarih"]=veri["Tarih"].dt.strftime('%d-%m-%Y')
    veri["CDS"]=veri["CDS"].str.replace(',', '.').astype(float)
    veri["CDS Oynaklık"]=veri["CDS"].pct_change()
    veri.dropna(axis=0,inplace=True)
    return veri

veri=cds()
st.dataframe(veri,hide_index=True,use_container_width=True)

for col,color,title in [("CDS","Red","Türkiye CDS 5 Year"), 
                            ("CDS Oynaklık","Blue","Türkiye CDS 5 Year Oynaklık")]:
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=pd.to_datetime(veri["Tarih"],format="%d-%m-%Y"),y=veri[col],
        mode="lines",
        name=col,
        line=dict(color=color)))

    fig.update_layout(title={"text":title,"x":0.5,"xanchor":"center"},
                        xaxis_title="Tarih",yaxis_title=col,
                        xaxis=dict(tickformat="%d-%m-%Y",tickmode="linear",dtick="M2",
                                   rangeslider=dict(visible=True,bgcolor="white",bordercolor="black",borderwidth=2)))
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig)