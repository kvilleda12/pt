'use client';
import Link from "next/link";
import styles from "./page.module.css";
import SplitText from "@/app/ui-components/reactbits/SplitText.js";
import Orb from "@/app/ui-components/reactbits/Orb.js";



export default function Home() {
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
        onLetterAnimationComplete={() => { }}
      />
      <h4 className={styles.subheading}>Your intelligent physical therapy assistant</h4>
      <main className={styles.main}>
        <div
          style={{
            width: '100%',
            height: '600px',
            position: 'relative',
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'center',
          }}
        >
          <Orb
            hoverIntensity={.7}
            rotateOnHover={true}
            hue={310}
            forceHoverState={false}
          >
            <Link href="/login">
              <button className={styles.buttonPrimary}>
                <span>START</span>
              </button>
            </Link>
          </Orb>
        </div>
      </main>
    </div>
  );
}
