# Vertex AI Workbench Lab

A step-by-step guide to provisioning Google Vertex AI Workbench via the Cloud Console UI, accessing it over SSH, and running BERT‐based notebooks (Transformer inference and Question Answering) from your local machine.

---

## 📁 File Structure

```text
google-ai-studio/                   # Lab root folder
├── .gitignore                       # Ignore secrets and caches
├── .env.example                     # GCP project & credentials placeholders
├── requirements.txt                 # Python SDK & utility libraries
├── vertex_workbench_example.py      # Sample Vertex AI SDK script
├── bert_transformer_toch_vertex_ai_remote_ssh.ipynb  # BERT embeddings notebook
├── question_answering_bert.ipynb    # BERT QA notebook
└── README.md                        # This file
```

---

## ⚙️ Prerequisites

* **Google Cloud account** with **\$300 free trial** credits
* **Application Default Credentials (ADC)**:

   * Run:

     ```bash
     gcloud auth application-default login
     ```
   * Or set a Service Account key via `.env`:

     ```env
     GOOGLE_APPLICATION_CREDENTIALS=/path/to/vertex-sa-key.json
     ```

* **Billing enabled** on your project
* **gcloud CLI** installed and authenticated locally
* **Vertex AI API** enabled in your project

---

## 2. gcloud CLI Installation & Configuration

Before you can SSH or manage resources, install and set up the Google Cloud CLI locally:

1. **Install via Homebrew (macOS)**

   ```bash
   brew install --cask google-cloud-sdk
   ```

   This installs `gcloud`, `gsutil`, and `bq` tools citeturn0search18.

2. **Initialize the CLI**

   ```bash
   gcloud init
   ```

   * Authenticates your Google account in a browser.
   * Prompts you to select or create a GCP project.
   * Configures default region/zone in `~/.config/gcloud/configurations/config_default` citeturn0search1.

3. **Authenticate your user**

   ```bash
   gcloud auth login
   ```

   Ensures `gcloud` can make API calls on your behalf.

4. **Verify setup**

   ```bash
   gcloud --version          # SDK version
   gcloud auth list          # active accounts
   gcloud config list project  # current project
   ```

   Confirm you see your account email, project ID, and a recent SDK release.

---

## 3. Cloud Setup (Console UI) (Console UI)

1. **Sign in** to the Cloud Console: [https://console.cloud.google.com](https://console.cloud.google.com)
2. **Select or create** a Project in the top project selector.
3. **Enable Billing**: Console → Billing → Link a billing account.
4. **Enable Vertex AI API**:

   * Navigation menu → **APIs & Services** → **Library**
   * Search **Vertex AI API** → click **Enable**
5. **Create a Workbench instance**:

   * Navigation menu → **Vertex AI** → **Workbench** → **New instance**
   * Choose **Vertex AI Workbench** (managed notebooks)
   * Configure:

     * **Name**: e.g. `genai-workbench`
     * **Region/Zone**: e.g. `asia-south1-a`
     * **Machine type**: CPU-only or GPU-enabled
     * **Environment**: prebuilt TensorFlow/PyTorch container
   * Click **Create** and wait until status is **Running**.
6. **Open JupyterLab**:

   * In the Workbench dashboard, click **Open JupyterLab** next to your instance.

---

## 2. SSH Access

### A) SSH via Cloud Console UI

* Console → Compute Engine → VM instances
* Locate `genai-workbench` → click **SSH** in its row
* A browser-based terminal opens directly on the VM

### B) SSH via gcloud CLI (IAP Tunnel)

Ensure you’ve granted yourself the **IAP-secured Tunnel User** role and allowed port 22 from `35.235.240.0/20` in your VPC firewall.

```bash
# Tunnel SSH over IAP (for VMs without external IPs)
gcloud compute ssh genai-workbench \
  --project=YOUR_PROJECT_ID \
  --zone=asia-south1-a \
  --tunnel-through-iap
```

---

## 3. Run JupyterLab on the VM (No Browser)

After SSH’ing into the VM (via UI or CLI):

```bash
# Start JupyterLab without a browser on port 8888
jupyter lab --no-browser --port=8888
```

Leave this process running in the SSH session.

---

## 4. SSH Tunnel for Local Browser

In a **new local terminal**, forward port 8888:

```bash
gcloud compute ssh genai-workbench \
  --project=YOUR_PROJECT_ID \
  --zone=asia-south1-a \
  --tunnel-through-iap \
  -- -L 8888:localhost:8888
```

Then open your local browser at:

```
http://localhost:8888
```

Enter the token shown in the VM’s JupyterLab launch output.

---

## 5. Local Environment & SDK Test

---

## 📋 .gitignore

```gitignore
# Google Cloud credentials
.env

# Python
__pycache__/
*.py[cod]

# Jupyter
.ipynb_checkpoints/

# VS Code
.vscode/
```

---

## 🔧 Environment Variables (`.env`)

Copy `.env.example` to `.env` and fill in your details:

```env
GCP_PROJECT=your-project-id
GCP_REGION=asia-south1
# Optional: path to service account key for ADC
GOOGLE_APPLICATION_CREDENTIALS=/full/path/to/vertex-sa-key.json
```

---

---

## 📦 Requirements (`requirements.txt`)

```
google-cloud-aiplatform
python-dotenv
jupyterlab
ipykernel
transformers
torch
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Vertex Workbench Utility Script

### `vertex_workbench_example.py`

This script lists:

1. Available Vertex AI models
2. Stopped Compute Engine VM instances in your project and zone
3. Vertex AI Workbench notebook instances

#### Usage

```bash
python vertex_workbench_example.py > output.txt 2>&1
```

Outputs are printed to console and saved in `output.txt`.

---

## 6. BERT Notebooks

### A) Embeddings Notebook

* **File:** `bert_transformer_toch_vertex_ai_remote_ssh.ipynb`
* **Task:** Compute sentence embeddings with `bert-base-uncased`

### B) Question Answering Notebook

* **File:** `question_answering_bert.ipynb`
* **Task:** Answer questions using `bert-large-cased-whole-word-masking-finetuned-squad`

Open and run these notebooks in the tunneled JupyterLab session.

---

## 🚀 Next Steps

1. Experiment with GPU-enabled instances for faster inference.
2. Containerize your notebooks and deploy as Vertex AI endpoints.
3. Integrate with Datasets and Pipelines for end-to-end MLOps.
4. Automate instance start/stop to optimize your cost usage.
5. Experiment with model inference in `vertex_workbench_example.ipynb`.
6. Develop custom training or deployment pipelines on Vertex AI.
7. Automate instance management via `gcloud` scripts or Terraform.

Happy exploring Vertex AI Workbench! 🚀
