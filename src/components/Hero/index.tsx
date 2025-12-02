import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

/**
 * Hero Component - User Story 1
 *
 * The primary landing section for the Smart Humanoid platform.
 * Displays platform identity and directs visitors to content.
 *
 * Requirements addressed:
 * - FR-017: Platform label "SMART HUMANOID" with accent color
 * - FR-018: Headline with "understand" highlighted in cyan
 * - FR-019: Subheading describing platform purpose
 * - FR-020: Two CTA buttons: "Get Started" and "Browse Content"
 * - FR-021: Right-side diagram placeholder
 * - FR-022: 50-60% viewport height on desktop
 * - FR-023: Flex layout with left text and right diagram
 */
export default function Hero(): React.ReactElement {
  return (
    <section className={styles.hero} aria-label="Platform introduction">
      <div className={styles.heroContent}>
        {/* Left side: Text content */}
        <div className={styles.heroText}>
          {/* Platform label */}
          <span className={styles.platformLabel}>SMART HUMANOID</span>

          {/* Main headline with highlighted word */}
          <h1 className={styles.headline}>
            Build robots that{' '}
            <span className={styles.highlight}>understand</span>
            {' '}the physical world
          </h1>

          {/* Subheading */}
          <p className={styles.subheading}>
            An open educational platform for learning physical AI and humanoid robotics.
            From fundamentals to advanced concepts, build your understanding through
            hands-on projects and expert-curated content.
          </p>

          {/* CTA Buttons */}
          <div className={styles.buttons}>
            <Link
              className={styles.buttonPrimary}
              to="/docs/intro"
              aria-label="Get started with the documentation"
            >
              Get Started
            </Link>
            <Link
              className={styles.buttonSecondary}
              to="/docs/intro"
            >
              Browse Content
            </Link>
          </div>
        </div>

        {/* Right side: Diagram placeholder */}
        <div
          className={styles.diagramPlaceholder}
          aria-label="Diagram placeholder for robot visualization"
          role="img"
        >
          <div className={styles.placeholderContent}>
            <span className={styles.placeholderIcon}>🤖</span>
            <span className={styles.placeholderText}>Robot Diagram</span>
            <span className={styles.placeholderSubtext}>Coming Soon</span>
          </div>
        </div>
      </div>
    </section>
  );
}
