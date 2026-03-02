# Deploy to Cloud Run

Run pre-flight checks and deploy to GCP Cloud Run.

## Steps

1. **Pre-flight checks**:
   - Verify `gcloud` CLI is authenticated: `gcloud auth list`
   - Verify Docker builds: `docker build .`
   - Run backend tests: `cd backend && uv run pytest`
   - Run frontend type check: `cd frontend && npm run lint`
2. **Deploy**:
   - Confirm target project and region with user
   - Run: `gcloud run deploy {service-name} --region=us-central1 --source=. --allow-unauthenticated`
   - Set environment variables from Doppler or secrets
3. **Verify**:
   - Hit the health endpoint: `curl {service-url}/api/v1/health`
   - Report the deployed URL
