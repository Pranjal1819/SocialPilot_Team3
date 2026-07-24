import { CalendarClock, Users, UserRound } from "lucide-react";
import {
  LayoutDashboard,
  Link2,
  BarChart3,
  Megaphone,
  Settings,
  HelpCircle,
  LucideIcon,
} from "lucide-react";
import { Role } from "@/types/user";

export interface NavItem {
  title: string;
  href: string;
  icon: LucideIcon;
  roles: Role[];
}

const allRoles: Role[] = [
  "content_creator",
  "marketing_team",
  "business_user",
  "administrator",
];

export const navigation: NavItem[] = [
  { title: "Dashboard", href: "/dashboard", icon: LayoutDashboard, roles: allRoles },
  { title: "Social Accounts", href: "/social-accounts", icon: Link2, roles: allRoles },
  {
    title: "Analytics",
    href: "/analytics",
    icon: BarChart3,
    roles: ["marketing_team", "business_user", "administrator"],
  },
  {
    title: "Campaigns",
    href: "/campaigns",
    icon: Megaphone,
    roles: ["marketing_team", "business_user", "administrator"],
  },
  {
    title: "Content Scheduling",
    href: "/content-scheduling",
    icon: CalendarClock,
    roles: ["content_creator", "marketing_team", "administrator"],
  },
  { title: "Users", href: "/users", icon: Users, roles: ["administrator"] },
];

export const secondaryNavigation: NavItem[] = [
  { title: "Profile", href: "/profile", icon: UserRound, roles: allRoles },
  { title: "Help & Support", href: "/help", icon: HelpCircle, roles: allRoles },
  { title: "Settings", href: "/settings", icon: Settings, roles: allRoles },
];
