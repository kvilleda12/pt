'use client';
import { handleSignUp } from '@/app/services/Auth';
import Link from 'next/link';
import { useState } from 'react';
import { redirect } from 'next/navigation';
import styles from '../auth.module.css';

export default function SignUpPage() {
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await handleSignUp(email, password, username, name);
            console.log('redirecting post sign up...')
            redirect('/start');
        } catch (err: any) {
            console.error('Sign up error:', err);
            setError(err.message || 'Failed to create account. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.authPage}>
            <div className={styles.headingBox}>
                <h1 className={styles.title}>Sign Up</h1>
                <p className={styles.subtitle}>
                    Create a new account to get started with PTI.
                </p>
            </div>
            <div className={styles.formContainer}>
                {error && (
                    <div className="mb-6 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-center">
                        <p className={styles.errorMessage}>{error}</p>
                    </div>
                )}

                <form onSubmit={handleSubmit} className={styles.form}>
                    <label className={styles.label} htmlFor="name">Full Name</label>
                    <input
                        type="text"
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className={styles.inputElem}
                        placeholder="Enter your full name"
                        required
                    />
                    <label className={styles.label} htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className={styles.inputElem}
                        placeholder="Choose a username"
                        required
                    />
                    <label className={styles.label} htmlFor="email">Email Address</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className={styles.inputElem}
                        placeholder="Enter your email"
                        required
                    />
                    <label className={styles.label} htmlFor="password">Password</label>
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
                            {loading ? 'Creating Account...' : 'Create Account'}
                        </button>
                    </div>
                </form>
            </div>
            {/* Signin Link */}
            <div className="mt-8 text-center">
                <p className="text-gray-400 text-sm">
                    Already have an account?{' '}
                    <Link href="/login" className="text-white font-medium hover:underline">
                        Sign in
                    </Link>
                </p>
            </div>
        </div>
    );
}

