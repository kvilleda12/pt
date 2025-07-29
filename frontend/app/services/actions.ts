// app/actions.ts
'use server';
import { signIn } from '@/auth';

// server action to handle authentication through useFormState. Caputres and receives form data.
export async function authenticate(
  prevState: string | undefined,
  formData: FormData
) {
  try {
    await signIn('credentials', formData);
  } catch (error: any) {
    if (error.type === 'CredentialsSignin') {
      return 'Invalid credentials. Please try again.';
    }
    return 'An unexpected error occurred.';
  }
}