import { SignIn } from "@clerk/clerk-react";
import { useNavigate } from "react-router-dom";

const hasClerk = !!import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

export default function SignInPage() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      {hasClerk ? (
        <SignIn routing="hash" />
      ) : (
        <div className="w-full max-w-sm rounded-lg border border-gray-200 bg-white p-8 text-center shadow-sm">
          <h1 className="mb-2 text-2xl font-bold text-gray-900">Template Stack</h1>
          <p className="mb-6 text-sm text-gray-500">Local Development</p>
          <button
            onClick={() => navigate("/dashboard")}
            className="w-full rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
          >
            Local Login
          </button>
        </div>
      )}
    </div>
  );
}
