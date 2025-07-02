import styles from "../page.module.css";

// About Page
export default function About() {
  return (
    <div className={styles.aboutPage}>
      <h2 className={styles.title}>About PTI</h2>
      <p className={styles.aboutDescription}>
        PTI is an AI-powered assistant designed to support you through every step of your physical therapy journey. After you describe the area of your body you're experiencing issues with, PTI suggests targeted exercises, guides you through them, and analyzes your form to ensure you're performing them correctly. It also tracks a variety of physical data that can be used to drive insights — potentially revolutionizing how specific areas of the body are treated across the field.      </p>
    </div>
  );
}