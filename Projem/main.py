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


hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: visible;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: visible;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style,unsafe_allow_html=True) 

st.markdown(
    """
    <style>
    .title {
        font-size: 36px;  
        font-family: 'Freestyle Script', Courier !important;  
        color: red !important;  
        text-align: center;  
    }
    </style>
    <h1 class="title">Via Anlaşılır Ekonomi</h1>
    """, 
    unsafe_allow_html=True)

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

mbfonlama=st.Page("mbfonlama.py",title="MB Fonlama",icon="📌", 
            default=False)

mbfaizler=st.Page("mbfaizler.py",title="MB Faizleri",icon="📌", 
            default=False)

mbkurlar=st.Page("mbkurlar.py",title="MB Kur Verileri",icon="📌", 
            default=False)

cds=st.Page("cds.py",title="CDS Türkiye",icon="📌", 
            default=False)

kredinot=st.Page("krediderece.py",title="Türkiye Kredi Notları",icon="📌", 
            default=False)

ekotakvim=st.Page("ekonomiktakvim.py",title="Ekonomi Takvimi",icon="📌", 
            default=False)

veritakvim=st.Page("veritakvim.py",title="Ulusal Veri Takvimi",icon="📌", 
            default=False)

tüfe=st.Page("tüfe.py",title="TÜFE Enflasyonu",icon="📌", 
            default=False)

ctüfe=st.Page("ctüfe.py",title="Çekirdek TÜFE Enflasyonu",icon="📌", 
            default=False)

üfe=st.Page("üfe.py",title="ÜFE Enflasyonu",icon="📌", 
            default=False)

ito=st.Page("ito.py",title="İTO Enflasyonu",icon="📌", 
            default=False)

enfanket=st.Page("enfanket.py",title="Enflasyon Anketi",icon="📌", 
            default=False)

issizlik=st.Page("issizlik.py",title="İşsizlik",icon="📌", 
            default=False)

banknot=st.Page("banknot.py",title="Banknot Dağılımı",icon="📌", 
            default=False)

dısticaret=st.Page("dısticaret.py",title="Dış Ticaret",icon="📌", 
            default=False)

mbbilanco=st.Page("mbbilanco.py",title="MB Bilanço",icon="📌", 
            default=False)

konutsatıs=st.Page("konutsatıs.py",title="Konut Satış İstatistikleri",icon="📌", 
            default=False)

konutm2=st.Page("konutm2.py",title="Konut Birim Fiyatları",icon="📌", 
            default=False)

rezerv=st.Page("mbrezerv.py",title="MB Rezervler",icon="📌", 
            default=False)

buyume=st.Page("buyume.py",title="GSYH",icon="📌", 
            default=False)

osd=st.Page("osd.py",title="OSD",icon="📌", 
            default=False)

kko=st.Page("kko.py",title="Kapasite Kullanım Oranı",icon="📌", 
            default=False)

demografik=st.Page("demografik.py",title="Nüfus ve Eğitim",icon="📌", 
            default=False)

bilancolar=st.Page("bilancolar.py",title="Hisse Senedi Bilançoları",icon="🔷", 
            default=False)

hissebilgi=st.Page("hissebilgi.py",title="Hisse Senedi Bilgileri",icon="🔷", 
            default=False)

hissefiyat=st.Page("hissefiyat.py",title="Hisse Senedi Fiyatları",icon="🔷", 
            default=False)

hissehedeffiyat=st.Page("hissehedeffiyat.py",title="Hisse Senedi Hedef Fiyatları",icon="🔷", 
            default=False)

bisttreemap=st.Page("bisttreemap.py",title="Bist TreeMap",icon="🔷", 
            default=False)

cnbc=st.Page("cnbcpro.py",title="CNBC Pro Makaleler",icon="🔷", 
            default=False)

döviz=st.Page("döviz.py",title="Döviz",icon="🔷", 
            default=False)

brent=st.Page("brent.py",title="Brent Petrol",icon="🔷", 
            default=False)

bist=st.Page("bist.py",title="Bist100",icon="🔷", 
            default=False)

altın=st.Page("altın.py",title="Altın",icon="🔷", 
            default=False)

vix=st.Page("vix.py",title="VIX",icon="🔷", 
            default=False)

tpp=st.Page("tpp.py",title="TPP",icon="🔷", 
            default=False)

teminat=st.Page("teminat.py",title="Teminat Tamamlama Çağrısı",icon="🔷", 
            default=False)

akaryakıt=st.Page("akaryakıt.py",title="Akaryakıt Fiyatları",icon="🔷", 
            default=False)

haber=st.Page("haber.py",title="Haber Akışı",icon="🔷", 
            default=False)


pg=st.navigation(
        {
        "Makro Veriler":[mbfonlama,mbfaizler,mbkurlar,cds,kredinot,ekotakvim,veritakvim,
                         rezerv,tüfe,ctüfe,üfe,ito,enfanket,issizlik,buyume,demografik,
                         kko,banknot,dısticaret,mbbilanco,konutsatıs,konutm2,osd],
        
        "Finansal Veriler":[haber,bilancolar,hissebilgi,hissefiyat,hissehedeffiyat,akaryakıt,tpp,teminat,
                            bisttreemap,cnbc,döviz,brent,bist,altın,vix]
        })

pg.run()

