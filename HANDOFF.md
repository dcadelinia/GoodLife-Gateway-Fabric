# 🛠️ Odynex Axis Engineering Handoff Manual
## GoodLifeGateway Core Multi-Agent Architecture Stack

This onboarding brief outlines execution parameters for deploying and maintaining the Regional Node SOWEGA digital twin framework loop.

### 🧱 1. Operational Stack Overview
The system architecture runs on an integrated, concurrent processing ecosystem:
*   **Intelligence:** OpenAI API Core Engine (`gpt-4o-2024-08-06`) running strict structured JSON payload parameters.
*   **Web Framework:** FastAPI network handling handling asynchronous JSON CORS streams.
*   **Data Grounding:** Real-time search orchestration using Perplexity's API endpoints.
*   **Spatial Twin Layer:** NVIDIA OpenUSD (Universal Scene Description) scene graph schema integration.
*   **Embodied AI:** NVIDIA Isaac Lab robotics control policies mapping to GR00T framework structures.

### 🏃 2. Initial Setup Requirements
Engineers must initialize their local runtime variables exactly as follows:

```bash
# Clone the unified development environment monorepo
git clone https://github.com
cd GoodLife-Gateway-Fabric

# Build project isolated environments and dependencies
pip install -r requirements.txt

# Bind structural production authentication key vectors
export OPENAI_API_KEY="your-verified-openai-developer-key"
export PERPLEXITY_API_KEY="your-verified-perplexity-search-key"
export NVIDIA_API_KEY="your-verified-nvidia-inception-api-key"

# Launch the primary local development listener
python main.py
```

### 🔍 3. Verification Testing
Before committing feature alterations to production branches, run the simulation loop verification script via the local execution shell to evaluate compliance parameters:
```bash
python test_launcher.py
```
