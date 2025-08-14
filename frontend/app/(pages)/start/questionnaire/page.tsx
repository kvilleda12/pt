'use client';
import styles from "./questionnaire.module.css";
import { handleSetupSubmit } from '@/app/services/userSetupActions';
import { useFormStatus } from 'react-dom';
import { useActionState } from 'react';
import { useState } from 'react';
import { useBodyPart } from "@/app/utils/BodyPartContext";
import { redirect } from 'next/navigation';
import Link from 'next/link';
import { BodyPartMap } from '@/app/utils/BodyPartTypes'

function SubmitButton() {
    const { pending } = useFormStatus();

    return (
        <button
            type="submit"
            className={styles.continueButton}
            disabled={pending}
        >
            {pending ? 'Saving...' : 'Continue'}
        </button>
    );
}

function NavigationButtons() {
    return (
        <div className={styles.navigationContainer}>
            <Link href='/start' className={styles.goBackButton}>← Go Back</Link>
            <Link href='/logout' className={styles.logoutButton}>Logout</Link>
        </div>
    );
}

export default function QuestionnairePage() {
    const [errorMessage, dispatch] = useActionState(handleSetupSubmit, undefined);
    const [showPreviousDate, setShowPreviousDate] = useState(false);

    const { selectedBodyPart } = useBodyPart();
    if (!selectedBodyPart) {
        // TODO: Why does loadingTimeout still run without being called? why cant i call it in the JSX?
        console.log('Body part:', selectedBodyPart, ' not tracked, redireccting back...')
        const loadingTimeout = setTimeout(() => {
            redirect('/start');
        }, 2500)
        return (
            <div>
                <h2 className={styles.redirectMessage}>Body part not tracked, redirecting to body part selection...</h2>
                {/* TODO: Add Loading Spinner */}
                {/* {loadingTimeout()} */}
            </div>
        )
    }

    // Map the body part to its label to store properly in the database:
    const bodyPartLabel = BodyPartMap[selectedBodyPart];

    return (
        <div className={styles.qPage}>
            <NavigationButtons />

            <div className={styles.formContainer}>
                <h1 className={styles.title}>Tell us about your condition</h1>
                <h2 className={styles.subtitle}>
                    Help us understand your situation better so we can provide personalized recommendations.
                </h2>

                <form action={dispatch} className={styles.questionnaireForm}>
                    {/* Hidden input to pass body part to server action */}
                    <input
                        type="hidden"
                        name="body_part"
                        value={bodyPartLabel || ''}
                    />

                    {/* Previous Problem Section */}
                    <div className={styles.questionSection}>
                        <h2 className={styles.sectionTitle}>Previous Experience</h2>

                        <div className={styles.questionGroup}>
                            <label className={styles.questionLabel}>
                                Have you had this problem before?
                            </label>
                            <div className={styles.radioGroup}>
                                <label className={styles.radioOption}>
                                    <input
                                        type="radio"
                                        name="had_this_problem_before"
                                        value="true"
                                        onChange={(e) => setShowPreviousDate(e.target.checked)}
                                        required
                                    />
                                    <span className={styles.radioLabel}>Yes</span>
                                </label>
                                <label className={styles.radioOption}>
                                    <input
                                        type="radio"
                                        name="had_this_problem_before"
                                        value="false"
                                        onChange={(e) => setShowPreviousDate(!e.target.checked)}
                                        required
                                    />
                                    <span className={styles.radioLabel}>No</span>
                                </label>
                            </div>
                        </div>

                        {showPreviousDate && (
                            <>
                                <div className={styles.questionGroup}>
                                    <label className={styles.questionLabel} htmlFor="previous_problem_date">
                                        When did you last experience this problem? (Estimate)
                                    </label>
                                    <input
                                        type="date"
                                        id="previous_problem_date"
                                        name="previous_problem_date"
                                        className={styles.dateInput}
                                        max={new Date().toISOString().split('T')[0]}
                                    />
                                </div>

                                <div className={styles.questionGroup}>
                                    <label className={styles.questionLabel} htmlFor="what_helped_before">
                                        What helped resolve it before? (If anything)
                                    </label>
                                    <textarea
                                        id="what_helped_before"
                                        name="what_helped_before"
                                        className={styles.textArea}
                                        placeholder="Describe any treatments, exercises, or remedies that helped..."
                                        rows={4}
                                    />
                                </div>
                            </>
                        )}
                    </div>

                    {/* Physical Therapy Section */}
                    <div className={styles.questionSection}>
                        <h2 className={styles.sectionTitle}>Treatment History</h2>

                        <div className={styles.questionGroup}>
                            <label className={styles.questionLabel}>
                                Have you had physical therapy before?
                            </label>
                            <div className={styles.radioGroup}>
                                <label className={styles.radioOption}>
                                    <input
                                        type="radio"
                                        name="had_physical_therapy_before"
                                        value="true"
                                        required
                                    />
                                    <span className={styles.radioLabel}>Yes</span>
                                </label>
                                <label className={styles.radioOption}>
                                    <input
                                        type="radio"
                                        name="had_physical_therapy_before"
                                        value="false"
                                        required
                                    />
                                    <span className={styles.radioLabel}>No</span>
                                </label>
                            </div>
                        </div>

                        <div className={styles.questionGroup}>
                            <label className={styles.questionLabel} htmlFor="previous_unrelated_problem">
                                Do you have any other ongoing health conditions?
                            </label>
                            <textarea
                                id="previous_unrelated_problem"
                                name="previous_unrelated_problem"
                                className={styles.textArea}
                                placeholder="Describe any other health conditions, past injuries, or relevant medical history..."
                                rows={4}
                            />
                            <small className={styles.helpText}>
                                This helps us avoid exercises that might aggravate other conditions.
                            </small>
                        </div>
                    </div>

                    {/* Additional Pain & Goal Questions */}
                    <div className={styles.questionSection}>
                        <h2 className={styles.sectionTitle}>Your Perspective</h2>

                        <div className={styles.questionGroup}>
                            <label className={styles.questionLabel} htmlFor="opinion_cause">
                                What in your opinion caused this problem?
                            </label>
                            <textarea
                                id="opinion_cause"
                                name="opinion_cause"
                                className={styles.textArea}
                                placeholder="Describe what you think might have caused this issue..."
                                rows={3}
                            />
                        </div>

                        <div className={styles.questionGroup}>
                            <label className={styles.questionLabel} htmlFor="pain_worse">
                                What makes your pain worse?
                            </label>
                            <textarea
                                id="pain_worse"
                                name="pain_worse"
                                className={styles.textArea}
                                placeholder="List activities, movements, or situations that make the pain worse..."
                                rows={3}
                            />
                        </div>

                        <div className={styles.questionGroup}>
                            <label className={styles.questionLabel} htmlFor="pain_better">
                                What makes your pain better?
                            </label>
                            <textarea
                                id="pain_better"
                                name="pain_better"
                                className={styles.textArea}
                                placeholder="List anything that relieves the pain, even temporarily..."
                                rows={3}
                            />
                        </div>

                        <div className={styles.questionGroup}>
                            <label className={styles.questionLabel} htmlFor="goal_for_pt">
                                What is your goal for physical therapy?
                            </label>
                            <textarea
                                id="goal_for_pt"
                                name="goal_for_pt"
                                className={styles.textArea}
                                placeholder="Describe what you hope to achieve by the end of therapy..."
                                rows={3}
                            />
                        </div>
                    </div>

                    {errorMessage && (
                        <div className={styles.errorMessage}>{errorMessage}</div>
                    )}

                    <div className={styles.buttonContainer}>
                        <SubmitButton />
                    </div>
                </form>
            </div>
        </div>
    );
}
