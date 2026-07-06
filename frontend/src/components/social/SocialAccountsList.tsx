import PlatformCard from "./PlatformCard";
import {
  FaFacebook,
  FaInstagram,
  FaLinkedin,
  FaYoutube,
  FaXTwitter,
} from "react-icons/fa6";

const platforms = [
  {
    name: "Facebook",
    icon: FaFacebook,
    connected: true,
  },
  {
    name: "Instagram",
    icon: FaInstagram,
    connected: false,
  },
  {
    name: "LinkedIn",
    icon: FaLinkedin,
    connected: true,
  },
  {
    name: "X (Twitter)",
    icon: FaXTwitter,
    connected: false,
  },
  {
    name: "YouTube",
    icon: FaYoutube,
    connected: true,
  },
];

export default function SocialAccountsList() {
  return (
    <div className="mt-8 space-y-4">
      {platforms.map((platform) => (
        <PlatformCard
          key={platform.name}
          {...platform}
        />
      ))}
    </div>
  );
}