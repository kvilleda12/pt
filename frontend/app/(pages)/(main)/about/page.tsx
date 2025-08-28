"use client";
import styles from "../page.module.css";
import Image from "next/image";
import Link from "next/link";
import { useInView } from 'react-intersection-observer';

export default function About() {
  //creating animation for the title slide
  const titleText = "The Future of Physical Therapy";
  const letters = titleText.split('');

  const { ref, inView } = useInView({
    triggerOnce: true, threshold: 0.1
  });

  const founders = [
    {
      href: "https://www.linkedin.com/in/adam-soliman-71256b291/",
      imgSrc: "/adam.jpg",
      imgAlt: "Adam Soliman",
      name: "Adam Soliman",
      title: "CTO | Frontend Lead",
      description: "Adam is a computer science student at NYU experienced in building user-friendly applications. He leads the frontend development of PTI, ensuring a seamless user experience. From setting technical direction to writing production-level code, Adam is hands-on at every level, bringing innovation and attention to detail to the heart of everything we do.",
      profileClass: styles.profileLeft,
    },
    {
      href: "https://www.linkedin.com/in/kvilledadeleon/",
      imgSrc: "/kevin.jpeg",
      imgAlt: "Kevin Villeda de Leon",
      name: "Kevin Villeda de Leon",
      title: "CEO | Backend Lead",
      description: "Kevin leads the vision and strategy behind our company while architecting the systems that power it. As CEO and Backend Lead, he combines big-picture thinking with deep technical expertise to build reliable, scalable infrastructure that drives real impact.",
      profileClass: styles.profileMiddle,
    },
    {
      href: "https://www.linkedin.com/in/shinthomas/",
      imgSrc: "/Thomas_img.png",
      imgAlt: "Thomas Shin",
      name: "Thomas Shin",
      title: "Backend Engineer",
      description: "Thomas is a backend engineer focused on building fast, secure, and scalable systems. He brings a sharp attention to detail and a passion for clean architecture, helping turn complex ideas into robust backend solutions.",
      profileClass: styles.profileRight,
    },
  ]

  return (
    <div className={styles.aboutPage}>
      {/* Mapped letters. Create array each letter then show them one by one.  */}
      <h2 className={styles.aboutTitle}>
        {letters.map((char, index) => (
          <span
            key={index}
            className={styles.animatedLetter}
            style={{ animationDelay: `${index * 25}ms` }}
          >
            {char === ' ' ? '\u00A0' : char}
          </span>
        ))}
      </h2>

      < div className={styles.aboutImage} >
        <Image src="/about_page_img.png" alt="AI Assistant in use on computer" width={500} height={500} className={styles.aboutImage} />
        <p className={styles.aboutCompanyDescription}>
          PTI is an AI-powered assistant designed to support you through every step of your physical therapy journey. After you describe the area of your body you're experiencing issues with, PTI suggests targeted exercises, guides you through them, and analyzes your form to ensure you're performing them correctly. It also tracks a variety of physical data that can be used to drive insights — potentially revolutionizing how specific areas of the body are treated across the field.
        </p>
      </div>

      <h2 className={styles.sectionHeader}>Meet The Founders</h2>
      <div className={styles.foundersContainer} ref={ref}>
        {founders.map((founder, index) => (
          <div
            key={index}
            className={`${styles.founderProfile} ${inView ? styles.fadeUp : ''}`}
          >
            <Link
              href={founder.href}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Image src={founder.imgSrc} alt={founder.imgAlt} width={150} height={150} className={styles.founderImage} />
              <p className={styles.founderName}>{founder.name}</p>
              <p className={styles.founderTitle}>{founder.title}</p>
              <p className={styles.founderDescription}>{founder.description}</p>
            </Link>
          </div>
        ))}
      </div>
    </div>

  );
}