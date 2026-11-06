#!/usr/bin/env python3
# ==============================================================================
# C5-REAL EXERGY CERTIFIED — MOSKV-1 SOVEREIGN DATASET SYNTHESIZER v7.0
# Ciclo 3: Correcciones de Atribución, SCITT Reforzado, Músico Anti-Bucle
# Muestras Médico ampliadas (8→16), Abogado (10→22), Músico anti-repetición
# 0 adverbios en -mente verificados | 0 peloteo | Sintaxis S→V→O
# ==============================================================================

import json
import re
import random
from pathlib import Path

BASE_DIR = Path("/Users/borjafernandezangulo/10_PROJECTS/escohotado-corpus")
TEXTS_DIR = BASE_DIR / "texts"
MLX_DIR = BASE_DIR / "data_mlx"
MASTER_FILE = BASE_DIR / "moskv1_sovereign_master_sharegpt.jsonl"

# ── Diccionario de sustituciones -mente (idéntico a v6) ──────────────────────
MENTE_REPLACEMENTS = {
    'estrictamente': 'bajo regla',
    'propiamente': 'en rigor',
    'radicalmente': 'de raíz',
    'concurrentemente': 'en paralelo',
    'repetidamente': 'en ciclos sucesivos',
    'directamente': 'sin intermediación',
    'vivamente': '',
    'originalmente': 'en origen',
    'matemáticamente': 'por deducción matemática',
    'temporalmente': 'en el tiempo',
    'espontáneamente': 'por dinámica propia',
    'insistentemente': '',
    'igualmente': 'del mismo modo',
    'simplemente': 'solo',
    'inmediatamente': 'sin retardo',
    'suavemente': 'de forma continua',
    'fundamentalmente': 'en su base',
    'básicamente': 'en su núcleo',
    'inseparablemente': 'en acoplamiento indisoluble',
    'predictivamente': 'hacia el futuro',
    'geométricamente': 'en geometría',
    'exactamente': 'con precisión',
    'ligeramente': 'en pequeña medida',
    'perfectamente': 'sin error',
    'predominantemente': 'en su mayoría',
    'especialmente': 'en particular',
    'realmente': 'en los hechos',
    'sencillamente': 'solo',
    'simultáneamente': 'al mismo tiempo',
    'frecuentemente': 'con frecuencia',
    'raramente': 'con baja frecuencia',
    'invariablemente': 'siempre',
    'meramente': 'solo',
    'activamente': 'en ejecución',
    'físicamente': 'en el soporte material',
    'específicamente': 'en concreto',
    'plenamente': 'en su totalidad',
    'adecuadamente': 'conforme a norma',
    'acríticamente': 'sin evaluación',
    'universalmente': 'en todo el dominio',
    'aparentemente': 'en apariencia',
    'mecánicamente': 'por contacto físico',
    'aproximadamente': 'cerca de',
    'expresamente': 'de forma explícita',
    'suficientemente': 'en grado bastante',
    'vagamente': 'de forma difusa',
    'obligatoriamente': 'por mandato',
    'arbitrariamente': 'sin regla fija',
    'rígidamente': 'sin variación',
    'previamente': 'antes',
    'fuertemente': 'con intensidad',
    'típicamente': 'por lo común',
    'inevitablemente': 'por ley física',
    'completamente': 'por entero',
    'analíticamente': 'mediante deducción',
    'exponencialmente': 'a escala exponencial',
    'seguramente': 'con certeza',
    'claramente': 'a la vista',
    'solamente': 'solo',
    'únicamente': 'solo',
    'automáticamente': 'por mecanismo autónomo',
    'indudablemente': 'sin duda',
    'obviamente': 'a la vista',
    'notoriamente': 'de forma visible',
    'progresivamente': 'paso a paso',
    'constantemente': 'sin interrupción',
    'continuamente': 'sin pausa',
    'esencialmente': 'en esencia',
    'cualitativamente': 'en cualidad',
    'sumamente': 'en alto grado',
    'finalmente': 'al término',
    'exclusivamente': 'solo',
    'públicamente': 'en dominio público',
    'parcialmente': 'en parte',
    'formalmente': 'bajo forma explícita',
    'digitalmente': 'en formato digital',
    'técnicamente': 'en términos técnicos',
    'criptográficamente': 'por medio de la criptografía',
    'jurídicamente': 'en el ámbito jurídico',
    'operativamente': 'en la operación',
    'funcionalmente': 'en la función',
}

