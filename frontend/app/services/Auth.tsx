
// Calls API to handle Sign In, returns a user object if successful
export const handleSignIn = async (email: string, password: string) => {
  try {
    const response = await fetch('http://localhost:8000/api/auth/signin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    console.log('Sign in response:', data);
    if (!response.ok) throw new Error(data.detail || 'Sign in failed. Incorrect email or password.');
    return data.user;

  } catch (err: any) {
    console.error('Error during sign in:', err);
    throw new Error('Failed to sign in.');
  }
};

export const handleSignUp = async (email: string, password: string, username: string) => {
  try {
    const response = await fetch('http://localhost:8000/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, username }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Failed to create account.');

  } catch (err: any) {
    console.error('Error during sign up:', err);
    throw new Error('Failed to create account.');
  }
};

export const verifyEmail = async (email: string) => {
  try {
    const response = await fetch('http://localhost:8000/api/auth/check-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Error');
  } catch (err: any) {
  } finally {
  }
};

