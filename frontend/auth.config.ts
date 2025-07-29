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
      const isOnLoginPage = nextUrl.pathname === '/login';
      const isOnSignUpPage = nextUrl.pathname === '/sign-up';
      
      console.log('authentication middleware (auth.config.ts): isLogged in', isLoggedIn, 'isRestricted', isRestricted);
      
      // If user is logged in and on login/sign-up pages, redirect to /start
      if (isLoggedIn && (isOnLoginPage || isOnSignUpPage)) {
        console.log('Auth middleware redirecting to /start');
        
        // Use environment variable for base URL or fallback to current origin
        const baseUrl = process.env.BASE_URL || nextUrl.origin;
        return Response.redirect(`${baseUrl}/start`);
      }
      
      if (isRestricted) {
        if (isLoggedIn) return true;
        return false; // Redirect unauthenticated users to login page
      }
      
      return true;
    },
  },
  providers: [], // Add providers with an empty array for now
} satisfies NextAuthConfig;