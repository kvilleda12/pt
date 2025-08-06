'use client';
import HumanModel from "@/app//ui-components/human-model";
import styles from "./start.module.css";
import { BodyPartProvider, useBodyPart } from "@/app/contexts/BodyPartContext";
import { redirect } from 'next/navigation';
import { handleBodyPartClick } from '@/app/services/userSetupActions';

function StartContent() {
    const { selectedBodyPart } = useBodyPart();

    const handleContinue = () => {
        if (selectedBodyPart) {
            console.log("Continuing with selected body part:", selectedBodyPart);
            handleBodyPartClick(selectedBodyPart); // Send to server
            redirect('/start/questionnaire')  // Navigate to next step
        }
    };

    return (
        <div className={styles.layout}>
            <h2 className={styles.header}>Select the area where you feel pain</h2>
            <h3 className={styles.subtitle}>You can drag the model to view different angles.</h3>
            <div className={styles.modelContainer}>
                <HumanModel />

                {selectedBodyPart && (
                    <button
                        className={styles.continueButton}
                        onClick={handleContinue}
                    >
                        Continue with {selectedBodyPart.replace('_', ' ')}
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

export default function Start() {
    return (
        <BodyPartProvider>
            <StartContent />
        </BodyPartProvider>
    );
}