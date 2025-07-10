import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';
import { Suspense } from 'react';
import { Html } from '@react-three/drei';
import styles from './ui.module.css';

function Human({ handleClick }: { handleClick: (e: { stopPropagation: () => void; object: { name: any; }; }) => void }) {
    const { scene, nodes } = useGLTF('/model-human.glb');

    return (<group scale={[125, 125, 125]} castShadow >
        <primitive object={scene} onClick={handleClick} />
    </group>);
}

export default function HumanModel( { handleClick }: { handleClick: (e: { stopPropagation: () => void; object: { name: any; }; }) => void }) {
    return (
        <Canvas camera={{ position: [0, 1, 3], fov: 50 }}
            style={{ height: '100vh', width: '100%' }}>
            <ambientLight intensity={0.5} />
            <directionalLight position={[5, 5, 5]} />
            <Suspense fallback={
                <Html>
                    <span className={styles.suspenseMessage}>Loading Human Model...</span>
                </Html>
            }>
                <Human handleClick={handleClick} />
                <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.5, 0]}>
                    <planeGeometry args={[100, 100]} />
                    <shadowMaterial opacity={0.3} />
                </mesh>
            </Suspense>
            <OrbitControls enableZoom={false} />
        </Canvas>
    );
}
