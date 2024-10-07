import requests
import pandas as pd
from io import StringIO
import streamlit as st
import locale
import plotly.graph_objects as go
import numpy as np

def ilduzey():
    url="https://cip.tuik.gov.tr/assets/geometri/nuts3.json"
    veri=requests.get(url).json()
    veri=veri["features"]

    iller=[]
    for i in veri:
        properties=i["properties"]
        iller.append(properties)

    veri=pd.DataFrame(iller)
    veri.drop(columns=["name","bolgeKodu","nutsKodu"],inplace=True)
    return veri


def cinsiyetnufus(il):
    url="https://nip.tuik.gov.tr/Home/GetInformation"

    yuk={"status":"1",
        "name":"CinsiyeteGoreNufus",
        "value":str(il)}
    
    req=requests.get(url,data=yuk)
    html=StringIO(req.text)
    veri=pd.read_html(html,decimal=",",thousands=".")[0]
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    veri.sort_values(by="Yıl",inplace=True)
    veri.drop(columns=["Düzey"],inplace=True)
    return veri

def yasnufus(yıl):
    url="https://nip.tuik.gov.tr/Home/GetInformation"

    yuk={"status":"1",
        "name":"YasGrubunaGoreNufus",
        "value":str(yıl)}
    req=requests.get(url,data=yuk)
    html=StringIO(req.text)
    veri=pd.read_html(html,decimal=",",thousands=".")[0]
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    yılliste=list(veri["Yıl"].unique())
    return veri,yılliste

def nufusartıshızı(il):
    url="https://nip.tuik.gov.tr/Home/GetInformation"

    yuk={"status":"1",
        "name":"NufusArtisHizi",
        "value":str(il)}
    req=requests.get(url,data=yuk)
    html=StringIO(req.text)
    veri=pd.read_html(html,decimal=",",thousands=".")[0],
    veri=np.array(veri)
    veri=veri.reshape(-1,veri.shape[-1])
    veri=pd.DataFrame(veri,columns=["Yıl","Düzey","Nüfus Artış Hızı (‰)"])
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    veri.sort_values(by="Yıl",inplace=True)
    veri.drop(columns=["Düzey"],inplace=True)
    return veri

def yabancınufus(il):
    url="https://nip.tuik.gov.tr/Home/GetInformation"

    yuk={"status":"1",
        "name":"YabanciNufusBuyuklugu",
        "value":str(il)}
    req=requests.get(url,data=yuk)
    html=StringIO(req.text)
    veri=pd.read_html(html,decimal=",",thousands=".")[0]
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    veri.sort_values(by="Yıl",inplace=True)
    veri.drop(columns=["Düzey"],inplace=True)
    return veri

def tabyabancınufus():
    url="https://nip.tuik.gov.tr/Home/TabiyetineYabanciNufusForTable?"

    yuk = {
        "draw": 1,
        "start": 0,
        "length": 10000,
        "search[regex]": "false",
        "ilAdi": "TÜRKİYE",
        "yabanciUlkeAdi": "Hepsi"}
    req=requests.post(url,data=yuk).json()["data"]
    veri=pd.DataFrame(req)
    veri.drop(columns=["IlKayitNo","IlAdi","YabanciUlkeKodu","Id","CreatedDate","CreatedUserId",
                    "IsUpdated","UpdatedDate","UpdatedUserId","IsDeleted"],inplace=True)
    veri.columns=["Yıl","Ülke","Toplam"]
    veri=veri.pivot_table(index="Yıl",columns="Ülke",values="Toplam",aggfunc="sum",fill_value=0)
    veri.reset_index(inplace=True)
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    veri.sort_values(by="Yıl",inplace=True)
    veri.columns=veri.columns.str.capitalize()
    veri["Toplam"]=veri.iloc[:, 1:].sum(axis=1)
    return veri

