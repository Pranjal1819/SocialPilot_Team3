import { Bell, Search } from "lucide-react";

const user = {
  name: "Pranjal",
  role: "Content Creator",
};

export default function Navbar() {
  return (
    <header className="h-24 bg-white border-b border-slate-100 flex items-center justify-between px-8 gap-8">
      <div className="flex flex-1 max-w-md items-center gap-3 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3.5 transition-all duration-200 ease-in-out focus-within:border-blue-300 focus-within:bg-white focus-within:ring-4 focus-within:ring-blue-50">
        <Search size={18} className="text-slate-400 shrink-0" />
        <input
          type="text"
          placeholder="Search..."
          className="w-full bg-transparent text-sm text-slate-900 placeholder:text-slate-400 outline-none"
        />
      </div>

      <div className="flex items-center gap-5 shrink-0">
        <button className="relative flex h-11 w-11 items-center justify-center rounded-xl text-slate-500 transition-all duration-200 ease-in-out hover:bg-slate-50 hover:text-slate-900">
          <Bell size={20} />
          <span className="absolute top-2.5 right-2.5 h-2 w-2 rounded-full bg-red-500 ring-2 ring-white" />
        </button>

        <div className="flex items-center gap-3 border-l border-slate-100 pl-5">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white">
            P
          </div>
          <div>
            <p className="text-sm font-semibold leading-tight text-slate-900">{user.name}</p>
            <p className="text-xs leading-tight text-slate-400">{user.role}</p>
          </div>
        </div>
      </div>
    </header>
  );
}