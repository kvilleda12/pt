'use server';

import { signIn, signOut } from '@/auth';
import { redirect } from 'next/navigation';

// server action to handle authentication through useFormState. Caputres and receives form data.
export async function authenticate(
  prevState: string | undefined,
  formData: FormData
) {
  try {
    const email = formData.get('email') as string;
    const password = formData.get('password') as string;
    
    // Call signIn with credentials object instead of formData
    await signIn('credentials', { 
      email, 
      password, 
      redirect: false 
    });
    
  } catch (error: any) {
    console.error('Authentication error:', error);
    
    if (error.type === 'CredentialsSignin') {
      return 'Invalid credentials. Please try again.';
    }
    return 'An unexpected error occurred. Please try again.';
  } finally {
    // If we get here, authentication was successful, so redirect
    redirect('/start');
  }
}

// Calls API to handle Sign In, returns a user object if successful
export const handleSignIn = async (email: string, password: string) => {
  try {
    const response = await fetch(`${process.env.AUTH_URL}/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    console.log('Sign in response:', data);
    
    if (!response.ok) {
      console.error('API error response:', data);
      throw new Error(data.detail || 'Sign in failed. Incorrect email or password.');
    }
    
    return data.user;

  } catch (err: any) {
    console.error('Error during sign in:', err);
    throw new Error('Failed to sign in: ' + err.message);
  }
};

// Calls API to handle Sign Up, returns a user object if successful
export const handleSignUp = async (email: string, password: string, username: string, name: string) => {
  try {
    const response = await fetch(`${process.env.AUTH_URL}/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, username, name }),
    });
    const data = await response.json();
    console.log('Sign up data:', data);
    if (!response.ok) throw new Error(data.detail || 'Unknown error');

  } catch (err: any) {
    console.error('Error during sign up:', err);
    throw new Error('Failed to create account: ' + (err.message || 'Unknown error'));
  }
};

// The new Server Action that combines both steps using useFormState
export async function signUpAndSignIn(prevState: string | undefined, formData: FormData) {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;
  const username = formData.get('username') as string;
  const name = formData.get('name') as string;

  try {
    await handleSignUp(email, password, username, name);

    // Step 2: If sign-up was successful, sign the user in
    await signIn('credentials', { email, password, redirect: false });

  } catch (error: any) {
    console.error('Sign-up and Sign-in error:', error);
    // Return a user-friendly error message to display on the form
    return error.message || 'An unexpected error occurred.';
  }

  // Step 3: If both steps succeed, redirect to the start page
  redirect('/start');
}

export const handleSignOut = async () => {
  try {
    await signOut({ redirect: false });
  } catch (err) {
    console.error('Error during sign out:', err);
    throw new Error('Failed to sign out: ' + (err as Error).message);
  }
  redirect('/'); // Redirect to home page after sign out
};