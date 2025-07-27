'use client';
import { signIn } from '@/auth';
import Link from 'next/link';
import { useState } from 'react';
// 1. Import useSearchParams to read URL errors
import { useSearchParams } from 'next/navigation';

export default function LoginPage() {
    const searchParams = useSearchParams();
    // 2. Get the error message from the URL
    const callbackError = searchParams.get('error');

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    
    // 3. This error message will be displayed to the user
    const error = callbackError === 'CredentialsSignin' 
        ? 'Invalid email or password. Please try again.'
        : null;

    // 4. Simplify the submit handler
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        // Let signIn handle the redirect and errors. No try/catch needed here.
        await signIn('credentials', {
            email: email,
            password: password,
            callbackUrl: '/start' // Redirect to /start on success
        });
    };

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col justify-center items-center p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-10">
                    <h1 className="text-4xl font-bold text-slate-800 mb-2">Welcome Back</h1>
                    <p className="text-slate-600">Sign in to continue</p>
                </div>

                <div className="bg-white rounded-3xl shadow-xl shadow-slate-200 p-10 border border-slate-100">
                    {error && (
                        <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-red-700 text-sm font-medium">{error}</p>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-8">
                        <div>
                            <label className="block text-xs font-semibold text-slate-600 tracking-wider uppercase mb-2" htmlFor="email">
                                Email address
                            </label>
                            <input
                                type="email"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full px-4 py-3 bg-slate-100 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                placeholder="you@example.com"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-xs font-semibold text-slate-600 tracking-wider uppercase mb-2" htmlFor="password">
                                Password
                            </label>
                            <input
                                type="password"
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-4 py-3 bg-slate-100 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        <div className="pt-2">
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full py-3 px-4 bg-slate-900 text-white font-semibold rounded-lg hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loading ? 'Signing in...' : 'Sign In'}
                            </button>
                        </div>
                    </form>

                    <div className="mt-8 text-center">
                        <p className="text-slate-600 text-sm">
                            Don't have an account?{' '}
                            <Link href="/sign-up" className="text-slate-800 font-semibold hover:underline">
                                Sign up
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
