import SocialAccountsHeader from "@/components/social/SocialAccountsHeader";
import SocialAccountsList from "@/components/social/SocialAccountsList";

export default function SocialAccountsPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <SocialAccountsHeader />
      <SocialAccountsList />
    </div>
  );
}
