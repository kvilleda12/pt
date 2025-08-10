// Credit reactbits.dev
// import ShinyText from "@/app/ui-components/reactbits/ShinyText.js";
import styles from './ui.module.css';

const ShinyText = ({ text, disabled = false, speed = 5, className = '' }) => {
  const animationDuration = `${speed}s`;

  return (
    <div
      className={`${styles.shinyText} ${disabled ? 'disabled' : ''} ${className}`}
      style={{ animationDuration }}
    >
      {text}
    </div>
  );
};

export default ShinyText;
