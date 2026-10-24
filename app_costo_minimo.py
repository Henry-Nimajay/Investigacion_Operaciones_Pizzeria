import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL Y ESTILOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Optimizador Logístico · Costo Mínimo (Quetzales)",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS profesionales
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Banner Principal */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 1.6rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(225, 29, 72, 0.2);
        color: #fda4af;
        border: 1px solid rgba(225, 29, 72, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    .hero-title {
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0 0 0.3rem 0;
        color: #ffffff;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0;
    }

    /* Tarjetas de Métricas */
    .metric-container {
        display: flex;
        gap: 15px;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        flex: 1;
    }
    .kpi-title {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
    }
    .kpi-val {
        font-size: 1.55rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0.3rem 0;
    }
    .kpi-badge-green {
        color: #15803d;
        background: #dcfce7;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
    }
    .kpi-badge-neutral {
        color: #475569;
        background: #f1f5f9;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
    }

    /* Tabla de Transporte */
    .trans-table {
        width: 100%;
        border-collapse: collapse;
        background: #ffffff;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #cbd5e1;
    }
    .trans-table th {
        background: #f8fafc;
        padding: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #334155;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .trans-table td {
        border: 1px solid #e2e8f0;
        padding: 8px;
        text-align: center;
        height: 72px;
        position: relative;
    }
    .cell-cost {
        position: absolute;
        top: 5px;
        right: 7px;
        font-size: 0.75rem;
        color: #475569;
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        padding: 1px 6px;
        font-weight: 600;
    }
    .cell-assigned {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 4px 14px;
        border-radius: 8px;
        margin-top: 14px;
    }
    .cell-empty {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-top: 14px;
        font-weight: 300;
    }

    /* Paso a paso */
    .step-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO BANNER
# ---------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">Investigación de Operaciones · Modelo de Transporte</div>
    <div class="hero-title">Optimización de Abastecimiento (Costo Mínimo)</div>
    <div class="hero-subtitle">Distribución logística de insumos y masas desde bodegas centrales hacia sucursales de 'Pizzería Bella Napoli'.</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATOS DEL PROBLEMA (EN QUETZALES)
# ---------------------------------------------------------
origenes_nombres = ["Bodega Norte (B1)", "Bodega Central (B2)", "Bodega Sur (B3)"]
destinos_nombres = ["Sucursal Centro (S1)", "Sucursal Plaza (S2)", "Sucursal Univ. (S3)", "Sucursal Periférico (S4)"]

oferta_base = [50, 70, 80]
demanda_base = [40, 60, 50, 50]

# Costos unitarios de flete en Quetzales (Q) por caja
costos_base = np.array([
    [4, 6, 8, 8],
    [6, 8, 6, 7],
    [5, 7, 11, 4]
])

# Sidebar
with st.sidebar:
    st.header("⚙️ Escenario de Transporte")
    modo = st.radio("Configuración de datos:", ["Caso de Estudio Oficial", "Personalizar Valores"])
    
    if modo == "Personalizar Valores":
        st.write("**Costos unitarios por caja en Quetzales (Q):**")
        df_input_costos = pd.DataFrame(costos_base, index=origenes_nombres, columns=destinos_nombres)
        costos = st.data_editor(df_input_costos).values
    else:
        costos = costos_base.copy()
        st.info("Valores monetarios expresados en Quetzales (GTQ).")

oferta = oferta_base.copy()
demanda = demanda_base.copy()

# ---------------------------------------------------------
# ALGORITMO DEL COSTO MÍNIMO
# ---------------------------------------------------------
def resolver_costo_minimo(mat_costos, sup, dem):
    mat = mat_costos.astype(float).copy()
    s = list(sup)
    d = list(dem)
    filas, cols = mat.shape
    asignacion = np.zeros((filas, cols), dtype=int)
    pasos = []

    f_disp = set(range(filas))
    c_disp = set(range(cols))

    paso = 1
    while f_disp and c_disp:
        min_val = float('inf')
        best_f, best_c = -1, -1

        for r in f_disp:
            for c in c_disp:
                if mat[r, c] < min_val:
                    min_val = mat[r, c]
                    best_f, best_c = r, c

        cant = min(s[best_f], d[best_c])
        asignacion[best_f, best_c] = cant
        subtotal = cant * int(mat[best_f, best_c])

        pasos.append({
            "paso": paso,
            "origen": origenes_nombres[best_f],
            "destino": destinos_nombres[best_c],
            "costo_u": int(min_val),
            "cant": cant,
            "subtotal": subtotal,
            "oferta_rest": s[best_f] - cant,
            "demanda_rest": d[best_c] - cant
        })

        s[best_f] -= cant
        d[best_c] -= cant

        if s[best_f] == 0:
            f_disp.remove(best_f)
        if d[best_c] == 0 and best_c in c_disp:
            c_disp.remove(best_c)

        paso += 1

    total_costo = int(np.sum(asignacion * mat_costos))
    return asignacion, total_costo, pasos

# Esquina Noroeste (para contraste)
def resolver_esquina_noroeste(mat_costos, sup, dem):
    s = list(sup)
    d = list(dem)
    filas, cols = mat_costos.shape
    asig = np.zeros((filas, cols), dtype=int)
    i, j = 0, 0
    while i < filas and j < cols:
        cant = min(s[i], d[j])
        asig[i, j] = cant
        s[i] -= cant
        d[j] -= cant
        if s[i] == 0:
            i += 1
        elif d[j] == 0:
            j += 1
    return asig, int(np.sum(asig * mat_costos))

asig_min, costo_min_total, pasos_list = resolver_costo_minimo(costos, oferta, demanda)
asig_eno, costo_eno_total = resolver_esquina_noroeste(costos, oferta, demanda)
ahorro = costo_eno_total - costo_min_total
pct_ahorro = (ahorro / costo_eno_total) * 100 if costo_eno_total > 0 else 0

# ---------------------------------------------------------
# INTERFAZ Y PESTAÑAS
# ---------------------------------------------------------
tab_tablero, tab_pasos, tab_comparativa = st.tabs([
    "📐 Cuadro de Transporte (Interactivo)", 
    "🔍 Demostración Paso a Paso", 
    "📊 Comparativa Financiera y Ahorro"
])

# ==========================================
# PESTAÑA 1: CUADRO DE TRANSPORTE
# ==========================================
with tab_tablero:
    st.subheader("Cuadro de Transporte General")
    st.markdown("Utiliza este control para explicar primero el problema sin resolver y luego revelar la asignación calculada:")

    # Interruptor para alternar entre "Sin resolver" y "Resuelta"
    col_control1, col_control2 = st.columns([1.5, 2])
    with col_control1:
        estado_resolucion = st.radio(
            "Estado del modelo:",
            ["📋 1. Planteamiento Inicial (Sin Resolver)", "✅ 2. Modelo Resuelto (Con Asignaciones)"],
            horizontal=True
        )
    
    mostrar_resuelto = "2. Modelo Resuelto" in estado_resolucion

    # Indicadores superiores adaptativos
    if mostrar_resuelto:
        st.markdown(f"""
        <div class="metric-container">
            <div class="kpi-card">
                <div class="kpi-title">Costo Total Óptimo</div>
                <div class="kpi-val">Q {costo_min_total:,}</div>
                <span class="kpi-badge-green">Método Costo Mínimo</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Costo Esquina Noroeste</div>
                <div class="kpi-val">Q {costo_eno_total:,}</div>
                <span class="kpi-badge-neutral">Método Base</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Ahorro Logístico</div>
                <div class="kpi-val">Q {ahorro:,}</div>
                <span class="kpi-badge-green">-{pct_ahorro:.1f}% de reducción</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Balance de Cajas</div>
                <div class="kpi-val">200 / 200</div>
                <span class="kpi-badge-neutral">Demanda Satisfecha al 100%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-container">
            <div class="kpi-card">
                <div class="kpi-title">Oferta Disponible Total</div>
                <div class="kpi-val">{sum(oferta)} cajas</div>
                <span class="kpi-badge-neutral">3 Bodegas Operativas</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Demanda Requerida Total</div>
                <div class="kpi-val">{sum(demanda)} cajas</div>
                <span class="kpi-badge-neutral">4 Sucursales</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Estado del Sistema</div>
                <div class="kpi-val" style="color: #15803d;">Balanceado</div>
                <span class="kpi-badge-green">Oferta = Demanda (200)</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Costo Total</div>
                <div class="kpi-val" style="color: #64748b;">Pendiente</div>
                <span class="kpi-badge-neutral">Presiona "Modelo Resuelto"</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Render de la tabla HTML (cambia dinámicamente)
    html_tablero = """<table class="trans-table"><thead><tr><th>Bodega / Origen</th>"""
    for d in destinos_nombres:
        html_tablero += f"<th>{d}</th>"
    html_tablero += "<th>Oferta (Cajas)</th></tr></thead><tbody>"

    for r_idx, orig in enumerate(origenes_nombres):
        html_tablero += f"<tr><td style='font-weight:600; text-align:left; padding-left:14px; background:#f8fafc;'>{orig}</td>"
        for c_idx in range(len(destinos_nombres)):
            c_unit = costos[r_idx, c_idx]
            cant_asig = asig_min[r_idx, c_idx]
            
            # Etiqueta de costo siempre visible en Quetzales
            badge_costo = f"<span class='cell-cost'>Q{c_unit}</span>"
            
            if mostrar_resuelto:
                if cant_asig > 0:
                    contenido_celda = f"{badge_costo}<span class='cell-assigned'>{cant_asig} cajas</span>"
                else:
                    contenido_celda = f"{badge_costo}<span class='cell-empty'>—</span>"
            else:
                contenido_celda = f"{badge_costo}<span class='cell-empty' style='color:#94a3b8;'>—</span>"
            
            html_tablero += f"<td>{contenido_celda}</td>"
        
        html_tablero += f"<td style='font-weight:700; color:#0f172a; font-size:1rem;'>{oferta[r_idx]}</td></tr>"

    html_tablero += "<tr><td style='font-weight:700; text-align:left; padding-left:14px; background:#f1f5f9;'>Demanda (Cajas)</td>"
    for d_val in demanda:
        html_tablero += f"<td style='font-weight:700; color:#0f172a; background:#f1f5f9; font-size:1rem;'>{d_val}</td>"
    html_tablero += f"<td style='font-weight:800; color:#0f172a; background:#e2e8f0; font-size:1.05rem;'>{sum(oferta)}</td></tr>"
    html_tablero += "</tbody></table>"

    st.markdown(html_tablero, unsafe_allow_html=True)
    st.caption("Nota técnica: El recuadro superior derecho en cada celda representa el costo unitario de transporte $c_{ij}$ en Quetzales.")

# ==========================================
# PESTAÑA 2: DEMOSTRACIÓN PASO A PASO
# ==========================================
with tab_pasos:
    st.subheader("Algoritmo del Menor Costo: Secuencia de Iteraciones")
    st.info("Regla de decisión: En cada paso se identifica la casilla con el costo unitario más bajo ($Q$) disponible en la matriz activa, se despacha la cantidad máxima $\\min(\\text{Oferta}_i, \\text{Demanda}_j)$ y se tacha la fila o columna cuyo saldo llegue a cero.")

    for p in pasos_list:
        st.markdown(f"""
        <div class="step-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 700; font-size: 0.95rem; color: #1e40af;">Iteración #{p['paso']}</span>
                <span style="background: #eff6ff; color: #1d4ed8; font-weight:600; padding: 2px 10px; border-radius: 12px; font-size: 0.82rem;">
                    Costo de Flete: Q{p['costo_u']} por caja
                </span>
            </div>
            <p style="margin: 6px 0 2px 0; font-size: 0.92rem; color: #334155;">
                Se asignan <b>{p['cant']} cajas</b> desde <b>{p['origen']}</b> hacia <b>{p['destino']}</b>.
            </p>
            <div style="font-size: 0.82rem; color: #64748b;">
                Subtotal de ruta: <b>Q {p['subtotal']:,}</b> &nbsp;|&nbsp; 
                Oferta restante en bodega: <b>{p['oferta_rest']} cajas</b> &nbsp;|&nbsp; 
                Demanda restante en sucursal: <b>{p['demanda_rest']} cajas</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PESTAÑA 3: COMPARATIVA FINANCIERA
# ==========================================
with tab_comparativa:
    col_g1, col_g2 = st.columns([1, 1.2])

    with col_g1:
        st.subheader("Cálculo de la Función Objetivo")
        st.latex(r"Z_{\min} = \sum_{i=1}^{m} \sum_{j=1}^{n} c_{ij} \cdot x_{ij}")
        st.write("Suma ponderada de rutas asignadas:")
        for p in pasos_list:
            st.markdown(f"• **{p['origen'].split(' ')[0]}** $\\rightarrow$ **{p['destino'].split(' ')[0]}**: {p['cant']} cajas $\\times$ Q{p['costo_u']} = **Q {p['subtotal']}**")
        st.divider()
        st.markdown(f"#### Costo Total Óptimo: **Q {costo_min_total:,}**")

    with col_g2:
        st.subheader("Comparativa de Costo Total (GTQ)")
        fig, ax = plt.subplots(figsize=(6, 3.8))
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')

        metodos = ["Esquina Noroeste\n(Asignación Básica)", "Costo Mínimo\n(Optimizado)"]
        valores = [costo_eno_total, costo_min_total]
        barras = ax.bar(metodos, valores, color=["#f87171", "#34d399"], width=0.45, edgecolor="none")

        ax.set_ylabel("Costo Total de Flete (Quetzales)", fontsize=10, color="#475569")
        ax.set_ylim(0, max(valores) * 1.25)
        ax.tick_params(colors="#475569", labelsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cbd5e1')
        ax.spines['bottom'].set_color('#cbd5e1')
        ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#e2e8f0")

        for bar in barras:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 25, f"Q {int(h):,}", 
                    ha="center", va="bottom", fontweight="bold", fontsize=11, color="#0f172a")

        st.pyplot(fig)
        st.caption(f"El método del costo mínimo logra un ahorro directo de Q {ahorro:,} ({pct_ahorro:.1f}%) frente a la asignación básica.")
        