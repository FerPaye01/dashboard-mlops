import streamlit as st
import numpy as np
import pandas as pd
import math
import os

from logic import (
    estimate_vram_requirements,
    calculate_erlang_c,
    fetch_huggingface_model_metadata,
    fetch_physical_performance_metrics,
    fetch_quality_and_benchmarks,
    normalize_weights,
    get_model_catalog,
    cargar_catalogo_modelos,
    get_cloud_performance,
    calculate_roofline_local_performance
)




# Configuración de la página con estética premium
st.set_page_config(
    page_title="Generative AI Model Selector - MLOps Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar CSS personalizado con identidad corporativa Osinergmin (Tipografía Poppins y Colores Oficiales Manual 2024 - Light Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Configuración de tipografía oficial Poppins y color de texto base */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Poppins', sans-serif !important;
        color: #0B0F19 !important;
        font-size: 0.85rem !important;
    }
    
    /* Asegurar que los iconos de Streamlit (Material Symbols/Icons) no se rompan por Poppins */
    [data-testid="stIcon"], .notranslate, [class*="notranslate"] {
        font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', 'Material Icons' !important;
    }
    
    /* Controlar tamaños de fuentes de cabeceras */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: #0039AA !important; /* Azul Osinergmin */
        letter-spacing: -0.3px !important;
        margin-top: 0.4rem !important;
        margin-bottom: 0.4rem !important;
    }
    h2 { font-size: 1.25rem !important; }
    h3 { font-size: 1.05rem !important; }
    h4 { font-size: 0.9rem !important; }
    
    /* Ajustes generales de contenedores Streamlit para compactación extrema */
    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 0.8rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Eliminar espaciado superior del header de Streamlit */
    [data-testid="stHeader"] {
        height: 1.5rem !important;
        background: transparent !important;
    }
    
    /* Reducir gaps en bloques verticales y horizontales */
    div[data-testid="stVerticalBlock"] {
        gap: 0.4rem !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
    }
    
    /* Compactar la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #F2F2F2 !important; /* Gris Claro */
        border-right: 1px solid #E5E7EB; /* Línea divisoria sutil */
    }
    [data-testid="stSidebarContent"] {
        padding: 0.8rem !important;
    }
    [data-testid="stSidebarContent"] div[data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }
    
    /* Tarjeta Elegante Compacta (Sin degradados, Light Theme) */
    .glass-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 10px 14px !important;
        border: 1px solid #E5E7EB; /* Gris Claro */
        box-shadow: 0 2px 4px -1px rgba(0, 57, 170, 0.04), 0 1px 2px -1px rgba(0, 57, 170, 0.02);
        margin-bottom: 6px !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }
    .glass-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 10px -3px rgba(0, 57, 170, 0.08), 0 2px 4px -4px rgba(0, 57, 170, 0.04);
        border-color: #0039AA; /* Borde resalta en Azul Osinergmin */
    }
    
    .gradient-text {
        color: #0039AA !important; /* Azul Osinergmin */
        font-weight: 800;
    }
    .gradient-sidebar-header {
        color: #0039AA !important; /* Azul Osinergmin */
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 2px;
    }
    
    /* Estilo de métricas customizado */
    .metric-value {
        font-size: 1.45rem !important;
        font-weight: 800;
        color: #0039AA; /* Azul Osinergmin */
        line-height: 1.25;
    }
    .metric-label {
        font-size: 0.7rem !important;
        color: #4B5563; /* Gris Oscuro */
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
        margin-bottom: 2px;
    }
    
    /* Estilo de Semáforos y Alertas */
    .status-badge-green {
        background-color: rgba(53, 204, 41, 0.08); /* Verde Osinergmin */
        color: #35CC29;
        border: 1px solid rgba(53, 204, 41, 0.25);
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.78rem;
        display: inline-block;
        margin-top: 4px;
    }
    .status-badge-red {
        background-color: rgba(246, 162, 41, 0.08); /* Naranja complementario */
        color: #F6A229;
        border: 1px solid rgba(246, 162, 41, 0.25);
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.78rem;
        display: inline-block;
        margin-top: 4px;
    }
    
    /* Personalización de Botones Streamlit (Azul Osinergmin a Amarillo Osinergmin, Sin Degradados) */
    .stButton > button {
        background-color: #0039AA !important; /* Azul Osinergmin */
        color: #FFFFFF !important;
        border: 1px solid #0039AA !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        padding: 0.3rem 0.8rem !important;
        transition: background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease, color 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #FBE122 !important; /* Amarillo Osinergmin */
        border-color: #FBE122 !important;
        color: #0039AA !important; /* Texto Azul Osinergmin */
        box-shadow: 0 3px 8px rgba(251, 225, 34, 0.25) !important;
    }
    
    /* Estilo de st.expander con borde izquierdo azul Osinergmin */
    .streamlit-expanderHeader {
        border-left: 3px solid #0039AA !important; /* Azul Osinergmin */
        background-color: #F2F2F2 !important; /* Gris Claro */
        border-radius: 6px !important;
        font-weight: 600 !important;
        color: #0B0F19 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 0.8rem !important;
    }
    .streamlit-expanderContent {
        padding: 0.6rem !important;
        border: 1px solid #E5E7EB !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
    }
    
    /* Subrayado y color de pestañas activas */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #0039AA !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #4B5563 !important; /* Gris Oscuro */
        font-weight: 500 !important;
        padding: 6px 12px !important;
        font-size: 0.82rem !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #0039AA !important;
    }
    .stTabs [aria-selected="true"] {
        color: #0039AA !important;
        font-weight: 700 !important;
    }
    
    /* Compactar inputs y widgets de Streamlit */
    div[data-testid="stWidgetLabel"] p {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        margin-bottom: 2px !important;
    }
    .stSelectbox, .stSlider, .stNumberInput, .stTextInput, .stToggle {
        margin-bottom: 2px !important;
    }
    
    /* Compactar st.info, st.success, etc. */
    div[data-testid="stAlert"] {
        padding: 6px 10px !important;
        margin-bottom: 4px !important;
    }
    div[data-testid="stAlert"] div[role="alert"] p, 
    div[data-testid="stAlert"] div[role="alert"] li {
        font-size: 0.78rem !important;
    }

    /* Compactación general de márgenes entre widgets */
    .stElementContainer {
        margin-bottom: 2px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
</style>
""", unsafe_allow_html=True)


# --- 1. Gestión de Estado (st.session_state) ---
# Cargar especificaciones físicas de las GPUs desde un archivo local si existe
def load_gpu_specs() -> dict:
    import json
    path = os.path.join(os.path.dirname(__file__), "gpu_specs.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "Personalizado (Manual)": {"vram": 24.0, "bw": 936.0, "tflops": 82.6}
    }

GPU_SPECS = load_gpu_specs()

if 'gpu_model' not in st.session_state:
    st.session_state.gpu_model = "Personalizado (Manual)"
if 'gpu_bw' not in st.session_state:
    st.session_state.gpu_bw = 936.0
if 'gpu_tflops' not in st.session_state:
    st.session_state.gpu_tflops = 82.6

# Inicialización de las variables de la Fase 1 en st.session_state
if 'server_vram' not in st.session_state:
    st.session_state.server_vram = 24.0
if 'context_length' not in st.session_state:
    st.session_state.context_length = 32000
if 'concurrent_users' not in st.session_state:
    st.session_state.concurrent_users = 15
if 'validated_model' not in st.session_state:
    st.session_state.validated_model = None
if 'validated_model_name' not in st.session_state:
    st.session_state.validated_model_name = None
if 'user_activity_rate' not in st.session_state:
    st.session_state.user_activity_rate = 0.40  # Porcentaje de tiempo que un usuario activo está pidiendo tokens

# Inicialización de las variables de la Fase 2 en st.session_state
if 'weight_quality' not in st.session_state:
    st.session_state.weight_quality = 60
if 'weight_speed' not in st.session_state:
    st.session_state.weight_speed = 20
if 'weight_efficiency' not in st.session_state:
    st.session_state.weight_efficiency = 20
if 'deployment_type' not in st.session_state:
    st.session_state.deployment_type = "Ambos (Híbrido)"

# Inicialización de las variables de paginación y almacenamiento de la Fase 3/4
if 'rows_per_page' not in st.session_state:
    st.session_state.rows_per_page = 10
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'catalog_df' not in st.session_state:
    import os
    cache_path = os.path.join(os.path.dirname(__file__), "model_catalog_cache.json")
    if os.path.exists(cache_path):
        try:
            st.session_state.catalog_df = pd.read_json(cache_path)
        except Exception:
            st.session_state.catalog_df = None
    else:
        st.session_state.catalog_df = None

# Sincronización inicial para los widgets temp correspondientes de la Fase 1, Fase 2 y Paginación
if 'temp_gpu_model' not in st.session_state:
    st.session_state.temp_gpu_model = st.session_state.gpu_model
if 'temp_gpu_bw' not in st.session_state:
    st.session_state.temp_gpu_bw = st.session_state.gpu_bw
if 'temp_gpu_tflops' not in st.session_state:
    st.session_state.temp_gpu_tflops = st.session_state.gpu_tflops

if 'temp_server_vram' not in st.session_state:
    st.session_state.temp_server_vram = st.session_state.server_vram
if 'temp_context_length' not in st.session_state:
    st.session_state.temp_context_length = st.session_state.context_length
if 'temp_concurrent_users' not in st.session_state:
    st.session_state.temp_concurrent_users = st.session_state.concurrent_users
if 'temp_user_activity_rate' not in st.session_state:
    st.session_state.temp_user_activity_rate = int(st.session_state.user_activity_rate * 100)

if 'temp_weight_quality' not in st.session_state:
    st.session_state.temp_weight_quality = st.session_state.weight_quality
if 'temp_weight_speed' not in st.session_state:
    st.session_state.temp_weight_speed = st.session_state.weight_speed
if 'temp_weight_efficiency' not in st.session_state:
    st.session_state.temp_weight_efficiency = st.session_state.weight_efficiency
if 'temp_deployment_type' not in st.session_state:
    st.session_state.temp_deployment_type = st.session_state.deployment_type
if 'temp_rows_per_page' not in st.session_state:
    st.session_state.temp_rows_per_page = st.session_state.rows_per_page

# Inicialización de las variables de Configuración Avanzada en st.session_state
if 'gpus_tp' not in st.session_state:
    st.session_state.gpus_tp = 1
if 'gpu_memory_utilization' not in st.session_state:
    st.session_state.gpu_memory_utilization = 0.90
if 'inference_engine' not in st.session_state:
    st.session_state.inference_engine = "vLLM (PagedAttention)"
if 'continuous_batching' not in st.session_state:
    st.session_state.continuous_batching = True
if 'chunked_prefill' not in st.session_state:
    st.session_state.chunked_prefill = False

# Sincronización inicial para los widgets temp de Configuración Avanzada
if 'temp_gpus_tp' not in st.session_state:
    st.session_state.temp_gpus_tp = st.session_state.gpus_tp
if 'temp_gpu_memory_utilization' not in st.session_state:
    st.session_state.temp_gpu_memory_utilization = st.session_state.gpu_memory_utilization
if 'temp_inference_engine' not in st.session_state:
    st.session_state.temp_inference_engine = st.session_state.inference_engine
if 'temp_continuous_batching' not in st.session_state:
    st.session_state.temp_continuous_batching = st.session_state.continuous_batching
if 'temp_chunked_prefill' not in st.session_state:
    st.session_state.temp_chunked_prefill = st.session_state.chunked_prefill


# Callbacks para actualización en tiempo real e instantánea (UI Reactiva)
def update_gpu_model():
    model = st.session_state.temp_gpu_model
    st.session_state.gpu_model = model
    if model != "Personalizado (Manual)":
        specs = GPU_SPECS[model]
        st.session_state.server_vram = specs["vram"]
        st.session_state.gpu_bw = specs["bw"]
        st.session_state.gpu_tflops = specs["tflops"]
        
        st.session_state.temp_server_vram = specs["vram"]
        st.session_state.temp_gpu_bw = specs["bw"]
        st.session_state.temp_gpu_tflops = specs["tflops"]

def update_gpu_bw():
    st.session_state.gpu_bw = st.session_state.temp_gpu_bw

def update_gpu_tflops():
    st.session_state.gpu_tflops = st.session_state.temp_gpu_tflops

def update_server_vram():
    st.session_state.server_vram = st.session_state.temp_server_vram

def update_context_length():
    st.session_state.context_length = st.session_state.temp_context_length

def update_concurrent_users():
    st.session_state.concurrent_users = st.session_state.temp_concurrent_users

def update_user_activity_rate():
    st.session_state.user_activity_rate = st.session_state.temp_user_activity_rate / 100.0

def update_gpus_tp():
    st.session_state.gpus_tp = st.session_state.temp_gpus_tp

def update_gpu_memory_utilization():
    st.session_state.gpu_memory_utilization = st.session_state.temp_gpu_memory_utilization

def update_inference_engine():
    st.session_state.inference_engine = st.session_state.temp_inference_engine

def update_continuous_batching():
    st.session_state.continuous_batching = st.session_state.temp_continuous_batching

def update_chunked_prefill():
    st.session_state.chunked_prefill = st.session_state.temp_chunked_prefill

def update_weight_quality():
    w_dict = {
        'weight_quality': st.session_state.temp_weight_quality,
        'weight_speed': st.session_state.weight_speed,
        'weight_efficiency': st.session_state.weight_efficiency
    }
    new_w = normalize_weights('weight_quality', w_dict)
    st.session_state.weight_quality = new_w['weight_quality']
    st.session_state.weight_speed = new_w['weight_speed']
    st.session_state.weight_efficiency = new_w['weight_efficiency']
    
    st.session_state.temp_weight_quality = new_w['weight_quality']
    st.session_state.temp_weight_speed = new_w['weight_speed']
    st.session_state.temp_weight_efficiency = new_w['weight_efficiency']

def update_weight_speed():
    w_dict = {
        'weight_quality': st.session_state.weight_quality,
        'weight_speed': st.session_state.temp_weight_speed,
        'weight_efficiency': st.session_state.weight_efficiency
    }
    new_w = normalize_weights('weight_speed', w_dict)
    st.session_state.weight_quality = new_w['weight_quality']
    st.session_state.weight_speed = new_w['weight_speed']
    st.session_state.weight_efficiency = new_w['weight_efficiency']
    
    st.session_state.temp_weight_quality = new_w['weight_quality']
    st.session_state.temp_weight_speed = new_w['weight_speed']
    st.session_state.temp_weight_efficiency = new_w['weight_efficiency']

def update_weight_efficiency():
    w_dict = {
        'weight_quality': st.session_state.weight_quality,
        'weight_speed': st.session_state.weight_speed,
        'weight_efficiency': st.session_state.temp_weight_efficiency
    }
    new_w = normalize_weights('weight_efficiency', w_dict)
    st.session_state.weight_quality = new_w['weight_quality']
    st.session_state.weight_speed = new_w['weight_speed']
    st.session_state.weight_efficiency = new_w['weight_efficiency']
    
    st.session_state.temp_weight_quality = new_w['weight_quality']
    st.session_state.temp_weight_speed = new_w['weight_speed']
    st.session_state.temp_weight_efficiency = new_w['weight_efficiency']

def update_deployment_type():
    st.session_state.deployment_type = st.session_state.temp_deployment_type

def update_rows_per_page():
    st.session_state.rows_per_page = st.session_state.temp_rows_per_page
    st.session_state.current_page = 0  # Resetear a primera página al cambiar paginación


# --- 1.2 Cálculos de Simulación (si hay modelo validado) ---
vram_calc = None
model_metadata = None
physical_servers_m = 0
available_vram = 0.0
offered_traffic_a = 0.0
erlang_results = None

if st.session_state.validated_model is not None:
    # Buscar el modelo en el catálogo dinámico o consultar metadatos
    catalog = get_model_catalog()
    model_metadata = next((m for m in catalog if m["model_id"] == st.session_state.validated_model), None)
    if not model_metadata:
        if st.session_state.catalog_df is not None and not st.session_state.catalog_df.empty:
            match_df = st.session_state.catalog_df[st.session_state.catalog_df["model_id"] == st.session_state.validated_model]
            if not match_df.empty:
                row = match_df.iloc[0]
                model_metadata = {
                    "model_id": row["model_id"],
                    "parameters_b": row["parameters_b"],
                    "layers": row["layers"],
                    "hidden_size": row["hidden_size"],
                    "num_heads": row["num_heads"],
                    "num_kv_heads": row["num_kv_heads"],
                    "attention_type": row["attention_type"]
                }
        if not model_metadata:
            model_metadata = fetch_huggingface_model_metadata(st.session_state.validated_model)
            
    model_params_b = float(model_metadata.get("parameters_b", 7.0))
    model_layers = int(model_metadata.get("layers", 32))
    model_hidden_size = int(model_metadata.get("hidden_size", 4096))
    model_num_heads = int(model_metadata.get("num_heads", 32))
    model_num_kv_heads = int(model_metadata.get("num_kv_heads", 8))
    model_attention_type = model_metadata.get("attention_type", "GQA")
    
    vram_calc = estimate_vram_requirements(
        model_params_b=model_params_b,
        precision_bits=16,
        context_length=st.session_state.context_length,
        attention_type=model_attention_type,
        num_users=st.session_state.concurrent_users,
        layers=model_layers,
        hidden_size=model_hidden_size,
        num_heads=model_num_heads,
        num_kv_heads=model_num_kv_heads
    )

    if st.session_state.inference_engine == "SGLang (RadixAttention)":
        vram_calc["total_kv_cache_gb"] = vram_calc["kv_cache_per_user_gb"] * (0.80 + 0.20 * st.session_state.concurrent_users)
        vram_calc["total_estimated_vram_gb"] = (
            vram_calc["base_vram_gb"] + 
            vram_calc["total_kv_cache_gb"] + 
            vram_calc["cuda_overhead_gb"] + 
            vram_calc["activation_overhead_gb"]
        )
    
    available_vram = st.session_state.server_vram * st.session_state.gpus_tp * st.session_state.gpu_memory_utilization
    vram_base_and_overhead = vram_calc["base_vram_gb"] + vram_calc["cuda_overhead_gb"] + vram_calc["activation_overhead_gb"]
    vram_available_for_kv = max(0.0, available_vram - vram_base_and_overhead)
    
    if vram_calc["kv_cache_per_user_gb"] > 0:
        if st.session_state.inference_engine == "SGLang (RadixAttention)":
            kv_user = vram_calc["kv_cache_per_user_gb"]
            physical_servers_m = int((vram_available_for_kv - (kv_user * 0.80)) // (kv_user * 0.20))
        else:
            physical_servers_m = int(vram_available_for_kv // vram_calc["kv_cache_per_user_gb"])
    else:
        physical_servers_m = 0
    
    physical_servers_m = max(1, physical_servers_m)
    if vram_base_and_overhead > available_vram:
        physical_servers_m = 0
        
    offered_traffic_a = st.session_state.concurrent_users * st.session_state.user_activity_rate
    erlang_results = calculate_erlang_c(physical_servers_m, offered_traffic_a)


# --- 2. Elementos de la Interfaz en la Barra Lateral (st.sidebar) ---
with st.sidebar:
    st.markdown('<div class="gradient-sidebar-header">⚙️ Restricciones de Infraestructura</div>', unsafe_allow_html=True)
    st.markdown("### (Límites Físicos)")
    st.write("---")
    
    # Elemento 0: Selector de GPU y especificaciones físicas
    st.selectbox(
        "🤖 Modelo de GPU",
        options=list(GPU_SPECS.keys()),
        key="temp_gpu_model",
        on_change=update_gpu_model,
        help="Selecciona un hardware de referencia para estimar de forma verídica y matemática el rendimiento local."
    )
    
    # Mostrar inputs manuales solo si se selecciona Personalizado
    if st.session_state.gpu_model == "Personalizado (Manual)":
        st.number_input(
            "VRAM Total del Servidor (GB)",
            min_value=8.0,
            max_value=1000.0,
            step=8.0,
            key="temp_server_vram",
            on_change=update_server_vram,
            help="Indica la VRAM física total de tu nodo de inferencia."
        )
        st.number_input(
            "Ancho de Banda de VRAM (GB/s)",
            min_value=10.0,
            max_value=10000.0,
            step=50.0,
            key="temp_gpu_bw",
            on_change=update_gpu_bw,
            help="Ancho de banda de lectura de memoria de la GPU (ej: RTX 3090 = 936 GB/s, A100 = 2039 GB/s)."
        )
        st.number_input(
            "Rendimiento FP16 (TFLOPs)",
            min_value=1.0,
            max_value=2000.0,
            step=10.0,
            key="temp_gpu_tflops",
            on_change=update_gpu_tflops,
            help="Capacidad de cómputo en media precisión (ej: RTX 4090 = 82.6 TFLOPs, H100 = 989 TFLOPs)."
        )
    else:
        # Mostrar las especificaciones actuales calculadas de forma informativa
        st.markdown(f"""
        <div style="background-color: rgba(0, 57, 170, 0.04); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(0, 57, 170, 0.1); font-size: 0.8rem; margin-bottom: 8px;">
            💼 <strong>Especificaciones {st.session_state.gpu_model.split(' ')[1]}:</strong><br>
            • VRAM Total: <strong>{st.session_state.server_vram:.1f} GB</strong><br>
            • Ancho de Banda: <strong>{st.session_state.gpu_bw:.1f} GB/s</strong><br>
            • Rendimiento: <strong>{st.session_state.gpu_tflops:.1f} TFLOPs</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Elemento 2: Slider de Longitud de Contexto
    st.slider(
        "Longitud de Contexto de RAG (Tokens)",
        min_value=4000,
        max_value=128000,
        step=2000,
        key="temp_context_length",
        on_change=update_context_length,
        help="Considera el peso de las plantillas EETT/TDR y la Ley N° 32069 (Ley de Contrataciones del Estado)."
    )
    
    # Elemento 3: Slider de Usuarios Concurrentes ($B_c$)
    st.slider(
        "Usuarios Concurrentes Esperados (Bc)",
        min_value=1,
        max_value=100,
        step=1,
        key="temp_concurrent_users",
        on_change=update_concurrent_users,
        help="Número máximo proyectado de usuarios redactando TDRs en paralelo."
    )
    
    # Control adicional para modelar la intensidad del tráfico Erlang (Tasa de actividad por usuario)
    st.slider(
        "Tasa de Actividad por Usuario (%)",
        min_value=5,
        max_value=100,
        step=5,
        key="temp_user_activity_rate",
        on_change=update_user_activity_rate,
        help="¿Qué % del tiempo pasa un usuario generando tokens simultáneamente? (Default: 20%)"
    )
    
    st.write("---")
    st.markdown("### 📊 Estado de Saturación")
    
    if st.session_state.validated_model is not None and erlang_results is not None:
        st.caption(f"Modelo: {st.session_state.validated_model_name}")
        saturacion_porcentaje = erlang_results["utilization_rate"] * 100
        
        col_stat_1, col_stat_2 = st.columns(2)
        with col_stat_1:
            st.metric(
                label="Saturación Cola",
                value=f"{saturacion_porcentaje:.1f}%",
                delta=f"Capacidad: {physical_servers_m} slots",
                delta_color="off"
            )
        with col_stat_2:
            st.metric(
                label="Prob. Espera",
                value=f"{erlang_results['waiting_probability'] * 100:.1f}%"
            )
            
        if erlang_results["status"] == "Alerta: Latencia Hiperbólica / Riesgo de Cola":
            st.error("🚨 **Alerta: Saturación**")
            st.markdown(
                "<div class='status-badge-red'>CRÍTICO: Tráfico excede la capacidad física de VRAM.</div>", 
                unsafe_allow_html=True
            )
        else:
            st.success("🟢 **Operación Fluida**")
            st.markdown(
                "<div class='status-badge-green'>SISTEMA ESTABLE: Latencia controlada en cola.</div>", 
                unsafe_allow_html=True
            )
    else:
        st.info("💡 Por favor, cargue el catálogo y valide un modelo para iniciar la simulación de cola.")
        


# --- 3. Cuerpo Principal del Dashboard (Visualización Premium) ---
# Cabecera con Logotipo Corporativo de Osinergmin (Versión Horizontal Oficial del Manual 2024)
st.markdown("""
<div style="margin-bottom: 12px; background: rgba(0, 57, 170, 0.04); padding: 8px 16px; border-radius: 8px; border-left: 4px solid #0039AA; display: flex; align-items: center; justify-content: flex-start;">
<svg width="280" height="60" viewBox="0 0 420 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<!-- Turbina de Pelton Oficial (Azul sobre fondo claro) -->
<g transform="translate(5, 5)">
<!-- Anillo circular base -->
<circle cx="40" cy="40" r="21" stroke="#0039AA" stroke-width="5.5" fill="none"/>
<!-- Aspa superior derecha -->
<path d="M 40,14 C 55,14 66,25 66,40 C 61,40 55,30 40,30 Z" fill="#0039AA"/>
<!-- Aspa inferior derecha -->
<path d="M 66,40 C 66,55 55,66 40,66 C 40,61 50,55 50,40 Z" fill="#0039AA"/>
<!-- Aspa inferior izquierda -->
<path d="M 40,66 C 25,66 14,55 14,40 C 19,40 25,50 40,50 Z" fill="#0039AA"/>
<!-- Aspa superior izquierda -->
<path d="M 14,40 C 14,25 25,14 40,14 C 40,19 30,25 30,40 Z" fill="#0039AA"/>
</g>
<!-- Tipografía Oficial: "Osinergmin" (Azul Osinergmin) -->
<text x="100" y="46" font-family="'Poppins', sans-serif" font-size="34" font-weight="800" fill="#0039AA" letter-spacing="-0.8px">Osinergmin</text>
<!-- Caja del Tagline Oficial (Amarillo Osinergmin #FBE122) -->
<rect x="100" y="56" width="310" height="15" fill="#FBE122" rx="1.5" />
<!-- Texto del Tagline Oficial (Azul Osinergmin #0039AA) -->
<text x="104" y="67" font-family="'Poppins', sans-serif" font-size="7.2" font-weight="800" fill="#0039AA" letter-spacing="0.2">TRABAJANDO POR UNA ENERGÍA Y MINERÍA SEGURAS Y SOSTENIBLES</text>
</svg>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-top: -10px; margin-bottom: 8px;">
    <h2 class="gradient-text" style="margin: 0; font-size: 1.3rem; font-weight: 800;">⚖️ Selector de Modelos de IA Generativa <span style="font-size: 0.95rem; font-weight: 500; color: #4B5563;">— Portal de Decisiones MLOps</span></h2>
    <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #4B5563; line-height: 1.3;">
        Evaluación de viabilidad de despliegue local o híbrido de modelos según restricciones físicas de memoria (VRAM) y red (Erlang-C), alineadas con la Ley N° 32069 (Perú).
    </p>
</div>
""", unsafe_allow_html=True)

# --- 3.1 Fase 2: Preferencias de Negocio y Despliegue ---
with st.expander("⚙️ Preferencias de Negocio y Despliegue", expanded=True):
    col_b1, col_b2, col_b3, col_b4 = st.columns([1.5, 1, 1, 1])
    
    with col_b1:
        st.selectbox(
            "💻 Entorno de Despliegue",
            options=["Solo Local (Privado / GGUF)", "Solo Cloud (APIs / OpenRouter)", "Ambos (Híbrido)"],
            key="temp_deployment_type",
            on_change=update_deployment_type,
            help="Local garantiza privacidad total de los datos usando hardware propio. Cloud ofrece mayor velocidad pero requiere pago por token a proveedores externos."
        )
        
        # Explicar la lógica de filtrado según la opción (Preparación para Fase 3)
        if st.session_state.deployment_type == "Solo Local (Privado / GGUF)":
            st.info("🔒 **Filtro Local Activo:** Solo se evaluarán modelos descargables (.safetensors / GGUF) compatibles con vLLM o llama.cpp y con límite físico de VRAM de la Fase 1.")
        elif st.session_state.deployment_type == "Solo Cloud (APIs / OpenRouter)":
            st.warning("🌐 **Filtro Cloud Activo:** Se ignorará la VRAM del servidor local. La inferencia se evaluará a través de proveedores MaaS (Artificial Analysis / OpenRouter) mediante coste por token.")
        else:
            st.success("⚖️ **Modo Híbrido Activo:** Se compararán todas las alternativas (Local y Cloud) balanceando privacidad, velocidad y coste.")
            
    with col_b2:
        st.slider(
            "🧠 Peso de Calidad Técnica (IFEval, MMLU)",
            min_value=0,
            max_value=100,
            key="temp_weight_quality",
            on_change=update_weight_quality,
            help="IFEval mide el cumplimiento estricto de formato de instrucciones (vital para el formato de TDRs Legales)."
        )
        
    with col_b3:
        st.slider(
            "⚡ Peso de Velocidad (Tokens/s)",
            min_value=0,
            max_value=100,
            key="temp_weight_speed",
            on_change=update_weight_speed,
            help="Ponderación dada a la latencia inicial (TTFT) y a la velocidad de respuesta."
        )
        
    with col_b4:
        # Nota dinámica e identificación dinámica de etiquetas
        if st.session_state.deployment_type == "Solo Local (Privado / GGUF)":
            efficiency_label = "💾 Eficiencia de VRAM"
            efficiency_help = "Ponderación dada a la optimización de uso de VRAM y cuantización (GGUF/AWQ/GPTQ) para hosting local."
        elif st.session_state.deployment_type == "Solo Cloud (APIs / OpenRouter)":
            efficiency_label = "🪙 Menor Coste por Token"
            efficiency_help = "Ponderación dada a minimizar la facturación mensual por millón de tokens en APIs."
        else:
            efficiency_label = "💰 Eficiencia de VRAM / Coste"
            efficiency_help = "Ponderación equilibrada para VRAM local y tarifas de APIs cloud."
            
        st.slider(
            efficiency_label,
            min_value=0,
            max_value=100,
            key="temp_weight_efficiency",
            on_change=update_weight_efficiency,
            help=efficiency_help
        )
        
    # Mostrar la barra de porcentaje de ponderación normalizada (100% total) de forma compacta
    st.markdown(f"""
    <div style="background-color: #F2F2F2; padding: 6px 12px; border-radius: 6px; display: flex; justify-content: space-around; align-items: center; border: 1px solid #E5E7EB; margin-top: 8px;">
        <span style="font-size: 0.8rem; color: #0B0F19;">🧠 Calidad Técnica: <strong style="color: #0039AA;">{st.session_state.weight_quality}%</strong></span>
        <span style="font-size: 0.8rem; color: #0B0F19; border-left: 1px solid #D1D5DB; padding-left: 15px;">⚡ Velocidad: <strong style="color: #35CC29;">{st.session_state.weight_speed}%</strong></span>
        <span style="font-size: 0.8rem; color: #0B0F19; border-left: 1px solid #D1D5DB; padding-left: 15px;">💼 {efficiency_label.split(' ', 1)[-1]}: <strong style="color: #F6A229;">{st.session_state.weight_efficiency}%</strong></span>
    </div>
    """, unsafe_allow_html=True)


# --- 3.1.2 Configuración Avanzada del Motor de Inferencia ---
with st.expander("⚙️ Configuración Avanzada del Motor de Inferencia", expanded=False):
    col_adv1, col_adv2, col_adv3 = st.columns(3)
    
    with col_adv1:
        st.markdown("### Escalabilidad Física")
        st.number_input(
            "Número de GPUs (Tensor Parallelism - TP)",
            min_value=1,
            step=1,
            key="temp_gpus_tp",
            on_change=update_gpus_tp,
            help="Divide las matrices del modelo entre varias tarjetas gráficas interconectadas para aumentar la VRAM total y reducir latencia."
        )
        
    with col_adv2:
        st.markdown("### Límites de Memoria del Motor")
        st.slider(
            "Utilización de VRAM (gpu_memory_utilization)",
            min_value=0.70,
            max_value=0.99,
            step=0.01,
            key="temp_gpu_memory_utilization",
            on_change=update_gpu_memory_utilization,
            help="Porcentaje de la VRAM reservado para los pesos y la Caché KV. Superar el 0.95 aumenta el riesgo de error Out Of Memory (OOM) por picos de activaciones."
        )
        st.selectbox(
            "Motor de Inferencia y Atención",
            options=["vLLM (PagedAttention)", "SGLang (RadixAttention)"],
            key="temp_inference_engine",
            on_change=update_inference_engine,
            help="PagedAttention divide el KV Cache en bloques lógicos. RadixAttention permite compartir prefijos en un árbol de búsqueda para reutilizar contextos comunes."
        )
        
    with col_adv3:
        st.markdown("### Técnicas de Planificación y Espera")
        st.toggle(
            "Loteamiento Continuo (Continuous Batching)",
            key="temp_continuous_batching",
            on_change=update_continuous_batching,
            help="Inyecta nuevas peticiones en el instante exacto en que otra termina, maximizando la ocupación del procesador."
        )
        st.toggle(
            "Prellenado Fraccionado (Chunked Prefill)",
            key="temp_chunked_prefill",
            on_change=update_chunked_prefill,
            help="Fragmenta la lectura de documentos gigantes para no congelar a los usuarios que ya están en la cola de generación."
        )



# --- 3.2 Tabla Dinámica de Clasificación de Modelos (Fase 3 y 4: Ingesta, Filtrado y Paginación) ---
st.markdown("""
<div style="margin-top: 8px; margin-bottom: 4px;">
    <h3 style="margin: 0; font-size: 1.1rem; color: #0039AA; font-weight: 700;">🏆 Clasificación y Selección de Modelos</h3>
</div>
""", unsafe_allow_html=True)

if st.session_state.catalog_df is None or st.session_state.catalog_df.empty:
    st.info("💡 **Catálogo Vacío:** Por favor presione el botón **'🔄 Actualizar Catálogo (Carga Completa)'** en la barra lateral izquierda para descargar dinámicamente los modelos en tiempo real.")
else:
    processed_models = []
    df_raw = st.session_state.catalog_df.copy()
    
    # Sobrescribir dinámicamente con los benchmarks oficiales verificados en caliente
    # para evitar problemas de caché, CSV o session state desactualizados.
    from logic import find_official_benchmarks
    df_raw["benchmarks_verificados"] = False
    for idx, row in df_raw.iterrows():
        official = find_official_benchmarks(row["model_id"])
        if official:
            df_raw.at[idx, "ifeval"] = official["ifeval"]
            df_raw.at[idx, "mmlu"] = official["mmlu"]
            df_raw.at[idx, "gpqa"] = official["gpqa"]
            df_raw.at[idx, "benchmarks_verificados"] = True
    
    # Iterar y aplicar la fórmula del Muro de Memoria para descarte de modelos locales
    for _, row in df_raw.iterrows():
        layers = int(row["layers"])
        hidden_size = int(row["hidden_size"])
        num_heads = int(row["num_heads"])
        num_kv_heads = int(row["num_kv_heads"])
        attention_type = row["attention_type"]
        params_b = float(row["parameters_b"])
        hosting = row["hosting"]
        
        # 1. Calcular VRAM Peak para modelos locales
        precision_bytes = 2.0 # FP16
        
        if attention_type == 'MLA':
            kv_bytes_per_token = (512 + 128) * layers * precision_bytes
        elif attention_type == 'GQA':
            head_dim = hidden_size / num_heads
            kv_bytes_per_token = 2 * layers * num_kv_heads * head_dim * precision_bytes
        else: # MHA
            head_dim = hidden_size / num_heads
            kv_bytes_per_token = 2 * layers * num_heads * head_dim * precision_bytes
            
        kv_cache_per_user_gb = (kv_bytes_per_token * st.session_state.context_length) / (1024 ** 3)
        
        # Pesos estáticos y activaciones
        pesos_estaticos = params_b * precision_bytes
        activaciones = 0.05 * pesos_estaticos
        
        # VRAM Peak = Pesos Estaticos + Activaciones + (KV Cache Dinamica) + Overhead 20%
        if st.session_state.inference_engine == "SGLang (RadixAttention)":
            kv_term = kv_cache_per_user_gb * (0.80 + 0.20 * st.session_state.concurrent_users)
        else:
            kv_term = kv_cache_per_user_gb * st.session_state.concurrent_users
            
        vram_peak = (pesos_estaticos + activaciones + kv_term) * 1.20
        
        # 2. Evaluación de Compatibilidad (Sin Eliminación)
        is_compatible = True
        reason = "Compatible"
        dep_choice = st.session_state.deployment_type
        
        available_vram = st.session_state.server_vram * st.session_state.gpus_tp * st.session_state.gpu_memory_utilization
        
        # Verificar compatibilidad de tipo de alojamiento
        if dep_choice == "Solo Local (Privado / GGUF)" and hosting == "Solo Cloud (APIs / OpenRouter)":
            is_compatible = False
            reason = "⚠️ Requiere Cloud"
        elif dep_choice == "Solo Cloud (APIs / OpenRouter)" and hosting == "Solo Local (Privado / GGUF)":
            is_compatible = False
            reason = "⚠️ Requiere Local"
        
        # Verificar límite de VRAM física para hosting local
        if is_compatible:
            if hosting == "Solo Local (Privado / GGUF)" or (dep_choice == "Solo Local (Privado / GGUF)"):
                if vram_peak > available_vram:
                    is_compatible = False
                    reason = "⚠️ VRAM Excedida"
            elif dep_choice == "Ambos (Híbrido)" and hosting == "Both":
                # Si el modelo soporta local pero excede la VRAM física disponible, se asume alojamiento Cloud
                if vram_peak > available_vram:
                    hosting = "Solo Cloud (APIs / OpenRouter) [Fallback]"
                    vram_peak = 0.0
            
        # 3. Calcular sub-puntajes normalizados (0-100)
        ifeval_raw = row.get("ifeval")
        mmlu_raw = row.get("mmlu")
        gpqa_raw = row.get("gpqa")
        
        has_quality = (ifeval_raw is not None and not pd.isna(ifeval_raw) and 
                       mmlu_raw is not None and not pd.isna(mmlu_raw) and 
                       gpqa_raw is not None and not pd.isna(gpqa_raw))
        
        if has_quality:
            quality_score = (float(ifeval_raw) * 0.60) + (float(mmlu_raw) * 0.30) + (float(gpqa_raw) * 0.10)
        else:
            quality_score = 0.0
        
        # Velocidad y latencia dinámicas
        if hosting == "Solo Local (Privado / GGUF)":
            perf_dict = calculate_roofline_local_performance(
                params_b=params_b,
                kv_cache_total_gb=kv_cache_per_user_gb * st.session_state.concurrent_users,
                bw=st.session_state.gpu_bw,
                tflops=st.session_state.gpu_tflops,
                gpus=st.session_state.gpus_tp,
                context_length=st.session_state.context_length
            )
            speed_val = perf_dict["tokens_per_sec"]
            ttft_val = perf_dict["ttft_ms"]
        elif hosting == "Solo Cloud (APIs / OpenRouter)" or hosting == "Solo Cloud (APIs / OpenRouter) [Fallback]":
            perf_dict = get_cloud_performance(row["model_id"], params_b)
            speed_val = perf_dict["tokens_per_sec"]
            ttft_val = perf_dict["ttft_ms"]
        else: # Híbrido / Both
            perf_local = calculate_roofline_local_performance(
                params_b=params_b,
                kv_cache_total_gb=kv_cache_per_user_gb * st.session_state.concurrent_users,
                bw=st.session_state.gpu_bw,
                tflops=st.session_state.gpu_tflops,
                gpus=st.session_state.gpus_tp,
                context_length=st.session_state.context_length
            )
            perf_cloud = get_cloud_performance(row["model_id"], params_b)
            if dep_choice == "Solo Local (Privado / GGUF)":
                speed_val = perf_local["tokens_per_sec"]
                ttft_val = perf_local["ttft_ms"]
            elif dep_choice == "Solo Cloud (APIs / OpenRouter)":
                speed_val = perf_cloud["tokens_per_sec"]
                ttft_val = perf_cloud["ttft_ms"]
            else:
                if vram_peak <= available_vram:
                    speed_val = perf_local["tokens_per_sec"]
                    ttft_val = perf_local["ttft_ms"]
                else:
                    speed_val = perf_cloud["tokens_per_sec"]
                    ttft_val = perf_cloud["ttft_ms"]
        
        # Aplicar bonificaciones de la configuración avanzada del motor de inferencia (vLLM/SGLang)
        if st.session_state.continuous_batching and st.session_state.chunked_prefill:
            speed_val = speed_val * 1.20
            
        speed_score = min(100.0, (speed_val / 110.0) * 100.0)
        
        # Eficiencia
        if dep_choice == "Solo Local (Privado / GGUF)":
            vram_pct = (vram_peak / available_vram)
            efficiency_score = max(0.0, (1.0 - vram_pct) * 100.0)
        elif dep_choice == "Solo Cloud (APIs / OpenRouter)":
            cost_m = row["cost_input_per_m"] + row["cost_output_per_m"]
            max_cost_m = 0.59 + 0.79
            efficiency_score = max(0.0, (1.0 - (cost_m / max_cost_m)) * 100.0)
        else:
            # Híbrido
            vram_pct = (vram_peak / available_vram) if vram_peak > 0 else 0.0
            eff_vram = max(0.0, (1.0 - vram_pct) * 100.0)
            cost_m = row["cost_input_per_m"] + row["cost_output_per_m"]
            max_cost_m = 0.59 + 0.79
            eff_cost = max(0.0, (1.0 - (cost_m / max_cost_m)) * 100.0)
            efficiency_score = (eff_vram + eff_cost) / 2.0
            
        # 4. Calcular Score Final Ponderado
        w_q = st.session_state.weight_quality / 100.0
        w_s = st.session_state.weight_speed / 100.0
        w_e = st.session_state.weight_efficiency / 100.0
        
        total_score = (quality_score * w_q) + (speed_score * w_s) + (efficiency_score * w_e)
        
        is_verified = bool(row.get("benchmarks_verificados", False))
        ifeval_val = f"{ifeval_raw:.1f}%" if (ifeval_raw is not None and not pd.isna(ifeval_raw)) else "N/A"
        if ifeval_val != "N/A" and not is_verified:
            ifeval_val += " ⚠️"
            
        mmlu_val = f"{mmlu_raw:.1f}%" if (mmlu_raw is not None and not pd.isna(mmlu_raw)) else "N/A"
        if mmlu_val != "N/A" and not is_verified:
            mmlu_val += " ⚠️"
            
        gpqa_val = f"{gpqa_raw:.1f}%" if (gpqa_raw is not None and not pd.isna(gpqa_raw)) else "N/A"
        if gpqa_val != "N/A" and not is_verified:
            gpqa_val += " ⚠️"
        
        processed_models.append({
            "Modelo": row["name"],
            "Alojamiento": hosting,
            "Compatibilidad": reason,
            "Atención": attention_type,
            "Calidad Legal (IFEval)": ifeval_val,
            "MMLU": mmlu_val,
            "GPQA (Raz. Científico)": gpqa_val,
            "VRAM Peak Est.": f"⚠️ {vram_peak:.1f} GB" if ("VRAM Excedida" in reason) else (f"{vram_peak:.1f} GB" if vram_peak > 0 else "N/A (Cloud)"),
            "Velocidad (Tok/s)": f"{speed_val:.1f}",
            "Latencia TTFT": f"{ttft_val:.0f} ms",
            "Coste Est. ($/M)": f"${(row['cost_input_per_m'] + row['cost_output_per_m'])/2:.3f}" if row["cost_input_per_m"] > 0 else "Gratis",
            "Puntaje Final": round(total_score, 1),
            "_score_raw": total_score,
            "_speed_raw": speed_val,
            "_quality_raw": quality_score,
            "_efficiency_raw": efficiency_score,
            "_compatible_raw": 1 if is_compatible else 0
        })
        
    if not processed_models:
        st.warning("⚠️ El catálogo de modelos está vacío. Presione el botón '🔄 Ejecutar Pipeline (Actualización Completa)' en la pestaña correspondiente.")
    else:
        # Si ningún modelo es compatible con el hardware, mostrar advertencia general
        has_compatible = any(m["_compatible_raw"] == 1 for m in processed_models)
        if not has_compatible:
            st.warning("⚠️ Todos los modelos del catálogo local exceden el límite de VRAM. Incremente la VRAM física en el sidebar o cambie a Cloud/Híbrido.")
            
        df_catalog = pd.DataFrame(processed_models).sort_values(
            by=["_compatible_raw", "_score_raw", "_speed_raw", "_quality_raw", "_efficiency_raw"],
            ascending=[False, False, False, False, False]
        )
        
        # Identificar el modelo recomendado en la fila número 1 de forma segura mediante iloc
        top_model_name = df_catalog.iloc[0]["Modelo"]
        df_catalog.iloc[0, df_catalog.columns.get_loc("Modelo")] = "⭐ " + top_model_name + " (Recomendado)"
        
        # Pre-seleccionar automáticamente el modelo recomendado como validado si es None
        match_row = df_raw[df_raw["name"] == top_model_name]
        if not match_row.empty:
            rec_model_id = match_row.iloc[0]["model_id"]
            if st.session_state.validated_model is None:
                st.session_state.validated_model = rec_model_id
                st.session_state.validated_model_name = top_model_name
                st.rerun()
        
        # Controles superiores: Buscador y selector de número de filas por página
        col_search, col_rpp = st.columns([3, 1])
        with col_search:
            search_query = st.text_input("🔍 Buscar modelo:", "")
        with col_rpp:
            st.selectbox(
                "Filas:",
                options=[10, 20, 50, "Todos"],
                key="temp_rows_per_page",
                on_change=update_rows_per_page
            )
            
        # Aplicar filtro de búsqueda
        if search_query:
            df_filtered = df_catalog[
                df_catalog["Modelo"].str.contains(search_query, case=False) |
                df_catalog["Alojamiento"].str.contains(search_query, case=False) |
                df_catalog["Atención"].str.contains(search_query, case=False)
            ]
        else:
            df_filtered = df_catalog
            
        # Banner Premium de recomendación para Osinergmin (Compacto)
        st.markdown(f"""
        <div style="background-color: rgba(53, 204, 41, 0.08); border-left: 4px solid #35CC29; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px;">
            <span style="font-size: 0.82rem; color: #0B0F19;">🏆 <strong>Modelo Recomendado para Osinergmin:</strong> <span style="color: #0039AA; font-weight: 700;">{top_model_name}</span> con una puntuación ponderada del <strong>{df_catalog.iloc[0]['Puntaje Final']:.1f}%</strong>.</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Lógica de Slicing y Paginación
        total_rows = len(df_filtered)
        rows_choice = st.session_state.rows_per_page
        
        if rows_choice == "Todos":
            df_page = df_filtered
            total_pages = 1
            st.session_state.current_page = 0
        else:
            rpp = int(rows_choice)
            total_pages = max(1, math.ceil(total_rows / rpp))
            
            # Limitar índice de página
            if st.session_state.current_page >= total_pages:
                st.session_state.current_page = total_pages - 1
            if st.session_state.current_page < 0:
                st.session_state.current_page = 0
                
            start_row = st.session_state.current_page * rpp
            end_row = start_row + rpp
            df_page = df_filtered.iloc[start_row:end_row]
            
        # Renderizado de la tabla con st.dataframe (excluyendo columnas internas auxiliares)
        cols_to_drop = [c for c in df_page.columns if c.startswith("_")]
        df_display = df_page.drop(columns=cols_to_drop)
        styled_df = df_display.style.map(
            lambda x: "color: #EF4444; font-weight: bold;" if (isinstance(x, str) and "⚠️" in x) else ""
        )
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Puntaje Final": st.column_config.ProgressColumn(
                    "Puntaje Final",
                    help="Puntaje calculado en base a las ponderaciones de negocio.",
                    format="%.1f",
                    min_value=0.0,
                    max_value=100.0,
                )
            }
        )
        
        # Controles inferiores de paginación (Anterior / Siguiente)
        if rows_choice != "Todos" and total_pages > 1:
            col_pag1, col_pag2, col_pag3 = st.columns([1, 2, 1])
            with col_pag2:
                st.markdown(f"<div style='text-align: center; color: #6B7280;'>Página **{st.session_state.current_page + 1}** de **{total_pages}** (Mostrando modelos {start_row + 1} a {min(end_row, total_rows)} de {total_rows})</div>", unsafe_allow_html=True)
            with col_pag1:
                if st.button("⬅️ Anterior", disabled=(st.session_state.current_page == 0), use_container_width=True):
                    st.session_state.current_page -= 1
                    st.rerun()
            with col_pag3:
                if st.button("Siguiente ➡️", disabled=(st.session_state.current_page == total_pages - 1), use_container_width=True):
                    st.session_state.current_page += 1
                    st.rerun()

        # --- 3.3 Sección de Validación y Simulación de Infraestructura ---
        st.markdown("""
        <div style="margin-top: 8px; margin-bottom: 4px;">
            <h3 style="margin: 0; font-size: 1.1rem; color: #0039AA; font-weight: 700;">🎯 Validación y Simulación de Infraestructura</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Obtener los modelos ordenados de df_catalog
        model_options = df_catalog["Modelo"].tolist()
        
        # Encontrar el índice del modelo validado actual
        clean_options = [m.replace("⭐ ", "").replace(" (Recomendado)", "") for m in model_options]
        default_idx = 0
        if st.session_state.validated_model_name in clean_options:
            default_idx = clean_options.index(st.session_state.validated_model_name)
            
        selected_display_name = st.selectbox(
            "🤖 Modelo a Validar y Simular:",
            options=model_options,
            index=default_idx,
            help="Selecciona un modelo del catálogo. Se recalcularán las métricas de saturación y VRAM en tiempo real."
        )
        
        # Si el modelo seleccionado cambió, actualizar el estado y hacer rerun
        clean_selected_name = selected_display_name.replace("⭐ ", "").replace(" (Recomendado)", "")
        if clean_selected_name != st.session_state.validated_model_name:
            selected_row = df_raw[df_raw["name"] == clean_selected_name]
            if not selected_row.empty:
                st.session_state.validated_model = selected_row.iloc[0]["model_id"]
                st.session_state.validated_model_name = clean_selected_name
                st.rerun()

        # Renderizar las KPI Cards para el modelo validado
        if vram_calc is not None:
            st.markdown(f"### 📊 Métricas de Despliegue para `{st.session_state.validated_model_name}`")
            col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
            
            vram_total = st.session_state.server_vram * st.session_state.gpus_tp
            with col_kpi1:
                st.markdown(f"""
                <div class="glass-card">
                    <div class="metric-label">VRAM Total Disponible</div>
                    <div class="metric-value">{vram_total * st.session_state.gpu_memory_utilization:.1f} GB</div>
                    <span style="color: #64748B; font-size: 0.8rem;">Física: {vram_total:.1f} GB (TP: {st.session_state.gpus_tp} GPUs)</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_kpi2:
                st.markdown(f"""
                <div class="glass-card">
                    <div class="metric-label">VRAM Modelo Base</div>
                    <div class="metric-value">{vram_calc['base_vram_gb']} GB</div>
                    <span style="color: #64748B; font-size: 0.8rem;">Pesos del modelo en FP16</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_kpi3:
                st.markdown(f"""
                <div class="glass-card">
                    <div class="metric-label">KV Cache / Usuario</div>
                    <div class="metric-value">{vram_calc['kv_cache_per_user_gb'] * 1024:.2f} MB</div>
                    <span style="color: #64748B; font-size: 0.8rem;">Para contexto de {st.session_state.context_length:,} tokens</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_kpi4:
                st.markdown(f"""
                <div class="glass-card">
                    <div class="metric-label">Slots Físicos (m)</div>
                    <div class="metric-value">{physical_servers_m}</div>
                    <span style="color: #64748B; font-size: 0.8rem;">Hilos de ejecución en paralelo</span>
                </div>
                """, unsafe_allow_html=True)

st.write("---")


# Sección de Desglose Matemático y Fórmulas
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dimensionamiento de VRAM", "🧮 Simulación de Colas (Erlang-C)", "🔌 Integración de APIs de Entrada", "🛠️ Pipeline de Datos Medallion"])

with tab1:
    st.markdown("#### Desglose de Consumo de VRAM para Inferencia Dinámica")
    if vram_calc is None or model_metadata is None:
        st.info("💡 Por favor, ejecute el pipeline de datos (Capa Plata) y seleccione/valide un modelo para ver las fórmulas y desgloses de simulación.")
    else:
        # Crear un DataFrame para graficar el consumo de VRAM
        vram_breakdown_data = {
            "Concepto": [
                "Pesos del Modelo (Base)",
                "Caché KV (Total de Usuarios)",
                "Sobrecarga de CUDA",
                "Sobrecarga de Activaciones",
                "VRAM Libre / Remanente"
            ],
            "VRAM (GB)": [
                vram_calc["base_vram_gb"],
                vram_calc["total_kv_cache_gb"],
                vram_calc["cuda_overhead_gb"],
                vram_calc["activation_overhead_gb"],
                max(0.0, available_vram - vram_calc["total_estimated_vram_gb"])
            ]
        }
        df_vram = pd.DataFrame(vram_breakdown_data)
        
        col_chart, col_explain = st.columns([2, 1])
        with col_chart:
            st.bar_chart(df_vram.set_index("Concepto"), y="VRAM (GB)", color="#0039AA")
        
        with col_explain:
            st.markdown("**Fórmulas de Memoria KV Cache Dinámica:**")
            st.latex(r"V_{\text{KV}} = 2 \times N_{\text{layers}} \times N_{\text{kv\_heads}} \times d_{\text{head}} \times L_{\text{context}} \times B_{\text{bytes}}")
            st.markdown(f"""
            *   **Capas ($N_{{\text{{layers}}}}$):** `{model_metadata['layers']}`
            *   **KV Heads ($N_{{\text{{kv\_heads}}}}$):** `{model_metadata['num_kv_heads']}` (Atención `{model_metadata['attention_type']}`)
            *   **Contexto ($L_{{\text{{context}}}}$):** `{st.session_state.context_length:,}` tokens
            *   **Modelo de Referencia:** `{st.session_state.validated_model}`
            """)

with tab2:
    st.markdown("#### Teoría de Colas Erlang-C aplicada a Motores de Inferencia LLM")
    if vram_calc is None:
        st.info("💡 Por favor, ejecute el pipeline de datos (Capa Plata) y seleccione/valide un modelo para iniciar la simulación de colas Erlang-C.")
    else:
        st.markdown("""
        En los motores de servicio LLM modernos (como vLLM con *PagedAttention* o TensorRT-LLM), el número de servidores paralelos reales $m$ 
        se define como la cantidad de solicitudes que el pool de KV Cache puede almacenar concurrentemente en VRAM física.
        
        Si el tráfico ofrecido $A = B_c \times \rho_{\text{user}}$ excede la capacidad de slots $m$, o se acerca al límite (tasa de uso $\ge 85\%$), 
        los tiempos de respuesta (TTFT) se degradan exponencialmente debido a que las solicitudes entrantes deben ser puestas en cola 
        (o realizar *swapping* de KV Cache a memoria CPU, lo cual destruye el rendimiento).
        """)
        
        st.latex(r"P_C(m, A) = \frac{\frac{A^m}{m!} \frac{m}{m - A}}{\sum_{k=0}^{m-1} \frac{A^k}{k!} + \frac{A^m}{m!} \frac{m}{m - A}}")
        
        col_erl_1, col_erl_2 = st.columns(2)
        with col_erl_1:
            st.info(f"""
            **Métricas de la Simulación Actual:**
            *   **Usuarios Activos ($B_c$):** {st.session_state.concurrent_users}
            *   **Tasa de Actividad:** {st.session_state.user_activity_rate * 100:.0f}%
            *   **Intensidad de Tráfico Ofrecido ($A$):** {offered_traffic_a:.2f} Erlangs
            *   **Capacidad de Canales ($m$):** {physical_servers_m} slots concurrentes
            """)
            
        with col_erl_2:
            util_steps = np.linspace(0.1, 0.99, 50)
            delay_factor = 1.0 / (1.0 - util_steps)
            
            df_delay = pd.DataFrame({
                "Tasa de Utilización (Rho)": util_steps * 100,
                "Multiplicador de Latencia / Espera": delay_factor
            }).set_index("Tasa de Utilización (Rho)")
            
            st.line_chart(df_delay, y="Multiplicador de Latencia / Espera", color="#03A9F4")
            st.caption("Efecto de cuello de botella: La latencia crece asintóticamente al superar el 85% de utilización.")

with tab3:
    st.markdown("#### Estructura y Fuentes de Datos Externas (Esqueleto de Integración)")
    if vram_calc is None or st.session_state.validated_model is None:
        st.info("💡 Por favor, ejecute el pipeline de datos (Capa Plata) y seleccione/valide un modelo para ver la integración de APIs y datos en tiempo real.")
    else:
        st.markdown("""
        Los datos técnicos y de calidad que alimentan este selector se ingestan diariamente de manera automatizada. 
        Para optimizar el rendimiento, las llamadas externas se encuentran protegidas por un caché local persistente.
        """)
        
        st.markdown("""
        ```python
        # Ejemplo de consumo e integración de APIs en Fase 2 (Comparación de Modelos)
        
        # 1. Hugging Face Hub: Extrae la topología de la red para el cálculo de KV Cache
        from huggingface_hub import HfApi
        api = HfApi()
        model_info = api.model_info("meta-llama/Meta-Llama-3-70B-Instruct")
        
        # 2. Artificial Analysis / OpenRouter: Extrae la latencia (TTFT) y coste real
        import requests
        response = requests.get("https://api.artificialanalysis.ai/v1/models/llama-3-70b")
        performance = response.json() # Contiene 'tokens_per_sec', 'cost_per_million'
        
        # 3. Open LLM Leaderboard (MMLU, IFEval, GPQA): Extrae capacidad de razonamiento legal
        # IFEval mide adherencia a instrucciones de formato (vital para el formato de TDRs Legales)
        quality_scores = load_leaderboard_score("meta-llama/Meta-Llama-3-70B-Instruct")
        ```
        """)
        
        st.subheader(f"Datos Obtenidos para `{st.session_state.validated_model}` (Caché Activo)")
        
        perf = fetch_physical_performance_metrics(st.session_state.validated_model)
        qual = fetch_quality_and_benchmarks(st.session_state.validated_model)
        
        col_api_1, col_api_2, col_api_3 = st.columns(3)
        with col_api_1:
            st.write("**Arquitectura (HF Hub):**")
            st.json(model_metadata)
        with col_api_2:
            st.write("**Rendimiento Físico (Artificial Analysis):**")
            st.json(perf)
        with col_api_3:
            st.write("**Calidad y Benchmarks (EleutherAI / HF Leaderboard):**")
            st.json(qual)

with tab4:
    st.markdown("#### 🛠️ Pipeline de Datos Medallion (Ingesta & Observabilidad)")
    st.markdown("""
    La arquitectura Medallion organiza y refina los datos en tres capas consecutivas para garantizar la calidad y consistencia de las decisiones MLOps.
    """)
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #F8FAFC; padding: 12px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 16px;">
        <div style="text-align: center; padding: 10px; background-color: rgba(239, 68, 68, 0.08); border-radius: 6px; width: 28%; border: 1px solid rgba(239, 68, 68, 0.3);">
            <strong style="color: #B91C1C; font-size: 0.85rem;">🟤 Capa Bronce (Raw)</strong><br>
            <span style="font-size: 0.72rem; color: #7F1D1D;">Descarga cruda desde Hugging Face y OpenRouter APIs.</span>
        </div>
        <div style="font-size: 1.2rem; color: #94A3B8; font-weight: bold;">➔</div>
        <div style="text-align: center; padding: 10px; background-color: rgba(245, 158, 11, 0.08); border-radius: 6px; width: 28%; border: 1px solid rgba(245, 158, 11, 0.3);">
            <strong style="color: #B45309; font-size: 0.85rem;">⚪ Capa Plata (Cleaned)</strong><br>
            <span style="font-size: 0.72rem; color: #78350F;">Unificación y almacenamiento local en JSON (Off-line cache).</span>
        </div>
        <div style="font-size: 1.2rem; color: #94A3B8; font-weight: bold;">➔</div>
        <div style="text-align: center; padding: 10px; background-color: rgba(16, 185, 129, 0.08); border-radius: 6px; width: 28%; border: 1px solid rgba(16, 185, 129, 0.3);">
            <strong style="color: #047857; font-size: 0.85rem;">🟢 Capa Oro (Enriched)</strong><br>
            <span style="font-size: 0.72rem; color: #065F46;">Mapeo de benchmarks, filtros físicos de VRAM y scoring final.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    import os
    import datetime
    cache_path = os.path.join(os.path.dirname(__file__), "model_catalog_cache.json")
    if os.path.exists(cache_path):
        mtime = os.path.getmtime(cache_path)
        last_updated = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        try:
            temp_df = pd.read_json(cache_path)
            total_items = len(temp_df)
            local_count = len(temp_df[temp_df["hosting"] == "Solo Local (Privado / GGUF)"])
            cloud_count = len(temp_df[temp_df["hosting"] == "Solo Cloud (APIs / OpenRouter)"])
        except Exception:
            total_items = 0
            local_count = 0
            cloud_count = 0
    else:
        last_updated = "Nunca (Catálogo vacío)"
        total_items = 0
        local_count = 0
        cloud_count = 0
        
    col_pipe1, col_pipe2, col_pipe3 = st.columns(3)
    with col_pipe1:
        st.markdown(f"""
        <div class="glass-card" style="height: 100px;">
            <div class="metric-label">Capa Bronce (Estado)</div>
            <div class="metric-value" style="color: #B91C1C; font-size: 1.3rem;">Conectado</div>
            <span style="color: #64748B; font-size: 0.75rem;">HuggingFace SDK / OpenRouter API</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_pipe2:
        st.markdown(f"""
        <div class="glass-card" style="height: 100px;">
            <div class="metric-label">Capa Plata (Base de Datos Local)</div>
            <div class="metric-value" style="color: #B45309; font-size: 1.3rem;">{total_items} Modelos</div>
            <span style="color: #64748B; font-size: 0.75rem;">{local_count} locales | {cloud_count} en la nube</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_pipe3:
        st.markdown(f"""
        <div class="glass-card" style="height: 100px;">
            <div class="metric-label">Capa Oro (Última Sincronización)</div>
            <div class="metric-value" style="color: #047857; font-size: 1.15rem; font-weight: 700; margin-top: 5px;">{last_updated}</div>
            <span style="color: #64748B; font-size: 0.75rem;">Persistido: model_catalog_cache.json</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("##### 🔄 Acciones del Pipeline")
    st.markdown("""
    La descarga y alineación completa de modelos (Bronce ➡️ Plata) requiere llamadas de red pesadas y procesamiento de topologías de Hugging Face.
    **Solo es necesario realizar esta acción una vez de forma periódica**. El filtrado y cálculo de scoring final (Plata ➡️ Oro) se realiza de forma instantánea al mover los controles del panel.
    """)
    
    if st.button("🔄 Ejecutar Pipeline (Actualización Completa)", type="primary", use_container_width=True, help="Descarga, limpia, unifica y guarda todos los modelos en el caché de disco local."):
        with st.spinner("Ejecutando Pipeline Medallion (Ingestando modelos de Hugging Face y OpenRouter)..."):
            st.session_state.catalog_df = cargar_catalogo_modelos(
                tipo_despliegue="Ambos (Híbrido)",
                server_vram=st.session_state.server_vram,
                context_length=st.session_state.context_length,
                concurrent_users=st.session_state.concurrent_users,
                limite_modelos=1000  # Carga de catálogo completa
            )
            st.session_state.validated_model = None
            st.session_state.validated_model_name = None
            st.session_state.current_page = 0  # Resetear paginación
            st.rerun()

st.write("---")
st.caption("Desarrollado para el Asistente RAG de Términos de Referencia Legales. Cumple con los requerimientos de la Ley N° 32069 (Perú).")
