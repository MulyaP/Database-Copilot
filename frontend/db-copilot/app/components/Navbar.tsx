"use client";

import Link from "next/link";
import { useAuth } from "../context/AuthContext";

export const Navbar = () => {
    const { user, logout } = useAuth();

    return (
        <nav className="w-full border-b border-white/10 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
            <div className="w-full px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    <div className="flex-shrink-0">
                        <Link href="/" className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 flex items-center justify-center">
                                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </div>
                            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                                DB Copilot
                            </span>
                        </Link>
                    </div>

                    <div>
                        {user ? (
                            <div className="flex items-center gap-4">
                                <span className="text-sm text-gray-300 hidden md:inline">
                                    {user.email}
                                </span>
                                <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-xs font-bold ring-2 ring-white/10">
                                    {user.email?.charAt(0).toUpperCase() || "U"}
                                </div>
                                <button
                                    onClick={logout}
                                    className="px-3 py-1.5 text-sm font-medium text-red-300 hover:text-red-200 hover:bg-red-900/20 rounded-lg transition-colors border border-transparent hover:border-red-900/30"
                                >
                                    Sign Out
                                </button>
                            </div>
                        ) : (
                            <Link
                                href="/login"
                                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-500 rounded-lg shadow-lg hover:shadow-blue-500/25 transition-all"
                            >
                                Sign In
                            </Link>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};
