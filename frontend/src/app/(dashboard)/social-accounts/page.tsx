import SocialAccountsHeader from "@/components/social/SocialAccountsHeader";
import SocialAccountsList from "@/components/social/SocialAccountsList";

export default function SocialAccountsPage() {
  return (
    <div className="min-h-full">
      <SocialAccountsHeader />
      <SocialAccountsList />
    </div>
  );
}