# FestAI — Referencia de funciones Python

Este documento explica cada función y variable del proyecto para alguien que quiera entender o modificar el código.

---

## `app.py` — Aplicación principal

### Orden de ejecución al arrancar

Cuando ejecutas `python app.py`, esto es lo que ocurre **en orden**:

1. **Importaciones** (líneas 32-46): se cargan todas las librerías.
2. **Variables de configuración** (líneas 53-68): se leen las variables de entorno o se asignan los valores por defecto.
3. **Carga del modelo de embeddings** (líneas 144-149): se descarga (si es la primera vez) y se carga en memoria el modelo `multilingual-e5-base` de HuggingFace. Esto tarda unos segundos y solo ocurre una vez.
4. **Interfaz Gradio** (líneas 322-351): se construye la web del chat.
5. **Entry point** (líneas 358-393): según los argumentos `--ingest`, `--download-model` o sin argumentos, ingesta el corpus o lanza la web.

---

### Variables de configuración (líneas 53-68)

Son variables globales (módulo) que se leen una vez al arrancar. Todas toman su valor de una variable de entorno y tienen un valor por defecto.

```python
LLM_URL = os.getenv("LLM_URL", os.getenv("VLLM_URL", "http://localhost:11434/v1/chat/completions"))
```

- **Doble fallback**: primero busca `LLM_URL`, si no existe busca `VLLM_URL` (nombre antiguo), si tampoco usa el valor por defecto (Ollama local).
- Los valores numéricos se convierten con `int()` o `float()`. Si la variable de entorno contiene texto no numérico, el programa fallará al arrancar.

| Variable | Tipo | Default | Qué controla |
|---|---|---|---|
| `LLM_URL` | `str` | `http://localhost:11434/v1/chat/completions` | Endpoint HTTP del modelo de lenguaje |
| `MODEL_NAME` | `str` | `phi3:mini` | Nombre del modelo a usar |
| `EMBEDDING_MODEL` | `str` | `intfloat/multilingual-e5-base` | Modelo de embeddings de HuggingFace |
| `EMBEDDING_DEVICE` | `str` | `cuda` | `cuda` para GPU, `cpu` para CPU |
| `CHROMA_DIR` | `Path` | `./chroma_db` | Carpeta donde se guarda la base vectorial |
| `DATA_DIR` | `Path` | `./festival_txts` | Carpeta raíz de los documentos |
| `CHUNK_SIZE` | `int` | `500` | Caracteres por fragmento al trocear documentos |
| `CHUNK_OVERLAP` | `int` | `50` | Caracteres de solapamiento entre fragmentos |
| `RETRIEVER_K` | `int` | `4` | Nº de fragmentos recuperados por pregunta |
| `MAX_TOKENS` | `int` | `512` | Tokens máximos en la respuesta del LLM |
| `TEMPERATURE` | `float` | `0.3` | Creatividad del LLM (0 = determinista) |
| `SERVER_PORT` | `int` | `7860` | Puerto donde se sirve la web |
| `HF_TOKEN` | `str` o `None` | `None` | Token de HuggingFace para modelos con acceso restringido |
| `LLM_API_KEY` | `str` o `None` | `None` | API key para Ollama Cloud. También acepta `OLLAMA_API_KEY` como fallback |

---

### Constantes del sistema

#### `PHASE_PROMPTS` (línea 115) — `dict[str, str]`

Diccionario con las instrucciones de sistema para cada fase de uso del chatbot. Las claves son `"Pre-festival"`, `"Durante"` y `"Post-festival"`. Cada valor es un párrafo en español que le dice al LLM cómo debe orientar su respuesta.

#### `SYSTEM_BASE` (línea 133) — `str`

Instrucción base que se incluye en **todos** los prompts, independientemente de la fase. Obliga al modelo a responder en español y a no inventar información.

---

### Funciones

#### `_get_token()` (línea 74) → `str | None`

**Función interna** (el guion bajo indica que no debe usarse desde fuera del módulo).

Obtiene el token de HuggingFace para descargar modelos con acceso restringido. Primero mira la variable de entorno `HF_TOKEN`; si no existe, pide al usuario que lo escriba en el terminal (sin mostrar lo que teclea, por seguridad). Si el usuario pulsa Enter sin escribir nada, devuelve `None`.

**Cuándo se usa**: solo dentro de `ensure_model_downloaded()`.

---

#### `ensure_model_downloaded(model_name: str)` (línea 83) → `None`

**Solo se ejecuta con `--download-model`.**

Comprueba si un modelo de HuggingFace ya está en la caché local (`~/.cache/huggingface/`). Si no está, lo descarga pidiendo el token si es necesario. Los modelos con acceso restringido (como Phi-3) requieren token; los públicos (como TinyLlama) no.

