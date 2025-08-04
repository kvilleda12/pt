// logout/page.tsx
import { Suspense } from 'react';
import Link from 'next/link';
import styles from '../auth.module.css';
import { handleSignOut } from '@/app/services/actions';

// Loading component to show while logging out
function LogoutLoading() {
    return (
        <div className={styles.authPage}>
            <div className={styles.loadingContainer}>
                <div className={styles.spinner}></div>
                <h2 className={styles.title}>Logging out...</h2>
                <p className={styles.subtitle}>Please wait while we sign you out.</p>
            </div>
        </div>
    );
}

// Form component for logout confirmation
function LogoutForm() {
    return (
        <div className={styles.authPage}>
            <h2 className={styles.title}>Confirm Logout</h2>
            <p className={styles.subtitle}>Are you sure you want to log out?</p>
            <div className={styles.logoutForm}>
                <form action={handleSignOut}>
                    <button type="submit" className={styles.submitButton}>
                        Yes, Log Out
                    </button>
                </form>
                <Link href="/">
                    <button className={styles.submitButton}>Cancel</button>
                </Link>
            </div>
        </div>
    );
}

// Main component for the logout page
export default function Logout() {
    return (
        <Suspense fallback={<LogoutLoading />}>
            <LogoutForm />
        </Suspense>
    );
}