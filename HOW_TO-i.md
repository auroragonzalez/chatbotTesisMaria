# FestGPT — Guía para personas que no saben programar

## ¿Qué es este proyecto?

FestGPT es un **chatbot** (un asistente virtual con el que hablas por texto) especializado en festivales de música. Le preguntas algo sobre un festival —horarios, cómo llegar, qué llevar— y te responde basándose en documentos reales del festival, no en información inventada.

Está pensado para que lo use el público de un festival desde el móvil, como si hablaras con un trabajador de información del festival, pero disponible 24 horas.

---

## ¿Cómo funciona? (explicado sin jerga técnica)

Imagina que tienes una carpeta con documentos sobre un festival: horarios, FAQs, información de transporte, etc. El chatbot hace tres cosas cada vez que le preguntas:

1. **Buscar**: lee tu pregunta y busca entre todos los documentos del festival los párrafos que más se parecen a lo que preguntas. Por ejemplo, si preguntas _"¿qué autobús me lleva al festival?"_, busca en los textos que hablan de transporte.

2. **Combinar**: junta esos párrafos encontrados con tu pregunta y con instrucciones sobre _cómo_ debe responder (por ejemplo: "el usuario está ya en el festival, responde breve y operativo").

3. **Redactar**: envía todo eso a un modelo de lenguaje (una inteligencia artificial que sabe escribir) y le dice: "redacta una respuesta en español usando solo esta información, no te inventes nada".

Así te da respuestas basadas en datos reales, no en lo que el modelo "cree" o "recuerda" de internet.

### Los dos motores del chatbot

FestGPT usa dos inteligencias artificiales distintas, cada una para una tarea:

| Motor | qué hace | De dónde sale | ¿Necesita internet? |
|---|---|---|---|
| **Buscador** (embeddings) | Convierte los documentos del festival y tu pregunta a números, para encontrar los párrafos más parecidos | HuggingFace: `multilingual-e5-base` | Solo la primera vez (descarga ~1 GB). Luego funciona sin internet. |
| **Redactor** (LLM) | Redacta la respuesta en español a partir de los párrafos encontrados | Ollama Cloud: `gemma3:27b-cloud` | Sí, cada vez que preguntas algo. |

El buscador (HuggingFace) se descarga automáticamente la primera vez que arrancas el chatbot. Se guarda en tu ordenador y no se vuelve a tocar. Como el modelo `multilingual-e5-base` es público, no necesita contraseña.

El redactor (Ollama Cloud) es el de pago. No está en tu ordenador: cada pregunta viaja a los servidores de Ollama y vuelve con la respuesta.

### ¿Por qué no usa ChatGPT sin más?

Porque ChatGPT (o cualquier otro modelo) cuando no se le da información específica, **alucina**: se inventa respuestas que suenan bien pero son falsas. FestGPT obliga al modelo a responder solo con los documentos que tú le has dado.

---

## Estructura del proyecto (lo que hay en cada carpeta)

```
chatbotTesisMaria/
├── app.py                    ← El programa principal (el "cerebro")
├── requirements.txt          ← Lista de piezas de software que necesita
├── Dockerfile                ← Instrucciones para meterlo en un contenedor
├── docker-compose.yml        ← Para arrancar el contenedor fácilmente
├── .env.example              ← Plantilla de configuración (cópiala a .env)
├── HOW_TO.md                 ← Guía técnica antigua
├── HOW_TO-i.md               ← Esta guía (la estás leyendo)
├── festival_txts/            ← La "biblioteca" de documentos del festival
│   ├── warm_up/              ← Documentos del festival Warm Up
│   │   ├── faq.txt           ← Preguntas frecuentes
│   │   ├── horarios.txt      ← Horarios del festival
│   │   ├── accesos.txt       ← Información de entradas y accesos
│   │   └── transporte.txt    ← Cómo llegar y volver
│   ├── animal_sound/         ← Otro festival
│   └── mar_de_musicas/       ← Otro festival
├── chroma_db/                ← La "base de datos de búsqueda" (se crea sola)
├── eval/                     ← Herramientas para medir la calidad del chatbot
│   ├── qa_benchmark.json     ← 17 preguntas de prueba con respuestas esperadas
│   └── run_eval.py           ← Programa que mide cómo de bien responde cada modelo
└── contexto/                 ← Documentos académicos de la tesis
```

### Las piezas clave explicadas

- **`app.py`**: es el archivo que lo hace todo. Unas 400 líneas de código que cargan documentos, los preparan para buscar, lanzan la página web del chat y conectan con la inteligencia artificial externa.

- **`festival_txts/`**: aquí viven los documentos de cada festival. Son archivos `.txt` normales (los puedes abrir con el bloc de notas). Cada festival tiene su propia carpeta con 4 archivos por tema. **Esta es la carpeta que editarías para añadir información o crear un festival nuevo.**

