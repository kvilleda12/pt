'use client';

import React, { useState } from 'react';
import Link from "next/link";
import styles from "./page.module.css";
import SignInButton from './ui-components/SignInButton';
import SignUpForm from './ui-components/SignUpForm';

export default function Home() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <div className={styles.page}>
      <h2 className={styles.title}>PTI</h2>
      <h4 className={styles.subheading}>Your intelligent physical therapy assistant</h4>

      <main className={styles.main}>
        <button className={styles.buttonPrimary}>
          <Link href="/about">Coming Soon</Link>
        </button>
        <div className="absolute top-[5px] left-[5px]" ></div>
          <SignInButton onClick={openModal} />

      </main>
      <footer className={styles.footer}>
      </footer>
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4">
          <SignUpForm onClose={closeModal} />
        </div>
      )}
    </div>
  );
}
