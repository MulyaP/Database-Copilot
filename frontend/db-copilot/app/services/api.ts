import { DatabaseConnection } from "../types/database";

const API_BASE_URL = "http://localhost:8000";

export const connectToDatabase = async (connection: DatabaseConnection) => {
  const response = await fetch(`${API_BASE_URL}/api/database/connect`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      db_type: connection.dbType,
      db_provider: connection.dbProvider,
      credentials: connection.credentials,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Connection failed");
  }

  return response.json();
};