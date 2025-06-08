# Anthropic Claude Lab

A hands-on workspace for exploring Anthropic’s Claude API, from setup through advanced usage, optimized for rapid prototyping with the Haiku 3.5 model.

---

## ⚙️ Setup & Configuration

1. **File structure**

   ```text
   anthropic/
   ├── .gitignore
   ├── .env.example
   ├── requirements.txt
   ├── anthropic_example.py
   ├── anthropic_example.ipynb
   └── README.md
   ```
2. **.gitignore**

   ```gitignore
   # Secrets
   .env

   # Python caches
   __pycache__/
   *.py[cod]

   # Jupyter
   .ipynb_checkpoints/

   # VS Code
   .vscode/
   ```
3. **Environment file** (`.env.example`)

   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

   Copy to `.env` (never check this in).

---

## 📦 Installation

In your Python virtual environment:

```bash
pip install anthropic python-dotenv jupyterlab ipykernel
```

---

## 🔑 API Key Setup

1. **Sign up** at the Anthropic Console:
   [https://console.anthropic.com/signup](https://console.anthropic.com/signup)
2. **Create** an API key under **Profile → API Keys → + Create Key**, then copy it.
3. **Populate** your `.env`:

   ```bash
   cd anthropic
   cp .env.example .env
   # edit .env to add your ANTHROPIC_API_KEY
   ```

---

## 🌐 Model Offerings & Pricing

Anthropic’s Claude models all support up to a **200 000-token** context window. Prices are per **million tokens (MTok)**:

| Model                 | Input Cost (\$/MTok) | Output Cost (\$/MTok) | Generation |
| --------------------- | -------------------- | --------------------- | ---------- |
| **Claude Haiku 3.5**  | 0.80                 | 1.00                  | v3         |
| **Claude Sonnet 3.5** | 3.00                 | 15.00                 | v3         |
| **Claude Sonnet 3.7** | 3.00                 | 15.00                 | v3         |
| **Claude Sonnet 4**   | 3.00                 | 15.00                 | v4         |
| **Claude Opus 3**     | 15.00                | 75.00                 | v3         |
| **Claude Opus 4**     | 15.00                | 75.00                 | v4         |

> We’ll use **Claude Haiku 3.5** (the fastest, cheapest) in this lab.

---

## 📈 Rate Limits

Default **Tier 1** limits (per organization):

| Metric                    | Value  |
| ------------------------- | ------ |
| Requests per minute (RPM) | 60     |
| Input tokens per minute   | 30 000 |
| Output tokens per minute  | 8 000  |

Exceeding any limit returns a 429 with a `Retry-After` header.

---

## 🛠️ API Methods

Using **Anthropic SDK v0.3.x+**:

| Endpoint               | Method                           | Description                                     |
| ---------------------- | -------------------------------- | ----------------------------------------------- |
| **List Models**        | `client.models.list()`           | Retrieve available model IDs                    |
| **Messages API**       | `client.messages.create(...)`    | Single request/response with `messages` list    |
| **Streaming**          | `client.messages.stream(...)`    | Incremental responses via `stream.text_stream`  |
| **Legacy Completions** | `client.completions.create(...)` | Older `/v1/complete` endpoint (not recommended) |

---

## 🎛️ Hyperparameters

Adjust these in your `messages.create()` or `messages.stream()` calls:

| Parameter          | Type               | Default | Description                                                                      |
| ------------------ | ------------------ | ------- | -------------------------------------------------------------------------------- |
| `model`            | `string`           | —       | Model ID (e.g. `"claude-3-haiku-20240307"`)                                      |
| `messages`         | `[{role,content}]` | —       | Conversation history; supply at least one `{role: "user", content: ...}` message |
| `max_tokens`       | `integer`          | —       | Maximum tokens to generate                                                       |
| `temperature`      | `float` (0–1)      | `1.0`   | Sampling randomness; higher = more creative                                      |
| `top_p`            | `float` (0–1)      | `1.0`   | Nucleus sampling threshold                                                       |
| `top_k`            | `int`              | —       | Limits to top-k tokens at each step                                              |
| `stop_sequences`   | `[string,…]`       | `[]`    | Sequences that halt generation                                                   |
| `stream`           | `bool`             | `false` | If `true`, returns streaming chunks                                              |
| `metadata.user_id` | `string`           | `null`  | Opaque end-user ID for monitoring                                                |

---

## 🎓 Findings & Learning

* **Haiku 3.5** offers the best cost/latency trade-off for prototyping.
* The **Messages API** is current and supports streaming; legacy completions are deprecated.
* Monitor rate limits via response headers like `anthropic-ratelimit-tokens-remaining`.

---

## 🚀 Next Steps

1. **Run** the example and capture logs:

   ```bash
   cd anthropic
   python anthropic_example.py > run.log 2>&1
   ```
2. **Tweak** hyperparameters (`temperature`, `max_tokens`, `stop_sequences`).
3. **Commit** your branch:

   ```bash
   git checkout -b lab-anthropic
   git add .
   git commit -m "feat: complete Anthropic Claude lab"
   git push -u origin lab-anthropic
   ```
4. **Extend**: integrate Claude with embeddings, RAG, or multi-agent orchestration in the next lab.
