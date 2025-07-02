import React from "react";
import Link from "next/link";
import styles from "./ui.module.css"

// This component can be imported and used in your layout or pages to provide a consistent navbar across the application.
export default function Navbar() {
    return (
        <ul className={styles.navbar}>
            <li className={styles.navItem}>
                <Link href="/">Home</Link>
            </li>
            <li className={styles.navItem}>
                <Link href="/about">About</Link>
            </li>
        </ul>
    );
}
