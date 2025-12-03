/**
 * Root theme component - Wraps entire Docusaurus site.
 *
 * Integrates ChatWidget and SelectionTrigger globally.
 *
 * FR References:
 * - FR-001: RAG-based Q&A
 * - FR-018: Selection-scoped queries
 * - FR-012: Session context from current page
 */

import React, { useCallback, useEffect, useState } from 'react';
import { useLocation } from '@docusaurus/router';
import ChatWidget from '@site/src/components/ChatWidget';
import SelectionTrigger from '@site/src/components/SelectionTrigger';
import type { PersonaType } from '@site/src/components/ChatWidget/types';

/** Maximum page content length per FR-034 */
const MAX_PAGE_CONTENT_LENGTH = 8000;

/** Props passed by Docusaurus */
interface RootProps {
  children: React.ReactNode;
}

/** Extract chapter number from URL path */
function extractChapterFromPath(pathname: string): number | undefined {
  // Match patterns like /docs/module-1/chapter-2-... or /docs/chapter-3-...
  const chapterMatch = pathname.match(/chapter-(\d+)/i);
  if (chapterMatch) {
    return parseInt(chapterMatch[1], 10);
  }
  return undefined;
}

/** Extract persona from URL path (explorer, builder, engineer) */
function extractPersonaFromPath(pathname: string): PersonaType | undefined {
  const lowerPath = pathname.toLowerCase();
  if (lowerPath.includes('-explorer')) return 'Explorer';
  if (lowerPath.includes('-builder')) return 'Builder';
  if (lowerPath.includes('-engineer')) return 'Engineer';
  return undefined;
}

/**
 * Extract page content from the <article> element (Docusaurus main content area).
 * FR-031: Frontend extracts and sends page content via WebSocket.
 * FR-034: Limits content to 8000 characters.
 */
function extractPageContent(): string | undefined {
  if (typeof document === 'undefined') return undefined;

  // Docusaurus uses <article> for main content
  const article = document.querySelector('article');
  if (!article) return undefined;

  // Get text content, preserving some structure
  const textContent = article.innerText || article.textContent || '';

  // Clean up excessive whitespace while preserving paragraph breaks
  const cleaned = textContent
    .replace(/\n{3,}/g, '\n\n')  // Collapse multiple newlines to double
    .replace(/[ \t]+/g, ' ')     // Collapse horizontal whitespace
    .trim();

  // Truncate to max length
  if (cleaned.length > MAX_PAGE_CONTENT_LENGTH) {
    return cleaned.slice(0, MAX_PAGE_CONTENT_LENGTH);
  }

  return cleaned || undefined;
}

/** Root component that wraps the entire site */
export default function Root({ children }: RootProps): React.ReactElement {
  const location = useLocation();
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [pageContent, setPageContent] = useState<string | undefined>(undefined);

  // Extract context from current page URL
  const currentChapter = extractChapterFromPath(location.pathname);
  const detectedPersona = extractPersonaFromPath(location.pathname);

  // FR-031: Extract page content when location changes
  useEffect(() => {
    // Small delay to ensure DOM is fully rendered after navigation
    const timeoutId = setTimeout(() => {
      const content = extractPageContent();
      setPageContent(content);
    }, 100);

    return () => clearTimeout(timeoutId);
  }, [location.pathname]);

  // Determine API base URL from environment or default
  const apiBaseUrl =
    typeof window !== 'undefined' && (window as unknown as { CHAT_API_URL?: string }).CHAT_API_URL
      ? (window as unknown as { CHAT_API_URL: string }).CHAT_API_URL
      : 'ws://localhost:8000';

  /** Handle selection trigger - open chat with selected text */
  const handleAskAboutSelection = useCallback(
    (selectedText: string, question?: string) => {
      // Always open the chat widget (safe to call even if already open)
      setIsChatOpen(true);

      // Send the selection query after a brief delay to allow widget to connect
      setTimeout(() => {
        const content = question || `Please explain: "${selectedText.slice(0, 200)}${selectedText.length > 200 ? '...' : ''}"`;

        // Dispatch custom event that ChatWidget listens to
        const event = new CustomEvent('chat:selection-query', {
          detail: {
            selectedText,
            question: content,
            queryType: 'selection' as const,
          },
        });
        window.dispatchEvent(event);
      }, 500);
    },
    [] // No dependencies - setIsChatOpen is stable from useState
  );

  /** Handle chat toggle */
  const handleChatToggle = useCallback((isOpen: boolean) => {
    setIsChatOpen(isOpen);
  }, []);

  return (
    <>
      {children}

      {/* Selection Trigger - shows when text is selected */}
      <SelectionTrigger
        onAskAboutSelection={handleAskAboutSelection}
        maxLength={2000}
        showInput={false}
        disabled={false}
      />

      {/* Chat Widget - floating button and panel */}
      <ChatWidget
        defaultPersona={detectedPersona || 'Default'}
        currentChapter={currentChapter}
        currentPage={location.pathname}
        pageContent={pageContent}
        apiBaseUrl={apiBaseUrl}
        isOpen={isChatOpen}
        onToggle={handleChatToggle}
      />
    </>
  );
}
