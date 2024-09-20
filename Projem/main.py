import streamlit as st
from datetime import datetime
from st_social_media_links import SocialMediaIcons

st.set_page_config(page_title="Anlaşılır Ekonomi",page_icon=':chart_with_upwards_trend:',
                   initial_sidebar_state="expanded")
                    
st.markdown("""
    <style>
    body {
        background-color: white;
    }
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        position: relative;
    }
    .title {
        color: red;
        border: 2px solid black;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Freestyle Script', cursive;
        font-size: 55px;
        position: relative;
    }
    .time-box {
        position: absolute;
        bottom: 10px;
        right: 10px;
        padding: 5px 10px;
        background-color: #ffffff;
        font-family: 'Freestyle Script', cursive;;
        font-size: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title">Via Anlaşılır Ekonomi</h1>',unsafe_allow_html=True)
tarihbugün=datetime.now().strftime('%d.%m.%Y')
st.markdown(f'<div class="time-box">{tarihbugün}</div>',unsafe_allow_html=True)

st.sidebar.title("İletişim")

iletisim_links=[
    "https://x.com/AnlasEkonomi",
    "https://www.youtube.com/@AnlasEkonomi",
    "https://github.com/AnlasEkonomi",
    "https://www.linkedin.com/in/yunus-arslan-413475325"]

iletisim=SocialMediaIcons(iletisim_links)
iletisim.render(sidebar=True,justify_content="start")

mbapi=st.Page("mbapi.py",title="MB Api Fonlama",icon="🛑", 
            default=False)

mbfaizler=st.Page("mbfaizler.py",title="MB Faizleri",icon="🛑", 
            default=False)

mbkurlar=st.Page("mbkurlar.py",title="MB Kur Verileri",icon="🛑", 
            default=False)

cds=st.Page("cds.py",title="CDS Türkiye",icon="🛑", 
            default=False)

ekotakvim=st.Page("ekonomiktakvim.py",title="Ekonomi Takvimi",icon="🛑", 
            default=False)

tüfe=st.Page("tüfe.py",title="TÜFE Enflasyonu",icon="🛑", 
            default=False)

ctüfe=st.Page("ctüfe.py",title="Çekirdek TÜFE Enflasyonu",icon="🛑", 
            default=False)

üfe=st.Page("üfe.py",title="ÜFE Enflasyonu",icon="🛑", 
            default=False)

ito=st.Page("ito.py",title="İTO Enflasyonu",icon="🛑", 
            default=False)

issizlik=st.Page("issizlik.py",title="İşsizlik",icon="🛑", 
            default=False)

bilancolar=st.Page("bilancolar.py",title="Hisse Senedi Bilançoları",icon="☠️", 
            default=False)

hissefiyat=st.Page("hissefiyat.py",title="Hisse Senedi Fiyatları",icon="☠️", 
            default=False)

bisttreemap=st.Page("bisttreemap.py",title="Bist TreeMap",icon="☠️", 
            default=False)

yahoofiyat=st.Page("bistyfhedef.py",title="Yahoo Hedef Fiyat",icon="☠️", 
            default=False)

cnbc=st.Page("cnbcpro.py",title="CNBC Pro Makaleler",icon="☠️", 
            default=False)

döviz=st.Page("döviz.py",title="Döviz",icon="☠️", 
            default=False)

bist=st.Page("bist.py",title="Bist",icon="☠️", 
            default=False)

altın=st.Page("altın.py",title="Altın",icon="☠️", 
            default=False)

pg=st.navigation(
        {
        "Makro Veriler":[mbapi,mbfaizler,mbkurlar,cds,ekotakvim,tüfe,
                         ctüfe,üfe,ito,issizlik],
        "Finansal Veriler":[bilancolar,hissefiyat,bisttreemap,yahoofiyat,
                            cnbc,döviz,bist,altın]
        })

pg.run()