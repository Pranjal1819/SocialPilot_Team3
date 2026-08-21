import { create } from "zustand";
import { api } from "@/lib/api";
import type { NotificationCategory, DeliveryChannel } from "@/lib/notifications";

export interface NotificationItem {
  id: string;
  title: string;
  description: string;
  category: NotificationCategory;
  timestamp: string;
  read: boolean;
  readAt?: string;
  deliveryChannel: DeliveryChannel;
}

export interface TeamActivityItem {
  id: string;
  type: "campaign_assigned" | "task_assigned" | "campaign_updated" | "content_review_requested" | "publishing_approval_requested" | "comment_added" | "task_completed";
  title: string;
  description: string;
  campaignName?: string;
  userName: string;
  timestamp: string;
}

export interface NotificationPreferences {
  publishing: boolean;
  campaigns: boolean;
  account: boolean;
  team: boolean;
  system: boolean;
}

export interface ChannelPreferences { in_app: boolean; email: boolean; push: boolean }
export type EmailFrequency = "immediate" | "daily" | "weekly";

interface BackendNotification {
  id: number;
  title?: string | null;
  message: string;
  category?: string | null;
  type: string;
  delivery_channel: string;
  is_read: boolean;
  created_at: string;
  read_at?: string | null;
}

interface NotificationsState {
  notifications: NotificationItem[];
  teamActivity: TeamActivityItem[];
  preferences: NotificationPreferences;
  channels: ChannelPreferences;
  emailFrequency: EmailFrequency;
  promotionalEmails: boolean;
  fetchNotifications: () => Promise<void>;
  markRead: (id: string) => Promise<void>;
  markAllRead: () => Promise<void>;
  deleteNotification: (id: string) => Promise<void>;
  togglePreference: (key: keyof NotificationPreferences) => void;
  toggleChannel: (key: keyof ChannelPreferences) => void;
  setEmailFrequency: (freq: EmailFrequency) => void;
  togglePromotional: () => void;
}

function mapNotification(item: BackendNotification): NotificationItem {
  const categories: NotificationCategory[] = ["publishing", "campaigns", "account", "team", "system"];
  const category = categories.includes(item.category as NotificationCategory) ? item.category as NotificationCategory : "system";
  const channels: DeliveryChannel[] = ["in_app", "email", "push"];
  const deliveryChannel = channels.includes(item.delivery_channel as DeliveryChannel) ? item.delivery_channel as DeliveryChannel : "in_app";
  return { id: String(item.id), title: item.title ?? item.type, description: item.message, category, timestamp: item.created_at, read: item.is_read, readAt: item.read_at ?? undefined, deliveryChannel };
}

export const useNotificationsStore = create<NotificationsState>((set, get) => ({
  notifications: [],
  teamActivity: [],
  preferences: { publishing: true, campaigns: true, account: true, team: true, system: true },
  channels: { in_app: true, email: true, push: false },
  emailFrequency: "immediate",
  promotionalEmails: false,
  fetchNotifications: async () => {
    const response = await api.get<{ notifications: BackendNotification[] }>("/notifications", { params: { limit: 100 } });
    set({ notifications: response.data.notifications.map(mapNotification) });
  },
  markRead: async (id) => {
    await api.patch(`/notifications/${id}/read`);
    set((state) => ({ notifications: state.notifications.map((item) => item.id === id ? { ...item, read: true, readAt: new Date().toISOString() } : item) }));
  },
  markAllRead: async () => {
    const unread = get().notifications.filter((item) => !item.read);
    await Promise.all(unread.map((item) => api.patch(`/notifications/${item.id}/read`)));
    set((state) => ({ notifications: state.notifications.map((item) => ({ ...item, read: true, readAt: item.readAt ?? new Date().toISOString() })) }));
  },
  deleteNotification: async (id) => {
    await api.delete(`/notifications/${id}`);
    set((state) => ({ notifications: state.notifications.filter((item) => item.id !== id) }));
  },
  togglePreference: (key) => set((state) => ({ preferences: { ...state.preferences, [key]: !state.preferences[key] } })),
  toggleChannel: (key) => set((state) => ({ channels: { ...state.channels, [key]: !state.channels[key] } })),
  setEmailFrequency: (freq) => set({ emailFrequency: freq }),
  togglePromotional: () => set((state) => ({ promotionalEmails: !state.promotionalEmails })),
}));
