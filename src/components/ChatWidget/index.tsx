/**
 * ChatWidget - Floating chat panel for RAG-powered Q&A.
 *
 * FR References:
 * - FR-001: RAG-based Q&A with citations
 * - FR-002: Keyboard accessible with ARIA labels
 * - FR-003: Query types (global, page, selection)
 * - FR-012: Session context maintained
 * - NFR-001: Streaming responses
 * - NFR-002: WCAG 2.1 AA compliance
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import type { ChatMessage, ChatWidgetProps, Citation, PersonaType } from './types';
import { useChat } from './useChat';
import styles from './styles.module.css';

/** Persona display names */
const PERSONA_LABELS: Record<PersonaType, string> = {
  Explorer: 'Explorer',
  Builder: 'Builder',
  Engineer: 'Engineer',
  Default: 'Default',
};

/** Chat icon SVG */
function ChatIcon(): React.ReactElement {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  );
}

/** Close icon SVG */
function CloseIcon(): React.ReactElement {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

/** Send icon SVG */
function SendIcon(): React.ReactElement {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <line x1="22" y1="2" x2="11" y2="13" />
      <polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
  );
}

/** Robot icon SVG for empty state */
function RobotIcon(): React.ReactElement {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <rect x="3" y="8" width="18" height="12" rx="2" />
      <circle cx="9" cy="14" r="1.5" />
      <circle cx="15" cy="14" r="1.5" />
      <path d="M12 2v4" />
      <circle cx="12" cy="2" r="1" />
      <path d="M9 18h6" />
    </svg>
  );
}

/** Citation component */
function CitationItem({ citation }: { citation: Citation }): React.ReactElement {
  return (
    <a
      href={citation.link}
      className={styles.citation}
      target="_self"
      rel="noopener"
      aria-label={`Citation from Chapter ${citation.chapter}: ${citation.heading}`}
    >
      <div className={styles.citationHeader}>
        <span className={styles.citationChapter}>Ch. {citation.chapter}</span>
        <span className={styles.citationHeading}>{citation.heading}</span>
      </div>
      <p className={styles.citationQuote}>"{citation.quote}"</p>
    </a>
  );
}

/** Message component */
function MessageBubble({ message }: { message: ChatMessage }): React.ReactElement {
  const isUser = message.role === 'user';

  return (
    <div
      className={`${styles.message} ${isUser ? styles.messageUser : styles.messageAssistant}`}
      role="article"
      aria-label={`${isUser ? 'Your' : 'Assistant'} message`}
    >
      <div
        className={`${styles.messageContent} ${message.isStreaming ? styles.messageStreaming : ''}`}
      >
        {message.content || (message.isStreaming && <LoadingDots />)}
      </div>

      {message.hasSafetyDisclaimer && (
        <div className={styles.safetyDisclaimer} role="alert">
          This involves physical hardware. Always consult official equipment manuals.
        </div>
      )}

      {message.citations && message.citations.length > 0 && (
        <div className={styles.citations}>
          <div className={styles.citationsLabel}>Sources</div>
          {message.citations.map((citation, index) => (
            <CitationItem key={`${citation.chapter}-${citation.section}-${index}`} citation={citation} />
          ))}
        </div>
      )}
    </div>
  );
}

/** Loading dots animation */
function LoadingDots(): React.ReactElement {
  return (
    <div className={styles.loadingDots} aria-label="Loading response">
      <span />
      <span />
      <span />
    </div>
  );
}

