# LiteLLM Gateway — Self-Hosted LLM Proxy

## Overview
Deploy LiteLLM as a self-hosted proxy to route LLM calls across providers (OpenAI, Anthropic, Google, etc.) with unified API, rate limiting, and cost tracking.

## Dependencies
No additional Python dependencies — the template already includes `litellm`.

For the gateway itself:
```bash
# Option 1: Docker
docker pull ghcr.io/berriai/litellm:main-latest

# Option 2: pip (for development)
pip install litellm[proxy]
```

## Doppler Secrets
- `LITELLM_API_BASE` — URL of your LiteLLM proxy (e.g., `http://localhost:4000`)
- `LITELLM_API_KEY` — Master key for the proxy
- `LITELLM_MASTER_KEY` — Master key for proxy admin (set on the proxy itself)

## Config Fields
Already present in `backend/app/config.py`:
```python
litellm_api_key: str = ""
litellm_api_base: str = ""
```

## Files to Create

### `litellm_config.yaml` (project root)
```yaml
model_list:
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-sonnet-4-5-20250929
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: gemini-pro
    litellm_params:
      model: google/gemini-2.0-flash
      api_key: os.environ/GOOGLE_API_KEY

litellm_settings:
  drop_params: true
  set_verbose: false

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

## Docker Compose Addition
Add to `docker-compose.yml`:
```yaml
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    ports:
      - "4000:4000"
    volumes:
      - ./litellm_config.yaml:/app/config.yaml
    environment:
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      LITELLM_MASTER_KEY: ${LITELLM_MASTER_KEY:-sk-master-key}
    command: ["--config", "/app/config.yaml", "--port", "4000"]
```

## Wiring Changes
The `backend/app/services/litellm_client.py` is already configured to use `LITELLM_API_BASE`. Just set the env var to point to your proxy.

## Usage Pattern
```python
from app.services.litellm_client import completion

# Routes through LiteLLM proxy — model name maps to config
response = await completion(
    model="claude-sonnet",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

## Migration SQL
No migration needed.
