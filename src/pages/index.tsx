import type { ReactNode } from 'react';
import Layout from '@theme/Layout';
import Hero from '@site/src/components/Hero';

/**
 * Homepage - User Story 1
 *
 * The main landing page for the Smart Humanoid platform.
 * Uses the Hero component as primary above-the-fold content.
 *
 * Requirements addressed:
 * - FR-024: Hero component as primary above-the-fold content
 * - FR-025: Dark, spacious background with minimal visual clutter
 * - FR-026: No default blog or template elements
 */
export default function Home(): ReactNode {
  return (
    <Layout
      title="Learn Physical AI & Humanoid Robotics"
      description="An open educational platform for learning physical AI and humanoid robotics. Build robots that understand the physical world."
    >
      <main>
        <Hero />
      </main>
    </Layout>
  );
}
