"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import authService from "@/lib/authService";
import { CurrentUser, mapBackendRole } from "@/types/user";

interface AuthContextValue {
  user: CurrentUser | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadUser() {
      if (!authService.isAuthenticated()) {
        setIsLoading(false);
        return;
      }
      try {
        const backendUser = await authService.getCurrentUser();
        setUser({
          name: backendUser.name,
          email: backendUser.email,
          role: mapBackendRole(backendUser.role),
        });
      } catch {
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    }
    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    await authService.login(email, password);
    const backendUser = await authService.getCurrentUser();
    setUser({
      name: backendUser.name,
      email: backendUser.email,
      role: mapBackendRole(backendUser.role),
    });
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}