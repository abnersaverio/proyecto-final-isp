import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración principal de la página
st.set_page_config(page_title="Dashboard ISP - Retención", layout="wide")

# 2. Título principal y descripción
st.title("📡 Análisis y Gestión de Fuga de Clientes (ISP)")
st.markdown("Plataforma interactiva para la exploración de datos y análisis de factores críticos de desconexión en servicios de telecomunicaciones.")
st.divider() # Línea divisoria visual

# 3. Función para cargar los datos en caché
@st.cache_data
def load_data():
    df = pd.read_csv("telco_churn.csv") 
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna()
    return df

# 4. Bloque principal de ejecución
try:
    df = load_data()
    
    # Barra lateral de información
    st.sidebar.header("Resumen Operativo")
    st.sidebar.info(f"Total de registros cargados: {df.shape[0]}")
    st.sidebar.success("✅ Base de datos conectada")
    
    # Mostrar el dataset en la pantalla principal
    st.subheader("Exploración Inicial del Dataset")
    st.write("Vista preliminar de los primeros registros de clientes:")
    st.dataframe(df.head(10))

    # --- ANÁLISIS VISUAL Y GRÁFICOS ---
    st.divider()
    st.header("📊 Análisis de Fuga (Churn)")

    # Calcular métricas clave
    total_clientes = df.shape[0]
    churn_rate = (df[df['Churn'] == 'Yes'].shape[0] / total_clientes) * 100
    fibra_clientes = df[df['InternetService'] == 'Fiber optic'].shape[0]

    # Mostrar KPIs en 3 columnas
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Clientes", f"{total_clientes:,}")
    col2.metric("Tasa de Cancelación Global", f"{churn_rate:.1f}%")
    col3.metric("Clientes con Fibra Óptica", f"{fibra_clientes:,}")

    st.write("---")

    # Crear gráficos en 2 columnas
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Cancelaciones por Tecnología")
        st.write("Comparativa de retención entre DSL y Fibra Óptica.")
        fig_internet = px.histogram(df, x="InternetService", color="Churn", barmode="group",
                                    color_discrete_sequence=['#2ecc71', '#e74c3c'])
        st.plotly_chart(fig_internet, use_container_width=True)

    with col_graf2:
        st.subheader("Impacto del Soporte Técnico")
        st.write("¿Los clientes con soporte técnico cancelan menos?")
        df_tech = df[df['TechSupport'] != 'No internet service']
        fig_tech = px.histogram(df_tech, x="TechSupport", color="Churn", barmode="group",
                                color_discrete_sequence=['#2ecc71', '#e74c3c'])
        st.plotly_chart(fig_tech, use_container_width=True)

# 5. Manejo de error si falta el archivo CSV
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo CSV. Asegúrate de que se llame 'telco_churn.csv' y esté en la misma carpeta que app.py")