import streamlit as st

st.set_page_config(
    page_title="Calculadora de notas",
    page_icon="📚",
    layout="centered"
)

SUBJECTS = {
    "Inglés": {
        "Speaking": 0.20,
        "Parcial": 0.24,
        "Final": 0.56,
    },
    "Lengua": {
        "Comportamiento": 0.20,
        "Parcial": 0.30,
        "Final": 0.50,
    },
    "Filosofía": {
        "Comportamiento": 0.20,
        "Debate": 0.30,
        "Final": 0.50,
    },
    "Mate": {
        "Parcial": 0.30,
        "Final": 0.70,
    },
    "Dibujo técnico": {
        "Parcial": 0.30,
        "Final": 0.70,
    },
    "Física": {
        "Parcial": 0.30,
        "Final": 0.70,
    },
}


def calcular_media(notas: dict, pesos: dict) -> float:
    return sum(notas[campo] * peso for campo, peso in pesos.items())


def umbral_objetivo(nota_objetivo: int) -> float:
    # Para redondear a N, hay que superar N - 0.49
    # Ejemplo: para sacar 7 redondeado, hay que superar 6.51
    return nota_objetivo - 0.49


def nota_necesaria_final(resto_componentes: float, peso_final: float, nota_objetivo: int) -> float:
    # Añadimos 0.01 para reflejar el "más de 6.51"
    umbral = umbral_objetivo(nota_objetivo)
    return (umbral - resto_componentes) / peso_final


st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0b1020 0%, #0f172a 100%);
    }

    .main .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        background: linear-gradient(135deg, #4f8cff 0%, #6d5dfc 100%);
        padding: 28px 26px;
        border-radius: 24px;
        color: white;
        box-shadow: 0 14px 35px rgba(79, 140, 255, 0.28);
        margin-bottom: 24px;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
        color: white;
    }

    .hero p {
        margin-top: 10px;
        margin-bottom: 0;
        font-size: 1.02rem;
        opacity: 0.96;
    }

    .section-box {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 20px 20px 12px 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(6px);
    }

    .criteria-pill {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 14px;
        padding: 12px 14px;
        margin-bottom: 10px;
        color: #f8fafc;
        font-size: 1rem;
    }

    .criteria-pill strong {
        color: #9ec5ff;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 14px !important;
    }

    .stNumberInput input {
        border-radius: 12px !important;
    }

    .stButton > button {
        width: 100%;
        border: 0;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        background: linear-gradient(135deg, #4f8cff 0%, #6d5dfc 100%);
        color: white;
        box-shadow: 0 10px 25px rgba(79, 140, 255, 0.22);
    }

    .stButton > button:hover {
        filter: brightness(1.05);
    }

    .footer-text {
        text-align: center;
        color: #94a3b8;
        margin-top: 12px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>📚 Calculadora de notas</h1>
    <p>Calcula tu media o descubre cuánto necesitas sacar en el examen final.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-box">', unsafe_allow_html=True)

asignatura = st.selectbox(
    "Selecciona una asignatura",
    list(SUBJECTS.keys())
)

opcion = st.radio(
    "¿Qué quieres calcular?",
    ["Conocer media", "¿Cuánto debo sacar en el final?"]
)

st.markdown('</div>', unsafe_allow_html=True)

pesos = SUBJECTS[asignatura]

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader(f"Asignatura: {asignatura}")
st.markdown("### Criterios de evaluación")

for campo, peso in pesos.items():
    st.markdown(
        f'<div class="criteria-pill"><strong>{campo}</strong>: {int(peso * 100)}%</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

if opcion == "Conocer media":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### Introduce tus notas")

    notas = {}
    for campo in pesos:
        notas[campo] = st.number_input(
            f"Nota de {campo}",
            min_value=0.0,
            max_value=10.0,
            step=0.01,
            format="%.2f",
            key=f"media_{campo}"
        )

    if st.button("Calcular media"):
        media = calcular_media(notas, pesos)
        redondeada = int(media + 0.49)

        st.success(f"Tu media es: **{media:.2f}**")
        st.info(f"Nota redondeada según tu instituto: **{redondeada}**")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### Introduce tus notas actuales")

    notas = {}
    peso_final = pesos["Final"]

    for campo in pesos:
        if campo != "Final":
            notas[campo] = st.number_input(
                f"Nota de {campo}",
                min_value=0.0,
                max_value=10.0,
                step=0.01,
                format="%.2f",
                key=f"objetivo_{campo}"
            )

    meta = st.selectbox("Meta objetivo", list(range(4, 11)))

    if st.button("Calcular nota necesaria en el final"):
        resto_componentes = sum(
            notas[campo] * peso
            for campo, peso in pesos.items()
            if campo != "Final"
        )

        necesaria = nota_necesaria_final(resto_componentes, peso_final, meta)

        st.markdown(f"### Resultado para alcanzar un **{meta}**")

        if necesaria < 0:
            st.success(
                f"Ya tienes suficiente con lo que llevas. Aunque saques un **0.00** en el final, alcanzarías el **{meta}** redondeado."
            )
        elif necesaria > 10:
            st.error(
                f"Necesitarías un **{necesaria:.2f}** en el final, así que con estas notas no es posible llegar a **{meta}**."
            )
        else:
            st.success(f"Debes sacar al menos un **{necesaria:.2f}** en el final.")
            st.info(
                f"Esto se ha calculado teniendo en cuenta que para redondear a **{meta}** necesitas superar el **{umbral_objetivo(meta):.2f}**."
            )

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<p class="footer-text">Hecho con Streamlit para calcular medias y objetivos de examen.</p>', unsafe_allow_html=True)
