export const DB_PROVIDERS = {
  sql: ["mysql", "postgresql", "supabase"],
  nosql: ["mongodb"]
} as const;

export const CREDENTIAL_FIELDS = {
  mysql: ["host", "port", "username", "password", "database"],
  postgresql: ["host", "port", "username", "password", "database"],
  supabase: ["supabase_url", "supabase_anon_key"],
  mongodb: ["connection_string"]
} as const;