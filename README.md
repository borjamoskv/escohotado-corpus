# ESCOTA · Antonio Escohotado & C5-REAL

Corpus documental mixto, catálogo de procedencia y herramientas de auditoría local para investigación filosófica computacional. Incluye materiales de MOSKV-1; no equivale a una edición de las obras completas ni a un modelo validado del pensamiento de Escohotado.

[![CI](https://github.com/borjamoskv/escohotado-corpus/actions/workflows/ci.yml/badge.svg)](https://github.com/borjamoskv/escohotado-corpus/actions/workflows/ci.yml)

## Consulta y verificación (Python 3.11+, sin dependencias)

```bash
python3 escota_search.py --check-catalog
python3 escota_search.py "substancia" --kind primary_ocr --limit 5
python3 escota_search.py "termodinámica" --kind interpretation --json
python3 audit_21_swarm_dataset.py
python3 -m unittest discover -s tests -v
python3 moskv1_pipeline.py status
```

El buscador realiza coincidencias literales insensibles a acentos, no inferencia semántica. Devuelve identificadores de obra, líneas, tipo de fuente, SHA-256 del archivo y recuento real de líneas coincidentes. Las líneas OCR no equivalen a páginas de una edición.

## Separación documental

| Tipo | Interpretación |
| --- | --- |
| `primary_ocr` | OCR atribuido a Antonio Escohotado; edición y derechos no verificados |
| `interpretation` | Análisis derivados y formalizaciones del proyecto |
| `project_document` | Documentos técnicos C5-REAL / MOSKV-1 |

El [manifiesto](manifest.json) usa rutas relativas y Git blob SHA-1 para identificar los bytes de cada archivo. Eso no demuestra autoría, fidelidad OCR ni autorización de redistribución. Los campos de fuente, edición y derechos desconocidos permanecen explícitamente sin verificar.

## Evidencia y límites

- [swarm_audit_report.json](swarm_audit_report.json): informe histórico de 836 registros, 25 fuentes y una raíz Merkle declarada.
- [dataset_health_report.json](dataset_health_report.json): informe histórico de 29.628 muestras multidominio, no 29.628 textos de Escohotado.
- El auditor reconstruye los fragmentos de 2.500 caracteres con paso 2.200 del generador legado, verifica el hash declarado y compara la respuesta almacenada con el fragmento original recortado. No sobrescribe informes; falla con código distinto de cero si detecta errores.
- La minería anterior usa fragmentos textuales como respuestas del asistente. Integridad de extracción no implica calidad instruccional, capacidad de razonamiento ni ausencia de contaminación train/valid.
- Los informes, splits y adaptadores existentes son artefactos históricos. Las cifras pueden corresponder a versiones distintas; no se certifican mediante este README.
- No se ha demostrado independencia de train/valid por obra o por fragmentos solapados. No usar esos splits para afirmar generalización.

## Ω118 · Marco interpretativo del proyecto

El proyecto relaciona el monismo, la emergencia no lineal y el intercambio libre con C5-REAL. Ω118 es una formalización interpretativa propia, no un teorema publicado por Escohotado ni una garantía formal demostrada aquí.

Los motores externos mencionados en versiones anteriores no forman parte de este repositorio. Véase [INDEX.md](INDEX.md).

## Entrenamiento legado

`swarm_miner.py`, `prepare_master_dataset.py`, los builders v3–v8, los entrenadores MLX/Unsloth y los adaptadores se conservan como material histórico/experimental. Algunos dependen de rutas y fuentes externas no incluidas. La preparación puede sobrescribir artefactos existentes. No ejecutar automáticamente ni utilizar para entrenamiento o publicación sin revisar la procedencia, los derechos y los splits.

## Licencia y procedencia

[MIT](LICENSE) para el código y documentación original que el titular del proyecto pueda licenciar. No se extiende automáticamente a libros, OCR, datasets derivados o modelos de terceros. La afirmación anterior de una licencia general «Copyfree» no está respaldada aquí por una autorización verificable por obra y edición.

Que un texto sea accesible públicamente no prueba permiso de redistribución o entrenamiento. Antes de ampliar, publicar o reutilizar el corpus, documentar titular, fuente, edición y alcance de la autorización. El estado actual de derechos no está verificado.

[Índice](INDEX.md) · [Seguridad](SECURITY.md)
