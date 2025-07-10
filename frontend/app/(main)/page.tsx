import Link from "next/link";
import styles from "../page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <h2 className={styles.title}>PTI</h2>
      <h4 className={styles.subheading}>Your intelligent physical therapy assistant</h4>
      <main className={styles.main}>
        <button className={styles.buttonPrimary}>
          <Link href="/start">Start</Link>
        </button>
      </main>
      <footer className={styles.footer}>
      </footer>
    </div>
  );
}
