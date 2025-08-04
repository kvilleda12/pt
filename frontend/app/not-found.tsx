// app/not-found.tsx
import Link from 'next/link';
import styles from './error.module.css';

export default function NotFound() {
    return (
        <div className={styles.errorPage}>
            <h1 className={styles.errorTitle}>404</h1>
            <h2 className={styles.errorSubtitle}>Page Not Found</h2>
            <p className="text-lg text-gray-600">
                Sorry, we couldn't find the page you were looking for.
            </p>
            <Link href="/">
                <button className={styles.errorButton} >Go Back Home</button>
            </Link>
        </div>
    );
}