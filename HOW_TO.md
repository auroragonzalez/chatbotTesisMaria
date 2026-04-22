# FestGPT — How To

## Estructura del proyecto

```
chatbotTesis/
├── app.py                  ← Aplicación de producción (chatbot + ingestión)
├── festgpt_pipeline.ipynb  ← Prototipo/exploración en notebook
├── requirements.txt        ← Dependencias Python
├── HOW_TO.md               ← Esta guía
├── chroma_db/              ← Base de datos vectorial (se genera automáticamente)
└── festival_txts/          ← Corpus de conocimiento (editar aquí para ampliar)
    ├── warm_up/
    │   ├── faq.txt
    │   ├── horarios.txt
    │   ├── accesos.txt
    │   ├── transporte.txt
    │   └── ...             ← Añadir más .txt aquí
    ├── animal_sound/
    └── mar_de_musicas/
```

---

## 1. Instalación (primera vez)

```bash
# Crear entorno virtual con Python 3.11
python3.11 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## 2. Flujo de trabajo habitual

### Paso 1 — Descargar el modelo (solo la primera vez)

Phi-3 es un modelo con acceso controlado en HuggingFace. Antes de descargar:

1. Acepta los términos en [huggingface.co/microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) (una sola vez, desde el navegador con tu cuenta HF).
2. Exporta tu token (opcional — si no lo haces, `app.py` te lo pedirá por teclado):
   ```bash
   export HF_TOKEN="hf_tu_token_aqui"
   ```
3. Ejecuta el comando de descarga:
   ```bash
   python app.py --download-model
   ```
   `app.py` comprueba si el modelo ya está en `~/.cache/huggingface/`. Si lo está, no descarga nada. Si no, inicia la descarga (~8 GB) y te pide el token si no está en el entorno.  
   Una vez descargado no hace falta repetirlo nunca más.

> **Modelo alternativo sin restricciones:** Si no tienes cuenta HF o quieres algo más ligero, puedes usar `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (no requiere token). Cambia `MODEL_NAME` antes de ejecutar:
> ```bash
> MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0 python app.py --download-model
> ```

### Paso 2 — Arrancar el modelo LLM con vLLM (en el servidor)

```bash
vllm serve microsoft/Phi-3-mini-4k-instruct \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.85 \
    --port 8000
```

Si el token sigue siendo necesario en el arranque (modelos gated):
```bash
HF_TOKEN="hf_tu_token_aqui" vllm serve microsoft/Phi-3-mini-4k-instruct \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.85 \
    --port 8000
```

Déjalo corriendo en segundo plano (tmux, screen, o `&`).

### Paso 2 — Ingestar el corpus (solo si es la primera vez o has añadido/modificado TXT)

```bash
# Todos los festivales de una vez
python app.py --ingest

# Solo un festival concreto
python app.py --ingest --festival warm_up
```

Esto lee todos los `.txt` de `festival_txts/<festival>/`, los trocea en chunks y los guarda en `chroma_db/`.  
Si el corpus ya existía, lo borra y lo reconstruye limpio.

### Paso 3 — Lanzar el chatbot

```bash
python app.py
```

Abre el navegador en `http://localhost:7860`.

---

## 3. Ampliar el corpus

1. Añade o edita archivos `.txt` dentro de la carpeta del festival correspondiente:
   ```
   festival_txts/warm_up/gastronomia.txt
   festival_txts/warm_up/alojamiento.txt
   ...
   ```
2. El formato recomendado es texto plano en español, una idea por párrafo o en formato pregunta-respuesta, como los archivos `faq.txt` existentes.
3. Re-ingestar:
   ```bash
   python app.py --ingest --festival warm_up
   ```
4. Relanzar `app.py` (o simplemente recargar — el retriever lee Chroma en cada consulta).

### Añadir un festival nuevo

1. Crea la carpeta `festival_txts/nombre_festival/` y añade los `.txt`.
2. Ingestar: `python app.py --ingest --festival nombre_festival`
3. El nuevo festival aparecerá automáticamente en el **dropdown de la UI** la próxima vez que lances `app.py`.

---

## 4. Configuración avanzada (variables de entorno)

Todas las variables tienen valor por defecto y no es obligatorio configurarlas. Útil para despliegues en servidor o para cambiar de modelo sin tocar el código.

