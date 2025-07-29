import type { NextAuthConfig } from 'next-auth';

const restrictedPaths = ['/start', '/dashboard'];

export const authConfig = {
  pages: {
    signIn: '/login',
    signOut: '/logout',
  },
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user;
      const isRestricted = restrictedPaths.some(path => nextUrl.pathname.startsWith(path));
      console.log('authentication middleware. isLogged in', isLoggedIn, 'isRestricted', isRestricted);
      if (isRestricted) {
        if (isLoggedIn) return true;
        return false; // Redirect unauthenticated users to login page
      } else if (isLoggedIn) {
        // return Response.redirect(new URL('/dashboard', nextUrl));    // Redirect authenticated users to dashboard
      }
      return true;
    },
  },
  providers: [], // Add providers with an empty array for now
} satisfies NextAuthConfig;