import { DatabaseType } from "../types/database";

interface Props {
  value: DatabaseType;
  onChange: (type: DatabaseType) => void;
}

export const DatabaseTypeSelector = ({ value, onChange }: Props) => (
  <div className="mb-6">
    <label className="block text-white font-medium mb-3">Database Type</label>
    <select 
      value={value} 
      onChange={(e) => onChange(e.target.value as DatabaseType)}
      className="w-full p-4 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
    >
      <option value="" className="text-gray-900">Select database type</option>
      <option value="sql" className="text-gray-900">SQL</option>
      <option value="nosql" className="text-gray-900">NoSQL</option>
    </select>
  </div>
);