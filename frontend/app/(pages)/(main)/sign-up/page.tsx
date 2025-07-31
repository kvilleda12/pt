'use client';
import { useFormStatus } from 'react-dom';
import { useActionState } from 'react';
import { signUpAndSignIn } from '@/app/services/actions'; // Import the new action
import Link from 'next/link';
import styles from '../auth.module.css';

export default function SignUpPage() {
    const [errorMessage, dispatch] = useActionState(signUpAndSignIn, undefined);

    function SubmitButton() {
        const { pending } = useFormStatus();
        return (
            <button type="submit" disabled={pending} className={styles.submitButton} >
                {pending ? 'Creating Account...' : 'Sign Up'}
            </button>
        );
    }

    return (
        <div className={styles.authPage}>
            <div className={styles.headingBox}>
                <h1 className={styles.title}>Sign Up</h1>
                <p className={styles.subtitle}>
                    Create a new account to get started with PTI.
                </p>
            </div>
            <div className={styles.formContainer}>
                {errorMessage && (
                    <div className="mb-6 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-center">
                        <p className={styles.errorMessage}>{errorMessage}</p>
                    </div>
                )}

                <form action={dispatch} className={styles.form}>
                    <label className={styles.label} htmlFor="name">Full Name</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        className={styles.inputElem}
                        placeholder="Enter your full name"
                        required
                    />
                    <label className={styles.label} htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        className={styles.inputElem}
                        placeholder="Choose a username"
                        required
                    />
                    <label className={styles.label} htmlFor="email">Email Address</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        className={styles.inputElem}
                        placeholder="Enter your email"
                        required
                    />
                    <label className={styles.label} htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        className={styles.inputElem}
                        placeholder="Enter your password"
                        required
                    />
                    <SubmitButton />
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

