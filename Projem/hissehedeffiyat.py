import pandas as pd
import cloudscraper
import streamlit as st

scraper=cloudscraper.CloudScraper()
url="https://api.fintables.com/analyst-ratings/?brokerage_id=&code=&in_model_portfolio="
r=scraper.get(url).json()["results"]
df=pd.DataFrame(r)

df["title"]=df["brokerage"].apply(lambda x: x.get("title") if isinstance(x,dict) else None)
columns_order=["code","title","type","published_at","price_target","in_model_portfolio"]
df=df[columns_order]
df["published_at"]=pd.to_datetime(df["published_at"]).dt.strftime('%d.%m.%Y')
df.columns=["Hisse","Kurum","Öneri","Öneri Tarih","Hedef Fiyat","Model Portföyünde"]
df["Model Portföyünde"]=df["Model Portföyünde"].map({True:"Var",False:"Yok"})
df["Öneri"]=df["Öneri"].map({"al":"Al","endeks_alti":"Endeks Altı","endeks_ustu":"Endeks Üstü",
                             "endekse_paralel":"Endekse Paralel","tut":"Tut","sat":"Sat"})

st.markdown("<h4 style='font-size:20px;'>Hedef Fiyatlar</h4>",unsafe_allow_html=True)
search_query=st.text_input("Hisse Ara:", "")
filtered_df=df[df["Hisse"].str.contains(search_query,case=False,na=False)]
st.dataframe(filtered_df,hide_index=True,use_container_width=True)