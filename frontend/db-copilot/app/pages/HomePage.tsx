"use client";
import { Header } from "../components/Header";
import { DatabaseTypeSelector } from "../components/DatabaseTypeSelector";
import { DatabaseProviderSelector } from "../components/DatabaseProviderSelector";
import { DatabaseNameField } from "../components/DatabaseNameField";
import { CredentialFields } from "../components/CredentialFields";
import { ConnectButton } from "../components/ConnectButton";
import { useDatabaseConnection } from "../hooks/useDatabaseConnection";

export const HomePage = () => {
  const {
    dbType,
    dbProvider,
    dbName,
    credentials,
    handleDbTypeChange,
    handleDbProviderChange,
    handleDbNameChange,
    handleCredentialChange,
    handleConnect
  } = useDatabaseConnection();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-lg">
        <Header />
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-8 shadow-2xl">
          <DatabaseTypeSelector value={dbType} onChange={handleDbTypeChange} />
          <DatabaseProviderSelector dbType={dbType} value={dbProvider} onChange={handleDbProviderChange} />
          <DatabaseNameField value={dbName} onChange={handleDbNameChange} dbProvider={dbProvider} />
          <CredentialFields dbProvider={dbProvider} credentials={credentials} onChange={handleCredentialChange} />
          <ConnectButton dbProvider={dbProvider} onClick={handleConnect} />
        </div>
      </div>
    </div>
  );
};