def dogyernufus(ikamet,dogyer):
    url="https://nip.tuik.gov.tr/Home/DogumYeriNufusForTable?"

    yuk = {
    "draw": 1,
    "start": 0,
    "length": 10000,
    "search[regex]": "false",
    "ilAdi": ikamet,
    "dogumYeriAd": dogyer}
    
    req=requests.post(url,data=yuk).json()["data"]
    veri=pd.DataFrame(req)
    veri=veri[["Yil","IlAdi","DogumYeriAd","Toplam","Erkek","Kadin"]]
    veri.columns=["Yıl","İkamet İl","Doğum Yeri","Toplam","Erkek","Kadın"]
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    veri.sort_values(by="Yıl",inplace=True)
    veri.columns=veri.columns.str.capitalize()
    return veri

def dogyeriyabancunufus():
    url="https://nip.tuik.gov.tr/Home/GetInformation"

    yuk={"status":"1",
        "name":"YurtdisiDogumluNufus",
        "value":"Hepsi"}
    req=requests.get(url,data=yuk)
    html=StringIO(req.text)
    veri=pd.read_html(html,decimal=",",thousands=".")[0]
    veri.drop(columns=["Erkek","Kadın"],inplace=True)
    veri=veri.pivot_table(index="Yıl",columns="Doğum Yeri",values="Toplam",aggfunc="sum",fill_value=0)
    veri.reset_index(inplace=True)
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    veri.sort_values(by="Yıl",inplace=True)
    
    return veri

def egitim(il):
    url="https://nip.tuik.gov.tr/Home/EgitimDurumForTable?"

    yuk={"draw": 1,
    "start": 0,
    "length": 20000,
    "search[regex]": "false",
    "ilAdi": str(il)}

    req=requests.post(url,data=yuk).json()["data"]
    veri=pd.DataFrame(req)
    veri.drop(columns=["IlKodu","Id","CreatedDate","CreatedUserId","IsUpdated",
                   "UpdatedDate","UpdatedUserId","IsDeleted"],inplace=True)
    veri.columns=["Yıl","İl","Eğitim Durumu (6+ Yaş)","Toplam","Erkek","Kadın",
              "Erkek Oran","Kadın Oran"]
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    veri.sort_values(by="Yıl",inplace=True)
    yılliste=list(veri["Yıl"].unique())
    return veri, yılliste

def medenidurum(il):
    url="https://nip.tuik.gov.tr/Home/GetInformation"

    yuk={"status":"1",
        "name":"MedeniDurum",
        "value":str(il)}
    
    req=requests.post(url,data=yuk)
    html=StringIO(req.text)
    veri=pd.read_html(html,decimal=",",thousands=".")[0]
    veri["Yıl"]=veri["Yıl"].astype(int).apply(lambda x: f"{x:,}".replace(",", ""))
    veri.sort_values(by="Yıl",inplace=True)
    yılliste=list(veri["Yıl"].unique())
    return veri,yılliste


iller=list(ilduzey()["ad"])
locale.setlocale(locale.LC_COLLATE,"tr_TR.UTF-8")
iller=sorted(iller,key=locale.strxfrm)
indeks=iller.index("KAYSERI")
iller[indeks]="KAYSERİ"
iller.insert(0,"TÜRKİYE")
iller2=iller.copy()
iller2.remove("TÜRKİYE")
iller2.append("BILINMEYEN")
iller3=iller.copy()
iller3.remove("TÜRKİYE")
iller3.insert(0,"Hepsi")



st.markdown("<h4 style='font-size:20px;'>Nüfus Verileri</h4>",unsafe_allow_html=True)

with st.expander("Cinsiyete Göre Nüfus"):
    secim=st.selectbox(label="İl Seçiniz:",options=iller,key="cinsiyetnufus")
    veri=cinsiyetnufus(secim)
    st.dataframe(veri,hide_index=True,use_container_width=True)
    
    bar_trace=go.Bar(
    x=veri["Yıl"],y=veri["Toplam Nüfus"],name='Toplam Nüfus',marker=dict(color='lightblue'))

    erkek=go.Scatter(x=veri["Yıl"],y=veri["Erkek Nüfus"],name="Erkek Nüfusu",
        mode="lines+markers",marker=dict(color="blue"))
    kadın=go.Scatter(x=veri["Yıl"],y=veri["Kadın Nüfus"],name="Kadın Nüfusu",
        mode="lines+markers",marker=dict(color="red"))
    fig=go.Figure(data=[bar_trace,erkek,kadın])
    fig.update_layout(
        title=f"Yıllara Göre Nüfus ({str(secim).capitalize()})",xaxis_title='Yıllar',
        yaxis_title="Nüfus",barmode="group")
    fig.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig)

