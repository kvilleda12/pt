// components/BodyPartHitboxes.tsx
import { useEffect, useRef } from 'react';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import { useBodyPart } from '../contexts/BodyPartContext';

export function BodyPartHitboxes() {
    const { scene, raycaster, camera, gl } = useThree();
    const { setSelectedBodyPart } = useBodyPart();
    const hitboxesRef = useRef<Map<string, THREE.Mesh>>(new Map());
    const mouseRef = useRef(new THREE.Vector2());

    useEffect(() => {
        const hitboxData = {
            neck: { position: [0, 0.8, -0.1] as [number, number, number], size: [0.2, 0.3, 0.2] as [number, number, number] },
            left_shoulder: { position: [-0.29, 0.5, -0.1] as [number, number, number], size: [0.25, 0.25, 0.25] as [number, number, number] },
            right_shoulder: { position: [0.29, 0.5, -0.1] as [number, number, number], size: [0.25, 0.25, 0.25] as [number, number, number] },
            chest: { position: [0, 0.4, 0.1] as [number, number, number], size: [0.6, 0.45, 0.25] as [number, number, number] },
            back: { position: [0, 0.4, -0.2] as [number, number, number], size: [0.6, 0.5, 0.25] as [number, number, number] },
            left_bicep: { position: [-0.45, 0.25, -0.05] as [number, number, number], size: [0.15, 0.5, 0.15] as [number, number, number] },
            left_tricep: { position: [-0.45, 0.25, -0.2] as [number, number, number], size: [0.15, 0.5, 0.15] as [number, number, number] },
            right_bicep: { position: [0.45, 0.25, -0.05] as [number, number, number], size: [0.15, 0.5, 0.15] as [number, number, number] },
            right_tricep: { position: [0.45, 0.25, -0.2] as [number, number, number], size: [0.15, 0.5, 0.15] as [number, number, number] },
            abdomen: { position: [0, 0.1, 0.0] as [number, number, number], size: [0.5, 0.3, 0.2] as [number, number, number] },
            left_quad: { position: [-0.2, -0.65, 0.0] as [number, number, number], size: [0.25, 0.5, 0.2] as [number, number, number] },
            left_hamstring: { position: [-0.2, -0.65, -0.2] as [number, number, number], size: [0.25, 0.5, 0.2] as [number, number, number] },
            right_quad: { position: [0.2, -0.65, 0.0] as [number, number, number], size: [0.25, 0.5, 0.2] as [number, number, number] },
            right_hamstring: { position: [0.2, -0.65, -0.2] as [number, number, number], size: [0.25, 0.5, 0.2] as [number, number, number] },
            left_calf: { position: [-0.2, -1.05, -0.1] as [number, number, number], size: [0.2, 0.4, 0.2] as [number, number, number] },
            right_calf: { position: [0.2, -1.05, -0.1] as [number, number, number], size: [0.2, 0.4, 0.2] as [number, number, number] },
            left_ankle: { position: [-0.2, -1.3, -0.1] as [number, number, number], size: [0.15, 0.12, 0.15] as [number, number, number] },
            right_ankle: { position: [0.2, -1.3, -0.1] as [number, number, number], size: [0.15, 0.12, 0.15] as [number, number, number] }
        };

        // Create hitboxes
        Object.entries(hitboxData).forEach(([partName, data]) => {
            const geometry = new THREE.BoxGeometry(...data.size);
            const material = new THREE.MeshBasicMaterial({
                transparent: true,
                opacity: 0,
                visible: false
            });

            const hitbox = new THREE.Mesh(geometry, material);
            hitbox.position.set(...data.position);
            hitbox.userData = { bodyPart: partName };
            hitbox.name = `hitbox_${partName}`;

            hitboxesRef.current.set(partName, hitbox);
            scene.add(hitbox);
        });

        // Click handler
        const handleClick = (event: MouseEvent) => {
            const rect = gl.domElement.getBoundingClientRect();
            mouseRef.current.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            mouseRef.current.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.setFromCamera(mouseRef.current, camera);
            const intersects = raycaster.intersectObjects(Array.from(hitboxesRef.current.values()));

            if (intersects.length > 0) {
                const bodyPart = intersects[0].object.userData.bodyPart;
                console.log('Body part clicked:', bodyPart);

                // Update context
                setSelectedBodyPart(bodyPart);

                // Send to server
                handleBodyPartClick(bodyPart, intersects[0].point);
            }
        };

        gl.domElement.addEventListener('click', handleClick);

        // Cleanup
        return () => {
            gl.domElement.removeEventListener('click', handleClick);
            hitboxesRef.current.forEach(hitbox => {
                scene.remove(hitbox);
                hitbox.geometry.dispose();
                if (hitbox.material instanceof THREE.Material) {
                    hitbox.material.dispose();
                }
            });
            hitboxesRef.current.clear();
        };
    }, [scene, raycaster, camera, gl, setSelectedBodyPart]);

    // Debug function to show hitboxes
    const toggleVisibility = (visible: boolean) => {
        hitboxesRef.current.forEach(hitbox => {
            if (hitbox.material instanceof THREE.MeshBasicMaterial) {
                hitbox.material.visible = visible;
                hitbox.material.opacity = visible ? 0.3 : 0;
            }
        });
    };

    // Expose debug function globally (remove in production)
    useEffect(() => {
        (window as any).toggleHitboxes = toggleVisibility;
    }, []);

    return null; // This component doesn't render anything visual
}

// Server communication function
async function handleBodyPartClick(bodyPart: string, position: THREE.Vector3) {
    console.log('Sending body part click to server:', bodyPart, position);
    // try {
    //     await fetch('/api/body-part-click', {
    //         method: 'POST',
    //         headers: { 'Content-Type': 'application/json' },
    //         body: JSON.stringify({
    //             bodyPart,
    //             position: { x: position.x, y: position.y, z: position.z },
    //             timestamp: new Date().toISOString()
    //         })
    //     });
    // } catch (error) {
    //     console.error('Failed to track body part click:', error);
    // }
}