# Setup Doppler

Configure Doppler for secrets management.

## Steps

1. Verify `doppler` CLI is installed: `doppler --version`
2. Create the Doppler project: `doppler projects create {project-name}`
3. Set up environments: dev, staging, production
4. Set placeholder secrets for all env vars in `.env.example`:
   ```
   doppler secrets set SUPABASE_URL "placeholder" --config dev
   doppler secrets set CLERK_SECRET_KEY "placeholder" --config dev
   ```
   (repeat for all vars)
5. Link the project: `doppler setup --project {project-name} --config dev`
6. Verify: `doppler secrets`
7. Remind user to fill in actual values in the Doppler dashboard
