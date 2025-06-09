#!/usr/bin/env python3
"""
Vertex AI Workbench Utility Script

This script lists:
  1. Available Vertex AI models
  2. Stopped Compute Engine VM instances in your project
  3. Vertex AI Workbench notebook instances

Requirements:
- .env with GCP_PROJECT, GCP_REGION
- (Optional) VM_INSTANCE_NAME if you want specific details
- (Optional) GOOGLE_APPLICATION_CREDENTIALS for a service account key
"""
import os
import sys
import json
import subprocess
from dotenv import load_dotenv
from google.cloud import aiplatform

# 1) Load environment variables
load_dotenv()
project_id = os.getenv("GCP_PROJECT")
region     = os.getenv("GCP_REGION")

if not all([project_id, region]):
    print("⚠️  Please set GCP_PROJECT, GCP_REGION in .env", file=sys.stderr)
    sys.exit(1)

# 2) Set ADC if using service account
key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if key_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# 3) Initialize Vertex AI SDK
aiplatform.init(project=project_id, location=region)

# 4) List Vertex AI models
def list_models():
    print(f"\n=== Vertex AI Models in {project_id} ({region}) ===")
    for m in aiplatform.Model.list():
        print(f"- {m.display_name} [{m.resource_name}]")

# 5) List stopped Compute Engine VM instances
def list_stopped_instances():
    print(f"\n=== Stopped VM Instances in {project_id}")
    cmd = [
        "gcloud", "compute", "instances", "list",
        "--project", project_id,
        "--filter", "status=TERMINATED",
        "--format", "json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error fetching stopped instances: {result.stderr}", file=sys.stderr)
        return
    instances = json.loads(result.stdout)
    if not instances:
        print("No stopped VM instances found.")
    else:
        for inst in instances:
            print(f"- {inst.get('name')}  (status: {inst.get('status')})")

# 6) List Vertex AI Workbench instances
def list_workbench_instances():
    print(f"\n=== Vertex AI Workbench Instances in {region} ===")
    cmd = [
        "gcloud", "notebooks", "instances", "list",
        "--project", project_id,
        "--location", region,
        "--format", "json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error listing Workbench instances: {result.stderr}", file=sys.stderr)
        return
    instances = json.loads(result.stdout)
    if not instances:
        print("No Workbench instances found.")
    else:
        for inst in instances:
            print(f"- {inst.get('name')}  (state: {inst.get('state')})")

# Entry point
if __name__ == "__main__":
    list_models()
    list_stopped_instances()
    list_workbench_instances()
