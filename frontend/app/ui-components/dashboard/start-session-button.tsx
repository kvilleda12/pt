'use client';

import { useState } from 'react';

interface StartSessionButtonProps {
  isActive: boolean;
  onStart: () => void;
  onEnd: () => void;
}

export function StartSessionButton({ isActive, onStart, onEnd }: StartSessionButtonProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = async () => {
    setIsLoading(true);
    try {
      if (isActive) {
        await onEnd();
      } else {
        await onStart();
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={isLoading}
      className={`
        relative group px-8 py-4 rounded-2xl font-semibold text-lg transition-all duration-500
        transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed
        overflow-hidden backdrop-blur-xl border border-white/30
        ${isActive 
          ? 'bg-gradient-to-r from-red-500 via-red-600 to-red-700 hover:from-red-600 hover:via-red-700 hover:to-red-800 text-white shadow-2xl shadow-red-500/40' 
          : 'bg-gradient-to-r from-emerald-500 via-emerald-600 to-emerald-700 hover:from-emerald-600 hover:via-emerald-700 hover:to-emerald-800 text-white shadow-2xl shadow-emerald-500/40'
        }
      `}
    >
      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
      
      {isLoading ? (
        <div className="flex items-center space-x-3 relative z-10">
          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          <span>{isActive ? 'Ending Session...' : 'Starting Session...'}</span>
        </div>
      ) : (
        <div className="flex items-center space-x-3 relative z-10">
          <div className={`
            w-6 h-6 rounded-full flex items-center justify-center transition-all duration-300
            ${isActive ? 'bg-white/20' : 'bg-white/20'}
          `}>
            <span className="text-lg">
              {isActive ? '⏹' : '▶'}
            </span>
          </div>
          <span>{isActive ? 'End Session' : 'Start Session'}</span>
        </div>
      )}
      
      {/* Pulse effect when active */}
      {isActive && (
        <>
          <div className="absolute inset-0 rounded-2xl bg-red-400 animate-ping opacity-30"></div>
          <div className="absolute inset-0 rounded-2xl bg-red-300 animate-pulse opacity-20"></div>
        </>
      )}
      
      {/* Glow effect */}
      <div className={`
        absolute inset-0 rounded-2xl blur-xl opacity-50 transition-opacity duration-300
        ${isActive ? 'bg-red-500' : 'bg-emerald-500'}
      `}></div>
    </button>
  );
}
