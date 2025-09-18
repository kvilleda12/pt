import type { NextAuthConfig } from 'next-auth';

const restrictedPaths = ['/start', '/app'];

export const authConfig = {
  pages: {
    signIn: '/login',
    signOut: '/logout',
  },
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const baseUrl = process.env.BASE_URL || nextUrl.origin;
      const isLoggedIn = !!auth?.user;
      const isRestricted = restrictedPaths.some(path => nextUrl.pathname.startsWith(path));
      const isOnLoginPage = nextUrl.pathname === '/login';
      const isOnSignUpPage = nextUrl.pathname === '/sign-up';

      // console.log('authentication middleware (auth.config.ts): isLogged in', isLoggedIn, 'isRestricted', isRestricted);

      // If user is logged in and on login/sign-up pages, redirect to /dashboard
      if (isLoggedIn && (isOnLoginPage || isOnSignUpPage)) {
        // console.log('Auth middleware redirecting to /dashboard');
        return Response.redirect(`${baseUrl}/app/dashboard`);
      }

      if (isRestricted) {
        if (isLoggedIn) return true;
        return Response.redirect(`${baseUrl}/sign-up`); // Redirect unauthenticated users to /sign-up
      }

      return true;
    },
  },
  providers: [], // Add providers with an empty array for now
} satisfies NextAuthConfig;