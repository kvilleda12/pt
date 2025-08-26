'use server';

import { auth } from '@/auth';
import { redirect } from 'next/navigation';

function buildApiUrl(path: string) {
  const base = (process.env.NEXT_PUBLIC_API_URL || '').replace(/\/$/, '');
  return `${base}/api${path.startsWith('/') ? path : `/${path}`}`;
}

export async function handleSetupSubmit(
  _prevState: string | undefined,
  formData: FormData
) {
  const session = await auth();
  if (!session?.user?.email) {
    redirect('/login');
  }

  try {
    // Accept either body_part_id (preferred) or body_part (string name)
    const body_part_id_raw = formData.get('body_part_id') as string | null;
    const body_part = (formData.get('body_part') as string | null) || null;

    const had_this_problem_before =
      formData.get('had_this_problem_before') === 'true';

    const previous_problem_date =
      (formData.get('previous_problem_date') as string | null) || null;

    const what_helped_before =
      (formData.get('what_helped_before') as string | null) || null;

    const had_physical_therapy_before =
      formData.get('had_physical_therapy_before') === 'true';

    const previous_unrelated_problem =
      (formData.get('previous_unrelated_problem') as string | null) || null;

    const payload = {
      email: session.user.email!,
      // Prefer numeric id if present; else send name and let API resolve
      body_part_id:
        body_part_id_raw && body_part_id_raw.trim() !== ''
          ? Number(body_part_id_raw)
          : null,
      body_part,
      had_this_problem_before,
      previous_problem_date,      // ISO date string or null
      what_helped_before,
      had_physical_therapy_before,
      previous_unrelated_problem,
    };

    const url = buildApiUrl('/set-up-user');

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const text = await response.text().catch(() => '');
      console.error('Setup API error:', response.status, text);
      return 'Failed to save your responses. Please try again.';
    }
  } catch (err) {
    console.error('Failed to send questionnaire to the server.', err);
    return 'Failed to save your responses. Please try again.';
  }

  redirect('/results');
}

