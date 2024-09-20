import streamlit as st
from bs4 import BeautifulSoup
from lxml import etree
import requests

def cnbcpro():
    url=st.text_input("**Lütfen URL Giriniz:**") 
    if url:
        try:
            soup=BeautifulSoup(requests.get(url).text,"html.parser")
            doc=etree.HTML(str(soup))
            metin=doc.xpath("//*[@id='RegularArticle-ArticleBody-5']/span[1]/span/span")[0].text
            st.markdown(f"""
<style>
     .arial {{
        font-family: Arial, sans-serif;;
    }}
</style>
<div class="arial">
    {metin}
</div>
""", unsafe_allow_html=True)
        except Exception as e:
             st.error("**Hatalı URL. Lütfen tekrar giriniz...**")

cnbcpro()