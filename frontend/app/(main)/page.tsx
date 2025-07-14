'use client';
import Link from "next/link";
import styles from "../page.module.css";
import SplitText from "@/app/ui-components/reactbits/SplitText.js";
import StarBorder from "@/app/ui-components/reactbits/StarBorder.js";

export default function Home() {
  const handleAnimationComplete = () => {
    console.log('Title animated!');
  };

  return (
    <div className={styles.page}>
      <SplitText
        text="Welcome to PTI"
        className={styles.title}
        delay={10}
        duration={2}
        ease="elastic.out(1, 0.3)"
        splitType="chars"
        from={{ opacity: 0, y: 40 }}
        to={{ opacity: 1, y: 0 }}
        threshold={0.1}
        rootMargin="-100px"
        textAlign="center"
        onLetterAnimationComplete={handleAnimationComplete}
      />
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
