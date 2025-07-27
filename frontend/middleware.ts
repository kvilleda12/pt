import NextAuth from 'next-auth';
import { authConfig } from './auth.config';
// https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher

export default NextAuth(authConfig).auth;

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
};