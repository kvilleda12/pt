'use client';
import HumanModel from "@/app/components/human-model";
import styles from "./start.module.css";
import { BodyPartProvider, useBodyPart } from "@/app/utils/BodyPartContext";
import { redirect } from 'next/navigation';
import Link from 'next/link';

export default function StartContent() {
    const { selectedBodyPart } = useBodyPart();

    return (
        <div className={styles.layout}>
            <h2 className={styles.header}>Select the area where you feel pain</h2>
            <h3 className={styles.subtitle}>You can drag the model to view different angles.</h3>
            <Link href='/logout' className={styles.logoutButton}>Logout</Link>
            <div className={styles.modelContainer}>
                <HumanModel />

                {selectedBodyPart && (
                    <button
                        className={styles.continueButton}
                        onClick={() => redirect('/start/questionnaire')}
                    >
                        <span>
                            Continue with {selectedBodyPart.replace('_', ' ')}
                        </span>
                    </button>
                )}
            </div>

            {/* Debug button 
            <button
                onClick={() => (window as any).toggleHitboxes?.(true)}
                className={styles.debugButton}
                style={{ position: 'absolute', top: '10px', right: '10px' }}
            >
                Show Hitboxes (Debug)
            </button>
            */}
        </div>
    );
}
