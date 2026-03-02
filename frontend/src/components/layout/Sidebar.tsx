import { UserButton } from "@clerk/clerk-react";
import { Link } from "react-router-dom";

const hasClerk = !!import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

export function Sidebar() {
  return (
    <aside className="flex w-64 flex-col border-r border-gray-200 bg-white">
      <div className="flex h-16 items-center px-6 font-semibold text-lg">
        Template Stack
      </div>
      <nav className="flex-1 space-y-1 px-3 py-4">
        <Link
          to="/dashboard"
          className="flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
        >
          Dashboard
        </Link>
      </nav>
      <div className="border-t border-gray-200 p-4">
        {hasClerk ? <UserButton afterSignOutUrl="/sign-in" /> : <span className="text-sm text-gray-400">Local Dev</span>}
      </div>
    </aside>
  );
}
