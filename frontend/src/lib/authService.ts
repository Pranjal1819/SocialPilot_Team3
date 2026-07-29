const API_BASE_URL = "http://localhost:8000/api/auth";

export interface BackendUser {
  id: number;
  email: string;
  name: string;
  role: string;
  profile_picture: string | null;
  is_active: boolean;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

class AuthService {
  async register(name: string, email: string, password: string) {
    const res = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Registration failed");
    return data as BackendUser;
  }

  async login(email: string, password: string) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const res = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Login failed");

    this.setToken(data.access_token);
    return data as LoginResponse;
  }

  async getCurrentUser(): Promise<BackendUser> {
    const token = this.getToken();
    if (!token) throw new Error("No token");

    const res = await fetch(`${API_BASE_URL}/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) {
      if (res.status === 401) this.logout();
      throw new Error("Failed to get user");
    }
    return res.json();
  }

  logout() {
    const token = this.getToken();
    if (token) {
      fetch(`${API_BASE_URL}/logout`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      }).catch(() => {});
    }
    if (typeof window !== "undefined") {
      localStorage.removeItem("access_token");
    }
  }

  getToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("access_token");
  }

  setToken(token: string) {
    if (typeof window !== "undefined") {
      localStorage.setItem("access_token", token);
    }
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export default new AuthService();