/**
 * Feature Flags Configuration
 *
 * All features are disabled by default.
 * Enable features by setting environment variables.
 *
 * @example
 * ENABLE_AUTH=true npm run start
 */

/**
 * Feature flag definitions
 */
export interface FeatureFlags {
  /** Enable authentication (login/signup) */
  auth: boolean;
  /** Enable LLM integration (AI features) */
  llm: boolean;
  /** Enable vector search (RAG/semantic search) */
  vectorSearch: boolean;
  /** Enable analytics tracking */
  analytics: boolean;
}

/**
 * Parse boolean environment variable
 */
function parseBoolean(value: string | undefined): boolean {
  return value?.toLowerCase() === 'true';
}

/**
 * Get current feature flags from environment
 *
 * Note: In Docusaurus, environment variables must be prefixed
 * and accessed differently in client vs server context.
 * This provides a unified interface.
 */
export function getFeatureFlags(): FeatureFlags {
  // In browser context, use process.env (bundled at build time)
  // These would need to be prefixed with REACT_APP_ or similar
  // for client-side access in a real implementation
  return {
    auth: parseBoolean(process.env.ENABLE_AUTH),
    llm: parseBoolean(process.env.ENABLE_LLM),
    vectorSearch: parseBoolean(process.env.ENABLE_VECTOR_SEARCH),
    analytics: parseBoolean(process.env.ENABLE_ANALYTICS),
  };
}

/**
 * Check if a specific feature is enabled
 */
export function isFeatureEnabled(feature: keyof FeatureFlags): boolean {
  return getFeatureFlags()[feature];
}

/**
 * Default feature flags (all disabled)
 */
export const defaultFeatureFlags: FeatureFlags = {
  auth: false,
  llm: false,
  vectorSearch: false,
  analytics: false,
};
