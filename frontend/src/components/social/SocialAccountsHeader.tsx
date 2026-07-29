export default function SocialAccountsHeader() {
  return (
    <div className="mb-8 flex items-center justify-between">
      <p className="text-lg font-bold text-slate-900">
        Connect and manage all your social media accounts.
      </p>

      <button className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition-all duration-200 ease-in-out hover:bg-blue-700">
        + Connect account
      </button>
    </div>
  );
}