# Next.js — Swap React SPA for Next.js

## Overview
This replaces the Vite React SPA frontend with a Next.js application. This is a significant change — only use if you need SSR, ISR, or Next.js-specific features.

## Dependencies
Replace the entire `frontend/` directory:
```bash
rm -rf frontend
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --no-import-alias
cd frontend && npm install @clerk/nextjs @tanstack/react-query axios
```

## Doppler Secrets
Same as SPA, plus:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` (replaces `VITE_CLERK_PUBLISHABLE_KEY`)

## Config Changes
No backend config changes needed.

## Key File Changes

### `frontend/src/app/layout.tsx`
```tsx
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

### `frontend/src/middleware.ts`
```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isPublicRoute = createRouteMatcher(["/sign-in(.*)", "/sign-up(.*)", "/"]);

export default clerkMiddleware(async (auth, request) => {
  if (!isPublicRoute(request)) {
    await auth.protect();
  }
});

export const config = {
  matcher: ["/((?!.*\\..*|_next).*)", "/", "/(api|trpc)(.*)"],
};
```

### `frontend/src/app/api/[...proxy]/route.ts`
Proxy API calls to FastAPI backend:
```typescript
import { auth } from "@clerk/nextjs/server";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const { getToken } = await auth();
  const token = await getToken();
  const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";
  const path = request.nextUrl.pathname.replace("/api/proxy", "/api/v1");

  const response = await fetch(`${backendUrl}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  return NextResponse.json(await response.json());
}
```

## Dockerfile Changes
The Dockerfile changes significantly — the frontend build step uses `next build` instead of `vite build`, and you may want to serve Next.js separately or use a unified container.

## Migration SQL
No migration needed.

## Notes
- This is a major architectural change — evaluate whether you truly need SSR
- The React SPA pattern is simpler and sufficient for most dashboard-style apps
- If you just need SEO for a landing page, consider keeping the SPA + a static landing page
