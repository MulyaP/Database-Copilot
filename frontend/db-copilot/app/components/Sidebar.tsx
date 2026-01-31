"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getConnections } from "../services/api";
import { useAuth } from "../context/AuthContext";

interface Connection {
  id: string;
  db_name: string;
  db_provider_name: string;
  connected: boolean;
}

export const Sidebar = () => {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (user != null || user != undefined) {
      fetchConnections();
    }
  }, [user]);

  const fetchConnections = async () => {
    try {
      setLoading(true);
      const response = await getConnections();
      setConnections(response.connections || []);
    } catch (error) {
      console.error("Failed to fetch connections:", error);
    } finally {
      setLoading(false);
    }
  };

  const dummyTitles = [
    "User Analytics Query",
    "Sales Report Analysis", 
    "Product Inventory Check",
    "Customer Data Review",
    "Monthly Revenue Stats"
  ];

  if (!user) return null;

  return (
    <div className="w-64 bg-slate-900 border-r border-slate-700 h-screen p-4">
      <div className="mb-6">
        <h2 className="text-white font-semibold text-lg mb-4">Database Connections</h2>
        
        {loading ? (
          <div className="text-slate-400">Loading...</div>
        ) : connections.length === 0 ? (
          <div className="text-slate-400 text-sm">No connections found</div>
        ) : (
          <div className="space-y-2">
            {connections.map((connection, index) => (
              <div
                key={connection.id}
                className="p-3 bg-slate-800 rounded-lg border border-slate-700 hover:bg-slate-750 cursor-pointer transition-colors"
                onClick={() => router.push(`/chat?connectionId=${connection.id}`)}
              >
                <div className="text-white font-medium text-sm mb-1">
                  {dummyTitles[index % dummyTitles.length]}
                </div>
                <div className="text-slate-400 text-xs">
                  {connection.db_name} • {connection.db_provider_name}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};