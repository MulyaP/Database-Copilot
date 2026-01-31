interface Props {
  value: string;
  onChange: (name: string) => void;
  dbProvider: string;
}

export const DatabaseNameField = ({ value, onChange, dbProvider }: Props) => {
  if (!dbProvider) return null;

  return (
    <div className="mb-8 animate-in slide-in-from-bottom duration-500">
      <h3 className="text-white font-medium mb-4 flex items-center">
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
        Database Name
      </h3>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full p-4 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        placeholder="Enter a name for your database connection (e.g., My Project DB)"
      />
    </div>
  );
};