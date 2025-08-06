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
        };

        const response = await fetch(`${process.env.API_URL}/set-up-user`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: session.user.email,
                body_part: questionnaireData.body_part,
                had_this_problem_before: questionnaireData.had_this_problem_before,
                previous_problem_date: questionnaireData.previous_problem_date,
                what_helped_before: questionnaireData.what_helped_before,
                had_physical_therapy_before: questionnaireData.had_physical_therapy_before,
                previous_unrelated_problem: questionnaireData.previous_unrelated_problem,
            })
        });

        if (!response.ok) {
            throw new Error('Failed to save questionnaire');
        }

    } catch (error) {
        console.error('Failed to send questionnaire to the server.', error);
        return 'Failed to save your responses. Please try again.'
    }
    
    redirect('/results'); // Redirect to next step

}
