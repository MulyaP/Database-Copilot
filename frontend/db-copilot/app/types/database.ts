export type DatabaseType = "sql" | "nosql" | "";
export type DatabaseProvider = "mysql" | "postgresql" | "supabase" | "mongodb" | "";

export interface Credentials {
  [key: string]: string;
}

export interface DatabaseConnection {
  dbType: DatabaseType;
  dbProvider: DatabaseProvider;
  dbName: string;
  credentials: Credentials;
  user_id: string | undefined;
}