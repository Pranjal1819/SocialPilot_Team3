export interface Campaign {
  id: number;
  name: string;
  objective: string;
  budget: number;
  category: string;
  priority: "High" | "Medium" | "Low";
  status: "Draft" | "Running" | "Completed";
  startDate: string;
  endDate: string;
  progress: number;
  totalPosts: number;
  completedPosts: number;
}