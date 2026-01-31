"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

interface AuthGuardProps {
  children: React.ReactNode;
}

export const AuthGuard = ({ children }: AuthGuardProps) => {
  const router = useRouter();

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    
    if (!accessToken) {
      router.push('/');
    }
  }, [router]);

  // Check if user is authenticated
  const accessToken = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!accessToken) {
    return null; // Will redirect to login
  }

  return <>{children}</>;
};