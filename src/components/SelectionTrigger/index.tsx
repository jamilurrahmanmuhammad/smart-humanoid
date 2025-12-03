/**
 * SelectionTrigger - Popover for selection-scoped queries.
 *
 * Shows a tooltip when text is selected, allowing users to ask about
 * the selected text.
 *
 * FR References:
 * - FR-018: Selection-scoped queries (max 2000 chars)
 * - FR-019: is_selection_scoped indicator
 * - FR-002: Keyboard accessible with ARIA labels
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import styles from './styles.module.css';

/** Selection trigger props */
export interface SelectionTriggerProps {
  /** Called when user wants to ask about selection */
  onAskAboutSelection: (selectedText: string, question?: string) => void;
  /** Maximum selection length (default 2000 per FR-018) */
  maxLength?: number;
  /** Whether to show expanded input mode */
  showInput?: boolean;
  /** Disable the trigger */
  disabled?: boolean;
}

/** Position for the popover */
interface PopoverPosition {
  top: number;
  left: number;
  isBelow: boolean;
}

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

/** Main SelectionTrigger component */
export default function SelectionTrigger({
  onAskAboutSelection,
  maxLength = 2000,
  showInput = false,
  disabled = false,
}: SelectionTriggerProps): React.ReactElement | null {
  const [isVisible, setIsVisible] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [position, setPosition] = useState<PopoverPosition | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [inputValue, setInputValue] = useState('');

  const popoverRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  /** Get position for popover based on selection */
  const getSelectionPosition = useCallback((): PopoverPosition | null => {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) return null;

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();

    if (rect.width === 0 || rect.height === 0) return null;

    const popoverHeight = 50; // Approximate height
    const popoverWidth = 200; // Approximate width
    const spacing = 8;

    // Check if there's room above
    const isBelow = rect.top < popoverHeight + spacing;

    // Calculate position
    let top: number;
    if (isBelow) {
      top = rect.bottom + spacing + window.scrollY;
    } else {
      top = rect.top - popoverHeight - spacing + window.scrollY;
    }

    // Center horizontally on selection
    let left = rect.left + rect.width / 2 - popoverWidth / 2 + window.scrollX;

    // Keep within viewport
    const viewportWidth = window.innerWidth;
    left = Math.max(10, Math.min(left, viewportWidth - popoverWidth - 10));

    return { top, left, isBelow };
  }, []);

  /** Handle text selection */
  const handleSelectionChange = useCallback(() => {
    if (disabled) return;

    const selection = window.getSelection();
    const text = selection?.toString().trim() || '';

    if (text.length > 0 && text.length <= maxLength) {
      setSelectedText(text);
      const pos = getSelectionPosition();
      if (pos) {
        setPosition(pos);
        setIsVisible(true);
      }
    } else {
      // Hide if selection is cleared or too long
      if (text.length === 0) {
        setIsVisible(false);
        setIsExpanded(false);
        setInputValue('');
      }
    }
  }, [disabled, maxLength, getSelectionPosition]);

  /** Handle click outside to dismiss - use mouseup to not interfere with button clicks */
  const handleClickOutside = useCallback((e: MouseEvent) => {
    // Small delay to allow button clicks to register first
    setTimeout(() => {
      if (popoverRef.current && !popoverRef.current.contains(e.target as Node)) {
        // Don't hide if selection is still active
        const selection = window.getSelection();
        if (!selection || selection.toString().trim().length === 0) {
          setIsVisible(false);
          setIsExpanded(false);
          setInputValue('');
        }
      }
    }, 100);
  }, []);

  /** Handle escape key to dismiss */
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape' && isVisible) {
      setIsVisible(false);
      setIsExpanded(false);
      setInputValue('');
      window.getSelection()?.removeAllRanges();
    }
  }, [isVisible]);

  /** Handle ask about selection */
  const handleAsk = useCallback(
    (question?: string) => {
      if (selectedText) {
        onAskAboutSelection(selectedText, question);
        setIsVisible(false);
        setIsExpanded(false);
        setInputValue('');
        window.getSelection()?.removeAllRanges();
      }
    },
    [selectedText, onAskAboutSelection]
  );

  /** Handle expanded mode submit */
  const handleSubmit = useCallback(
    (e?: React.FormEvent) => {
      e?.preventDefault();
      if (inputValue.trim()) {
        handleAsk(inputValue.trim());
      } else {
        handleAsk();
      }
    },
    [inputValue, handleAsk]
  );

  /** Expand to show input */
  const handleExpand = useCallback(() => {
    setIsExpanded(true);
    setTimeout(() => inputRef.current?.focus(), 50);
  }, []);

  /** Listen for selection changes */
  useEffect(() => {
    document.addEventListener('selectionchange', handleSelectionChange);
    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('touchend', handleSelectionChange);
    // Use click instead of mousedown to not interfere with button clicks
    document.addEventListener('click', handleClickOutside);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('touchend', handleSelectionChange);
      document.removeEventListener('click', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleSelectionChange, handleClickOutside, handleKeyDown]);

  // Don't render if disabled or hidden
  if (disabled || !isVisible || !position) {
    return null;
  }

  // Truncate selection text for display
  const displayText =
    selectedText.length > 100 ? `${selectedText.slice(0, 100)}...` : selectedText;

  return (
    <div
      ref={popoverRef}
      className={`${styles.popover} ${position.isBelow ? styles.popoverBelow : ''} ${
        isExpanded ? styles.expandedPopover : ''
      }`}
      style={{
        top: `${position.top}px`,
        left: `${position.left}px`,
      }}
      role="dialog"
      aria-label="Text selection actions"
    >
      {isExpanded && (
        <div className={styles.selectionPreview}>
          <p className={styles.selectionText}>{displayText}</p>
        </div>
      )}

      {showInput && isExpanded ? (
        <form className={styles.expandedInput} onSubmit={handleSubmit}>
          <input
            ref={inputRef}
            type="text"
            className={styles.inputField}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask a question about this..."
            aria-label="Question about selection"
          />
          <button
            type="submit"
            className={styles.sendButton}
            aria-label="Send question"
          >
            <SendIcon />
          </button>
        </form>
      ) : (
        <>
          <button
            className={`${styles.actionButton} ${styles.actionButtonPrimary}`}
            onClick={() => (showInput ? handleExpand() : handleAsk())}
            aria-label="Ask about selected text"
            type="button"
          >
            <ChatIcon />
            <span>Ask about this</span>
          </button>
        </>
      )}

      {/* Screen reader announcement */}
      <div className={styles.srOnly} aria-live="polite">
        {isVisible && `Text selected: ${displayText.slice(0, 50)}. Press Enter to ask about it.`}
      </div>
    </div>
  );
}

// Also export as named export
export { SelectionTrigger };