with st.expander("Yaş Grubuna Göre Nüfus"):
    yıllar=yasnufus("0")[1]
    secim=st.selectbox(label="Yıl Seçiniz:",options=yıllar,key="yasnufus")
    veri2=yasnufus(secim)[0]
    st.dataframe(veri2,hide_index=True,use_container_width=True)
    
    fig=go.Figure()
    fig.add_trace(go.Bar(y=veri2["Yaş Grubu"].iloc[1:-1],x=veri2["Erkek"].iloc[1:-1]*-1,
        name="Erkek",orientation="h",marker=dict(color="#87CEFA")))

    fig.add_trace(go.Bar(y=veri2["Yaş Grubu"].iloc[1:-1],x=veri2["Kadın"].iloc[1:-1],
        name="Kadın",orientation="h",marker=dict(color="pink")))
    
    fig.update_layout(template="plotly_white",title=f"Nüfus Piramidi ({secim})",
        barmode="relative",bargap=0.0,bargroupgap=0)
    
    fig.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_xaxes(tickangle=-45) 
    st.plotly_chart(fig)

with st.expander("Nüfus Artış Hızı"):
    secim=st.selectbox(label="İl Seçiniz:",options=iller,key="nufusartıshızı")
    veri3=nufusartıshızı(secim)
    st.dataframe(veri3,hide_index=True,use_container_width=True)

    fig=go.Figure()

    fig.add_trace(go.Scatter(x=veri3["Yıl"],y=veri3["Nüfus Artış Hızı (‰)"],
    mode="lines+markers",name="Nüfus Artış Hızı",line=dict(color='red')))

    fig.update_layout(title=f"Nüfus Artış Hızı (‰) ({str(secim).capitalize()})",
        xaxis_title="Yıl",yaxis_title="Nüfus Artış Hızı (‰)",
        template="plotly_dark")
    
    fig.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig)

with st.expander("Yabancı Nüfus"):
    secenek=["Cinsiyete Göre Nüfus","Vatandaşlığa Göre Nüfus"]
    st.markdown('<p style="font-weight:bold; color:black;">Tür Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)

    if secim=="Cinsiyete Göre Nüfus":
        secim=st.selectbox(label="İl Seçiniz:",options=iller,key="yabancınufus")
        veri4=yabancınufus(secim)
        st.dataframe(veri4,hide_index=True,use_container_width=True)

        fig=go.Figure()

        fig.add_trace(go.Bar(x=veri4["Yıl"],y=veri4["Erkek"],name="Erkek",
                            marker_color="blue"))

        fig.add_trace(go.Bar(x=veri4["Yıl"],y=veri4["Kadın"],name="Kadın",
            marker_color="pink"))
        
        fig.add_trace(go.Scatter(x=veri4["Yıl"],y=veri4["Toplam"],name="Toplam",
        mode="lines+markers",line=dict(color="green",width=3),marker=dict(size=8)))

        fig.update_layout(title=f"Yabancı Nüfus Sayısı ({str(secim).capitalize()})",
            xaxis_title="Tarih",yaxis_title="Nüfus",barmode="stack",template="plotly_white")
        
        fig.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_xaxes(tickangle=-45)

        st.plotly_chart(fig)
    
    elif secim=="Vatandaşlığa Göre Nüfus":
        veri5=tabyabancınufus()
        st.dataframe(veri5,hide_index=True,use_container_width=True)
        
        ilk="Toplam"
        secim=st.multiselect(
    "Grafikte göstermek istediğiniz sütunları seçin:", 
        veri5.columns[1:], 
        default=[ilk] if ilk in veri5.columns else None)

        if secim:
            fig=go.Figure()
            for i,column in enumerate(secim):
                fig.add_trace(go.Scatter(
                    x=veri5["Yıl"],y=veri5[column],mode="lines",name=column))

            fig.update_layout(
                title="Nüfus",
                xaxis_title="Tarih",yaxis_title="",
                xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))

            fig.update_xaxes(dtick="M12",tickformat="%Y",tickfont=dict(color="black",size=8,family="Arial Black"))
            fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
            fig.update_xaxes(tickangle=-45)

            st.plotly_chart(fig)
        else:
            st.warning("Lütfen grafikte göstermek için en az veri seçin.")