/** Main ChatWidget component */
export default function ChatWidget({
  defaultPersona = 'Default',
  currentChapter,
  currentPage,
  pageContent,
  apiBaseUrl = 'ws://localhost:8000',
  isOpen: controlledIsOpen,
  onToggle,
}: ChatWidgetProps): React.ReactElement {
  // Support both controlled and uncontrolled modes
  const [internalIsOpen, setInternalIsOpen] = useState(false);
  const isControlled = controlledIsOpen !== undefined;
  const isOpen = isControlled ? controlledIsOpen : internalIsOpen;

  const setIsOpen = (newState: boolean) => {
    if (!isControlled) {
      setInternalIsOpen(newState);
    }
    onToggle?.(newState);
  };

  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const {
    messages,
    isLoading,
    connectionState,
    persona,
    sendMessage,
    setPersona,
    connect,
    disconnect,
  } = useChat({
    apiBaseUrl,
    defaultPersona,
    currentChapter,
    currentPage,
    pageContent,
  });

  /** Toggle panel open/close */
  const togglePanel = useCallback(() => {
    const newState = !isOpen;
    setIsOpen(newState);

    if (newState && connectionState === 'disconnected') {
      connect();
    }
  }, [isOpen, connectionState, connect, setIsOpen]);

  /** Handle close with disconnect */
  const handleClose = useCallback(() => {
    setIsOpen(false);
    disconnect();
  }, [disconnect, setIsOpen]);

  /** Handle send message */
  const handleSend = useCallback(() => {
    if (inputValue.trim() && !isLoading) {
      sendMessage(inputValue);
      setInputValue('');
    }
  }, [inputValue, isLoading, sendMessage]);

  /** Handle keyboard events */
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    },
    [handleSend]
  );

  /** Auto-connect when panel opens (for controlled mode) */
  useEffect(() => {
    if (isOpen && connectionState === 'disconnected') {
      connect();
    }
  }, [isOpen, connectionState, connect]);

  /** Listen for selection query events from SelectionTrigger */
  useEffect(() => {
    const handleSelectionQuery = (e: CustomEvent<{
      selectedText: string;
      question: string;
      queryType: 'selection';
    }>) => {
      const { selectedText, question } = e.detail;

      // Send the selection query after connection is established
      // The panel should already be open (Root.tsx opens it before dispatching the event)
      // Give time for connection to be established
      setTimeout(() => {
        sendMessage(question, { selectedText, queryType: 'selection' });
      }, connectionState === 'connected' ? 100 : 1000);
    };

    window.addEventListener('chat:selection-query', handleSelectionQuery as EventListener);
    return () => {
      window.removeEventListener('chat:selection-query', handleSelectionQuery as EventListener);
    };
  }, [connectionState, sendMessage]);

  /** Auto-scroll to bottom when messages change */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  /** Focus input when panel opens */
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  /** Handle Escape key to close panel */
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        handleClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, handleClose]);

  return (
    <>
      {/* Toggle Button */}
      <button
        className={`${styles.toggleButton} ${isOpen ? styles.toggleButtonOpen : ''}`}
        onClick={togglePanel}
        aria-label={isOpen ? 'Close chat' : 'Open chat assistant'}
        aria-expanded={isOpen}
        aria-controls="chat-panel"
        type="button"
      >
        {isOpen ? <CloseIcon /> : <ChatIcon />}
      </button>

      {/* Chat Panel */}
      <div
        id="chat-panel"
        className={`${styles.chatPanel} ${!isOpen ? styles.chatPanelHidden : ''}`}
        role="dialog"
        aria-modal="true"
        aria-label="Chat assistant"
      >
        {/* Header */}
        <header className={styles.header}>
          <div className={styles.headerTitle}>
            <RobotIcon />
            <span>Smart Humanoid Assistant</span>
          </div>
          <div className={styles.headerActions}>
            <div
              className={styles.connectionIndicator}
              data-state={connectionState}
              title={`Connection: ${connectionState}`}
              aria-label={`Connection status: ${connectionState}`}
            />
            <button
              className={styles.closeButton}
              onClick={handleClose}
              aria-label="Close chat"
              type="button"
            >
              <CloseIcon />
            </button>
          </div>
        </header>

        {/* Persona Selector */}
        <div className={styles.personaSelector} role="radiogroup" aria-label="Select your learning persona">
          {(Object.keys(PERSONA_LABELS) as PersonaType[]).map((p) => (
            <button
              key={p}
              className={`${styles.personaButton} ${persona === p ? styles.personaButtonActive : ''}`}
              onClick={() => setPersona(p)}
              role="radio"
              aria-checked={persona === p}
              type="button"
            >
              {PERSONA_LABELS[p]}
            </button>
          ))}
        </div>

        {/* Messages Area */}
        <div
          className={styles.messagesArea}
          role="log"
          aria-live="polite"
          aria-label="Chat messages"
        >
          {messages.length === 0 ? (
            <div className={styles.emptyState}>
              <RobotIcon />
              <p>
                Ask me anything about ROS 2, robotics, or physical AI from the textbook!
              </p>
            </div>
          ) : (
            messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className={styles.inputArea}>
          <div className={styles.inputWrapper}>
            <textarea
              ref={inputRef}
              className={styles.input}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question..."
              aria-label="Type your question"
              rows={1}
              disabled={connectionState !== 'connected'}
            />
          </div>
          <button
            className={styles.sendButton}
            onClick={handleSend}
            disabled={!inputValue.trim() || isLoading || connectionState !== 'connected'}
            aria-label="Send message"
            type="button"
          >
            <SendIcon />
          </button>
        </div>
      </div>

      {/* Screen reader announcements */}
      <div className={styles.srOnly} aria-live="assertive">
        {isLoading && 'Assistant is typing...'}
      </div>
    </>
  );
}

// Also export as named export for flexibility
export { ChatWidget };
