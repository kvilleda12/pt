'use server';
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

// Server communication function
export async function handleBodyPartClick(bodyPart: string) {
    const session = await auth()
    if (!session?.user?.email) {
        redirect('/login')
    }

    console.log('Server action sending body part click to server:', bodyPart);
    console.log('User session:', session);
    try {
        await fetch(`${process.env.API_URL}/set-body-part`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                bodyPart,
                email: session.user.email,
            })
        });
    } catch (error) {
        console.error('Failed to track body part click:', error);
    }
}
