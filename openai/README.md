# OpenAI Learning Workspace

A hands-on workspace for exploring OpenAI’s API, from setup to advanced function calling, optimized for minimal costs and maximum learning.

---

## ⚙️ Prerequisites

* **macOS** with Homebrew installed
* **pyenv** (for Python version management)
* **VS Code** with Python & Jupyter extensions

---

## 🔧 Configuration

### 1. .env & .env.example

* **.env.example**:

  ```env
  OPENAI_API_KEY=your_openai_api_key_here
  ```
* Copy to **.env** and replace with your real key.

### 2. .gitignore

```gitignore
# Secrets
.env

# Python
__pycache__/
*.py[cod]

# Version management
# Ensure the .python-version file is tracked (do NOT ignore it) so pyenv can auto-switch environments.

# Jupyter
.ipynb_checkpoints/

# VS Code
.vscode/
```

---

## 🚀 API Methods Overview

OpenAI’s Python SDK (v1.x) exposes these main services:

| Service               | Endpoint                                              | Use-case                                               |
| --------------------- | ----------------------------------------------------- | ------------------------------------------------------ |
| **Completions**       | `openai.completions.create()`                         | Single-turn text tasks (summaries, Q\&A)               |
| **Chat Completions**  | `openai.chat.completions.create()`                    | Multi-turn conversations, system/user roles, streaming |
| **Edits**             | `openai.edits.create()`                               | Grammar corrections, rewrites                          |
| **Embeddings**        | `openai.embeddings.create()`                          | Vectorize text for search & RAG                        |
| **Images**            | `openai.images.create()`, `create_edit()`             | DALL·E generation & inpainting                         |
| **Audio**             | `openai.audio.transcribe()`, `translate()`            | Whisper-based transcription & translation              |
| **Moderation**        | `openai.moderations.create()`                         | Content safety checks                                  |
| **Files & Fine-tune** | `openai.files.create()`, `openai.fine_tunes.create()` | Upload data & run fine-tuning jobs                     |
| **Models**            | `openai.models.list()`, `retrieve()`                  | List available models and metadata                     |

---

## 💰 Model Pricing & Selection

Choose a model balancing **cost**, **speed**, and **capability**:

| Model                | Input \$\$/1K tokens | Output \$\$/1K tokens | Context window | Best for                             |
| -------------------- | -------------------- | --------------------- | -------------- | ------------------------------------ |
| `gpt-3.5-turbo`      | 0.0015               | 0.0020                | 4K             | Cheap, fast prototyping              |
| `gpt-3.5-turbo-16k`  | 0.0030               | 0.0040                | 16K            | Longer context, docs & logs          |
| `gpt-3.5-turbo-1106` | 0.0015               | 0.0020                | 4K             | Stable snapshot of 3.5-turbo         |
| `gpt-4`              | 0.03                 | 0.06                  | 8K             | High-quality reasoning & code review |
| `gpt-4-32k`          | 0.06                 | 0.12                  | 32K            | Very long context, transcripts       |

> **Tip:** Default to `gpt-3.5-turbo` for dev and testing; upgrade to 16K or GPT-4 variants as needs evolve.

---

## 🔄 Function Calling

1. **Define functions** in your request:

   ```python
   functions=[{
     "name": "get_current_weather",
     "description": "Get the current weather",
     "parameters": { /* JSON Schema */ }
   }]
   ```
2. **Invoke the API** with `function_call="auto"` or force via `{"name":...}`.
3. **Detect calls** on the Pydantic response:

   ```python
   message = response.choices[0].message
   if message.function_call:
       args = json.loads(message.function_call.arguments)
       result = get_current_weather(**args)
   ```
4. **Return structured data** without brittle parsing, enabling seamless tool integration.

---

## 🛠️ ChatCompletion Hyperparameters

Fine-tune response behavior by adjusting these parameters on your `openai.chat.completions.create()` calls:

| Parameter           | Type                        | Default       | Description                                                                                  |
| ------------------- | --------------------------- | ------------- | -------------------------------------------------------------------------------------------- |
| `model`             | string                      | –             | Model ID to use (e.g., `"gpt-3.5-turbo"`).                                                   |
| `messages`          | array of objects            | –             | Chat history: each item with `role` (`system`,`user`,`assistant`) and `content` string.      |
| `temperature`       | float (0–2)                 | `1.0`         | Controls randomness. Lower = more deterministic; higher = more creative.                     |
| `top_p`             | float (0–1)                 | `1.0`         | Nucleus sampling: consider only tokens comprising the top *p* probability mass.              |
| `n`                 | integer                     | `1`           | Number of independent completions to generate (A/B testing).                                 |
| `max_tokens`        | integer                     | model default | Max tokens to generate in the response.                                                      |
| `stream`            | boolean                     | `false`       | If `true`, stream partial response chunks back as they arrive.                               |
| `stop`              | string or array             | `null`        | Up to 4 sequences where the API will stop generating further tokens.                         |
| `presence_penalty`  | float (−2.0–2.0)            | `0.0`         | Penalize new tokens based on whether they appear in the text so far (encourages new topics). |
| `frequency_penalty` | float (−2.0–2.0)            | `0.0`         | Penalize tokens based on their existing frequency in the text so far (reduces repetition).   |
| `logit_bias`        | object mapping token → bias | `null`        | Adjust likelihood of specific tokens by applying −100 to 100 bias to selected token IDs.     |
| `user`              | string                      | `null`        | A unique identifier for your end-user, helping OpenAI monitor for misuse.                    |
| `functions`         | array of function defs      | `[]`          | JSON-Schema definitions to enable function-calling.                                          |
| `function_call`     | `"auto"`/`"none"`/object    | `"none"`      | Controls if and how the model attempts to call provided functions.                           |

## 📚 Learning & Next Steps

* **Explore each demo** in the `openai/` folder: script (`.py`) and notebook (`.ipynb`).
* **Watch costs** via `response.usage.prompt_tokens` & `.completion_tokens`.
* **Experiment** with hyperparameters: `temperature`, `top_p`, `max_tokens`, `stop`, `n`, penalties.
* **Extend**: add embeddings + vector DB for RAG, or images + audio for multimodal apps.

Happy coding! 🚀
