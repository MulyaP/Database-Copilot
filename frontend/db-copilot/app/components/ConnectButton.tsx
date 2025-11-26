import { DatabaseProvider } from "../types/database";

interface Props {
  dbProvider: DatabaseProvider;
  onClick: () => void;
}

export const ConnectButton = ({ dbProvider, onClick }: Props) => {
  if (!dbProvider) return null;

  return (
    <button 
      onClick={onClick}
      className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transform hover:scale-[1.02] transition-all duration-200 shadow-lg hover:shadow-xl animate-in slide-in-from-bottom duration-700"
    >
      <span className="flex items-center justify-center">
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        Connect to Database
      </span>
    </button>
  );
};