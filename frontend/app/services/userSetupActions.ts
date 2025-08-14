'use server';
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

// Server communication function
export async function handleSetupSubmit(
    prevState: string | undefined,
    formData: FormData
) {
    const session = await auth()
    if (!session?.user?.email) {
        redirect('/login')
    }

    console.log('User session:', session);
    console.log('form data:', formData);

    try {
        const questionnaireData = {
            body_part: formData.get('body_part') as string,
            had_this_problem_before: formData.get('had_this_problem_before') === 'true',
            previous_problem_date: formData.get('previous_problem_date') || null,
            what_helped_before: formData.get('what_helped_before') || null,
            had_physical_therapy_before: formData.get('had_physical_therapy_before') === 'true',
            previous_unrelated_problem: formData.get('previous_unrelated_problem') || null,
            opinion_cause: (formData.get('opinion_cause') as string).trim(),
            pain_worse: (formData.get('pain_worse') as string).trim(),
            pain_better: (formData.get('pain_better') as string).trim(),
            goal_for_pt: (formData.get('goal_for_pt') as string).trim(),
        };

        const response = await fetch(`${process.env.API_URL}/set-up-user`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: session.user.email,
                ...questionnaireData,
            })
        });

        if (!response.ok) {
            throw new Error('Failed to save questionnaire');
        }

    } catch (error) {
        console.error('Failed to send questionnaire to the server.', error);
        return 'Failed to save your responses. Please try again.'
    }
    
    redirect('/dashboard'); // Redirect to next step
}