**Flujo**:
1. Intenta `snapshot_download(model_name, local_files_only=True)` — si funciona, el modelo ya está en caché y termina.
2. Si falla con `LocalEntryNotFoundError`, el modelo no está descargado → pide el token y descarga.

**Aviso**: esta función es un vestigio de cuando el LLM se ejecutaba en local con vLLM. Con Ollama Cloud ya no es necesaria, porque el modelo está en los servidores de Ollama.

---

#### `get_festivals()` (línea 103) → `list[str]`

Devuelve una lista con los nombres de los festivales disponibles. Los detecta automáticamente escaneando las subcarpetas dentro de `DATA_DIR` (`festival_txts/`). Si la carpeta no existe o está vacía, devuelve `["warm_up"]` como fallback.

**Se llama dos veces**:
- Al construir la UI de Gradio (línea 329) para rellenar el desplegable.
- Al ingestar con `--ingest` sin especificar festival (línea 383).

---

#### `embedding_model` (línea 145) — `HuggingFaceEmbeddings`

No es una función, es un **objeto global** que se crea al importar el módulo. Carga el modelo `intfloat/multilingual-e5-base` de HuggingFace y lo deja en memoria (GPU o CPU según `EMBEDDING_DEVICE`).

**Importante**: se carga al hacer `import app`, no al arrancar la web. Cualquier script que importe `app.py` (como `eval/run_eval.py`) pagará el coste de cargar este modelo.

---

#### `ingest_corpus(festival: str)` (línea 156) → `None`

**Solo se ejecuta con `--ingest`.**

Lee todos los archivos `.txt` de `festival_txts/<festival>/`, los convierte en fragmentos y los guarda en ChromaDB para poder hacer búsquedas.

**Flujo detallado**:

1. **Verifica** que la carpeta del festival existe. Si no, lanza `FileNotFoundError`.
2. **Carga** los `.txt` con `DirectoryLoader` + `TextLoader` (encoding utf-8). Busca recursivamente en subcarpetas con `glob="**/*.txt"`.
3. **Trocea** cada documento en chunks con `RecursiveCharacterTextSplitter`. Intenta cortar por párrafos, no por mitad de palabra. El tamaño y solapamiento vienen de las variables `CHUNK_SIZE` y `CHUNK_OVERLAP`.
4. **Borra** la colección anterior del mismo festival en ChromaDB. Esto garantiza que tras editar los `.txt`, la base vectorial se reconstruye limpia (sin mezclar chunks viejos y nuevos).
5. **Guarda** los nuevos chunks en ChromaDB. Internamente, ChromaDB convierte cada chunk a un vector numérico usando `embedding_model` y lo almacena.

**Las colecciones en ChromaDB tienen el mismo nombre que la carpeta del festival**. Ej: `warm_up`, `animal_sound`.

---

#### `get_context(query: str, festival: str)` (línea 204) → `str`

Dada una pregunta y un festival, busca en ChromaDB los fragmentos más relevantes y los devuelve como un solo texto.

**Flujo**:

1. Abre la colección ChromaDB del festival indicado.
2. Crea un `retriever` que busca por similitud (comparando vectores numéricos).
3. Recupera los `k` fragmentos más parecidos a la pregunta (`RETRIEVER_K`, por defecto 4).
4. Los junta en un solo string separados por doble salto de línea.

**Esta función se llama en cada pregunta del chat.** Es rápida (milisegundos) porque ChromaDB ya tiene los vectores precalculados.

---

#### `build_prompt(context: str, question: str, phase: str)` (línea 223) → `str`

Construye el texto completo que se enviará al LLM. Ensambla cuatro piezas:

```
[SYSTEM_BASE]
Contexto de uso: [PHASE_PROMPTS[phase]]
CONTEXTO DEL CORPUS:
[context]
PREGUNTA: [question]
RESPUESTA:
```

La fase se busca en `PHASE_PROMPTS`; si no se encuentra (por ejemplo, `phase=""`), se omite la instrucción de fase.

**El prompt es un solo string**, no una lista de mensajes. La función `generate_stream` lo convierte a formato chat si es necesario.

---

#### `generate_stream(prompt: str)` (línea 238) → `Generator[str, None, None]`

Es un **generador** (usa `yield`). Cada vez que produce un valor, ese valor es una palabra o fragmento de la respuesta del LLM.

**Flujo detallado**:

1. **Detecta el tipo de API**: mira si la URL contiene `/chat/completions`:
   - Si sí → formato chat de Ollama/OpenAI: `{"messages": [{"role": "user", "content": prompt}]}`
   - Si no → formato completions de vLLM: `{"prompt": prompt}`
