# Índice documental ESCOTA

Colección mixta de OCR atribuidos a Antonio Escohotado, interpretaciones del proyecto y documentación técnica C5-REAL/MOSKV-1. No es una edición crítica ni un inventario de la obra completa.

## Catálogo

El [manifiesto](manifest.json) es el inventario legible por máquina. Cada entrada distingue tipo documental, ruta relativa, identificador de bytes Git y estado de derechos.

| Capa | Documentos |
| --- | ---: |
| OCR atribuido a Escohotado | 2 |
| Interpretaciones y formalizaciones | 5 |
| Documentación técnica del proyecto | 18 |

Los dos OCR son *Realidad y Substancia* y *Caos y Orden*. Los materiales relativos a *Los enemigos del comercio*, *Historia general de las drogas* y *Somos información, somos bytes* son análisis derivados, no ediciones completas de esas obras.

## Consulta local

```bash
python3 escota_search.py --check-catalog
python3 escota_search.py "substancia" --kind primary_ocr --json
python3 escota_search.py "termodinámica" --kind interpretation
```

Las referencias de línea son posiciones del OCR local, no paginación editorial. El SHA-256 identifica el archivo consultado. La atribución y edición requieren comprobación documental independiente.

## Marco Ω118

Monismo de substancia, emergencia no lineal e intercambio libre constituyen una lectura propia de C5-REAL inspirada en Escohotado. No se presentan como axiomas del autor ni como verificación formal.

Los nombres `escohotado_tripartite_invariant.yaml`, `escohotado_substance_ontology.py`, `escohotado_chaos_engine.py` y `escohotado_cli.py` corresponden a integraciones externas no incluidas en este árbol; no hay enlaces locales portables a ellas.

## Derechos

El [README](README.md#licencia-y-procedencia) delimita licencia del código, procedencia y derechos de terceros. Los campos desconocidos no se completan por inferencia.
