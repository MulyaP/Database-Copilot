import { DatabaseType, DatabaseProvider } from "../types/database";
import { DB_PROVIDERS } from "../constants/database";

interface Props {
  dbType: DatabaseType;
  value: DatabaseProvider;
  onChange: (provider: DatabaseProvider) => void;
}

export const DatabaseProviderSelector = ({ dbType, value, onChange }: Props) => {
  if (!dbType) return null;

  return (
    <div className="mb-6 animate-in slide-in-from-top duration-300">
      <label className="block text-white font-medium mb-3">Database Provider</label>
      <select 
        value={value} 
        onChange={(e) => onChange(e.target.value as DatabaseProvider)}
        className="w-full p-4 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
      >
        <option value="" className="text-gray-900">Select database provider</option>
        {DB_PROVIDERS[dbType].map(provider => (
          <option key={provider} value={provider} className="text-gray-900">
            {provider.charAt(0).toUpperCase() + provider.slice(1)}
          </option>
        ))}
      </select>
    </div>
  );
};