import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";

export interface AssignedClient {
  id: number;
  name: string;
  email: string;
  organization: string | null;
  role: string;
}

/**
 * Fetches the list of Business Users assigned to the currently
 * logged-in Marketing Team via GET /api/business/my-clients.
 *
 * This is the server-side scoped list — a Marketing Team only ever
 * sees the clients that have been assigned to them.
 */
export function useAssignedClients() {
  const [clients, setClients] = useState<AssignedClient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchClients = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get<AssignedClient[]>("/business/my-clients");
      setClients(res.data ?? []);
    } catch (err) {
      setError("Failed to load assigned clients");
      setClients([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchClients();
  }, [fetchClients]);

  return { clients, loading, error, refetch: fetchClients };
}