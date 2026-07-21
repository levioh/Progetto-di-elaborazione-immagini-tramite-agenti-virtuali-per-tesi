# Progetto-di-elaborazione-immagini-tramite-agenti-virtuali-per-tesi

Scaricare ollama da questo link: https://ollama.com/download

digitare sulla console per scaricare i modelli llm: ollama pull llava e ollama pull moondream

scaricare le librerie necessarie da bash usando questo comando: pip install -r requirements.txt

Ho deciso di creare un'applicazione browser che utilizza come framework Ollama , uno strumento open source che permette di scaricare modelli AI direttamente in locale.
Come modello linguistico sto usando LLava che è un modello addestrato sia su testo che immagini.
Lo scopo del mio progetto è quello di fornire al modello degli strumenti realizzati con la libreria opencv per l'elaborazione di immagini , infatti il progetto è diviso in 3 file: 
-image tools dove sono definiti tutti gli strumenti che l'agente può utilizzare  
-agent core dove è definito il system prompt dell'agente ovvero la logica che deve seguire e come deve trasformare le richieste dell'utente.
-app dove dove è definita l'app browser e come vengono trattate le eventuali richieste dell'utente.

Usare questo approccio rende l'elaborazione di immagini particolarmente agile , in quanto tutto quello che deve fare l'agente è quello di tradurre le richieste dell'utente in una semplice linea json con che tipo di strumento utilizzare e che parametri scegliere.

Al momento la demo ha a disposizione 7 strumenti per:
-cambiare l'illuminazione ed il contrasto
-applicare un filtro di colore ad esempio scala di grigi o effetto negativo
-ruotare
-rilevare i contorni 
-ridimensionare
-ritagliare l'immagine
-rimuovere scritte o scarabocchi dall'immagine e poi effettuare un'interpolazione sull'immagine.
