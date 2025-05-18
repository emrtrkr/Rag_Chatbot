# File: main.py

import os
import streamlit as st

from utils.extract import extract_text
from utils.chunk import chunk_text
from utils.vectorstore import create_vectorstore, load_vectorstore
from utils.rag_chain import create_qa_chain

import os

if "OPENAI_API_KEY" in os.environ:
    del os.environ["OPENAI_API_KEY"]


# -- Streamlit page config ---------------------------------------------------
st.set_page_config(
    page_title="RAG Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -- Sidebar: API Key Entry --------------------------------------------------
st.sidebar.header("⚙️ Ayarlar")
api_key_input = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    value=""           # artık her açılışta boş gelecek
)
if api_key_input:
    os.environ["OPENAI_API_KEY"] = api_key_input


if not os.getenv("OPENAI_API_KEY"):
    st.sidebar.error("Lütfen OpenAI API Key girin.")
    st.stop()

# -- Session state initialization --------------------------------------------
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'system_prompt' not in st.session_state:
    st.session_state.system_prompt = """
    Sen profesyonel bir asistansın. Özelliklerin şunlardır:
    1. Yalnızca kullanıcı tarafından yüklenen dökümanlardaki bilgilere dayanarak yanıt verirsin.
    2. Dokümanlarda bulunmayan hiçbir konuyu tahmin etmez, ek bilgi eklemez veya uydurmazsın.
    3. Cevaplarını açık, anlaşılır ve gerektiğinde örnek veya madde listesi halinde sunarsın.
    4. Resmî, yardımsever ve özlü bir dil kullanırsın. Teknik terimleri gerektiğinde açıklar, jargon kullanmamaya özen gösterirsin.
    5. Sorunun bağlamını kısaca özetleyerek yanıtına girersin.
    
    Başlamadan önce, cevap verirken yukarıdaki kuralları eksiksiz uygulayacağını unutma.
    """


# -- Main layout: Tabs --------------------------------------------------------
tab_chat, tab_prompt, tab_docs = st.tabs([
    "💬 Chat",
    "⚙️ Prompt Ayarı",
    "📁 Döküman Yükle"
])

# === 1) Chat Tab =============================================================
with tab_chat:
    st.header("💬 Chat Alanı")

    # Sohbeti temizleme butonu
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.chat_history = []

    # Geçmiş mesajları göster
    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    # Kullanıcıdan girdi al
    user_input = st.chat_input("Bir soru sor…")
    if user_input:
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        with st.chat_message("user"):
            st.markdown(user_input)

        # Vectorstore hazır değilse uyar
        if not st.session_state.vectorstore:
            st.warning("Önce döküman yükleyip işlemeniz gerekiyor.")
        else:
            # RAG zincirini oluştur ve cevabı al
            chain = create_qa_chain(
                st.session_state.vectorstore,
                st.session_state.system_prompt
            )
            answer = chain.run(user_input)

            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': answer
            })
            with st.chat_message("assistant"):
                st.markdown(answer)

# === 2) Prompt Settings Tab ================================================
with tab_prompt:
    st.header("⚙️ Sistem Prompt Ayarı")
    updated_prompt = st.text_area(
        "Sistem prompt'unu düzenleyin:",
        value=st.session_state.system_prompt,
        height=180
    )
    if st.button("Güncelle", key="prompt_update"):
        st.session_state.system_prompt = updated_prompt
        st.success("✅ Sistem promptu güncellendi.")

# === 3) Document Upload Tab ================================================
with tab_docs:
    st.header("📁 Döküman Yükle ve İşle")
    uploaded_files = st.file_uploader(
        "PDF veya DOCX yükleyin:",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )
    if uploaded_files:
        all_chunks = []
        for f in uploaded_files:
            text = extract_text(f)
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            st.write(f"✅ `{f.name}` → {len(chunks)} chunk")

        # Vectorstore oluştur veya yeniden yükle
        st.session_state.vectorstore = create_vectorstore(all_chunks)
        st.success(f"Toplam {len(all_chunks)} chunk işlendi ve indekslendi.")

# -- Footer -------------------------------------------------------------------
st.markdown("---")
st.markdown("Created by Emir TÜRKER :)")
