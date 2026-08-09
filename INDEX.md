<!-- C5-REAL EXERGY CERTIFIED -->
# Repositorio Especial Antonio Escohotado ("Escota")

Este directorio constituye la colección documental y ontológica especializada de la obra completa, textos y modelos formales de **Antonio Escohotado (Escota)** dentro del marco **C5-REAL / Teorema Robinson-Moskv**.

---

## 1. Estructura del Repositorio

- `texts/`: Almacenamiento en texto plano sin sobrecoste (formatos OCR `DjVuTXT` / `hOCR`).
- `manifest.json`: Índice estructurado de obras, hashes, URLs de Internet Archive e identificadores.
- `escota_search.py`: Motor de búsqueda y consulta ontológica por comandos sobre el corpus en local.
- Integración ontológica existente en el proyecto:
  - Definición YAML: [escohotado_tripartite_invariant.yaml](file:///Users/borjafernandezangulo/10_PROJECTS/Teorema-Robinson-Moskv/docs/ontology/escohotado_tripartite_invariant.yaml)
  - Motor de Sustancia: [escohotado_substance_ontology.py](file:///Users/borjafernandezangulo/10_PROJECTS/Teorema-Robinson-Moskv/src/cortex-engine/cortex-persist/cortex_python/core/escohotado_substance_ontology.py)
  - Motor de Caos y Complejidad: [escohotado_chaos_engine.py](file:///Users/borjafernandezangulo/10_PROJECTS/Teorema-Robinson-Moskv/src/cortex-engine/cortex-persist/cortex_python/engines/escohotado_chaos_engine.py)
  - CLI: [escohotado_cli.py](file:///Users/borjafernandezangulo/10_PROJECTS/Teorema-Robinson-Moskv/src/cortex-engine/cortex-persist/cortex_python/core/escohotado_cli.py)

---

## 2. Invariante Tripartito Escohotadiano (Ω118)

Toda auditoría y evaluación de sistemas dinámicos en el proyecto sigue el Invariante Ω118:
1. **Monismo de Sustancia Continua**: Superación del dualismo sujeto-objeto (*Realidad y Substancia*, 1985).
2. **Emergencia No Lineal sin Diseñador Exógeno**: Autogestión de la complejidad (*Caos y Orden*, 1999).
3. **Inviolabilidad de las Señales de Precio e Intercambio Libre**: Rechazo del dirigismo burocrático (*Los Enemigos del Comercio* / *Las Drogas*).

---

## 3. Principio de Licenciamiento "Copyfree"

Toda la obra de Antonio Escohotado fue declarada explícitamente por el autor en modalidad **Copyfree** (libre distribución, copia y acceso universal al conocimiento), eliminando monopolios artificiales de difusión. La conservación e ingesta de su corpus en `scratch/corpus/escota/` respeta íntegramente la voluntad expresa del pensador.

---

## 4. Uso del Búsqueda en Local

```bash
python3 scratch/corpus/escota/escota_search.py "substancia"
python3 scratch/corpus/escota/escota_search.py "termodinámica"
```
