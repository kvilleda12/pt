'use client';
import React, { useState } from "react";
import HumanModel from "../ui-components/human-model";
import styles from "./start.module.css"

// This component is the start page where the user selects the area of pain
export default function Start() {
    const [painSelected, setPainSelected] = useState(false);

    const handleClick = (e: { stopPropagation: () => void; object: { name: any; }; }) => {
        e.stopPropagation();
        // setPainSelected(true);
        console.log("User Selected: ", e.object.name);
    }

    return (
        <div className={styles.layout}>
            <h2 className={styles.header}>Select the area where you feel pain</h2>
            <HumanModel handleClick={handleClick}/>
            {painSelected && (
                <button>
                    Continue
                </button>)}
        </div>
    );
}