import React, { useState } from 'react';
import { useRouter } from 'next/navigation'; // <-- IMPORT THE ROUTER

type AuthStep = 'email_check' | 'sign_in' | 'sign_up';

type AuthModalProps = {
  onClose: () => void;
};

export default function AuthModal({ onClose }: AuthModalProps) {
  const router = useRouter(); // <-- INITIALIZE THE ROUTER
  const [step, setStep] = useState<AuthStep>('email_check');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [username, setUsername] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleEmailCheck = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch('http://localhost:8000/api/auth/check-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Error');
      setStep(data.exists ? 'sign_in' : 'sign_up');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  //sign_in stuff
  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
        const response = await fetch('http://localhost:8000/api/auth/signin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Sign in failed.');

        // go to start page
        router.push('/start');

    } catch (err: any) {
        setError(err.message);
    } finally {
        setIsLoading(false);
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
        const response = await fetch('http://localhost:8000/api/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, name, username }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Failed to create account.');

        // When they sign up just sign them in automatically
        router.push('/start');
    } catch (err: any) {
        setError(err.message);
    } finally {
        setIsLoading(false);
    }
  };

  const renderStep = () => {
    switch (step) {
      case 'email_check':
        return (
          <form onSubmit={handleEmailCheck} className="space-y-6">
            <h2 className="text-2xl font-bold text-center text-white">Get Started</h2>
            <div>
              <label htmlFor="email" className="text-sm font-medium text-gray-300 block mb-2">Email Address</label>
              <input id="email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} className="w-full px-4 py-2 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="you@example.com"/>
            </div>
            <button type="submit" disabled={isLoading} className="w-full primary-btn">
              {isLoading ? 'Checking...' : 'Continue'}
            </button>
          </form>
        );
      
      case 'sign_in':
        return (
          <form onSubmit={handleSignIn} className="space-y-6">
            <h2 className="text-2xl font-bold text-center text-white">Welcome Back!</h2>
            <p className="text-center text-gray-400 bg-gray-900/50 p-2 rounded-md">{email}</p>
            <div>
                <label htmlFor="password" className="text-sm font-medium text-gray-300 block mb-2">Password</label>
                <input id="password" type="password" required value={password} onChange={(e) => setPassword(e.target.value)} className="w-full px-4 py-2 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="••••••••"/>
            </div>
            <button type="submit" disabled={isLoading} className="w-full primary-btn">
              {isLoading ? 'Signing In...' : 'Sign In'}
            </button>
          </form>
        );

      case 'sign_up':
        return (
          <form onSubmit={handleSignUp} className="space-y-6">
            <h2 className="text-2xl font-bold text-center text-white">Create Your Account</h2>
            <p className="text-center text-gray-400 bg-gray-900/50 p-2 rounded-md">{email}</p>
            <div>
                <label htmlFor="name" className="text-sm font-medium text-gray-300 block mb-2">Full Name</label>
                <input id="name" type="text" required value={name} onChange={(e) => setName(e.target.value)} className="w-full px-4 py-2 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Jane Doe"/>
            </div>
             <div>
                <label htmlFor="username" className="text-sm font-medium text-gray-300 block mb-2">Username</label>
                <input id="username" type="text" required value={username} onChange={(e) => setUsername(e.target.value)} className="w-full px-4 py-2 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="janedoe"/>
            </div>
            <div>
                <label htmlFor="password" className="text-sm font-medium text-gray-300 block mb-2">Create Password</label>
                <input id="password" type="password" required value={password} onChange={(e) => setPassword(e.target.value)} className="w-full px-4 py-2 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="••••••••"/>
            </div>
            <button type="submit" disabled={isLoading} className="w-full primary-btn">
              {isLoading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>
        );
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4">
      <div className="relative w-full max-w-md p-8 space-y-4 bg-gray-800 rounded-xl shadow-lg">
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-white transition" aria-label="Close">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
        {renderStep()}
        {error && <p className="text-red-400 text-sm text-center pt-2">{error}</p>}
      </div>
      <style>{`
        .primary-btn { padding: 0.75rem 1rem; font-weight: 600; color: white; background-color: #4f46e5; border-radius: 0.375rem; transition: background-color 0.3s; }
        .primary-btn:hover { background-color: #4338ca; }
        .primary-btn:disabled { background-color: #4b5563; cursor: not-allowed; }
      `}</style>
    </div>
  );
}

