'use client';

import Link from 'next/link';
import { useFormStatus } from 'react-dom';
import { useActionState } from 'react';
import { authenticate } from '@/app/services/actions';
import styles from '../auth.module.css';

// Helper component to manage the button's loading state
function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button
      type="submit"
      disabled={pending}
      className={styles.submitButton}
    >
      {pending ? 'Authenticating...' : 'Sign In'}
    </button>
  );
}

export default function LoginPage() {
  // 'errorMessage' will hold the string returned from the server action on failure
  // 'dispatch' is the function to trigger the action
  const [errorMessage, dispatch] = useActionState(authenticate, undefined);

  return (
    <div className={styles.authPage}>
      <div className={styles.headingBox}>
        <h1 className={styles.title}>Sign In</h1>
        <p className={styles.subtitle}>Enter your credentials to access your account.</p>
      </div>
      <div className={styles.formContainer}>
        <form action={dispatch} className={styles.form}>
          <label htmlFor="email" className={styles.label}>
            Email Address
          </label>
          <input
            type="email"
            id="email"
            name="email"
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
            name="password"
            className={styles.inputElem}
            placeholder="Enter your password"
            required
          />
          <div className="pt-2">
            <SubmitButton />
          </div>
          {errorMessage && (
            <div className="mt-4 p-3 text-center">
              <p className={styles.errorMessage}>{errorMessage}</p>
            </div>
          )}
        </form>
      </div>
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