2. **Añade la API key** si existe: cabecera HTTP `Authorization: Bearer <LLM_API_KEY>`. Si `LLM_API_KEY` es `None` (Ollama local), no añade cabecera.
3. **Envía la petición HTTP POST** con `stream=True` y timeout de 120 segundos.
4. **Lee la respuesta línea a línea** (SSE — Server-Sent Events):
   - Omite líneas vacías.
   - Omite líneas que no empiezan por `data:`.
   - Si encuentra `[DONE]`, termina.
   - Extrae el texto del JSON: en chat API busca `choices[0].delta.content`; en completions busca `choices[0].text`.
   - Si encuentra texto, lo emite con `yield`.
   - Si el JSON está mal formado, ignora esa línea y sigue.

**Por qué usa `yield`**: permite que Gradio muestre la respuesta palabra por palabra en vez de esperar a que esté completa. El usuario ve el texto aparecer progresivamente.

---

#### `chat(message, history, festival, phase)` (línea 300) → `Generator[str, None, None]`

Es la función que Gradio llama cada vez que el usuario escribe un mensaje. Encadena toda la pipeline RAG:

```
pregunta → get_context() → build_prompt() → generate_stream() → respuesta
```

**Parámetros** (los pasa Gradio automáticamente):
- `message`: lo que el usuario ha escrito.
- `history`: historial de la conversación (no se usa, pero Gradio lo requiere).
- `festival`: valor del desplegable de festival.
- `phase`: valor del selector de fase.

**Flujo**:
1. Si el mensaje está vacío, devuelve `""` y termina.
2. Mide el tiempo con `time.time()`.
3. Recupera contexto → construye prompt → genera streaming.
4. Acumula los fragmentos en `partial` y los va emitiendo.
5. Al terminar, imprime en terminal un resumen: `[chat] festival=... phase=... time=...s`.

---

#### UI de Gradio (líneas 322-351)

Se construye al importar el módulo (antes del `if __name__ == "__main__"`). Componentes:

- `gr.Blocks(title="FestAI")` — contenedor principal.
- `gr.Markdown(...)` — título.
- `gr.Dropdown` — selector de festival, se rellena con `get_festivals()`.
- `gr.Radio` — selector de fase, usa las claves de `PHASE_PROMPTS`.
- `gr.ChatInterface` — el chat en sí, conectado a la función `chat()`.

`additional_inputs=[festival_selector, phase_selector]` le dice a Gradio que pase esos valores como argumentos extra a `chat()`.

---

#### Entry point (líneas 358-393)

Tres modos de ejecución según los argumentos:

| Comando | Qué hace |
|---|---|
| `python app.py --download-model` | Descarga el modelo LLM de HuggingFace y sale |
| `python app.py --ingest` | Ingosta todos los festivales y sale |
| `python app.py --ingest --festival X` | Ingosta solo el festival X y sale |
| `python app.py` | Lanza la web en `http://0.0.0.0:7860` |

Los tres primeros modos llaman a `sys.exit(0)` al terminar, así que no lanzan la web.

---

## `eval/run_eval.py` — Evaluación comparativa

### Importaciones desde `app.py`

El script importa directamente variables y funciones de `app.py`:

```python
from app import (
    CHROMA_DIR, EMBEDDING_MODEL, EMBEDDING_DEVICE,
    RETRIEVER_K, TEMPERATURE, VLLM_URL,
    embedding_model, get_context, build_prompt, PHASE_PROMPTS,
)
```

**Atención**: `VLLM_URL` ya no existe en `app.py` (se renombró a `LLM_URL` en la rama `feat/ollama-cloud-integration`). Esta importación fallará hasta que se actualice.

El script paga el coste de cargar `embedding_model` al importar `app`.

---

### Constantes

#### `MODEL_ALIASES` (línea 47) — `dict[str, str]`

Mapea nombres cortos a nombres completos de HuggingFace:

```python
{
    "phi3":       "microsoft/Phi-3-mini-4k-instruct",
    "salamandra": "BSC-LT/salamandra-7b-instruct",
    "mistral":    "mistralai/Mistral-7B-Instruct-v0.3",
    "llama3":     "meta-llama/Llama-3.1-8B-Instruct",
    "qwen":       "Qwen/Qwen2.5-7B-Instruct",
    "tinyllama":  "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
}
```

#### `BENCHMARK_PATH` y `FESTIVAL`

El benchmark está fijado al festival `warm_up`. Si se evalúa con otro corpus, hay que cambiar `FESTIVAL` y posiblemente las preguntas.

