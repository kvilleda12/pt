// app/error.tsx
'use client';
import styles from './error.module.css';
import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service or the console
    console.error(error);
  }, [error]);

  return (
    <div className={styles.errorPage}>
        <h1 className={styles.errorTitle}>
          Oops, something went wrong.
        </h1>
        <p className={styles.errorSubtitle}>
          We encountered an unexpected issue.<br></br>Please try again, or contact support if the problem persists.
        </p>

        <button
          onClick={() => reset()}
          className={styles.errorButton}
        >
          Try Again
        </button>

        {/* Conditionally render the error digest for debugging in development */}
        {process.env.NODE_ENV === 'development' && (
          <div className="mt-10 text-xs text-gray-500 bg-gray-100 p-4 rounded-lg">
            <p className="font-mono">
              <strong>Error Digest:</strong> {error.digest}
            </p>
          </div>
        )}
    </div>
  );
}