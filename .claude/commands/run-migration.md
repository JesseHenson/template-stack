# Run Migration

Apply SQL migrations to the Supabase database.

## Steps

1. Read the latest migration file(s) from `supabase/migrations/`
2. Confirm with the user which migration(s) to apply
3. Connect to Supabase using the DATABASE_URL or Supabase CLI
4. Apply the migration: `psql $DATABASE_URL -f supabase/migrations/{file}.sql`
5. Verify the tables were created: `psql $DATABASE_URL -c '\dt'`
6. Report success or errors
