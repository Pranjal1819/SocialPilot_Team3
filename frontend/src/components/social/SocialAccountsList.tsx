import PlatformCard from "./PlatformCard";
import { platforms } from "@/constants/platforms";

export default function SocialAccountsList() {
  return (
    <div className="mt-8 flex flex-col gap-6">
      {platforms.map((platform) => (
        <PlatformCard key={platform.name} {...platform} />
      ))}
    </div>
  );
}