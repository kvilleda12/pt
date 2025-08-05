'use client';
import { useState } from "react";
import HumanModel from "../../ui-components/human-model";
import styles from "./start.module.css"

class BodyPartHitboxes {
    constructor(humanModel, scene) {
        this.humanModel = humanModel;
        this.scene = scene;
        this.hitboxes = new Map();
        this.createHitboxes();
    }

    createHitboxes() {
        // Define hitbox positions and sizes relative to your model
        const hitboxData = {
            head: { position: [0, 1.7, 0], size: [0.3, 0.3, 0.3] },
            chest: { position: [0, 1.2, 0], size: [0.5, 0.4, 0.3] },
            left_arm: { position: [-0.4, 1.2, 0], size: [0.2, 0.6, 0.2] },
            right_arm: { position: [0.4, 1.2, 0], size: [0.2, 0.6, 0.2] },
            left_leg: { position: [-0.2, 0.4, 0], size: [0.2, 0.8, 0.2] },
            right_leg: { position: [0.2, 0.4, 0], size: [0.2, 0.8, 0.2] },
            abdomen: { position: [0, 0.9, 0], size: [0.4, 0.3, 0.2] }
        };

        Object.entries(hitboxData).forEach(([partName, data]) => {
            const geometry = new THREE.BoxGeometry(...data.size);
            const material = new THREE.MeshBasicMaterial({ 
                transparent: true, 
                opacity: 0,
                visible: false // Make completely invisible
            });
            
            const hitbox = new THREE.Mesh(geometry, material);
            hitbox.position.set(...data.position);
            hitbox.userData = { bodyPart: partName };
            hitbox.name = `hitbox_${partName}`;
            
            this.hitboxes.set(partName, hitbox);
            this.scene.add(hitbox);
        });
    }

    // Optional: Show hitboxes for debugging
    toggleHitboxVisibility(visible = true) {
        this.hitboxes.forEach(hitbox => {
            hitbox.material.visible = visible;
            hitbox.material.opacity = visible ? 0.3 : 0;
        });
    }

    // Get all hitbox meshes for raycasting
    getHitboxMeshes() {
        return Array.from(this.hitboxes.values());
    }
}

// Usage
const hitboxSystem = new BodyPartHitboxes(humanModel, scene);

// Modified click handler
function onMouseClick(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    
    // Only check hitboxes
    const intersects = raycaster.intersectObjects(hitboxSystem.getHitboxMeshes());

    if (intersects.length > 0) {
        const bodyPart = intersects[0].object.userData.bodyPart;
        handleBodyPartClick(bodyPart, intersects[0].point);
    }
}

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