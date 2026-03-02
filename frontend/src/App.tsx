import { useEffect } from "react";
import { SignedIn, SignedOut, useAuth } from "@clerk/clerk-react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { setTokenGetter } from "@/api/client";
import SignInPage from "@/pages/SignInPage";
import DashboardPage from "@/pages/DashboardPage";

const hasClerk = !!import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

function AuthSetup({ children }: { children: React.ReactNode }) {
  const { getToken } = useAuth();

  useEffect(() => {
    setTokenGetter(getToken);
  }, [getToken]);

  return <>{children}</>;
}

function App() {
  if (!hasClerk) {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/sign-in" element={<SignInPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="*" element={<Navigate to="/sign-in" replace />} />
        </Routes>
      </BrowserRouter>
    );
  }

  return (
    <BrowserRouter>
      <SignedOut>
        <Routes>
          <Route path="/sign-in" element={<SignInPage />} />
          <Route path="*" element={<Navigate to="/sign-in" replace />} />
        </Routes>
      </SignedOut>
      <SignedIn>
        <AuthSetup>
          <Routes>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </AuthSetup>
      </SignedIn>
    </BrowserRouter>
  );
}

export default App;
