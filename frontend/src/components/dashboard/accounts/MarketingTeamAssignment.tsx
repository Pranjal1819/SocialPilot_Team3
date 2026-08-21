"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, RefreshCw, Users } from "lucide-react";
import { api } from "@/lib/api";

interface MarketingTeam {
  id: number;
  name: string;
  email: string;
}

export default function MarketingTeamAssignment() {
  const [teams, setTeams] = useState<MarketingTeam[]>([]);
  const [selectedTeamId, setSelectedTeamId] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      api.get<MarketingTeam[]>("/business-management/marketing-teams"),
      api.get<MarketingTeam[]>("/business/my-marketing-team"),
    ])
      .then(([teamsResponse, assignedResponse]) => {
        setTeams(teamsResponse.data);
        setSelectedTeamId(assignedResponse.data[0] ? String(assignedResponse.data[0].id) : "");
      })
      .catch(() => setError("Could not load marketing teams. Please try again."))
      .finally(() => setIsLoading(false));
  }, []);

  async function handleAssign() {
    if (!selectedTeamId) return;

    setIsSaving(true);
    setMessage(null);
    setError(null);
    try {
      await api.post("/business/my-marketing-team", null, {
        params: { marketing_team_id: selectedTeamId },
      });
      setMessage("Marketing team assigned successfully.");
    } catch {
      setError("Could not assign this marketing team. Please try again.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <section className="mt-8 border border-border bg-surface p-5">
      <div className="flex items-center gap-2">
        <Users size={16} className="text-muted" />
        <h2 className="font-display font-bold">Choose your Marketing Team</h2>
      </div>
      <p className="mt-2 text-sm text-muted">
        Assign the team that will manage the social accounts connected above.
      </p>

      {isLoading ? (
        <div className="mt-4 flex items-center gap-2 text-sm text-muted">
          <RefreshCw size={14} className="animate-spin" /> Loading teams...
        </div>
      ) : (
        <>
          <div className="mt-4 max-w-sm">
            <select
              value={selectedTeamId}
              onChange={(event) => setSelectedTeamId(event.target.value)}
              className="w-full border border-border bg-background px-3 py-2.5 text-sm outline-none"
            >
              <option value="">Select a Marketing Team</option>
              {teams.map((team) => (
                <option key={team.id} value={team.id}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>
          <button
            type="button"
            disabled={!selectedTeamId || isSaving}
            onClick={handleAssign}
            className="mt-4 bg-accent px-5 py-2.5 text-sm font-medium text-ink hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isSaving ? "Assigning..." : "Assign Marketing Team"}
          </button>
        </>
      )}

      {message ? (
        <p className="mt-3 flex items-center gap-1.5 text-sm text-success">
          <CheckCircle2 size={15} /> {message}
        </p>
      ) : null}
      {error ? <p className="mt-3 text-sm text-danger">{error}</p> : null}
    </section>
  );
}