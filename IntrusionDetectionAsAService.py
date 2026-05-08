from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import os

app = FastAPI()

# Cargar modelo
model = joblib.load('Models_API/modelo_rf_grouped.pkl')
features = joblib.load('Models_API/features_rf_grouped.pkl')

print(f"Modelo cargado correctamente")
print(f"Features esperadas: {len(features)}")

clases = {
    0: 'BENIGN',
    1: 'Bot',
    2: 'DDoS',
    3: 'DoS GoldenEye',
    4: 'DoS Hulk',
    5: 'DoS Slowhttptest',
    6: 'DoS slowloris',
    7: 'FTP-Patator',
    8: 'Heartbleed',
    9: 'Infiltration',
    10: 'PortScan',
    11: 'SSH-Patator',
    12: 'Web Attack'
}

class TrafficData(BaseModel):
    destination_port: int = 0
    flow_duration: float = 0.0
    total_fwd_packets: int = 0
    total_backward_packets: int = 0
    total_length_of_fwd_packets: float = 0.0
    fwd_packet_length_mean: float = 0.0
    fwd_packet_length_std: float = 0.0
    fwd_packet_length_max: float = 0.0
    total_length_of_bwd_packets: float = 0.0
    bwd_packet_length_min: float = 0.0
    bwd_packet_length_max: float = 0.0
    bwd_packet_length_std: float = 0.0
    bwd_packet_length_mean: float = 0.0
    flow_bytes_s: float = 0.0
    flow_packets_s: float = 0.0
    flow_iat_min: float = 0.0
    flow_iat_mean: float = 0.0
    flow_iat_std: float = 0.0
    flow_iat_max: float = 0.0
    fwd_iat_min: float = 0.0
    fwd_iat_total: float = 0.0
    fwd_iat_std: float = 0.0
    fwd_iat_mean: float = 0.0
    fwd_iat_max: float = 0.0
    bwd_iat_total: float = 0.0
    bwd_iat_mean: float = 0.0
    bwd_iat_std: float = 0.0
    bwd_iat_max: float = 0.0
    bwd_iat_min: float = 0.0
    fwd_psh_flags: int = 0
    fwd_urg_flags: int = 0
    fwd_header_length: int = 0
    bwd_header_length: int = 0
    fwd_packets_s: float = 0.0
    bwd_packets_s: float = 0.0
    min_packet_length: int = 0
    max_packet_length: int = 0
    packet_length_mean: float = 0.0
    packet_length_std: float = 0.0
    packet_length_variance: float = 0.0
    fin_flag_count: int = 0
    syn_flag_count: int = 0
    rst_flag_count: int = 0
    psh_flag_count: int = 0
    ack_flag_count: int = 0
    urg_flag_count: int = 0
    cwe_flag_count: int = 0
    ece_flag_count: int = 0
    down_up_ratio: float = 0.0
    average_packet_size: float = 0.0
    avg_fwd_segment_size: float = 0.0
    avg_bwd_segment_size: float = 0.0
    subflow_fwd_packets: int = 0
    subflow_fwd_bytes: int = 0
    subflow_bwd_packets: int = 0
    subflow_bwd_bytes: int = 0
    act_data_pkt_fwd: int = 0
    min_seg_size_forward: int = 0
    active_mean: float = 0.0
    active_std: float = 0.0
    active_max: float = 0.0
    active_min: float = 0.0
    idle_mean: float = 0.0
    idle_std: float = 0.0
    idle_max: float = 0.0
    idle_min: float = 0.0
    fwd_packet_length_min: float = 0.0

@app.post("/predict")
def predict(data: TrafficData):
    try:
        # Convertir a diccionario
        input_dict = data.model_dump()
        
        # Crear diccionario con los nombres correctos
        model_input = {}
        for key, value in input_dict.items():
            if key == 'flow_bytes_s':
                model_input['flow_bytes/s'] = value
            elif key == 'flow_packets_s':
                model_input['flow_packets/s'] = value
            elif key == 'fwd_packets_s':
                model_input['fwd_packets/s'] = value
            elif key == 'bwd_packets_s':
                model_input['bwd_packets/s'] = value
            elif key == 'down_up_ratio':
                model_input['down/up_ratio'] = value
            else:
                model_input[key] = value
        
        # Crear dataframe
        df = pd.DataFrame([model_input])
        
        # Seleccionar features
        df = df[features]
        
        # Predecir
        pred = model.predict(df)[0]
        proba = model.predict_proba(df)[0].max()
        
        # Convertir a tipos nativos de Python
        codigo = int(pred)
        confianza = float(proba)
        es_ataque = bool(pred != 0)
        
        return {
            "codigo": codigo,
            "tipo": clases[codigo],
            "confianza": confianza,
            "es_ataque": es_ataque
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    print("Iniciando API en http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)