with st.expander("Doğum Yeri ve İkametine Göre Nüfus"):
    secenek=["Yurtiçi","Yurtdışı"]
    st.markdown('<p style="font-weight:bold; color:black;">Tür Seçiniz:</p>',unsafe_allow_html=True)
    secim=st.radio("",secenek,index=0,horizontal=True)

    if secim=="Yurtiçi":
        secim=st.selectbox(label="İkamet İli Seçiniz:",options=iller2,key="dogyernufus1")
        secim2=st.selectbox(label="Doğum İli Seçiniz:",options=iller2,key="dogyernufus2")
        veri6=dogyernufus(str(secim),str(secim2))
        st.dataframe(veri6,hide_index=True,use_container_width=True)

        fig=go.Figure()

        fig.add_trace(go.Bar(x=veri6["Yıl"],y=veri6["Erkek"],name="Erkek",
                            marker_color="blue"))

        fig.add_trace(go.Bar(x=veri6["Yıl"],y=veri6["Kadın"],name="Kadın",
            marker_color="pink"))
        
        fig.add_trace(go.Scatter(x=veri6["Yıl"],y=veri6["Toplam"],name="Toplam",
        mode="lines+markers",line=dict(color="green",width=3),marker=dict(size=8)))

        fig.update_layout(title=f"İkamet Yeri: {str(secim).capitalize()}    Doğum Yeri: {str(secim2).capitalize()}",
            xaxis_title="Tarih",yaxis_title="Nüfus",barmode="stack",template="plotly_white")
        
        fig.update_xaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
        fig.update_xaxes(tickangle=-45)

        st.plotly_chart(fig)
    
    if secim=="Yurtdışı":
        veri7=dogyeriyabancunufus()
        st.dataframe(veri7,hide_index=True,use_container_width=True)

        ilk="AFGANİSTAN"
        secim=st.multiselect(
    "Grafikte göstermek istediğiniz sütunları seçin:", 
        veri7.columns[1:], 
        default=[ilk] if ilk in veri7.columns else None)

        if secim:
            fig=go.Figure()
            for i,column in enumerate(secim):
                fig.add_trace(go.Scatter(
                    x=veri7["Yıl"],y=veri7[column],mode="lines",name=column))

            fig.update_layout(
                title="Nüfus",
                xaxis_title="Tarih",yaxis_title="",
                xaxis=dict(rangeslider=dict(visible=True,bgcolor="white",bordercolor="red",borderwidth=2)))

            fig.update_xaxes(dtick="M12",tickformat="%Y",tickfont=dict(color="black",size=8,family="Arial Black"))
            fig.update_yaxes(tickfont=dict(color="black",size=8,family="Arial Black"))
            fig.update_xaxes(tickangle=-45)

            st.plotly_chart(fig)
        else:
            st.warning("Lütfen grafikte göstermek için en az veri seçin.")

st.markdown("<h4 style='font-size:20px;'>Eğitim ve Medeni Durum Verileri</h4>",unsafe_allow_html=True)

