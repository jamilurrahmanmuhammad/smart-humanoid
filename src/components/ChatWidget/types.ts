/**
 * Type definitions for ChatWidget component.
 *
 * FR References: FR-003 (query types), FR-004 (citations), FR-012 (sessions)
 */

/** Learner persona types per Constitution Section XIII */
export type PersonaType = 'Explorer' | 'Builder' | 'Engineer' | 'Default';

/** Query scope types */
export type QueryType = 'global' | 'page' | 'selection';

/** Message role */
export type MessageRole = 'user' | 'assistant';

/** Citation from textbook source */
export interface Citation {
  chapter: number;
  section: string;
  heading: string;
  quote: string;
  link: string;
  relevance_score?: number;
}

/** Chat message in conversation history */
export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  citations?: Citation[];
  hasSafetyDisclaimer?: boolean;
  timestamp: Date;
  isStreaming?: boolean;
}

/** WebSocket client -> server message */
export interface ClientMessage {
  type: 'message' | 'ping' | 'context';
  data?: {
    content?: string;
    query_type?: QueryType;
    current_chapter?: number | null;
    selected_text?: string | null;
    current_page?: string;
    /** FR-031: Page content for vague contextual queries */
    page_content?: string;
  };
}

/** WebSocket server -> client message types */
export type ServerMessageType =
  | 'welcome'
  | 'content'
  | 'citation'
  | 'safety'
  | 'done'
  | 'error'
  | 'pong'
  | 'message_start';

/** WebSocket server -> client message */
export interface ServerMessage {
  type: ServerMessageType;
  session_id?: string;
  message_id?: string;
  content?: string;
  citation?: Citation;
  data?: {
    session_id?: string;
    persona?: PersonaType;
    connected_at?: string;
    chunk?: string;
    message_id?: string;
    chapter?: number;
    section?: string;
    heading?: string;
    quote?: string;
    link?: string;
    relevance_score?: number;
    message?: string;
    citation_count?: number;
    has_safety_disclaimer?: boolean;
    latency_ms?: number;
    code?: string;
    recoverable?: boolean;
    timestamp?: string;
  };
}

/** Connection state for WebSocket */
export type ConnectionState = 'connecting' | 'connected' | 'disconnected' | 'error';

/** ChatWidget props */
export interface ChatWidgetProps {
  /** Initial persona (can be changed by user) */
  defaultPersona?: PersonaType;
  /** Current chapter context from Docusaurus page */
  currentChapter?: number;
  /** Current page path */
  currentPage?: string;
  /** FR-031: Page content for vague contextual queries (max 8000 chars) */
  pageContent?: string;
  /** API base URL */
  apiBaseUrl?: string;
  /** Controlled open state from parent */
  isOpen?: boolean;
  /** Callback when widget opens/closes */
  onToggle?: (isOpen: boolean) => void;
}

/** Chat context for managing global state */
export interface ChatContextValue {
  messages: ChatMessage[];
  isOpen: boolean;
  isLoading: boolean;
  connectionState: ConnectionState;
  persona: PersonaType;
  sessionId: string | null;
  sendMessage: (content: string, options?: SendMessageOptions) => void;
  setPersona: (persona: PersonaType) => void;
  toggleWidget: () => void;
  clearMessages: () => void;
}

/** Options for sending a message */
export interface SendMessageOptions {
  queryType?: QueryType;
  selectedText?: string;
  currentChapter?: number;
}
