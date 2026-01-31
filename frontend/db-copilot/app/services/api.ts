import { DatabaseConnection } from "../types/database";

const API_BASE_URL = "http://localhost:8000";

const authenticatedFetch = async (url: string, options: RequestInit = {}) => {
  const accessToken = localStorage.getItem('access_token');
  
  const headers = {
    "Content-Type": "application/json",
    ...(accessToken && { "Authorization": `Bearer ${accessToken}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
};

export const createConnection = async (connection: DatabaseConnection) => {
  const response = await fetch(`${API_BASE_URL}/api/database/create_connection`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      db_type: connection.dbType,
      db_provider: connection.dbProvider,
      db_name: connection.dbName,
      credentials: connection.credentials,
      user_id: connection.user_id,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Connection failed");
  }

  return response.json();
};

export const signup = async (userData: any) => {
  const response = await fetch(`${API_BASE_URL}/api/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Signup failed");
  }

  return response.json();
};

export const login = async (credentials: any) => {
  const response = await fetch(`${API_BASE_URL}/api/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  return response.json();
};

export const sendChatMessage = async (message: string, connectionId: string) => {
  return authenticatedFetch("/api/chat", {
    method: "POST",
    body: JSON.stringify({
      message,
      connection_id: connectionId,
      model_provider: "groq"
    }),
  });
};

export const getConnections = async () => {
  return authenticatedFetch("/api/database/connections");
};

export const disconnectDatabase = async () => {
  const response = await fetch(`${API_BASE_URL}/api/database/disconnect`, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Disconnect failed");
  }

  return response.json();
};

export const signout = async (tokens: { access_token: string; refresh_token: string | null }) => {
  const response = await fetch(`${API_BASE_URL}/api/signout`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(tokens),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Signout failed");
  }

  return response.json();
};