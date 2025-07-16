import React from 'react';


type SignInButtonProps = {
    onClick: () => void; 
  };


export default function SignInButton({ onClick }: SignInButtonProps) {
  return (
    <button 
      onClick={onClick} 
      className="bg-indigo-600 text-white py-2 px-6 rounded-lg font-semibold hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-indigo-500 transition-colors duration-300"
    >
      Sign In / Sign Up
    </button>
  );
}