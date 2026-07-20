import streamlit as st
import os
import json
from PIL import Image

from agent_core import interroga_agente
from image_tools import (
    regola_luminosita_contrasto, 
    applica_filtro_colore, 
    ruota_immagine, 
    rileva_contorni, 
    ridimensiona_immagine, 
    rimuovi_contrassegni,
    taglia_immagine,     
    rimuovi_persona_bbox   
)

st.set_page_config(layout="wide", page_title="AI Image Editor Agent")

st.title("Agente Intelligente di Computer Vision")
st.write("Inserisci un'immagine e chiedi all'agente cosa fare.")

UPLOAD_DIR = "temp_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

input_path = os.path.join(UPLOAD_DIR, "input_image.png")
output_path = os.path.join(UPLOAD_DIR, "output_image.png")

uploaded_file = st.file_uploader("Scegli un'immagine...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    if "ultimo_file" not in st.session_state or st.session_state["ultimo_file"] != uploaded_file.name:
        st.session_state["ultimo_file"] = uploaded_file.name
        if os.path.exists(output_path):
            os.remove(output_path) 
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.form(key="image_processing_form"):
        prompt_utente = st.text_input(
            "Cosa vuoi fare con questa immagine?", 
            placeholder="Es: Rimpicciolisci del 50% / Rimuovi le X gialle..."
        )
        modello = st.selectbox("Seleziona il Modello Visione (VLM)", ["llava", "moondream"], index=0)
        
        submit_button = st.form_submit_button(label="Esegui Elaborazione", type="primary")

    if submit_button:
        if prompt_utente:
            with st.spinner("L'agente sta analizzando l'immagine e pianificando l'azione..."):
                risposta_agente = interroga_agente(prompt_utente, input_path, modello=modello)
            
            st.subheader("Logica dell'Agente (Output JSON)")
            st.json(risposta_agente)

            if "error" in risposta_agente:
                st.error(f"Errore dell'agente: {risposta_agente['error']}")
            else:
                tool = risposta_agente.get("tool")
                params = risposta_agente.get("params", {})
                messaggio_successo = ""
                
                with st.spinner("Esecuzione dell'algoritmo OpenCV..."):
                    if tool in ["BLACK_AND_WHITE", "GRAYSCALE", "GREYSCALE"]:
                        tool = "COLOR_FILTER"
                        params = {"tipo_filtro": "GRAY"}
                    
                    if tool == "BRIGHTNESS_CONTRAST":
                        b = params.get("brightness", 0)
                        c = params.get("contrast", 1.0)
                        messaggio_successo = regola_luminosita_contrasto(input_path, output_path, brightness=b, contrast=c)
                    elif tool == "COLOR_FILTER":
                        tipo = params.get("tipo_filtro", "GRAY")
                        messaggio_successo = applica_filtro_colore(input_path, output_path, tipo_filtro=tipo)
                    elif tool == "ROTATE":
                        angolo = params.get("angolo", 90)
                        messaggio_successo = ruota_immagine(input_path, output_path, angolo=angolo)
                    elif tool == "CANNY_EDGE":
                        messaggio_successo = rileva_contorni(input_path, output_path)
                    elif tool == "RESIZE":
                        percentuale = params.get("percentuale", 100)
                        metodo = params.get("metodo_interpolazione", "LINEAR")
                        messaggio_successo = ridimensiona_immagine(input_path, output_path, percentuale=percentuale, metodo_interpolazione=metodo)
                    elif tool == "INPAINT":
                        colore_rilevato = params.get("colore_disturbo", "YELLOW")
                        messaggio_successo = rimuovi_contrassegni(input_path, output_path, colore_disturbo=colore_rilevato)
                    elif tool == "CROP":
                        messaggio_successo = taglia_immagine(input_path, output_path, params.get("x_min_pct", 0), params.get("y_min_pct", 0), params.get("x_max_pct", 100), params.get("y_max_pct", 100))
                    elif tool == "REMOVE_OBJECT":
                        messaggio_successo = rimuovi_persona_bbox(input_path, output_path, params.get("x_min_pct", 0), params.get("y_min_pct", 0), params.get("x_max_pct", 100), params.get("y_max_pct", 100))
                    else:
                        st.error(f"Strumento '{tool}' non supportato.")

                if messaggio_successo:
                    st.success(messaggio_successo)
        else:
            st.warning("Per favore, inserisci una richiesta testuale.")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Immagine Originale")
        if os.path.exists(input_path):
            img_orig = Image.open(input_path)
            w_orig, h_orig = img_orig.size
            st.caption(f"📏 Risoluzione Reale nel disco: **{w_orig}x{h_orig}** pixel")
            st.image(img_orig, use_container_width=True)

    with col2:
        st.subheader("Risultato Elaborato")
        if os.path.exists(output_path):
            img_res = Image.open(output_path)
            w_res, h_res = img_res.size
            st.caption(f"📏 Risoluzione Reale nel disco: **{w_res}x{h_res}** pixel")
            st.image(img_res, use_container_width=True)
            
            with open(output_path, "rb") as file:
                st.download_button(
                    label="Scarica Immagine Elaborata",
                    data=file,
                    file_name="risultato_agente.png",
                    mime="image/png"
                )
        else:
            st.info("In attesa di un'azione per generare il file di output.")