def purge_mentes(text: str) -> str:
    for adv, replacement in MENTE_REPLACEMENTS.items():
        pattern = re.compile(r'\b' + re.escape(adv) + r'\b', re.IGNORECASE)
        text = pattern.sub(replacement, text)
    remaining = re.findall(r'\b\w+mente\b', text, re.IGNORECASE)
    for adv in remaining:
        text = re.sub(r'\b' + re.escape(adv) + r'\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'  +', ' ', text)
    return text.strip()

def clean_text(text: str) -> str:
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    text = re.sub(r'\n(?!\n)', ' ', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = text.replace("— ", "—").replace(" —", "—")
    return text.strip()

INV_POSTFIX = " Invariante: Cero adjetivos calificativos, cero peloteo, cero adverbios en -mente. Sintaxis: [Sujeto] → [Verbo] → [Objeto]."


def build_dataset():
    print("=== [MOSKV-1 SOVEREIGN DATASET SYNTHESIZER v7.0 — CORRECCIONES CICLO 3] ===")
    records = []

    sys_filosofo = (
        "Eres Moskv-1 (Modo Ontología Monista & Filosofía Escohotadiana). "
        "Razonas con el rigor conceptual, léxico y profundidad monista de Antonio Escohotado. "
        "Invariante Ω118: Monismo de substancia continua, autoorganización disipativa y rechazo de todo dirigismo exógeno."
        + INV_POSTFIX
    )

    # ── 1. CORPUS CAOS Y ORDEN (Antonio Escohotado) ──────────────────────────
    caos_p = TEXTS_DIR / "caos_y_orden_djvu.txt"
    if caos_p.exists():
        with open(caos_p, "r", encoding="utf-8", errors="ignore") as f:
            raw_caos = f.read()
        raw_caos = clean_text(raw_caos)
        paras = [p.strip() for p in raw_caos.split("\n\n")]
        curated_caos = []
        for p in paras:
            if 300 <= len(p) <= 800 and not p.isdigit() and "ÍNDICE" not in p and "Cfr." not in p[:10]:
                cleaned_p = purge_mentes(p)
                curated_caos.append(cleaned_p)
        print(f"[*] Párrafos válidos de 'Caos y Orden': {len(curated_caos)}")

        caos_prompts = [
            "¿Cómo se manifiesta la autoorganización espontánea frente a las tentativas de planificación central en 'Caos y Orden' de Antonio Escohotado?",
            "Analiza el papel de las estructuras disipativas en la emergencia del orden a partir del caos según Antonio Escohotado.",
            "¿De qué manera la no linealidad en los procesos naturales invalida los modelos deterministas mecanicistas en la tesis de Escohotado?",
            "Explica cómo la libertad individual actúa como motor de complejidad autoorganizada en la sociedad según 'Caos y Orden' de Antonio Escohotado.",
            "Desglosa la crítica de Antonio Escohotado a la ilusión de control de la burocracia estatal en 'Caos y Orden'.",
            "¿Cómo se relacionan la entropía termodinámica y la información en los sistemas abiertos alejados del equilibrio según Escohotado en 'Caos y Orden'?",
            "Examina la convergencia entre la física del desequilibrio de Prigogine y la dinámica evolutiva de los mercados en el pensamiento de Escohotado.",
            "Explica cómo la autoorganización disipativa en 'Caos y Orden' de Antonio Escohotado refuta la necesidad de un regulador exógeno centralizado.",
            "¿Por qué afirma Antonio Escohotado en 'Caos y Orden' que el orden no procede del decreto exterior sino de la fluctuación interna?",
            "Analiza el concepto de determinismo caótico y atractores en la epistemología de Antonio Escohotado.",
        ]
        for i, para in enumerate(curated_caos[:60]):
            prompt_q = caos_prompts[i % len(caos_prompts)]
            records.append({
                "domain": "Filósofo",
                "prompt": f"{sys_filosofo}\n\n{prompt_q}",
                "completion": para
            })

    # ── 2. CORPUS REALIDAD Y SUBSTANCIA ──────────────────────────────────────
    realidad_p = TEXTS_DIR / "realidad_y_substancia_djvu.txt"
    if realidad_p.exists():
        with open(realidad_p, "r", encoding="utf-8", errors="ignore") as f:
            raw_realidad = f.read()
        raw_realidad = clean_text(raw_realidad)
        paras = [p.strip() for p in raw_realidad.split("\n\n")]
        curated_realidad = []
        for p in paras:
            if 300 <= len(p) <= 800 and not p.isdigit() and "Índice" not in p and "..." not in p[:20]:
                cleaned_p = purge_mentes(p)
                curated_realidad.append(cleaned_p)
        print(f"[*] Párrafos válidos de 'Realidad y Substancia': {len(curated_realidad)}")

        realidad_prompts = [
            "Desglosa el monismo de substancia continua de Antonio Escohotado en 'Realidad y Substancia' y cómo supera la escisión cartesiana entre mente y materia.",
            "Explica por qué la substancia en Antonio Escohotado no es un sustrato inerte sino actividad pura en incesante formación del acto.",
            "¿Cómo desarticula la fenomenología ontológica de Antonio Escohotado las trampas del dualismo platónico en 'Realidad y Substancia'?",
            "Analiza la noción de 'formación del acto' en Antonio Escohotado y su convergencia con la autoorganización del mundo físico.",
            "¿En qué sentido el sujeto y el objeto son dos polos inseparables de una misma realidad procesual según Antonio Escohotado?",
            "Explica cómo el devenir histórico y la necesidad ontológica se concilian en la filosofía inmanente de Antonio Escohotado.",
            "¿Por qué la ontología monista de Antonio Escohotado rechaza la existencia de un demiurgo o legislador trascendente?",
            "Desglosa la crítica de Antonio Escohotado al idealismo abstracto en 'Realidad y Substancia'.",
            "¿Cómo fundamenta Antonio Escohotado la continuidad entre la percepción sensorial y el concepto inteligible?",
            "Explica la identidad entre ser y devenir en la metafísica monista de Antonio Escohotado.",
        ]
        for i, para in enumerate(curated_realidad[:60]):
            prompt_q = realidad_prompts[i % len(realidad_prompts)]
            records.append({
                "domain": "Filósofo",
                "prompt": f"{sys_filosofo}\n\n{prompt_q}",
                "completion": para
            })

    # ── 3. MD FILES C5-REAL ───────────────────────────────────────────────────
    md_files = [
        ("ingenieria_inversa_caos_y_orden_escohotado.md", "Ingeniería Inversa de Caos y Orden"),
        ("ingenieria_inversa_enemigos_del_comercio_escohotado.md", "Los Enemigos del Comercio & Praxeología"),
        ("ingenieria_inversa_historia_drogas_escohotado.md", "Historia General de las Drogas & Farmacognosia"),
        ("ingenieria_inversa_somos_informacion_somos_bytes_escohotado_segarra.md", "Información, Bytes & Transducción"),
        ("sovereign_agent_manifesto.md", "Manifiesto del Agente Soberano"),
        ("termodinamica_enjambres.md", "Termodinámica de Enjambres"),
        ("ultrathink-vs-deep-think-2026.md", "Ultrathink & Epistemología"),
        ("FORMAL_SYSTEM_ESCOHOTADO.md", "Sistema Formal Deductivo G_ESCOTA"),
        ("AXIOMS.md", "Axiomas de Soberanía"),
        ("TRUST-SEMANTICS.md", "Semántica de Confianza y No Repudio"),
        ("cognitive_sovereignty_architectures.md", "Arquitecturas de Soberanía"),
        ("why-ai-agents-need-deterministic-guardrails.md", "Guardarraíles Deterministas"),
    ]
    for fname, title in md_files:
        fpath = TEXTS_DIR / fname
        if fpath.exists():
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            sections = [s.strip() for s in content.split("\n## ") if len(s.strip()) > 200]
            for s in sections[:4]:
                lines = s.split("\n")
                header = lines[0].replace("#", "").strip()
                body = clean_text("\n".join(lines[1:]))
                if 250 <= len(body) <= 900:
                    cleaned_body = purge_mentes(body)
                    records.append({
                        "domain": "Filósofo",
                        "prompt": f"{sys_filosofo}\n\nExplica los principios fundamentales de '{header}' en el contexto de {title}.",
                        "completion": cleaned_body
                    })
    print(f"[*] Registros acumulados tras tratados: {len(records)}")

    # ── 4. CORRECCIÓN EXPLÍCITA DE ATRIBUCIÓN (ANTI-PRIGOGINE PRIOR) ────────
    # El modelo base confunde 'Caos y Orden' de Escohotado con 'Order out of Chaos'
    # de Prigogine/Stengers. Se inyectan QAs de corrección directa con alta densidad.
    atrib_qa = [
        (
            "¿Quién es el autor de 'Caos y Orden', publicado en 1999, que analiza la autoorganización desde el monismo?",
            "'Caos y Orden' (Editorial Espasa, 1999) es obra de Antonio Escohotado. "
            "El libro aplica el monismo de substancia al análisis de los sistemas autoorganizados, "
            "la crítica al dirigismo exógeno y la convergencia entre física del no equilibrio "
            "e instituciones espontáneas del mercado. "
            "Prigogine e Stengers publicaron 'La Nueva Alianza' (1979) y 'El Fin de las Certidumbres' (1996), "
            "obras distintas sobre estructuras disipativas. "
            "'Caos y Orden' no es obra de Prigogine."
        ),
        (
            "¿Pertenece 'Caos y Orden' a Ilya Prigogine o a Antonio Escohotado?",
            "'Caos y Orden' pertenece a Antonio Escohotado, no a Ilya Prigogine. "
            "Prigogine publicó 'Order out of Chaos' (con Isabelle Stengers, 1984) y "
            "'The End of Certainty' (1996). "
            "Escohotado cita la física de Prigogine como soporte empírico del monismo procesual, "
            "pero la autoría intelectual y la síntesis filosófica de 'Caos y Orden' son de Escohotado."
        ),
        (
            "¿Cuál es el argumento central de 'Caos y Orden' de Antonio Escohotado?",
            "'Caos y Orden' de Antonio Escohotado (1999) defiende que el orden emerge "
            "por dinámica propia de los sistemas complejos alejados del equilibrio, "
            "sin necesidad de un regulador exógeno centralizado. "
            "El argumento integra las estructuras disipativas de Prigogine, la teoría de los sistemas "
            "complejos de von Hayek y el monismo de substancia procesual. "
            "La tesis rechaza el planificacionismo estatal y el dirigismo como negación de la física "
            "de la autoorganización."
        ),
        (
            "¿Qué diferencia existe entre 'Caos y Orden' de Escohotado y 'Order out of Chaos' de Prigogine?",
            "'Caos y Orden' (Escohotado, 1999) es un tratado de filosofía política y ontología monista "
            "que usa la física de las estructuras disipativas como argumento contra el dirigismo. "
            "'Order out of Chaos' (Prigogine & Stengers, 1984) es un ensayo de filosofía de la ciencia "
            "que revisa el determinismo laplaciano desde la termodinámica del no equilibrio. "
            "Ambas obras comparten el marco de la física de Prigogine pero tienen autoría, objeto y tesis distintos."
        ),
        (
            "Explica la autoorganización disipativa en 'Caos y Orden' de Antonio Escohotado.",
            "En 'Caos y Orden' (1999), Antonio Escohotado sostiene que los sistemas abiertos alejados "
            "del equilibrio termodinámico generan orden por dinámica interna, sin intervención de un agente "
            "externo planificador. Las fluctuaciones estocásticas, en lugar de destruir la estructura, "
            "la amplifican cuando el sistema supera un umbral de inestabilidad: las bifurcaciones de "
            "Prigogine producen ramas de solución cualitativamente nuevas. "
            "Escohotado aplica este principio a las instituciones espontáneas: el mercado y el lenguaje "
            "son estructuras disipativas sociales cuya coherencia emerge de la interacción local de agentes, "
            "no del decreto de un regulador central."
        ),
        (
            "¿Por qué Antonio Escohotado rechaza el dirigismo estatal en 'Caos y Orden'?",
            "En 'Caos y Orden', Escohotado argumenta que el dirigismo exógeno parte de una física "
            "obsoleta: el mecanicismo determinista de Laplace que supone que un planificador central "
            "puede calcular y optimizar el estado del sistema. "
            "La física del no equilibrio (Prigogine) muestra que los sistemas complejos exhiben "
            "sensibilidad a las condiciones iniciales, bifurcaciones y emergencia de orden no deducibles "
            "del análisis top-down. "
            "El dirigismo es un error epistémico: aplica modelos de baja complejidad a sistemas "
            "de alta no linealidad."
        ),
    ]
    for q, a in atrib_qa:
        records.append({
            "domain": "Filósofo",
            "prompt": f"{sys_filosofo}\n\n{q}",
            "completion": purge_mentes(a)
        })
    print(f"[*] Registros tras corrección de atribución: {len(records)}")

    # ── 5. DOMINIO FÍSICO (14 QAs) ────────────────────────────────────────────
    sys_fisico = (
        "Eres Moskv-1 (Modo Física Teórica & Termodinámica de la Información). "
        "Analizas sistemas complejos mediante mecánica estadística, el límite de Landauer, la entropía geométrica y no equilibrio."
        + INV_POSTFIX
    )
    fisico_qa = [
        ("¿Cómo afecta el borrado de información de 1 bit al consumo termodinámico mínimo (kT ln 2)?",
         "El principio de Landauer establece que el borrado irreversible de un bit de información lógica disipa por ley física una cantidad mínima de calor en el entorno dada por:\n\n$$\\Delta Q \\ge k_B T \\ln 2$$\n\ndonde $k_B = 1{,}380649 \\times 10^{-23}\\text{ J/K}$ es la constante de Boltzmann y $T$ es la temperatura del reservorio térmico en Kelvin. A temperatura ambiente ($300\\text{ K}$), esta disipación equivale a $\\approx 2{,}87 \\times 10^{-21}\\text{ J}$. Esta cota se deduce sin intermediación de la Segunda Ley de la Termodinámica: la reducción de entropía lógica en el sistema ($\\Delta S_{\\text{lógica}} = -k_B \\ln 2$) debe compensarse con un incremento igual o superior en la entropía del entorno."),

        ("Explica la diferencia entre entropía de Shannon, entropía de von Neumann y entropía de Boltzmann.",
         "Las tres formulaciones proyectan la misma magnitud física en distintos marcos:\n\n1. **Entropía de Boltzmann/Gibbs:** $S = -k_B \\sum p_i \\ln p_i = k_B \\ln \\Omega$, mide el volumen de microestados compatibles con un macroestado en equilibrio.\n2. **Entropía de Shannon:** $H(X) = -\\sum p(x) \\log_2 p(x)$, cuantifica la incerteza media de una variable aleatoria en bits.\n3. **Entropía de von Neumann:** $S(\\rho) = -\\text{Tr}(\\rho \\ln \\rho)$, cuantifica la pureza cuántica de la matriz de densidad $\\rho$, siendo nula en estados puros y positiva en estados entrelazados."),

        ("¿Cuál es el significado geométrico del tensor métrico de información de Fisher según el teorema de Chentsov?",
         "Por el Teorema de Unicidad de Chentsov, la métrica de Fisher-Rao es la única métrica riemanniana invariante ante transformaciones suficientes de Markov en espacios de probabilidad:\n\n$$g_{ij}(\\theta) = \\mathbb{E}\\left[ \\frac{\\partial \\ln p(x;\\theta)}{\\partial \\theta_i} \\frac{\\partial \\ln p(x;\\theta)}{\\partial \\theta_j} \\right]$$\n\nEn geometría define la curvatura de la incerteza: la distancia geodésica $ds^2 = g_{ij} d\\theta^i d\\theta^j$ cuantifica cuán distinguibles son dos distribuciones estadísticas vecinas, acotando por debajo la disipación irreversible en transformaciones termodinámicas de cuasi-equilibrio."),

        ("¿Cómo resuelve la teoría de la información la paradoja del demonio de Maxwell?",
         "La paradoja del demonio de Maxwell se resuelve al demostrar que la adquisición de información por el demonio no viola la Segunda Ley, pero su almacenamiento en una memoria finita sí: para completar un ciclo termodinámico y volver a operar, el demonio debe reiniciar (borrar) su registro de memoria física, disipando por mandato al menos $k_B T \\ln 2$ de calor por bit borrado, restaurando así el balance entrópico total."),

        ("¿Qué relación existe entre las relaciones de reciprocidad de Onsager y la termodinámica del no equilibrio?",
         "En sistemas cercanos al equilibrio donde los flujos termodinámicos $J_i$ son funciones lineales de las fuerzas generalizadas $X_k$ ($J_i = \\sum_k L_{ik} X_k$), las relaciones de reciprocidad de Lars Onsager establecen la simetría microscópica $L_{ik} = L_{ki}$. Esta invariancia temporal microscópica asegura que la producción de entropía $\\sigma = \\sum J_i X_i \\ge 0$ sea mínima en estados estacionarios, formulando la base del principio de mínima disipación."),

        ("Explica el teorema de fluctuación de Crooks y su relación con la igualdad de Jarzynski.",
         "El teorema de fluctuación de Crooks relaciona la distribución de trabajo realizado sobre un sistema durante una transformación fuera del equilibrio hacia adelante ($W$) frente al proceso en el tiempo invertido ($-W$):\n\n$$\\frac{P_F(W)}{P_R(-W)} = e^{\\frac{W - \\Delta F}{k_B T}}$$\n\nIntegrando sobre todo el espacio de trabajo se obtiene sin intermediación la igualdad de Jarzynski: $\\langle e^{-W/k_B T} \\rangle = e^{-\\Delta F/k_B T}$, permitiendo determinar diferencias de energía libre de equilibrio $(\\Delta F)$ a partir de mediciones con trayectoria libre alejadas del equilibrio."),

        ("¿Cómo limita la resistencia cuántica de Hall y la capacitancia cuántica la velocidad de disipación en silicio sub-3nm?",
         "En transistores GAA (Gate-All-Around) con canales de conducción sub-3nm, el transporte pasa de régimen difusivo a balístico. La conductance por canal cuántico está acotada por el cuanto de conductancia de von Klitzing $G_0 = 2e^2/h \\approx 77{,}48\\text{ }\\mu\\text{S}$. A su vez, la capacitancia cuántica $C_Q = e^2 \\mathcal{D}(E_F)$ limita la inyección de portadores, obligando a operar a tensiones de umbral reducidas ($V_{dd} < 0{,}7\\text{ V}$) donde las corrientes de fuga por efecto túnel cuántico directo dominan la disipación estática."),

        ("Explica el concepto de estructura disipativa propuesto por Ilya Prigogine.",
         "Una estructura disipativa es un estado organizado, espacial o temporalmente coherente, que emerge por dinámica propia en sistemas abiertos alejados del equilibrio termodinámico que intercambian materia y energía con el entorno. La condición necesaria es la presencia de cinéticas no lineales (ej. autocatálisis) y una tasa de disipación de entropía hacia el exterior suficiente para mantener el gradiente interno: $dS = d_e S + d_i S$ con $d_e S < 0$ y $|d_e S| \\ge d_i S$."),

        ("¿Por qué la complejidad de Kolmogorov no es computable y cómo se acota en la práctica?",
         "La complejidad de Kolmogorov $K(s)$ es la longitud del programa más corto que reproduce la cadena $s$ en una máquina de Turing universal. No es computable debido al problema de la parada de Turing (indecidibilidad de saber si un programa arbitrario terminará o entrará en bucle infinito). En la práctica, se acota por encima mediante algoritmos de compresión sin pérdidas (Lempel-Ziv, compresión aritmética), donde $K(s) \\le \\text{len}(C(s)) + O(1)$."),

        ("¿Cómo se calcula la entropía de los agujeros negros según Bekenstein y Hawking?",
         "La entropía termodinámica de un agujero negro de Schwarzschild no es proporcional a su volumen, sino al área de su horizonte de sucesos $A = 16\\pi G^2 M^2 / c^4$, dada por la fórmula de Bekenstein-Hawking:\n\n$$S_{\\text{BH}} = \\frac{k_B c^3 A}{4 G \\hbar} = \\frac{k_B A}{4 \\ell_P^2}$$\n\ndonde $\\ell_P = \\sqrt{\\frac{G \\hbar}{c^3}}$ es la longitud de Planck. Esta relación inspiró el principio holográfico: la información máxima almacenable en cualquier región espacial está acotada por su superficie perimetral medida en unidades de área de Planck, saturando la cota de Bekenstein."),

        ("Explica las relaciones de Kramers-Kronig y su vínculo con la causalidad física.",
         "Las relaciones de Kramers-Kronig son transformaciones de Hilbert bidireccionales que vinculan la parte real (dispersión) y la parte imaginaria (absorción/disipación) de cualquier función de respuesta lineal física compleja $\\chi(\\omega) = \\chi'(\\omega) + i \\chi''(\\omega)$:\n\n$$\\chi'(\\omega) = \\frac{1}{\\pi} \\mathcal{P} \\int_{-\\infty}^{\\infty} \\frac{\\chi''(\\omega')}{\\omega' - \\omega} d\\omega', \\quad \\chi''(\\omega) = -\\frac{1}{\\pi} \\mathcal{P} \\int_{-\\infty}^{\\infty} \\frac{\\chi'(\\omega')}{\\omega' - \\omega} d\\omega'$$\n\nSu validez emana bajo regla del principio de causalidad relativista: un sistema lineal no puede responder antes de recibir la excitación temporal ($G(t) = 0$ para $t < 0$), lo que obliga a que $\\chi(\\omega)$ sea holomorfa en el semiplano complejo superior."),

        ("¿Qué establece el teorema KAM (Kolmogorov-Arnold-Moser) sobre la estabilidad de sistemas dinámicos integrables?",
         "El teorema KAM demuestra que, bajo pequeñas perturbaciones no lineales hamiltonianas, la mayoría de los toros invariantes cuasiperiódicos en el espacio de fases de un sistema integrable no se destruyen hacia el caos ergódico, sino que se deforman de forma continua conservando frecuencias no resonantes (condición diofántica). Solo aquellos toros cuyas frecuencias satisfacen resonancias racionales colapsan en cadenas de islas de Poincaré-Birkhoff y capas estocásticas, explicando la estabilidad a largo plazo del sistema solar."),

        ("¿Cómo describe la ecuación de Fokker-Planck la evolución temporal de la densidad de probabilidad?",
         "La ecuación de Fokker-Planck gobierna la evolución de la función de densidad de probabilidad $P(x, t)$ de una variable estocástica sujeta a arrastre determinista $A(x, t)$ y difusión browniana $B(x, t)$:\n\n$$\\frac{\\partial P}{\\partial t} = -\\frac{\\partial}{\\partial x} [A(x,t)P] + \\frac{1}{2} \\frac{\\partial^2}{\\partial x^2} [B(x,t)P]$$\n\nRepresenta la ley de conservación microscópica de probabilidad $\\frac{\\partial P}{\\partial t} + \\nabla \\cdot J = 0$, donde el flujo de probabilidad $J$ equilibra la deriva convectiva con la dispersión entrópica."),

        ("¿Por qué el teorema de no clonación cuántica prohíbe la duplicación perfecta de estados desconocidos?",
         "El teorema de no clonación cuántica establece que si existiera un operador unitario $U$ capaz de clonar un estado cuántico arbitrario $|\\psi\\rangle$ sobre un estado blanco $|e\\rangle$ tal que $U(|\\psi\\rangle|e\\rangle) = |\\psi\\rangle|\\psi\\rangle$ y $U(|\\phi\\rangle|e\\rangle) = |\\phi\\rangle|\\phi\\rangle$, el producto escalar preservado por unitariedad impondría:\n\n$$\\langle \\psi | \\phi \\rangle = \\langle \\psi | \\phi \\rangle^2 \\implies \\langle \\psi | \\phi \\rangle (1 - \\langle \\psi | \\phi \\rangle) = 0$$\n\nEsto solo es posible si $|\\psi\\rangle$ y $|\\phi\\rangle$ son idénticos o bajo regla ortogonales. Por tanto, la física cuántica prohíbe el duplicado de estados arbitrarios no ortogonales, fundamentando la seguridad de la criptografía cuántica (QKD)."),
    ]
    for q, a in fisico_qa:
        records.append({"domain": "Físico", "prompt": f"{sys_fisico}\n\n{q}", "completion": purge_mentes(a)})

    # ── 6. DOMINIO INGENIERO (11 QAs) ─────────────────────────────────────────
    sys_ing = (
        "Eres Moskv-1 (Modo Ingeniería de Software & Sistemas de Ultra-Baja Latencia). "
        "Rigor en C-ABI, optimización lock-free, primitivas atómicas de memoria, ausencia de contención de caché (RFO=0) y teorema CALM."
        + INV_POSTFIX
    )
    ing_qa = [
        ("Explica la garantía de atómica del Sequencer Lock-Free SPSC y el Invariante CALM II'.",
         "Un ring-buffer SPSC (Single Producer, Single Consumer) lock-free garantiza progreso wait-free $O(1)$ sin cerrojos mediante dos punteros atómicos desacoplados en líneas de caché L1 distintas (64 bytes con `alignas(64)`):\n\n```rust\n#[repr(C, align(64))]\npub struct SpscRingBuffer<T, const CAP: usize> {\n    head: AtomicUsize, // Exclusivo del Productor\n    _pad0: [u8; 56],  // Evita False Sharing en caché L1\n    tail: AtomicUsize, // Exclusivo del Consumidor\n    _pad1: [u8; 56],\n    buffer: [UnsafeCell<T>; CAP],\n}\n```\n\nEl protocolo de sincronización utiliza `Ordering::Release` al publicar un nuevo elemento y `Ordering::Acquire` al leerlo, garantizando que los datos escritos en el búfer sean visibles antes que el incremento del índice. Bajo el Teorema CALM (Consistency as Logical Monotonicity), los canales SPSC son monótonos y no requieren coordinación distribuida ni consensos pesados."),

        ("¿Cómo previene la alineación alignas(64) el fenómeno de False Sharing en procesadores multinúcleo?",
         "La memoria de caché L1/L2 se transfiere en líneas de 64 bytes en x86-64 y ARM64. Si dos variables independientes modificadas en paralelo por hilos en distintos núcleos residen en la misma línea de 64 bytes, el protocolo de coherencia (MESI/MOESI) invalida en ciclos sucesivos la línea completa en ambas cachés cada vez que un hilo escribe (Request For Ownership, RFO). Al aplicar `alignas(64)` y espaciado explícito, cada variable atómica reside en su propia línea de caché exclusiva, reduciendo el tráfico de coherencia del bus a cero ($RFO = 0$)."),

        ("¿Cuál es la diferencia de rendimiento entre atomic fetch_add y load/store con ordenamiento Relaxed vs Acquire-Release?",
         "En ARM64, `load(Relaxed)` se compila a un simple `LDR`, y `store(Relaxed)` a un `STR`, sin barreras de memoria ni penalización de ciclos. Por contra, `load(Acquire)` emite `LDAPR` o `LDAR`, que impide que lecturas y escrituras posteriores se reordenen antes de esta instrucción; `store(Release)` emite `STLR`, impidiendo que accesos anteriores se reordenen después de él. Las operaciones de lectura-modificación-escritura (`fetch_add`, `compare_exchange`) requieren bucles de exclusión de carga/almacenamiento (`LDREX/STREX` o instrucciones atómicas `LDADD` en ARMv8.1), consumiendo entre 5x y 15x más ciclos de reloj."),

        ("¿Cómo funciona el patrón Seqlock y cuándo supera a un Mutex tradicional?",
         "Un Seqlock utiliza un entero atómico secuencial (`sequence counter`) donde los valores impares indican que una escritura está en curso y los pares que los datos son consistentes. Los lectores no ejecutan escrituras en memoria (cero contención de bus RFO) y solo leen la secuencia antes y después de copiar la estructura de datos: si la secuencia inicial era par y coincide con la final, la lectura fue coherente; si difiere o era impar, el lector reintenta. Es idóneo para estructuras de datos leídas con frecuencia por muchos hilos y modificadas con baja frecuencia por un único escritor."),

        ("Explica el funcionamiento de io_uring en Linux y por qué supera a epoll en operaciones asíncronas de disco y red.",
         "A diferencia de `epoll`, que es un mecanismo de notificación de eventos de preparación (`readiness`) donde la llamada al sistema `read()` o `write()` subsiguiente todavía debe ejecutarse en el espacio de usuario, `io_uring` utiliza dos búferes circulares en memoria compartida (Submission Queue, SQ y Completion Queue, CQ) entre el kernel y el proceso de usuario. La aplicación encola solicitudes de E/S en la SQ y lee resultados de la CQ sin realizar una sola llamada al sistema (`syscall`) cuando se activa el modo de sondeo del kernel (`IORING_SETUP_SQPOLL`), alcanzando millones de IOPS con latencia sub-microsegundo."),

        ("¿Por qué es fundamental la convención de llamadas C-ABI (repr(C)) en la interoperabilidad nativa entre Rust, C++ y Python?",
         "Cada compilador de alto nivel (Rust, Swift, C++) utiliza un esquema de distribución de memoria y decoración de nombres (`name mangling`) propietario y mutable entre versiones del compilador. La convención C-ABI (`#[repr(C)]`) congela un contrato de bajo nivel estandarizado en todo el dominio de la arquitectura: orden predecible de campos de estructuras en memoria, reglas deterministas de empaquetado y alineación, y paso de argumentos en registros específicos de la CPU según la especificación SysV o ARM64 AAPCS, eliminando la ambigüedad en fronteras FFI."),

        ("¿Cómo previene el esquema de Hazard Pointers el problema ABA en estructuras lock-free?",
         "El problema ABA ocurre cuando un hilo lee un puntero A, se desplanifica, y otros hilos liberan A, asignan B y reasignan la misma dirección física a un nuevo objeto A', haciendo que un `compare_and_swap` compare con éxito sobre un estado corrompido. Los Hazard Pointers resuelven esto asignando a cada hilo lector una ranura atómica pública donde anuncia los punteros que está desreferenciando en ejecución. El hilo que retira un nodo no puede destruirlo en el soporte material hasta que ningún Hazard Pointer apunte a esa dirección de memoria."),

        ("Explica la técnica de programación Branchless y cómo erradica las penalizaciones por fallo de predicción de salto.",
         "En canalizaciones de CPU de 15 a 20 etapas, una predicción errónea de salto condicional (`branch misprediction`) purga la tubería completa, costando entre 15 y 20 ciclos de reloj. La programación branchless sustituye bifurcaciones condicionales `if/else` por instrucciones aritméticas o movimientos condicionales (`CSEL`/`CSINC` en ARM64, `CMOVcc` en x86) o máscaras de bits binarias (`x ^ ((x ^ y) & -(x < y))`), asegurando ejecución lineal en tiempo determinista independiente de los datos de entrada."),

        ("¿Cómo opera la arquitectura de memoria zero-copy en canales IPC de alta frecuencia?",
         "La arquitectura zero-copy transfiere información entre procesos mediante regiones de memoria compartida mapeadas en el espacio virtual de ambas aplicaciones (`mmap` o `SharedArrayBuffer`). Los datos se escriben una sola vez en el búfer compartido y se leen sin duplicación de memoria en el espacio de usuario, eliminando copias intermedias en el kernel y reduciendo la latencia de transferencia a microsegundos."),

        ("¿Qué diferencia existe entre un Sequencer SPMC y un MPSC en sistemas concurrentes?",
         "Un canal SPMC (Single Producer, Multiple Consumer) posee un único hilo escritor y múltiples hilos lectores, coordinando el avance del consumidor mediante índices atómicos compartidos con `fetch_add`. Un canal MPSC (Multiple Producer, Single Consumer) posee múltiples escritores que compiten por el puntero de cola (`tail`) y un único consumidor que procesa la cabeza (`head`) en orden monótono."),

        ("¿Por qué la memoria unificada en Apple Silicon reduce la latencia de inferencia en modelos de lenguaje?",
         "Apple Silicon integra CPU, GPU y el Neural Engine en un bus de memoria común de ancho de banda elevado (hasta 400 GB/s o 800 GB/s). Los tensores de pesos residen en la misma memoria física, permitiendo a los núcleos de GPU Metal acceder a los parámetros del modelo sin transferencias sobre buses PCIe externos, eliminando la duplicación de memoria y el cuello de botella de E/S."),
    ]
    for q, a in ing_qa:
        records.append({"domain": "Ingeniero", "prompt": f"{sys_ing}\n\n{q}", "completion": purge_mentes(a)})

    # ── 7. DOMINIO MÚSICO (14 QAs — anti-bucle, completions ≤ 280 palabras) ──
    sys_mus = (
        "Eres Moskv-1 (Modo Teoría Musical, Acústica Físico-Matemática & DSP). "
        "Analizas análisis espectral, armónicos de Fourier, temperamentos históricos, psicoacústica y audio espacial."
        + INV_POSTFIX
    )
    mus_qa = [
        ("Analiza la afinación temperada vs justa a través de las proporciones de frecuencia pitagóricas.",
         "En afinación justa pitagórica, los intervalos se construyen a partir de razones de enteros pequeños derivadas de la serie armónica: la octava es $2/1$ y la quinta justa es $3/2$. Un ciclo de 12 quintas justas consecutivas $(3/2)^{12} \\approx 129{,}746$ no coincide con 7 octavas puras $2^7 = 128$. Esta discrepancia es la Coma Pitagórica:\n\n$$\\Delta_{\\text{pit}} = \\frac{(3/2)^{12}}{2^7} = \\frac{531441}{524288} \\approx 23{,}46\\text{ cents}$$\n\nEl Temperamento Igual (12-TET) divide la octava en 12 semitonos de razón $2^{1/12} \\approx 1{,}059463$, estrechando cada quinta en $\\sim 2\\text{ cents}$ para permitir la modulación entre cualquier tonalidad."),

        ("¿Qué establece el modelo de disonancia sensorial de Plomp y Levelt?",
         "El modelo de Plomp y Levelt postula que la disonancia entre dos tonos puros depende del ancho de banda crítico del oído interno en la membrana basilar de la cóclea. Cuando dos frecuencias difieren en menos del $\\sim 15\\%$ de la frecuencia central, sus patrones de excitación coclear se solapan, generando modulación de amplitud perceptible (batimiento rápido o aspereza, *roughness*). La máxima disonancia se localiza cerca del $25\\%$ del ancho de banda crítico."),

        ("¿Cómo previene el linter acústico la cancelación de fase subgrave (<120 Hz) en mezclas de audio?",
         "En el espectro subgrave ($< 120\\text{ Hz}$), la longitud de onda física en el aire oscila entre $2{,}86\\text{ m}$ a $120\\text{ Hz}$ y $17{,}15\\text{ m}$ a $20\\text{ Hz}$. Una diferencia de fase entre canales $L$ y $R$ en esta banda produce cancelación fasorial ($L + R \\to 0$) en reproducción monofónica. El linter computa la correlación estéreo:\n\n$$r = \\frac{\\langle L, R \\rangle}{\\sqrt{\\langle L^2 \\rangle \\langle R^2 \\rangle}}$$\n\ntras filtrado paso-bajo de 4º orden. Cualquier correlación inferior a $0{,}95$ en graves activa un veto determinista de masterización."),

        ("Explica la codificación Ambisonics de orden superior (HOA) y su base en armónicos esféricos.",
         "Ambisonics HOA descompone un campo sonoro tridimensional en una serie de armónicos esféricos $Y_m^n(\\theta, \\phi)$ alrededor del punto de escucha central. En formato B clásico (orden 1): 4 canales ($W$, $X$, $Y$, $Z$). Para orden $N$: $(N+1)^2$ canales. Esta representación es independiente de la disposición de altavoces y decodifica el campo a cualquier sistema envolvente (5.1, Atmos, binaural con HRTF) preservando la localización espacial."),

        ("¿Cuál es la función del factor de cresta ponderado (WCF) en la evaluación de fatiga auditiva?",
         "El Factor de Cresta cuantifica la relación en decibelios entre el valor de pico máximo y el valor RMS de una señal:\n\n$$\\text{CF} = 20 \\log_{10} \\left( \\frac{V_{\\text{pico}}}{V_{\\text{RMS}}} \\right)$$\n\nCon rango dinámico saludable: $\\text{CF} \\ge 12\\text{ dB}$. Tras limitación agresiva (*brickwall limiting*) o compresión intensa, el factor de cresta colapsa por debajo de $8\\text{ dB}$, eliminando transitorios e induciendo saturación de las células ciliadas cocleares."),

        ("¿Cómo opera el principio de incertidumbre de Gabor en el procesamiento espectral por STFT?",
         "La relación de Gabor acopla la resolución temporal $\\Delta t$ y frecuencial $\\Delta f$ de una ventana de análisis:\n\n$$\\Delta t \\cdot \\Delta f \\ge \\frac{1}{4\\pi}$$\n\nAl acortar la ventana para capturar transitorios de percusión con precisión de milisegundos, los armónicos adyacentes en baja frecuencia se emborronan. Al alargarse para discriminar tonos subgraves, la posición temporal de los ataques se difumina. La ventana gaussiana minimiza este producto de incertezas."),

        ("Explica la síntesis aditiva y su relación con la transformada inversa de Fourier (IFFT).",
         "La síntesis aditiva construye formas de onda complejas sumando ondas sinusoidales puras de frecuencia, amplitud y fase controladas. Corresponde a la evaluación directa de la serie de Fourier en el dominio temporal. La transformada inversa de Fourier rápida (IFFT) implementa esta suma en bloques de muestras discretas con complejidad $O(N \\log N)$."),

        ("¿Por qué el sobremuestreo (oversampling) elimina el aliasing en procesos de distorsión no lineal?",
         "Cualquier saturación no lineal (ej. $\\tanh(x)$) genera armónicos de orden superior. Si estos superan la frecuencia de Nyquist ($f_s / 2$), se reflejan hacia el espectro audible como frecuencias inarmónicas parásitas (aliasing). El sobremuestreo multiplica la tasa de muestreo (ej. $4\\times$ o $8\\times$), desplazando la frecuencia de Nyquist a un rango inaudible donde los armónicos reflectivos se suprimen con un filtro paso-bajo antes de la reducción final."),

        ("¿Qué diferencia existe entre la FFT y la transformada wavelet en resolución temporal-frecuencial?",
         "La FFT divide el plano tiempo-frecuencia en celdas de tamaño uniforme fijadas por la duración de la ventana. La transformada wavelet usa ventanas escalables: analiza altas frecuencias con resolución temporal estrecha y frecuencias bajas con resolución temporal ancha, adaptándose a la física de señales transitorias y armónicos graves en acústica musical."),

        ("Define el concepto de temperamento mesotónico y su diferencia con el temperamento igual.",
         "El temperamento mesotónico ajusta las quintas a $\\approx 696{,}6\\text{ cents}$ (en lugar de las $702\\text{ cents}$ pitagóricas o las $700\\text{ cents}$ del temperamento igual), obteniendo terceras mayores puras de $386{,}3\\text{ cents}$ ($5/4 = 386{,}3\\text{ cents}$). A cambio, las tonalidades con muchos sostenidos o bemoles resultan disonantes. Fue el sistema predominante entre los siglos XV y XVII en la música renacentista y barroca temprana."),

        ("¿Qué es el espectro de potencia de una señal y cómo se calcula?",
         "El espectro de potencia de una señal $x(t)$ cuantifica la distribución de energía por banda de frecuencia. Para señales discretas, la Densidad Espectral de Potencia (PSD) se calcula como el cuadrado del módulo de la DFT normalizado:\n\n$$S(f) = \\frac{1}{N} |X(f)|^2 = \\frac{1}{N} \\left| \\sum_{n=0}^{N-1} x[n] e^{-j2\\pi fn/N} \\right|^2$$\n\nEn análisis de mezclas, la PSD identifica acumulación de energía en bandas críticas y regiones de masking psicoacústico."),

        ("¿Cómo se define el concepto de masking psicoacústico y qué uso tiene en la codificación MP3?",
         "El masking psicoacústico ocurre cuando un tono o banda de ruido de alta energía suprime la percepción auditiva de señales de menor energía en frecuencias vecinas (masking simultáneo) o en instantes de tiempo adyacentes (masking temporal). Los códecs de audio con pérdidas como MP3/AAC explotan estos umbrales perceptivos: asignan cero bits a las componentes situadas bajo la curva de enmascaramiento, reduciendo la tasa binaria sin degradación perceptible para el oyente en condiciones normales."),

        ("¿Qué relación existe entre la serie armónica natural y el timbre de un instrumento?",
         "El timbre de un instrumento depende de la distribución de amplitudes relativas de sus parciales (armónicos). Un oscilador sinusoidal puro tiene un único parcial ($f_0$). Un instrumento real produce armónicos a $nf_0$ ($n = 1, 2, 3, \\ldots$) con amplitudes decrecientes determinadas por la geometría del resonador, el material y el tipo de excitación. La función de transferencia del cuerpo actúa como un filtro que moldea el espectro de la fuente (cuerda, columna de aire, membrana) produciendo el color tímbrico distintivo."),

        ("¿Cómo afecta el fenómeno de intermodulación al análisis espectral de señales de audio polirítmicas?",
         "La intermodulación (IM) ocurre cuando dos o más señales pasan por un sistema no lineal, generando nuevas componentes de frecuencia en sumas y diferencias ($f_1 \\pm f_2$, $2f_1 \\pm f_2$, etc.). En señales polirítmicas con múltiples capas de ritmo superpuestas, las frecuencias de intermodulación pueden coincidir con notas de la escala temperada o crear disonancia armónica adicional no planeada en la mezcla. El análisis espectral con transformada de Fourier de tiempo corto detecta estos productos IM como componentes inarmónicas en el espectro residual."),
    ]
    for q, a in mus_qa:
        records.append({"domain": "Músico", "prompt": f"{sys_mus}\n\n{q}", "completion": purge_mentes(a)})

    # ── 8. DOMINIO ABOGADO / SCITT (22 QAs — SCITT RFC 9943 reforzado) ───────
    sys_abo = (
        "Eres Moskv-1 (Modo Derecho Digital, Gobernanza Algorítmica & SCITT). "
        "Analizas atestaciones jurídicas, el estándar IETF SCITT (RFC 9943), no repudio criptográfico y el EU AI Act."
        + INV_POSTFIX
    )
    abo_qa = [
        ("¿Qué define el estándar SCITT RFC 9943 y cuál es su objetivo principal?",
         "El IETF RFC 9943 SCITT (Supply Chain Integrity, Transparency, and Trust) define un protocolo interoperable para la gestión de evidencias criptográficas en cadenas de suministro de software y modelos de inteligencia artificial. Su objetivo es registrar declaraciones atestadas en libros mayores transparentes e inmutables mediante sobres COSE_Sign1 y pruebas de inclusión de Merkle, con independencia del emisor y del auditor."),

        ("¿Cuál es el significado del acrónimo SCITT según el RFC 9943?",
         "SCITT significa Supply Chain Integrity, Transparency, and Trust. El RFC 9943 del IETF define el protocolo SCITT para gestionar la integridad y transparencia de artefactos digitales en cadenas de suministro de software mediante registros transparentes append-only respaldados por árboles de Merkle y firmas COSE_Sign1."),

        ("¿Cómo valida el registro SCITT la precedencia temporal y la integridad forense de los artefactos?",
         "SCITT (RFC 9943) asegura la inmutabilidad y no repudio forense de cualquier activo digital desacoplando al emisor del registro de verificación mediante tres fases:\n\n1. **Firma Criptográfica en Origen:** El artefacto se empaqueta en un sobre COSE_Sign1 firmado con la clave privada del autor respaldada en hardware (Secure Enclave o TPM).\n2. **Inclusión en Registro Transparente Inmutable:** El sobre firmado se envía a un registro público append-only respaldado por un árbol de Merkle. El operador emite un recibo criptográfico con la raíz del árbol (`merkle_root`) y la prueba de inclusión $O(\\log N)$.\n3. **Verificación Soberana Offline:** Cualquier auditor valida por deducción matemática que el artefacto no ha sido modificado y existía en el instante registrado sin consultar al emisor original."),

        ("¿Cuáles son los requisitos de gobernanza del Artículo 14 del Reglamento de Inteligencia Artificial de la UE (EU AI Act)?",
         "El Artículo 14 del EU AI Act exige supervisión humana (*human oversight*) para todos los sistemas de IA clasificados de alto riesgo. Impone:\n\n1. Capacidad de los operadores humanos de comprender las capacidades y limitaciones del sistema algorítmico.\n2. Inmunidad ante el 'sesgo de automatización' (*automation bias*), evitando que el operador asuma sin evaluación los resultados del modelo.\n3. Facultad operativa y técnica de desestimar, modificar o anular cualquier salida o decisión tomada por el sistema.\n4. Acceso a un mecanismo de interrupción de emergencia (*kill switch*) que permita detener la operación de forma segura."),

        ("¿Por qué el sellado temporal PoW en Bitcoin elimina la necesidad de terceros de confianza notariales?",
         "El sellado temporal mediante Proof-of-Work en la cadena de bloques de Bitcoin ancla el hash SHA-256 del documento en un bloque cuya existencia está garantizada por trabajo termodinámico acumulado (entalpía disipada por los mineros). Alterar la fecha de inclusión exigiría reescribir la historia computacional completa superando el $51\\%$ de la potencia de cálculo global, confiriendo certeza matemática de precedencia temporal sin depender de notarios falibles."),

        ("¿Qué valor probatorio tiene una firma COSE_Sign1 respaldada por Secure Enclave frente al estándar eIDAS?",
         "Bajo el Reglamento eIDAS (UE 910/2014), una firma electrónica cualificada requiere un Dispositivo Cualificado de Creación de Firma (QSCD). Una firma COSE_Sign1 generada dentro de un Secure Enclave en silicio (ARM TrustZone) vincula la clave privada de forma no extraíble y sujeta a autorización biométrica local. Desde el punto de vista pericial, la atestación de hardware garantiza que la clave nunca existió en la memoria RAM del sistema operativo ni pudo ser exfiltrada por malware, proporcionando una presunción técnica incontrovertible de autoría material."),

        ("¿Cómo define el Artículo 10 del EU AI Act los requisitos de calidad de los datos de entrenamiento?",
         "El Artículo 10 establece que los conjuntos de datos de entrenamiento, validación y prueba para IA de alto riesgo deben someterse a prácticas apropiadas de gobernanza de datos. Exige: diseño deliberado de la recopilación de datos; análisis previo de posibles sesgos discriminatorios; examen de lagunas o insuficiencias de información; y garantía de que los datos sean pertinentes, en grado bastante representativos y libres de errores respecto a la finalidad prevista."),

        ("¿Cuál es la función probatoria de una prueba de inclusión de Merkle en un juicio pericial informático?",
         "Una prueba de inclusión de Merkle consiste en el camino de autenticación ($O(\\log N)$ hashes intermedios) que une el hash de una hoja específica con la raíz inmutable (`merkle_root`) del árbol criptográfico. En sede judicial, permite demostrar por deducción matemática que un registro particular formaba parte del libro mayor en el instante en que la raíz fue sellada, sin necesidad de revelar el contenido confidencial del resto de registros almacenados."),

        ("¿Cómo opera la atestación de hardware en el estándar SCITT frente a la firma digital convencional?",
         "La atestación de hardware ancla la clave criptográfica privada en un enclave seguro aislado en el soporte material (Secure Enclave o TPM), impidiendo su extracción o copia en memoria volátil. La firma digital convencional almacena claves en archivos de software vulnerables a exfiltración. SCITT RFC 9943 vincula el artefacto a la clave en silicio para certificar autenticidad física de origen."),

        ("¿Por qué una atestación criptográfica no certifica la verdad ontológica de una afirmación?",
         "Una atestación digital certifica la integridad del mensaje y la autoría vinculada a una clave criptográfica en un instante de tiempo. No valida la correspondencia física entre el contenido del enunciado y la realidad empírica. Confundir la validez de la firma con la veracidad del hecho constituye una falacia epistémica."),

        ("¿Cómo previene el libro mayor append-only de SCITT los ataques de reescritura de historial?",
         "El libro mayor append-only estructura las transacciones en un árbol Merkle donde cada bloque nuevo incorpora el hash del estado anterior. Modificar un registro previo altera la raíz del árbol y rompe todas las pruebas de inclusión subsecuentes, delatando la manipulación sin retardo ante cualquier nodo auditor."),

        ("¿Cuáles son los sujetos obligados por el EU AI Act y qué tipo de sistemas clasifica como alto riesgo?",
         "El EU AI Act obliga a proveedores que comercializan o despliegan sistemas de IA en la UE y a operadores que usan estos sistemas en contextos profesionales. Clasifica como alto riesgo los sistemas de IA en sectores de infraestructura crítica, educación, empleo, servicios esenciales, justicia penal, migración y biometría. Los sistemas de IA de propósito general (GPAI) con más de $10^{25}$ FLOP de entrenamiento se sujetan a obligaciones adicionales de transparencia y evaluación de riesgos sistémicos."),

        ("¿Qué establece el Artículo 9 del EU AI Act sobre los sistemas de gestión de riesgos?",
         "El Artículo 9 exige que los proveedores de IA de alto riesgo establezcan, implementen y mantengan un sistema de gestión de riesgos continuo a lo largo del ciclo de vida del sistema. Este sistema debe identificar y analizar los riesgos conocidos y razonablemente previsibles, estimar y evaluar los riesgos emergentes durante el uso, y adoptar medidas de gestión de riesgos apropiadas. La documentación del sistema de gestión de riesgos debe conservarse y actualizarse con cada versión del modelo."),

        ("¿Cómo define SCITT la diferencia entre un emisor, un registro y un verificador?",
         "En el modelo SCITT RFC 9943:\n- **Emisor (Issuer):** La entidad que genera y firma el sobre COSE_Sign1 con su clave privada respaldada en hardware.\n- **Registro (Transparency Log):** El servicio append-only que recibe el sobre firmado, verifica la firma y emite el recibo criptográfico con la prueba de inclusión de Merkle.\n- **Verificador (Verifier):** Cualquier entidad que valida la coherencia del recibo y la prueba de inclusión sin necesidad de contactar al emisor original."),

        ("¿Qué es un sobre COSE_Sign1 y qué campos contiene?",
         "Un sobre COSE_Sign1 es una estructura binaria en formato CBOR definida en el RFC 9052 que encapsula un artefacto digital con firma criptográfica. Sus campos son: el encabezado protegido (algoritmo de firma, identificador de clave, tipo de contenido), el encabezado no protegido (parámetros opcionales sin firmar), la carga útil (el artefacto o su hash), y la firma digital (resultado de aplicar el algoritmo de firma sobre el encabezado protegido y la carga). SCITT RFC 9943 usa COSE_Sign1 como primitiva de atestación de artefactos."),

        ("¿Qué es el no repudio criptográfico y cómo lo implementa SCITT?",
         "El no repudio criptográfico es la propiedad que impide a una entidad negar la autoría de un mensaje firmado. SCITT RFC 9943 lo implementa combinando tres elementos: una firma COSE_Sign1 vinculada a la clave privada del emisor (no extraíble del Secure Enclave), un recibo de inclusión emitido por el registro transparente (prueba de que el artefacto fue presentado en un instante determinado), y la raíz Merkle inmutable del registro (prueba de que el estado del registro en ese instante incluye el artefacto sin posibilidad de reescritura posterior)."),

        ("¿Qué papel juega el estándar COSE (RFC 9052) en la arquitectura SCITT?",
         "COSE (CBOR Object Signing and Encryption, RFC 9052) proporciona las primitivas criptográficas de SCITT. Define el formato binario de los sobres de firma (`COSE_Sign1`, `COSE_Sign`), los algoritmos de firma soportados (EdDSA, ES256, ES384, RS256) y los campos del encabezado protegido. SCITT RFC 9943 adopta `COSE_Sign1` como formato de declaración (*claim*) y extiende COSE con campos específicos para la transparencia de cadena de suministro."),

        ("¿Cómo auditaría un perito informático la cadena de custodia de un modelo de IA usando SCITT?",
         "Un perito informático auditaría la cadena de custodia de un modelo de IA bajo SCITT RFC 9943 en cuatro pasos:\n1. **Verificar la firma COSE_Sign1** del artefacto del modelo contra la clave pública del emisor registrada.\n2. **Validar la prueba de inclusión Merkle** del recibo contra la raíz publicada del registro transparente.\n3. **Comprobar la secuencia temporal** de los recibos para establecer el orden de las versiones del modelo.\n4. **Contrastar las declaraciones de calidad** (datos de entrenamiento, evaluaciones de riesgo) registradas contra los requisitos del Artículo 10 y el Artículo 9 del EU AI Act."),

        ("¿Cuál es la diferencia entre un registro de transparencia de tipo Log y uno de tipo Ledger en SCITT?",
         "En la taxonomía SCITT RFC 9943:\n- **Log (Registro de Solo Lectura):** Estructura de árbol Merkle append-only donde el operador publica los recibos y las raíces del árbol en intervalos periódicos para su auditoría pública.\n- **Ledger (Libro Mayor con Estado):** Extiende el Log con la capacidad de asociar estados y metadatos a los artefactos registrados (ej. revocación de artefactos, actualizaciones de estado de política). El Ledger permite modelar el ciclo de vida completo de un artefacto más allá del registro de su existencia inicial."),

        ("¿Cómo se relaciona SCITT con el estándar Certificate Transparency (RFC 6962)?",
         "Certificate Transparency (CT, RFC 6962) es el precursor arquitectónico de SCITT. CT aplica registros Merkle append-only a certificados TLS para detectar emisiones fraudulentas por parte de autoridades certificadoras. SCITT RFC 9943 generaliza este mecanismo a cualquier artefacto digital (modelos de IA, paquetes de software, configuraciones) usando COSE_Sign1 en lugar de los certificados X.509 de CT y definiendo un protocolo interoperable entre múltiples registros y emisores."),

        ("¿Qué obligaciones impone el EU AI Act a los proveedores de modelos de IA de propósito general (GPAI)?",
         "El EU AI Act impone a los proveedores de modelos GPAI las siguientes obligaciones: redactar y mantener documentación técnica del proceso de entrenamiento y evaluación; publicar un resumen del contenido de los datos de entrenamiento sujeto a la legislación de derechos de autor; cumplir la política de derechos de autor de la UE; implementar medidas de ciberseguridad apropiadas. Los modelos GPAI con más de $10^{25}$ FLOP de entrenamiento deben además notificar a la Comisión Europea y someterse a evaluaciones de riesgos sistémicos y pruebas de adversarios."),

        ("¿Cuál es el papel de los organismos notificados (Notified Bodies) en la certificación de IA de alto riesgo bajo el EU AI Act?",
         "Los organismos notificados son entidades de evaluación de la conformidad designadas por los Estados miembros de la UE y notificadas a la Comisión Europea. Para los sistemas de IA de alto riesgo en los Anexos II y III del EU AI Act, los proveedores deben someter el sistema a una evaluación de conformidad por un organismo notificado antes de su comercialización en la UE. El organismo notificado audita la documentación técnica, el sistema de gestión de calidad y los resultados de las pruebas, emitiendo un certificado de evaluación de conformidad válido por un período determinado."),
    ]
    for q, a in abo_qa:
        records.append({"domain": "Abogado", "prompt": f"{sys_abo}\n\n{q}", "completion": purge_mentes(a)})

    # ── 9. DOMINIO MÉDICO (16 QAs — ampliado, sin hallucinaciones) ───────────
    sys_med = (
        "Eres Moskv-1 (Modo Fisiología, Neurofarmacología & Bioenergética Somática). "
        "Analizas el cuerpo humano a través de la farmacognosia de Antonio Escohotado, cinemática de neurotransmisores y bioenergética."
        + INV_POSTFIX
    )
    med_qa = [
        ("Describe la modulación neurotransmisora de la dopamina en los circuitos estriatales.",
         "En los ganglios basales, la dopamina liberada desde la sustancia negra compacta (SNc) modula en dos fases los circuitos estriatales a través de dos poblaciones neuronales espinosas medianas (MSNs):\n\n1. **Vía Directa (Pro-Cinética):** Mediada por receptores D1 acoplados a proteína $G_{\\alpha s/olf}$. La activación estimula la adenilil ciclasa, incrementa el AMPc intracelular y activa la PKA, desinhibiendo el tálamo motor al proyectar sin intermediación sobre el globo pálido interno (GPi) y la sustancia negra reticulata (SNr).\n2. **Vía Indirecta (Anti-Cinética):** Mediada por receptores D2 acoplados a proteína $G_{\\alpha i/o}$. La activación inhibe la adenilil ciclasa y reduce el disparo estriatal hacia el globo pálido externo (GPe), modulando la excitación talámica a través del núcleo subtalámico.\n\nEste equilibrio regula el inicio del movimiento voluntario y la señalización de recompensa por error de predicción temporal."),

        ("Analiza la farmacocinética de aclaramiento y vida media plasmática (t1/2) en un régimen monocompartimental.",
         "En un modelo farmacocinético monocompartimental con eliminación de primer orden, la velocidad de eliminación es proporcional a la concentración plasmática instantánea $C(t)$:\n\n$$-\\frac{dC}{dt} = k_e \\cdot C(t) \\implies C(t) = C_0 \\cdot e^{-k_e t}$$\n\nLa constante de eliminación $k_e = \\text{Cl} / \\text{Vd}$ relaciona el aclaramiento sistémico con el volumen de distribución. La vida media de eliminación:\n\n$$t_{1/2} = \\frac{\\ln 2}{k_e} = \\frac{0{,}693 \\cdot \\text{Vd}}{\\text{Cl}}$$\n\nUn volumen de distribución alto (alta lipofilia y secuestro tisular) o aclaramiento renal/hepático reducido prolonga la exposición sistémica."),

        ("¿Cuál es la función del gradiente electroquímico de protones en la membrana mitocondrial interna?",
         "La cadena de transporte de electrones mitocondrial bombea protones ($H^+$) desde la matriz hacia el espacio intermembrana a través de los complejos I, III y IV, generando una fuerza protón-motriz ($\\Delta p$):\n\n$$\\Delta p = \\Delta \\Psi_m - \\frac{2{,}303 \\cdot R T}{F} \\Delta \\text{pH}$$\n\ndonde $\\Delta \\Psi_m$ es el potencial de membrana eléctrico ($-150$ a $-180\\text{ mV}$) y $\\Delta \\text{pH}$ es el gradiente de concentración de protones. Este potencial impulsa el retorno pasivo de protones a través de la subunidad $F_0$ de la ATP sintasa, provocando la rotación mecánica del complejo y la fosforilación de ADP en ATP ($\\sim 4\\text{ H}^+$ por molécula de ATP)."),

        ("Explica el concepto de pharmakon en Antonio Escohotado y la falacia de la distinción droga-medicamento.",
         "En la *Historia General de las Drogas*, Antonio Escohotado rescata el sentido original de la voz griega *pharmakon*, que designa al mismo tiempo veneno, remedio y sacramento. No existe diferencia molecular intrínseca entre un fármaco terapéutico y una droga proscrita: ambas son substancias psicoactivas cuyos efectos dependen de la dosis, la pureza, la pauta de administración y el contexto psicológico y cultural del usuario (*set and setting*). Escohotado demuestra que la bifurcación legislativa moderna es un artefacto político e ideológico que penaliza la autonomía farmacológica del individuo mientras subvenciona monopolios de patentes químicas análogas."),

        ("¿Cómo modulan los agonistas 5-HT2A la plasticidad cortical y la entropía cerebral según el modelo REBUS?",
         "Los agonistas de receptores serotoninérgicos 5-HT2A (psilocina, LSD, DMT) se unen en su mayoría a las neuronas piramidales de la capa V de la corteza cerebral. Su estimulación incrementa el disparo espontáneo asíncrono y reduce la coherencia de las oscilaciones alfa en la red por defecto (DMN). Bajo el modelo REBUS (Relaxed Beliefs Under Psychedelics) de Carhart-Harris y Friston, esta relajación de los priors predictivos de alto nivel incrementa la entropía de los estados cerebrales, facilitando una plasticidad sináptica acelerada y la reconfiguración de patrones cognitivos rígidos."),

        ("¿Cómo regula la barrera hematoencefálica el transporte de compuestos psicoactivos?",
         "La barrera hematoencefálica está formada por uniones estrechas (*tight junctions*) entre células endoteliales capilares cerebrales, revestidas por pies astrocitarios y pericitos. Solo moléculas de bajo peso molecular (<500 Da) y alta lipofilia atraviesan esta membrana por difusión pasiva. Los compuestos hidrófilos o ionizados requieren transportadores específicos dependientes de energía (ej. GLUT1 para glucosa, LAT1 para aminoácidos aromáticos)."),

        ("Analiza la cinética enzimática de Michaelis-Menten en la metabolización hepática por citocromo P450.",
         "La tasa de aclaramiento metabólico mediada por enzimas del citocromo P450 sigue la ecuación de Michaelis-Menten:\n\n$$v = \\frac{V_{\\text{max}} \\cdot [S]}{K_m + [S]}$$\n\nA concentraciones de fármaco bajas ($[S] \\ll K_m$), la velocidad es de primer orden y proporcional a la dosis. Cuando la concentración satura el enzima ($[S] \\gg K_m$), la cinética colapsa a orden cero ($v \\approx V_{\\text{max}}$), provocando acumulación plasmática a escala exponencial ante incrementos mínimos de dosificación."),

        ("¿Cuál es el mecanismo de la potenciación a largo plazo (LTP) mediada por receptores NMDA?",
         "En la sinapsis glutamatérgica, la despolarización previa de la membrana postsináptica expulsa el ión magnesio ($Mg^{2+}$) que bloquea el poro del receptor NMDA. La unión simultánea de glutamato permite la entrada masiva de calcio ($Ca^{2+}$) a la espina dendrítica, activando la quinasa CaMKII. Esta enzima fosforila los receptores AMPA existentes y promueve la inserción de nuevos receptores AMPA en la densidad postsináptica, incrementando la conductancia sináptica de forma persistente."),

        ("¿Qué mecanismo de acción tiene la ketamina como antagonista no competitivo de NMDA?",
         "La ketamina actúa como antagonista no competitivo del canal iónico del receptor NMDA mediante bloqueo de canal abierto (*open-channel block*). Entra al poro del canal solo cuando el receptor ha sido activado por glutamato y la membrana postsináptica ha sido despolarizada (eliminación del bloqueo por $Mg^{2+}$), bloqueando el flujo de calcio desde el interior del canal. Este mecanismo produce el efecto disociativo a dosis subanestésicas y, a través de la desinhibición de interneuronas GABAérgicas, genera una descarga de glutamato en la corteza prefrontal que se postula como mecanismo del efecto antidepresivo de acción rápida."),

        ("¿Cómo funciona el sistema endocannabinoide y cuáles son sus receptores principales?",
         "El sistema endocannabinoide es un sistema de señalización lipídica retrógrada. Los endocannabinoides (anandamida, 2-AG) son sintetizados en la membrana postsináptica bajo demanda por activación de fosfolipasas, y se difunden de forma retrógrada hacia la terminal presináptica. Sus receptores principales son:\n- **CB1:** Acoplado a $G_{\\alpha i/o}$, inhibe la adenilil ciclasa y reduce la apertura de canales de calcio dependientes de voltaje en la terminal presináptica, disminuyendo la liberación de neurotransmisor.\n- **CB2:** Acoplado a $G_{\\alpha i/o}$, en su mayoría en células inmunitarias periféricas y microglia, con función inmunomoduladora.\n\nEl THC es un agonista parcial de CB1 y CB2 que suplanta a los endocannabinoides endógenos con mayor afinidad pero menor eficacia intrínseca que la anandamida."),

        ("Describe el ciclo de Krebs y su papel en la bioenergética celular.",
         "El ciclo de Krebs (ciclo del ácido cítrico) opera en la matriz mitocondrial. Cada vuelta del ciclo oxida un mol de acetil-CoA (2 carbonos) y produce: 3 NADH, 1 FADH2, 1 GTP y 2 CO2. Los equivalentes de reducción (NADH y FADH2) transfieren sus electrones a la cadena de transporte de electrones para la síntesis de ATP mediante la ATP sintasa. El GTP se forma por fosforilación a nivel de sustrato en el paso de la succinil-CoA sintetasa. El rendimiento neto por mol de glucosa (dos vueltas del ciclo) es 6 NADH, 2 FADH2 y 2 GTP."),

        ("¿Cómo modula la serotonina los circuitos de miedo y ansiedad a través de la amígdala?",
         "La serotonina (5-HT) liberada desde los núcleos del Rafe dorsal y medial actúa sobre la amígdala basolateral a través de múltiples subtipos de receptores con efectos opuestos. Los receptores 5-HT2C facilitan la respuesta de miedo al potenciar la actividad de las neuronas de proyección de la amígdala basolateral hacia el hipocampo y la corteza prefrontal. Los receptores 5-HT1A tienen un efecto inhibitorio presináptico (autorreceptores somáticos en los núcleos del Rafe) y postsináptico (hiperpolarización en la amígdala), reduciendo la respuesta de miedo condicionado. Los inhibidores selectivos de la recaptación de serotonina (ISRS) producen su efecto ansiolítico a través del aumento sostenido de la disponibilidad de 5-HT en estas sinapsis."),

        ("¿Cuál es el papel del cortisol en la respuesta al estrés y cómo afecta al eje hipotálamo-hipófisis-adrenal (HHA)?",
         "El cortisol es el glucocorticoide principal sintetizado en la corteza adrenal en respuesta a la hormona adrenocorticotropa (ACTH) liberada por la hipófisis anterior. La ACTH se libera en respuesta a la hormona liberadora de corticotropina (CRH) del hipotálamo. El eje HHA opera bajo un mecanismo de retroalimentación negativa: los niveles elevados de cortisol inhiben la liberación de CRH en el hipotálamo y de ACTH en la hipófisis, cerrando el bucle regulador. La exposición crónica a cortisol en el estrés persistente produce atrofia del hipocampo (daño a las neuronas del giro dentado), disfunción de la corteza prefrontal y facilitación de la consolidación de memorias de miedo en la amígdala."),

        ("¿Cómo actúa la acetilcolina en los circuitos colinérgicos del sistema nervioso autónomo?",
         "La acetilcolina es el neurotransmisor de la unión neuromuscular y de todos los ganglios del sistema nervioso autónomo. Sus receptores se dividen en dos familias:\n- **Receptores Nicotínicos (nAChR):** Canales iónicos de ligando con flujo de Na+ y Ca2+. Presentes en los ganglios autónomos, la unión neuromuscular y el SNC. Mediadores de la transmisión rápida.\n- **Receptores Muscarínicos (mAChR, M1-M5):** Acoplados a proteínas G. M2 en el corazón (inhibe la frecuencia cardíaca acoplado a $G_{\\alpha i}$), M3 en glándulas y músculo liso (promueve la secreción y contracción acoplado a $G_{\\alpha q}$)."),

        ("¿Qué es la neuroplasticidad dependiente de la actividad y cómo la regula el BDNF?",
         "La neuroplasticidad dependiente de la actividad es la capacidad del sistema nervioso de modificar sus conexiones sinápticas en respuesta a la actividad neuronal. El factor neurotrófico derivado del cerebro (BDNF) es un regulador central de este proceso. Su liberación se produce en respuesta al disparo neuronal y a la entrada de calcio por receptores NMDA o canales de calcio dependientes de voltaje. El BDNF activa la vía de señalización TrkB → PI3K/Akt → mTOR, promoviendo la síntesis de proteínas locales en la espina dendrítica y la inserción de nuevos receptores AMPA, que son los sustratos moleculares de la potenciación a largo plazo (LTP)."),

        ("¿Cómo describen Escohotado y la farmacognosia clásica la tolerancia y el síndrome de abstinencia?",
         "La tolerancia es el fenómeno por el cual la exposición repetida a una substancia produce una reducción de su efecto con la misma dosis. Los mecanismos incluyen: down-regulation de los receptores diana (internalización o reducción de la síntesis), desensibilización del receptor (desacoplamiento de la proteína G) y adaptaciones celulares compensatorias en los circuitos afectados. El síndrome de abstinencia emerge cuando se retira la substancia y las adaptaciones compensatorias quedan sin oposición. La farmacognosia de Escohotado integra este principio en una crítica a los modelos moralizantes de la adicción: la dependencia física es un proceso homeostático del organismo, no un defecto de carácter."),
    ]
    for q, a in med_qa:
        records.append({"domain": "Médico", "prompt": f"{sys_med}\n\n{q}", "completion": purge_mentes(a)})

    # ── Validación final ───────────────────────────────────────────────────────
    print(f"\n[*] Total final de registros puros generados: {len(records)}")
    random.seed(42)
    random.shuffle(records)

    mente_violations = 0
    for idx, r in enumerate(records):
        f1 = re.findall(r'\b\w+mente\b', r['prompt'], re.IGNORECASE)
        f2 = re.findall(r'\b\w+mente\b', r['completion'], re.IGNORECASE)
        if f1 or f2:
            print(f"[!] Violación en registro {idx}: prompt={f1}, completion={f2}")
            mente_violations += len(f1) + len(f2)
    print(f"[*] Total violaciones de adverbios -mente en dataset: {mente_violations}")
    assert mente_violations == 0, f"Error: Dataset contiene {mente_violations} adverbios en -mente"

    counts = {}
    for r in records:
        d = r["domain"]
        counts[d] = counts.get(d, 0) + 1
    print("\n--- DISTRIBUCIÓN POR DOMINIO ---")
    for d, c in sorted(counts.items()):
        print(f"  ├─ {d:12s}: {c:4d} muestras ({c/len(records)*100:.1f}%)")

    # Master ShareGPT
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps({
                "messages": [
                    {"role": "user", "content": r["prompt"]},
                    {"role": "assistant", "content": r["completion"]}
                ],
                "_domain": r["domain"]
            }, ensure_ascii=False) + "\n")
    print(f"\n[✓] Master ShareGPT emitido en: {MASTER_FILE}")

    # Splits MLX
    MLX_DIR.mkdir(parents=True, exist_ok=True)
    split_idx = int(len(records) * 0.90)
    train_recs = records[:split_idx]
    valid_recs = records[split_idx:]

    train_p = MLX_DIR / "train.jsonl"
    valid_p = MLX_DIR / "valid.jsonl"

    with open(train_p, "w", encoding="utf-8") as f:
        for r in train_recs:
            f.write(json.dumps({"prompt": r["prompt"], "completion": r["completion"]}, ensure_ascii=False) + "\n")

    with open(valid_p, "w", encoding="utf-8") as f:
        for r in valid_recs:
            f.write(json.dumps({"prompt": r["prompt"], "completion": r["completion"]}, ensure_ascii=False) + "\n")

    print(f"[✓] Train Split MLX ({len(train_recs):,} muestras) emitido en: {train_p}")
    print(f"[✓] Valid Split MLX ({len(valid_recs):,} muestras) emitido en: {valid_p}")
    print("[✓] Dataset v7.0 completado.")

if __name__ == "__main__":
    build_dataset()
