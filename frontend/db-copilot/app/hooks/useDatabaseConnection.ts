import { useState } from "react";
import { useRouter } from "next/navigation";
import { DatabaseType, DatabaseProvider, Credentials } from "../types/database";
import { createConnection } from "../services/api";
import { useAuth } from "../context/AuthContext";

export const useDatabaseConnection = () => {
  const { user } = useAuth();
  const router = useRouter();
  const [dbType, setDbType] = useState<DatabaseType>("");
  const [dbProvider, setDbProvider] = useState<DatabaseProvider>("");
  const [dbName, setDbName] = useState<string>("");
  const [credentials, setCredentials] = useState<Credentials>({});

  const handleDbTypeChange = (type: DatabaseType) => {
    setDbType(type);
    setDbProvider("");
    setDbName("");
    setCredentials({});
  };

  const handleDbProviderChange = (provider: DatabaseProvider) => {
    setDbProvider(provider);
    setCredentials({});
  };

  const handleDbNameChange = (name: string) => {
    setDbName(name);
  };

  const handleCredentialChange = (field: string, value: string) => {
    setCredentials(prev => ({ ...prev, [field]: value }));
  };

  const handleConnect = async () => {
    try {
      const result = await createConnection({ dbType, dbProvider, dbName, credentials, user_id: user?.id });
      router.push(`/chat?connectionId=${result.connection_id}`);
    } catch (error : any) {
      alert(`Connection failed: ${error.message}`);
    }
  };

  return {
    dbType,
    dbProvider,
    dbName,
    credentials,
    handleDbTypeChange,
    handleDbProviderChange,
    handleDbNameChange,
    handleCredentialChange,
    handleConnect
  };
};