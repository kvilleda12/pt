"use client";

import styles from "../page.module.css";
import Image from "next/image";
import {useInView} from 'react-intersection-observer';


export default function About() {
  //creating animation for the title slide
  const titleText = "Changing the Way Physical Therapy is done";
  const letters = titleText.split('');

  const {ref, inView} = useInView({
    triggerOnce:true, threshold:0.1
  })
  return (
    <div className={styles.aboutPage}>
      {/* Mapped letters. Create array each letter then show them one by one.  */}
      <h2 className={styles.aboutTitle}>
        {letters.map((char, index) => (
          <span
            key={index}
            className={styles.animatedLetter}
            style={{ animationDelay: `${index * 40}ms` }}
          >
            {char === ' ' ? '\u00A0' : char}
          </span>
        ))}
      </h2>

      < div className = { styles.aboutImage} >
        <Image src = "/about_page_img.png" alt = "AI Assistant in use on computer" width = {500} height ={500} className = {styles.aboutImage} />
        <p className={styles.aboutCompanyDescription}>
          PTI is an AI-powered assistant designed to support you through every step of your physical therapy journey. After you describe the area of your body you're experiencing issues with, PTI suggests targeted exercises, guides you through them, and analyzes your form to ensure you're performing them correctly. It also tracks a variety of physical data that can be used to drive insights — potentially revolutionizing how specific areas of the body are treated across the field.
        </p>
      </div>



      <h2 className={styles.sectionHeader}>Meet The Founders</h2>
      <div className={styles.foundersContainer} ref = {ref}>
      <div className={`${styles.founderProfile} ${inView ? styles.fadeUp : ''} ${styles.profileLeft}`}>
  <a 
    href="https://www.linkedin.com/in/adam-soliman-71256b291/" 
    target="_blank" 
    rel="noopener noreferrer"
    >
    <Image src="/adam.jpg" alt="Adam Soliman" width={150} height={150} className={styles.founderImage}/>
    <p className={styles.founderName}>Adam Soliman</p>
    <p className={styles.founderTitle}>Frontend Lead</p>
    <p className={styles.founderDescription}>[]</p>
    </a>
  </div>

  <div className={`${styles.founderProfile} ${inView ? styles.fadeUp : ''} ${styles.profileMiddle}`}>
  <a 
    href="https://www.linkedin.com/in/kvilledadeleon/" 
    target="_blank" 
    rel="noopener noreferrer"
    >
    <Image src="/kevin.jpeg" alt="Kevin Villeda de Leon" width={150} height={150} className={styles.founderImage}/>
    <p className={styles.founderName}>Kevin Villeda de Leon</p>
    <p className={styles.founderTitle}>CEO/ Backend Lead</p>
    <p className={styles.founderDescription}>[]</p>
    </a>
  </div>

  <div className={`${styles.founderProfile} ${inView ? styles.fadeUp : ''} ${styles.profileRight}`}>
  <a 
    href="https://www.linkedin.com/in/shinthomas/" 
    target="_blank" 
    rel="noopener noreferrer"
    >
    <Image src="/Thomas_img.png" alt="Thomas Shin" width={150} height={150} className={styles.founderImage}/>
    <p className={styles.founderName}>Thomas Shin</p>
    <p className={styles.founderTitle}>Backend Engineer</p>
    <p className={styles.founderDescription}>[]</p>
    </a>
  </div>
    </div>
    </div>

  );
}