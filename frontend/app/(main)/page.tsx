'use client';
import Link from "next/link";
import styles from "./page.module.css";
import SplitText from "@/app/ui-components/reactbits/SplitText.js";
import Orb from "@/app/ui-components/reactbits/Orb.js";
import SignInButton from '../ui-components/SignInButton';
import SignUpForm from '../ui-components/SignUpForm';
import React, { useState } from 'react';

export default function Home() {
  const handleAnimationComplete = () => {
    console.log('Title animated!');
  };

  const [isModalOpen, setIsModalOpen] = useState(false);

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
            <button className={styles.buttonPrimary}>
              <Link href="/start"><span>START</span></Link>
            </button>
          </Orb>
        </div>
        <div className="absolute top-[5px] left-[5px]" >
          <SignInButton onClick={() => setIsModalOpen(true)} />
        </div>
      </main>
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4">
          <SignUpForm onClose={() => setIsModalOpen(false)} />
        </div>
      )}
    </div>
  );
}
