import { useState } from "react";
import { useRouter } from "next/navigation";
import { DatabaseType, DatabaseProvider, Credentials } from "../types/database";
import { connectToDatabase } from "../services/api";

export const useDatabaseConnection = () => {
  const router = useRouter();
  const [dbType, setDbType] = useState<DatabaseType>("");
  const [dbProvider, setDbProvider] = useState<DatabaseProvider>("");
  const [credentials, setCredentials] = useState<Credentials>({});

  const handleDbTypeChange = (type: DatabaseType) => {
    setDbType(type);
    setDbProvider("");
    setCredentials({});
  };

  const handleDbProviderChange = (provider: DatabaseProvider) => {
    setDbProvider(provider);
    setCredentials({});
  };

  const handleCredentialChange = (field: string, value: string) => {
    setCredentials(prev => ({ ...prev, [field]: value }));
  };

  const handleConnect = async () => {
    try {
      const result = await connectToDatabase({ dbType, dbProvider, credentials });
      router.push(`/chat?connectionId=${result.connection_id}`);
    } catch (error : any) {
      alert(`Connection failed: ${error.message}`);
    }
  };

  return {
    dbType,
    dbProvider,
    credentials,
    handleDbTypeChange,
    handleDbProviderChange,
    handleCredentialChange,
    handleConnect
  };
};