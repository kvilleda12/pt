'use client';
import "@/app/globals.css";
import GooeyNav from "@/app/components/reactbits/GooeyNav.js";
import { useState } from "react";
import { usePathname } from "next/navigation";
// import styles from './page.module.css';  className={styles.background}

// This is the layout component for the main pages, which includes the GooeyNav navigation bar.

export default function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const items = [
    { label: "Home", href: "/" },
    { label: "About", href: "/about" },
  ];

  const pathname = usePathname();
  const initialIndex = items.findIndex(item => item.href === pathname); // get index from pathname to prevent refresh cheesing
  const [activeIndex, setActiveIndex] = useState(initialIndex); // Hold state in the parent component and pass to navbar

  return (
    <div >
      <div style={{ height: '40px', position: 'relative' }}>
        <GooeyNav
          items={items}
          particleCount={5}
          particleDistances={[70, 15]}
          particleR={100}
          setActiveIndex={setActiveIndex}
          activeIndex={activeIndex}
          animationTime={600}
          timeVariance={300}
          colors={[1, 2, 3, 1, 2, 3, 1, 4]}
        />
      </div>
      {/* Divider line below navbar */}
      <div style={{
        borderBottom: '.5px solid #e0e0e0',
        width: '95%',
        marginTop: '20px',
        marginLeft: 'auto',
        marginRight: 'auto',
      }} />
      {children}
    </div>
  );
}
