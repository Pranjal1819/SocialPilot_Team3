import {
  FaFacebookF,
  FaInstagram,
  FaLinkedinIn,
  FaYoutube,
  FaXTwitter,
  FaPinterest,
} from "react-icons/fa6";
import { IconType } from "react-icons";

export type ConnectionStatus = "connected" | "error" | "disconnected";

export interface PlatformEntry {
  name: string;
  icon: IconType;
  brandColor: string;
  status: ConnectionStatus;
  errorMessage?: string;
}

export const platforms: PlatformEntry[] = [
  { name: "Facebook", icon: FaFacebookF, brandColor: "#1877F2", status: "connected" },
  {
    name: "Instagram",
    icon: FaInstagram,
    brandColor:
      "linear-gradient(45deg, #FEDA75 0%, #FA7E1E 25%, #D62976 50%, #962FBF 75%, #4F5BD5 100%)",
    status: "disconnected",
  },
  { name: "LinkedIn", icon: FaLinkedinIn, brandColor: "#0A66C2", status: "error", errorMessage: "Token Expired" },
  { name: "X (Twitter)", icon: FaXTwitter, brandColor: "#000000", status: "disconnected" },
  { name: "YouTube", icon: FaYoutube, brandColor: "#FF0000", status: "connected" },
  { name: "Pinterest", icon: FaPinterest, brandColor: "#E60023", status: "disconnected" },
];