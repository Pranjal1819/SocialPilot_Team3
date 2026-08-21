import { create } from "zustand";
import { api } from "@/lib/api";
import type { Role } from "@/lib/validation";

export interface AdminUserRecord {
  id: string;
  name: string;
  email: string;
  role: Role;
  status: "active" | "suspended";
  joinedAt: string;
  lastActive: string;
  connectedAccounts: number;
}

interface BackendUser {
  id: number;
  name: string;
  email: string;
  role: Role;
  is_active: boolean;
  created_at?: string;
  connected_accounts?: number;
}

interface AdminUsersState {
  users: AdminUserRecord[];
  isLoading: boolean;
  error: string | null;
  fetchUsers: () => Promise<void>;
  toggleStatus: (id: string, isActive: boolean) => Promise<void>;
}

function mapUser(user: BackendUser): AdminUserRecord {
  return {
    id: String(user.id),
    name: user.name,
    email: user.email,
    role: user.role,
    status: user.is_active ? "active" : "suspended",
    joinedAt: user.created_at?.slice(0, 10) ?? "",
    lastActive: "",
    connectedAccounts: user.connected_accounts ?? 0,
  };
}

export const useAdminUsersStore = create<AdminUsersState>((set, get) => ({
  users: [],
  isLoading: false,
  error: null,
  fetchUsers: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get<{ users: BackendUser[] }>("/admin/users", {
        params: { skip: 0, limit: 100 },
      });
      set({ users: response.data.users.map(mapUser), isLoading: false });
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : "Failed to load users.",
      });
    }
  },
  toggleStatus: async (id, isActive) => {
    await api.patch(`/admin/users/${id}/status`, null, { params: { is_active: isActive } });
    set((state) => ({
      users: state.users.map((user) =>
        user.id === id ? { ...user, status: isActive ? "active" : "suspended" } : user
      ),
    }));
    await get().fetchUsers();
  },
}));
