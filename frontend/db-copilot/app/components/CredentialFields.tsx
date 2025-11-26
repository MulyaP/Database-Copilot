import { DatabaseProvider, Credentials } from "../types/database";
import { CREDENTIAL_FIELDS } from "../constants/database";

interface Props {
  dbProvider: DatabaseProvider;
  credentials: Credentials;
  onChange: (field: string, value: string) => void;
}

export const CredentialFields = ({ dbProvider, credentials, onChange }: Props) => {
  if (!dbProvider || !CREDENTIAL_FIELDS[dbProvider]) return null;

  return (
    <div className="mb-8 animate-in slide-in-from-bottom duration-500">
      <h3 className="text-white font-medium mb-4 flex items-center">
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        Connection Details
      </h3>
      <div className="space-y-4">
        {CREDENTIAL_FIELDS[dbProvider].map(field => (
          <div key={field}>
            <label className="block text-slate-300 text-sm font-medium mb-2">
              {field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </label>
            <input
              type={field.includes('password') || field.includes('key') ? 'password' : 'text'}
              value={credentials[field] || ''}
              onChange={(e) => onChange(field, e.target.value)}
              className="w-full p-4 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              placeholder={`Enter ${field.replace(/_/g, ' ')}`}
            />
          </div>
        ))}
      </div>
    </div>
  );
};