- **`chroma_db/`**: cuando ejecutas el comando de "ingestión", el programa lee los `.txt`, los trocea en fragmentos pequeños y los guarda aquí en un formato especial optimizado para búsquedas rápidas. No se edita a mano.

- **`eval/`**: contiene un "examen" de 17 preguntas para ver cómo de bueno es el chatbot con distintos modelos de inteligencia artificial.

---

## Cómo ponerlo en marcha (paso a paso)

Necesitas tener Python 3.11 instalado en tu ordenador. Si no lo tienes, instálalo desde [python.org](https://python.org).

### 1. Instalar lo necesario (solo la primera vez)

Abre un terminal (la pantalla negra de comandos) en la carpeta del proyecto y escribe:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Esto crea un "entorno virtual" (una burbuja donde instalar cosas sin afectar al resto del ordenador) e instala todas las piezas que necesita el proyecto.

### 2. Configurar la conexión a Ollama Cloud (solo la primera vez)

Este proyecto usa **Ollama Cloud**, lo que significa que el modelo de IA no está en tu ordenador, sino en los servidores de Ollama. Tú pagas una suscripción y ellos ponen las máquinas que ejecutan el modelo.

Crea un archivo llamado `.env` copiando la plantilla:

```bash
cp .env.example .env
```

Abre `.env` con el bloc de notas y configura estos tres datos:

```
LLM_URL=https://ollama.com/v1/chat/completions
MODEL_NAME=gemma3:27b-cloud
LLM_API_KEY=tu_clave_de_api_de_ollama_cloud
```

- `LLM_URL`: la dirección de internet de los servidores de Ollama Cloud
- `MODEL_NAME`: el modelo al que te has suscrito (`gemma3:27b-cloud`)
- `LLM_API_KEY`: tu clave personal de acceso a Ollama Cloud. La encuentras en tu panel de Ollama, en la sección de API keys. **Sin esta clave, Ollama rechazará la conexión.**

### 3. Preparar los documentos del festival (cada vez que cambies los .txt)

```bash
python app.py --ingest
```

Esto lee todos los `.txt` de `festival_txts/`, los trocea y los guarda en `chroma_db/` para poder buscar rápido.

Si solo quieres procesar un festival concreto:

```bash
python app.py --ingest --festival warm_up
```

### 4. Arrancar el chatbot

```bash
python app.py
```

Abre tu navegador en `http://localhost:7860` y ya puedes hablar con FestGPT.

---

## Cómo usar la interfaz

Cuando abres `http://localhost:7860` ves:

- Un **desplegable de Festival** arriba: elige sobre qué festival quieres preguntar.
- Un **selector de Momento**: "Pre-festival" (antes de ir), "Durante" (ya estás allí), "Post-festival" (ya ha terminado). El chatbot cambia su forma de responder según esta fase.
- Una **caja de texto** donde escribes tu pregunta.
- El **chat** donde aparecen las respuestas.

### Ejemplos de preguntas que puedes hacer

- _"¿A qué hora abren las puertas el viernes?"_
- _"¿Cómo llego desde el centro de Murcia?"_
- _"¿Puedo entrar con una botella de agua?"_
- _"¿Hay guardarropa?"_

---

## Cómo añadir información nueva o un festival nuevo

### Añadir información a un festival que ya existe

1. Ve a la carpeta del festival dentro de `festival_txts/`, por ejemplo `festival_txts/warm_up/`.
2. Crea un archivo nuevo `.txt` (con el bloc de notas) o edita uno que ya exista.
3. Escribe la información con este formato:
   - Una idea por párrafo, o en formato pregunta-respuesta.
   - En español.
   - Sin formato especial, solo texto plano.
4. Vuelve a ejecutar: `python app.py --ingest --festival warm_up`
5. El chatbot ya sabrá responder sobre esa información nueva.

### Crear un festival desde cero

1. Crea una carpeta nueva: `festival_txts/nombre_de_tu_festival/`
2. Mete dentro archivos `.txt` con la información del festival (horarios, transporte, FAQs, accesos...).
3. Ejecuta: `python app.py --ingest --festival nombre_de_tu_festival`
4. El festival nuevo aparecerá automáticamente en el desplegable de la web.

---

## Configuración (el archivo .env)

Puedes cambiar el comportamiento del chatbot sin tocar el código editando el archivo `.env`:

| Variable | Qué hace | Valor por defecto |
|---|---|---|
| `LLM_URL` | Dirección de Ollama Cloud | `https://ollama.com/v1/chat/completions` |
| `MODEL_NAME` | Modelo contratado en Ollama Cloud | `gemma3:27b-cloud` |
| `LLM_API_KEY` | Tu clave de API de Ollama Cloud | (obligatorio, la obtienes en tu panel de Ollama) |
| `CHUNK_SIZE` | Tamaño de los fragmentos al trocear documentos | 500 |
| `RETRIEVER_K` | Cuántos fragmentos recuperar por pregunta | 4 |
| `TEMPERATURE` | Creatividad del modelo (0 = preciso, 1 = creativo) | 0.3 |
| `SERVER_PORT` | Puerto donde se abre la web | 7860 |

---

## Cómo viaja tu pregunta hasta Ollama Cloud y vuelve la respuesta

Cuando escribes una pregunta en el chat, esto es lo que ocurre por dentro:

### El viaje, paso a paso

**Paso 1 — Buscar en los documentos (local)**

El programa busca en `chroma_db/` los párrafos del festival que más se parecen a tu pregunta. Esto ocurre en tu ordenador, no gasta suscripción de Ollama.

**Paso 2 — Preparar el mensaje (local)**

Junta los párrafos encontrados con tu pregunta y con instrucciones sobre cómo debe responder. Por ejemplo: *"Responde en español usando solo esta información, no te inventes nada".*

**Paso 3 — Enviar a Ollama Cloud (internet)**

El programa abre una conexión a internet hacia `https://ollama.com/v1/chat/completions` y envía:
- El mensaje completo (contexto + pregunta + instrucciones)
- Tu `LLM_API_KEY` (para demostrar que eres tú quien paga la suscripción)
- El nombre del modelo (`gemma3:27b-cloud`)

**Paso 4 — Ollama Cloud genera la respuesta (internet)**

Los servidores de Ollama reciben tu petición, ejecutan el modelo `gemma3:27b-cloud` en sus máquinas, y **van devolviendo la respuesta palabra por palabra** según la generan.

**Paso 5 — Mostrar la respuesta (local)**

El programa recibe ese goteo de palabras y las muestra en el chat en tiempo real. Por eso ves el texto aparecer poco a poco, como si alguien estuviera escribiendo.

### Esquema visual

```
Tú (navegador)          app.py (tu ordenador)         Ollama Cloud (internet)
     │                         │                              │
     │ escribes "¿horarios?"   │                              │
     │────────────────────────>│                              │
     │                         │                              │
     │                         │ busca en chroma_db           │
     │                         │ los párrafos relevantes      │
     │                         │                              │
     │                         │ POST /v1/chat/completions    │
     │                         │ API key + prompt             │
     │                         │─────────────────────────────>│
     │                         │                              │ ejecuta
     │                         │                              │ gemma3:27b
     │                         │        "Las puertas"         │
     │                         │<─────────────────────────────│
     │       "Las puertas"     │                              │
     │<────────────────────────│                              │
     │                         │     "abren el viernes"       │
     │                         │<─────────────────────────────│
     │    "abren el viernes"   │                              │
     │<────────────────────────│                              │
     │                         │        "a las 17:00"         │
     │                         │<─────────────────────────────│
     │      "a las 17:00"      │                              │
     │<────────────────────────│                              │
```

### Qué va a internet y qué no

| Va a internet | Se queda en tu ordenador |
|---|---|
| La pregunta ya preparada (contexto + instrucciones) | La búsqueda en los documentos (`chroma_db/`) |
| La respuesta del modelo | Los documentos originales (`festival_txts/`) |
| Tu API key (para identificarte) | La interfaz del chat (Gradio) |

El modelo de IA **no está en tu ordenador**. Está en los servidores de Ollama. Tú pagas la suscripción y ellos ponen las máquinas. Tu ordenador solo se encarga de buscar entre los documentos del festival y de preparar la pregunta.

---

## Cómo medir la calidad del chatbot

El proyecto incluye un "examen" automático para ver cómo de bien responde:

```bash
python eval/run_eval.py --models phi3
```

Esto:
- Hace las 17 preguntas del examen al chatbot.
- Compara las respuestas con las respuestas esperadas.
- Mide: precisión, velocidad, y si se inventa cosas cuando no tiene información.
- Guarda los resultados en archivos CSV dentro de `eval/`.

---

## Resumen rápido de comandos

```bash
# Activar el entorno (siempre antes de cualquier cosa)
source .venv/bin/activate

# Preparar documentos
python app.py --ingest

# Arrancar el chatbot
python app.py

# Abrir en el navegador: http://localhost:7860
```

---

## Preguntas frecuentes

**¿Necesito internet para usarlo?**
Sí. Este proyecto usa Ollama Cloud, así que necesita conexión a internet para enviar las preguntas al modelo y recibir las respuestas. La búsqueda en los documentos del festival sí ocurre en tu ordenador sin internet, pero la generación de la respuesta no.

**¿Puedo usarlo en Windows?**
Sí, el proyecto funciona en Windows, Mac y Linux. Los comandos de terminal cambian ligeramente en Windows (usa `venv\Scripts\activate` en vez de `source .venv/bin/activate`).

**¿Funciona en español?**
Sí, todo el sistema está diseñado para funcionar en español: los documentos, las respuestas, las instrucciones al modelo.

**¿Se inventa respuestas?**
Está diseñado para no hacerlo: el modelo solo puede responder con la información de los documentos. Si no encuentra nada relevante, debe decir "no tengo esa información". Aun así, ningún sistema es perfecto; la evaluación mide precisamente cuánto alucina.