| Variable | Por defecto | Descripción |
|---|---|---|
| `CUDA_VISIBLE_DEVICES` | `"0"` | GPU a usar |
| `VLLM_URL` | `http://localhost:8000/v1/completions` | Endpoint vLLM |
| `MODEL_NAME` | `microsoft/Phi-3-mini-4k-instruct` | Modelo servido en vLLM |
| `EMBEDDING_MODEL` | `intfloat/multilingual-e5-base` | Modelo de embeddings |
| `EMBEDDING_DEVICE` | `cuda` | `cpu` o `cuda` |
| `CHROMA_DIR` | `./chroma_db` | Ruta de la base vectorial |
| `DATA_DIR` | `./festival_txts` | Carpeta raíz del corpus |
| `CHUNK_SIZE` | `500` | Tamaño de chunk (caracteres) |
| `CHUNK_OVERLAP` | `50` | Solapamiento entre chunks |
| `RETRIEVER_K` | `4` | Nº de chunks a recuperar por consulta |
| `MAX_TOKENS` | `512` | Tokens máximos de respuesta |
| `TEMPERATURE` | `0.3` | Temperatura del LLM (0 = determinista) |
| `SERVER_PORT` | `7860` | Puerto de Gradio |

Ejemplo: cambiar GPU y puerto antes de lanzar:
```bash
export CUDA_VISIBLE_DEVICES=1
export SERVER_PORT=8080
python app.py
```

---

## 5. Uso de la interfaz

La UI tiene dos controles encima del chat:

- **Festival** — selecciona de qué festival quieres información. El retriever busca solo en ese corpus.
- **Momento de uso** — adapta el sistema prompt al contexto del usuario:
  - `Pre-festival`: planificación, alojamiento, transporte, cartel.
  - `Durante`: respuestas operativas breves, accesos, normativa, emergencias.
  - `Post-festival`: prolongar la estancia en Murcia, gastronomía, turismo, merchandising.

---


6. Evaluación comparativa de modelos LLM

Para fortalecer la contribución técnica del paper (Sección 5.1), el plan es evaluar varios modelos y presentar una tabla comparativa. Esto convierte la evaluación en una aportación comparativa real, no solo el análisis de un único sistema.

Modelos candidatos (de mayor a menor relevancia para el paper):

    BSC-LT/salamandra-7b-instruct → especialmente relevante por ser el único entrenado específicamente con texto en español (Barcelona Supercomputing Center). Argumento académico fuerte para una tesis española sobre un festival español.
    mistralai/Mistral-7B-Instruct-v0.3 → muy buen rendimiento en español, sin token HF, 7B params (~16 GB VRAM).
    meta-llama/Llama-3.1-8B-Instruct → muy buen rendimiento, requiere token HF, 8B params (~18 GB VRAM).
    Qwen/Qwen2.5-7B-Instruct → muy buen rendimiento en español, sin restricciones, 7B params (~16 GB VRAM).
    microsoft/Phi-3-mini-4k-instruct → modelo base ya integrado, 3.8B params (~8 GB VRAM), requiere token HF.
    TinyLlama/TinyLlama-1.1B-Chat-v1.0 → útil solo para pruebas locales en CPU, español básico.

Infraestructura de evaluación ya creada en el proyecto:

    eval/qa_benchmark.json → dataset sintético de 17 preguntas con respuestas esperadas, distribuidas en pre/durante/post y con preguntas fuera de corpus para medir alucinación.
    eval/run_eval.py → script de evaluación comparativa. Calcula automáticamente:
        ROUGE-L (solapamiento léxico con la respuesta esperada)
        BERTScore F1 en español (similitud semántica)
        Latencia de respuesta en segundos (relevante para el uso "durante el festival")
        Tasa de alucinación (fracción de preguntas fuera de corpus donde el modelo inventa información)
    La salida se guarda en eval/results_<timestamp>.csv (por pregunta) y eval/summary_<timestamp>.csv (media por modelo y fase).

Cómo ejecutar la evaluación:

    # Un solo modelo
    python eval/run_eval.py --models phi3

    # Comparativa completa
    python eval/run_eval.py --models phi3 salamandra mistral qwen

Pendiente para ampliar el benchmark:
    Añadir preguntas de fase post cuando el corpus turístico esté completo (gastronomía, alojamiento, planes en Murcia).
    Ampliar a ~60-80 preguntas totales (20 por fase) para tener potencia estadística suficiente en el paper.
    Considerar añadir RAGAS (Faithfulness + Answer Relevancy) una vez el corpus esté más maduro.



## 7. Referencia rápida de comandos

```bash
# Activar entorno
source .venv/bin/activate

# Descargar el modelo LLM (solo la primera vez)
python app.py --download-model

# Ingestar corpus completo
python app.py --ingest

# Ingestar un festival concreto
python app.py --ingest --festival warm_up

# Lanzar chatbot
python app.py

# Lanzar en puerto alternativo
SERVER_PORT=8080 python app.py
```


