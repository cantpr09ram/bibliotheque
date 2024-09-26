import { getToken } from "next-auth/jwt";
import { NextResponse } from "next/server";

export async function middleware(req: { cookies: any; nextUrl: { pathname: any; }; url: string | URL | undefined; }) {
  const token = await getToken({ req, secret: process.env.NEXTAUTH_SECRET });
  const { pathname } = req.nextUrl;

  // Allow access if it's an auth request, an API request, or the user is authenticated
  if (pathname.startsWith("/api") || pathname.startsWith("/auth") || token) {
    return NextResponse.next();
  }

  // Redirect to sign-in if the user is not authenticated
  if (!token && pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/auth", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/auth"],
};
""