---

### Funciones

#### `rouge_l(prediction: str, reference: str)` (línea 64) → `float`

Calcula la métrica ROUGE-L (solapamiento léxico) entre la respuesta generada y la esperada. Mide cuántas secuencias de palabras coinciden, sin importar el orden exacto.

Usa `rouge_scorer` de la librería `rouge_score`. Valor entre 0 y 1.

---

#### `bertscore_f1(predictions: list[str], references: list[str])` (línea 71) → `list[float]`

Calcula BERTScore F1 en español para una lista de respuestas. A diferencia de ROUGE, BERTScore mide **similitud semántica** (significado) usando embeddings contextuales.

Se procesa en bloque (todas las respuestas juntas) en vez de una a una, porque es mucho más rápido en GPU.

---

#### `hallucination_rate(answers: list[str], expected_no_info: list[bool])` (línea 78) → `float`

Mide la **tasa de alucinación**: fracción de preguntas fuera de corpus donde el modelo NO dijo "no tengo esa información".

**Cómo funciona**:
1. Para cada pregunta marcada como `fuera_de_corpus`, mira si la respuesta contiene frases como "no tengo esa información", "no dispongo de esa información", etc.
2. Si no contiene ninguna de esas frases, cuenta como alucinación.
3. Devuelve: `alucinaciones / total_preguntas_fuera_de_corpus`.

El valor ideal es 0.0 (siempre admite que no sabe). Un valor alto indica que el modelo se inventa respuestas.

---

#### `generate_answer(question, phase, model_name, max_tokens=256)` (línea 105) → `tuple[str, float]`

Similar a `generate_stream()` en `app.py`, pero sin streaming. Hace una llamada bloqueante al LLM y devuelve `(respuesta, latencia_segundos)`.

**Diferencia con `generate_stream()`**:
- Usa el formato completions de vLLM (no chat), mediante `VLLM_URL`.
- `stream=False`: espera la respuesta completa.
- Extrae `choices[0].text`.
- Captura excepciones y devuelve `[ERROR: ...]` si algo falla.

---

#### `run_evaluation(model_aliases: list[str])` (línea 135) → `None`

Función principal de la evaluación. Itera sobre cada modelo y cada pregunta del benchmark.

**Flujo**:

1. Carga `qa_benchmark.json` y crea un timestamp para los archivos de salida.
2. Para cada modelo:
   - Para cada pregunta del benchmark:
     - Genera respuesta con `generate_answer()`.
     - Guarda respuesta, referencia esperada, latencia.
   - Calcula ROUGE-L para cada pregunta individual.
   - Calcula BERTScore en bloque para todas las preguntas del modelo.
   - Calcula tasa de alucinación global del modelo.
3. Guarda dos CSVs:
   - `results_<timestamp>.csv`: una fila por pregunta, con todas las métricas.
   - `summary_<timestamp>.csv`: una fila por modelo × fase, con medias de ROUGE-L, BERTScore y latencia.
4. Imprime una tabla resumen en consola.

---

### Orden de ejecución del benchmark

```
run_evaluation()
  └─ para cada modelo:
       └─ para cada pregunta:
            ├─ get_context(pregunta, "warm_up")    ← busca en ChromaDB
            ├─ build_prompt(contexto, pregunta, fase) ← construye el prompt
            ├─ generate_answer(pregunta, fase, modelo) ← llama al LLM
            ├─ rouge_l(respuesta, referencia)       ← métrica individual
            ├─ (guarda respuesta para BERTScore en bloque)
            └─ (guarda flag fuera_de_corpus)
       └─ bertscore_f1(todas_las_respuestas, todas_las_referencias)
       └─ hallucination_rate(todas_las_respuestas, flags)
```

---

## Flujo completo de una pregunta en el chat

```
Usuario escribe "¿A qué hora abren el viernes?"
  │
  ▼
chat(message="¿A qué hora abren el viernes?", festival="warm_up", phase="Pre-festival")
  │
  ▼
get_context(query="¿A qué hora abren el viernes?", festival="warm_up")
  │  Abre ChromaDB → busca los 4 chunks más parecidos → devuelve texto
  ▼
build_prompt(context="...", question="¿A qué hora abren el viernes?", phase="Pre-festival")
  │  Junta: SYSTEM_BASE + phase_instruction + context + question
  ▼
generate_stream(prompt="[texto completo del prompt]")
  │  POST HTTPS a Ollama Cloud → lee streaming SSE → yield cada palabra
  ▼
chat() acumula palabras con yield partial
  │
  ▼
Gradio muestra el texto palabra por palabra en el navegador
```
