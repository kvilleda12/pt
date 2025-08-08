'use client';
// contexts/BodyPartContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react';

// This file provides a context (global variables) to manage the selected body part state in /start/page.tsx
interface BodyPartContextType {
    selectedBodyPart: string;
    setSelectedBodyPart: (part: string) => void;
}

const BodyPartContext = createContext<BodyPartContextType | undefined>(undefined);

export function BodyPartProvider({ children }: { children: ReactNode }) {
    const [selectedBodyPart, setSelectedBodyPart] = useState<string>('');

    return (
        <BodyPartContext.Provider value={{
            selectedBodyPart,
            setSelectedBodyPart,
        }}>
            {children}
        </BodyPartContext.Provider>
    );
}

export function useBodyPart() {
    const context = useContext(BodyPartContext);
    if (!context) {
        throw new Error('useBodyPart must be used within BodyPartProvider');
    }
    return context;
}