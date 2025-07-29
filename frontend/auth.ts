import NextAuth from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import { authConfig } from './auth.config';
import { z } from 'zod';
import { handleSignIn } from '@/app/services/Auth';

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
    providers: [
        Credentials({
            async authorize(credentials) {
                const parsedCredentials = z
                    .object({ email: z.string().email(), password: z.string().min(5) })
                    .safeParse(credentials);

                console.log('auth.ts, authenticating user:', parsedCredentials);
                if (parsedCredentials.success) {
                    const { email, password } = parsedCredentials.data;
                    try {
                        const user = await handleSignIn(email, password);
                        if (!user) return null;
                        return user;
                    } catch (error) {
                        console.error('Error during sign in:', error);
                        return null;
                    }
                } else {
                    console.error('Invalid credentials:', parsedCredentials.error);
                    return null;
                }
            },
        }),
    ],
});