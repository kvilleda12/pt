'use client';
import { signIn } from '@/auth';
import Link from 'next/link';
import { useState } from 'react';
import styles from '../auth.module.css';

export default function LoginPage() {
    const [error, setError] = useState<string | null>(null);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            console.log('attempting sign in...')
            await signIn('credentials', {
                email: email,
                password: password,
                redirect: true,
                callbackUrl: '/start'
            });
        } catch (err: any) {
            console.error('Sign in error:', err);
            setError(err.message || 'Failed to sign in. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.authPage}>
            <div className={styles.headingBox}>
                <h1 className={styles.title}>Sign In</h1>
                <p className={styles.subtitle}>Enter your credentials to access your account.</p>
            </div>
            <div className={styles.formContainer}>
                {error && (
                    <div className="mb-6 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-center">
                        <p className={styles.errorMessage}>{error}</p>
                    </div>
                )}

                <form onSubmit={handleSubmit} className={styles.form}>
                    <label htmlFor="email" className={styles.label}>
                        Email Address
                    </label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className={styles.inputElem}
                        placeholder="Enter your email"
                        required
                    />
                    <label htmlFor="password" className={styles.label}>
                        Password
                    </label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className={styles.inputElem}
                        placeholder="Enter your password"
                        required
                    />
                    <div className="pt-2">
                        <button
                            type="submit"
                            disabled={loading}
                            className={styles.submitButton}
                        >
                            {loading ? 'Authenticating...' : 'Sign In'}
                        </button>
                    </div>
                </form>
            </div>
            {/* Sign Up Link */}
            <div className="mt-8 text-center">
                <p className="text-gray-400 text-sm">
                    Don't have an account?{' '}
                    <Link href="/sign-up" className="text-white font-medium hover:underline">
                        Sign up now
                    </Link>
                </p>
            </div>
        </div>
    );
}
