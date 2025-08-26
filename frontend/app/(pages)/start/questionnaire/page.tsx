'use client';

import styles from "./questionnaire.module.css";
import { handleSetupSubmit } from '@/app/services/userSetupActions';
import { useFormStatus } from 'react-dom';
import { useActionState } from 'react';
import { useState } from 'react';
import { useBodyPart } from "@/app/contexts/BodyPartContext";
import Link from 'next/link';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" className={styles.continueButton} disabled={pending}>
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
  const [showPreviousHelp, setShowPreviousHelp] = useState(false);
  const [showPhysicalTherapy, setShowPhysicalTherapy] = useState(false);

  // Assumes your context provides at least a name; if it also provides an ID, include it.
  const { selectedBodyPart, selectedBodyPartId } = useBodyPart() as {
    selectedBodyPart?: string | null;
    selectedBodyPartId?: number | null;
  };

  return (
    <div className={styles.qPage}>
      <NavigationButtons />

      <div className={styles.formContainer}>
        <h1 className={styles.title}>Tell us about your condition</h1>
        <h2 className={styles.subtitle}>
          Help us understand your situation better so we can provide personalized recommendations.
        </h2>

        <form action={dispatch} className={styles.questionnaireForm}>
          {/* Hidden inputs to pass body part to server action */}
          <input type="hidden" name="body_part" value={selectedBodyPart || ''} />
          <input
            type="hidden"
            name="body_part_id"
            value={selectedBodyPartId != null ? String(selectedBodyPartId) : ''}
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
                    When did you last experience this problem?
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
                    What helped resolve it before?
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
                    onChange={(e) => setShowPhysicalTherapy(e.target.checked)}
                    required
                  />
                  <span className={styles.radioLabel}>Yes</span>
                </label>
                <label className={styles.radioOption}>
                  <input
                    type="radio"
                    name="had_physical_therapy_before"
                    value="false"
                    onChange={(e) => setShowPhysicalTherapy(!e.target.checked)}
                    required
                  />
                  <span className={styles.radioLabel}>No</span>
                </label>
              </div>
            </div>

            <div className={styles.questionGroup}>
              <label className={styles.questionLabel} htmlFor="previous_unrelated_problem">
                Do you have any other ongoing health conditions or injuries we should know about?
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
