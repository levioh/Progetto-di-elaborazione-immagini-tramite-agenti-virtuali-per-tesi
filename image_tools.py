# image_tools.py
import cv2
import numpy as np
from ultralytics import YOLO

def regola_luminosita_contrasto(input_path, output_path, brightness: int, contrast: float):
    img = cv2.imread(input_path)
    if img is None:
        return "Errore: Immagine non trovata."
    
    # Formula OpenCV standard: g(x) = contrast * f(x) + brightness
    nuova_img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
    cv2.imwrite(output_path, nuova_img)
    return f"Luminosità impostata a {brightness} e Contrasto a {contrast}."

def applica_filtro_colore(input_path, output_path, tipo_filtro: str):

    img = cv2.imread(input_path)
    if img is None:
        return "Errore: Immagine non trovata."
        
    if tipo_filtro.upper() == 'GRAY':
        risultato = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif tipo_filtro.upper() == 'INVERT':
        risultato = cv2.bitwise_not(img)
    elif tipo_filtro.upper() == 'SEPIA':
        # Matrice di trasformazione per l'effetto seppia
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        risultato = cv2.transform(img, kernel)
    else:
        return "Filtro non supportato."
        
    cv2.imwrite(output_path, risultato)
    return f"Filtro {tipo_filtro} applicato con successo."

def ruota_immagine(input_path, output_path, angolo: int):

    img = cv2.imread(input_path)
    if img is None:
        return "Errore: Immagine non trovata."
        
    if angolo == 90:
        risultato = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif sk == 180 or angolo == 180:
        risultato = cv2.rotate(img, cv2.ROTATE_180)
    elif angolo == 270:
        risultato = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return f"Angolo di {angolo}° non supportato. Usa 90, 180 o 270."
        
    cv2.imwrite(output_path, risultato)
    return f"Immagine ruotata di {angolo} gradi."

def rileva_contorni(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        return "Errore: Immagine non trovata."
        
    # Converte in scala di grigi prima del rilevamento bordi
    grigio = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Applica il filtro Canny 
    contorni = cv2.Canny(grigio, 100, 200)
    
    cv2.imwrite(output_path, contorni)
    return "Contorni rilevati con l'algoritmo di Canny."

def ridimensiona_immagine(input_path, output_path, percentuale: int, metodo_interpolazione: str = "LINEAR"):

    img = cv2.imread(input_path)
    if img is None:
        return "Errore: Immagine non trovata."
    
    # Calcolo delle nuove dimensioni
    scala = percentuale / 100.0
    nuova_larghezza = int(img.shape[1] * scala)
    nuova_altezza = int(img.shape[0] * scala)
    nuove_dimensioni = (nuova_larghezza, nuova_altezza)
    
    # Mappatura delle stringhe ai metodi nativi di OpenCV
    metodi = {
        "NEAREST": cv2.INTER_NEAREST,
        "LINEAR": cv2.INTER_LINEAR,
        "CUBIC": cv2.INTER_CUBIC
    }
    
    interp_cv = metodi.get(metodo_interpolazione.upper(), cv2.INTER_LINEAR)
    
    # Esecuzione del ridimensionamento geometrico
    risultato = cv2.resize(img, nuove_dimensioni, interpolation=interp_cv)
    
    cv2.imwrite(output_path, risultato)
    return f"Immagine ridimensionata al {percentuale}% usando l'interpolazione {metodo_interpolazione}."

def rimuovi_contrassegni(input_path, output_path, colore_disturbo: str):

    img = cv2.imread(input_path)
    if img is None:
        return "Errore: Immagine non trovata."
        
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    colore = str(colore_disturbo).strip().upper()
    
    mappa_colori = {
        "YELLOW": "YELLOW", "GIALLO": "YELLOW",
        "RED": "RED", "ROSSO": "RED",
        "BLUE": "BLUE", "BLU": "BLUE",
        "GREEN": "GREEN", "VERDE": "GREEN",
        "DARK": "DARK", "NERO": "DARK", "SCURO": "DARK"
    }
    colore_effettivo = mappa_colori.get(colore, "YELLOW")
    
    if colore_effettivo == "YELLOW":
        lower = np.array([15, 100, 100])
        upper = np.array([35, 255, 255])
        mask_colore = cv2.inRange(hsv, lower, upper)
    elif colore_effettivo == "RED":
        mask1 = cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([170, 120, 70]), np.array([180, 255, 255]))
        mask_colore = cv2.bitwise_or(mask1, mask2)
    else:
        lower = np.array([0, 0, 0])
        upper = np.array([180, 255, 255])
        mask_colore = cv2.inRange(hsv, lower, upper)

    mask_finale = np.zeros_like(mask_colore)
    
    contorni, _ = cv2.findContours(mask_colore, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contorni:
        area = cv2.contourArea(c)
        if area > 300:
            cv2.drawContours(mask_finale, [c], -1, 255, thickness=cv2.FILLED)
    
    kernel = np.ones((3, 3), np.uint8)
    mask_finale = cv2.dilate(mask_finale, kernel, iterations=1)
    
    risultato = cv2.inpaint(img, mask_finale, inpaintRadius=4, flags=cv2.INPAINT_TELEA)
    
    cv2.imwrite(output_path, risultato)
    return f"Inpainting geometrico selettivo completato per oggetti di colore {colore_effettivo}."


def taglia_immagine(input_path, output_path, x_min_pct: int, y_min_pct: int, x_max_pct: int, y_max_pct: int):

    img = cv2.imread(input_path)
    if img is None:
        return "Errore: Immagine non trovata."
    
    h, w, _ = img.shape
    
    x1 = int((x_min_pct / 100) * w)
    y1 = int((y_min_pct / 100) * h)
    x2 = int((x_max_pct / 100) * w)
    y2 = int((y_max_pct / 100) * h)
    
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    
    if x2 - x1 < 10 or y2 - y1 < 10:
        return "Errore: L'area di ritaglio selezionata è troppo piccola."
        
    risultato = img[y1:y2, x1:x2]
    cv2.imwrite(output_path, risultato)
    return f"Immagine ritagliata con successo alle coordinate percentuali [{x1}px, {y1}px] a [{x2}px, {y2}px]."


def rimuovi_persona_bbox(input_path, output_path, x_min_pct=0, y_min_pct=0, x_max_pct=100, y_max_pct=100):

    img = cv2.imread(input_path)
    if img is None:
        return "Errore: Immagine non trovata."
        
    h, w, _ = img.shape
    
    model = YOLO("yolov8n.pt")
    
    results = model(img, verbose=False)
    
    mask = np.zeros((h, w), dtype=np.uint8)
    oggetto_trovato = False
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            nome_classe = model.names[cls_id]
            
            if nome_classe in ["person", "cat", "dog", "chair", "backpack", "umbrella"]:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                cv2.rectangle(mask, (x1, y1), (x2, y2), 255, thickness=cv2.FILLED)
                oggetto_trovato = True
                break 
                
    if not oggetto_trovato:
        x1 = int((x_min_pct / 100) * w)
        y1 = int((y_min_pct / 100) * h)
        x2 = int((x_max_pct / 100) * w)
        y2 = int((y_max_pct / 100) * h)
        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, thickness=cv2.FILLED)

    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    risultato = cv2.inpaint(img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)
    
    cv2.imwrite(output_path, risultato)
    
    if oggetto_trovato:
        return f"Soggetto di tipo '{nome_classe}' rilevato con successo da YOLOv8 e rimosso tramite Inpainting."
    else:
        return "Nessun soggetto standard rilevato da YOLO. Applicato Inpainting sulla coordinata stimata dall'agente."