with st.expander("Eğitim Durum"):
    secim=st.selectbox(label="İl Seçiniz:",options=iller3,key="egitim")
    veri8=egitim(str(secim))[0]
    veri8yıl=egitim(str(secim))[1]
    secim2=st.selectbox(label="Yıl Seçiniz:",options=veri8yıl,key="egitimyıl")
    veri8filtre=veri8[veri8["Yıl"]==secim2]
    st.dataframe(veri8filtre,hide_index=True,use_container_width=True)

    fig=go.Figure()
    veri8filtre=veri8filtre[veri8filtre["Eğitim Durumu (6+ Yaş)"] !="TOPLAM"]


    fig.add_trace(go.Pie(
        labels=veri8filtre["Eğitim Durumu (6+ Yaş)"],values=veri8filtre["Toplam"],
        title=f"Eğitim Durumuna Göre Toplam ({str(secim).capitalize()})",domain=dict(x=[0,1],y=[0,1]),name="Toplam",
        hoverinfo="label+value",textinfo="none"))

    fig.add_trace(go.Pie(
        labels=veri8filtre["Eğitim Durumu (6+ Yaş)"],values=veri8filtre["Erkek"],
        title=f"Eğitim Durumuna Göre Erkek ({str(secim).capitalize()})",domain=dict(x=[0,1],y=[0,1]),
        visible=False,hoverinfo="label+value",textinfo="none"))

    fig.add_trace(go.Pie(
        labels=veri8filtre["Eğitim Durumu (6+ Yaş)"],values=veri8filtre["Kadın"],
        title=f"Eğitim Durumuna Göre Kadın Dağılım ({str(secim).capitalize()})",domain=dict(x=[0,1],y=[0,1]),
        visible=False,name="Kadın",hoverinfo="label+value",textinfo="none"))

    fig.update_layout(
        updatemenus=[
            dict(type="buttons",direction="down",
                buttons=list([
                    dict(args=[{"visible":[True,False,False]}],
                        label="Toplam",method="update"),
                    dict(args=[{"visible":[False,True,False]}],
                        label="Erkek",method="update"),
                    dict(args=[{"visible":[False,False,True]}],
                        label="Kadın",method="update")]),
                showactive=True,x=0.17,y=1.2)])
    st.plotly_chart(fig)

with st.expander("Medeni Durum"):
    secim=st.selectbox(label="İl Seçiniz:",options=iller3,key="medeni")
    veri9=medenidurum(str(secim))[0]
    veri9yıl=medenidurum(str(secim))[1]
    st.dataframe(veri9,hide_index=True,use_container_width=True)
    
    secim2=st.selectbox(label="Yıl Seçiniz:",options=veri8yıl,key="medeniyıl")
    secim3=st.selectbox(label="Cinsiyet Seçiniz:",options=["Toplam","Erkek","Kadın"],key="medeniyılcins")
    veri9filtre=veri9[veri9["Yıl"]==secim2]
    
    if secim3=="Toplam":
        sütun=["Hiç Evlenmedi Toplam","Evli Toplam","Boşandı Toplam",
               "Eşi Öldü Toplam","Bilinmeyen Toplam"]
        
        values=veri9filtre[sütun].sum().values
        fig=go.Figure(data=[go.Pie(labels=sütun,values=values,hoverinfo="label+value",
                                   textinfo="none")])
    
        fig.update_layout(
            title={
                'text':f"Eğitim Durumuna Göre Toplam ({str(secim).capitalize()}-{secim2})",
                'font':{'size': 15,'color':'black','family':'Arial','weight':'bold'}})
        
        st.plotly_chart(fig)
    
    elif secim3=="Erkek":
        sütun=["Hiç Evlenmedi Erkek","Evli Erkek","Boşandı Erkek",
               "Eşi Öldü Erkek","Bilinmeyen Erkek"]
        
        values=veri9filtre[sütun].sum().values
        fig=go.Figure(data=[go.Pie(labels=sütun,values=values,hoverinfo="label+value",
                                   textinfo="none")])
    
        fig.update_layout(
            title={
                'text':f"Eğitim Durumuna Göre Erkek ({str(secim).capitalize()}-{secim2})",
                'font':{'size': 15,'color':'black','family':'Arial','weight':'bold'}})
        
        st.plotly_chart(fig)
    
    elif secim3=="Kadın":
        sütun=["Hiç Evlenmedi Kadın","Evli Kadın","Boşandı Kadın",
               "Eşi Öldü Kadın","Bilinmeyen Kadın"]
        
        values=veri9filtre[sütun].sum().values
        fig=go.Figure(data=[go.Pie(labels=sütun,values=values,hoverinfo="label+value",
                                   textinfo="none")])
    
        fig.update_layout(
            title={
                'text':f"Eğitim Durumuna Göre Kadın ({str(secim).capitalize()}-{secim2})",
                'font':{'size': 15,'color':'black','family':'Arial','weight':'bold'}})
        
        st.plotly_chart(fig)