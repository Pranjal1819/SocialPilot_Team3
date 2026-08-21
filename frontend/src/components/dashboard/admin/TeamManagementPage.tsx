"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Users, X } from "lucide-react";
import { api } from "@/lib/api";

interface AssignmentResponse {
  assignment_id: number;
  business_user: {
    id: number;
    name: string;
    email: string;
  };
  marketing_team: {
    id: number;
    name: string;
  };
  assigned_at: string;
}

interface TeamGroup {
  teamId: number;
  teamName: string;
  assignments: Array<{
    id: number;
    businessOwnerName: string;
    businessOwnerEmail: string;
    assignedAt: string;
  }>;
}

export default function TeamManagementPage() {
  const [groups, setGroups] = useState<TeamGroup[]>([]);

  useEffect(() => {
    api.get<AssignmentResponse[]>("/business/assignments").then(({ data }) => {
      const grouped = data.reduce<TeamGroup[]>((teams, assignment) => {
        let team = teams.find((item) => item.teamId === assignment.marketing_team.id);
        if (!team) {
          team = {
            teamId: assignment.marketing_team.id,
            teamName: assignment.marketing_team.name,
            assignments: [],
          };
          teams.push(team);
        }
        team.assignments.push({
          id: assignment.assignment_id,
          businessOwnerName: assignment.business_user.name,
          businessOwnerEmail: assignment.business_user.email,
          assignedAt: new Date(assignment.assigned_at).toLocaleDateString(),
        });
        return teams;
      }, []);
      setGroups(grouped);
    });
  }, []);

  async function removeAssignment(teamId: number, assignmentId: number) {
    await api.delete(`/business/assign/${assignmentId}`);
    setGroups((currentGroups) =>
      currentGroups
        .map((group) =>
          group.teamId === teamId
            ? { ...group, assignments: group.assignments.filter((assignment) => assignment.id !== assignmentId) }
            : group
        )
        .filter((group) => group.assignments.length > 0)
    );
  }

  return (
    <div className="space-y-5">
      {groups.map((group, i) => (
        <motion.div
          key={group.teamId}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: i * 0.06 }}
          className="border border-border bg-surface"
        >
          <div className="flex items-center justify-between border-b border-border px-6 py-4">
            <div className="flex items-center gap-2">
              <Users size={16} className="text-muted" />
              <p className="font-display font-bold">{group.teamName}</p>
            </div>
            <span className="font-mono text-xs text-muted">
              {group.assignments.length} client{group.assignments.length === 1 ? "" : "s"}
            </span>
          </div>

          <div className="divide-y divide-border">
            <AnimatePresence initial={false}>
              {group.assignments.map((a) => (
                <motion.div
                  key={a.id}
                  layout
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0, height: 0 }}
                  className="flex items-center justify-between px-6 py-4"
                >
                  <div>
                    <p className="text-sm">{a.businessOwnerName}</p>
                    <p className="text-xs text-muted">{a.businessOwnerEmail}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="font-mono text-xs text-muted">Since {a.assignedAt}</span>
                    <button
                      onClick={() => removeAssignment(group.teamId, a.id)}
                      title="Remove assignment"
                      className="text-muted hover:text-danger"
                    >
                      <X size={15} />
                    </button>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            {group.assignments.length === 0 ? (
              <p className="px-5 py-6 text-center text-sm text-muted">
                No clients assigned to this team yet.
              </p>
            ) : null}
          </div>
        </motion.div>
      ))}
    </div>
  );
}
