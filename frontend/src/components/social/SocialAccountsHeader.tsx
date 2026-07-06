export default function SocialAccountsHeader() {
  return (
    <div className="mb-8 flex items-center justify-between">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight text-slate-900">
          Social Accounts
        </h1>
        <p className="mt-1.5 text-sm text-slate-500">
          Connect and manage all your social media accounts.
        </p>
      </div>

      <button className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition-all duration-200 ease-in-out hover:bg-blue-700">
        + Connect account
      </button>
    </div>
  );
}