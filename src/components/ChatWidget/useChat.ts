/**
 * Custom hook for chat functionality with WebSocket connection.
 *
 * FR References: FR-003 (query types), FR-012 (session context), NFR-001 (streaming)
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import type {
  ChatMessage,
  Citation,
  ClientMessage,
  ConnectionState,
  PersonaType,
  QueryType,
  SendMessageOptions,
  ServerMessage,
} from './types';

/** Generate a simple UUID */
function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

/** Hook options */
interface UseChatOptions {
  apiBaseUrl?: string;
  defaultPersona?: PersonaType;
  currentChapter?: number;
  currentPage?: string;
  /** FR-031: Page content for vague contextual queries */
  pageContent?: string;
  onError?: (error: string) => void;
}

/** Return type for useChat hook */
interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  connectionState: ConnectionState;
  persona: PersonaType;
  sessionId: string | null;
  sendMessage: (content: string, options?: SendMessageOptions) => void;
  setPersona: (persona: PersonaType) => void;
  clearMessages: () => void;
  connect: () => void;
  disconnect: () => void;
}

export function useChat(options: UseChatOptions = {}): UseChatReturn {
  const {
    apiBaseUrl = 'ws://localhost:8000',
    defaultPersona = 'Default',
    currentChapter,
    currentPage,
    pageContent,
    onError,
  } = options;

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [connectionState, setConnectionState] = useState<ConnectionState>('disconnected');
  const [persona, setPersona] = useState<PersonaType>(defaultPersona);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const messageBufferRef = useRef<string>('');
  const currentMessageIdRef = useRef<string | null>(null);
  const citationsRef = useRef<Citation[]>([]);
  const reconnectAttemptRef = useRef(0);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  /** Connect to WebSocket */
  const connect = useCallback(() => {
    // Generate session ID if not exists
    const sid = sessionId || generateId();
    if (!sessionId) {
      setSessionId(sid);
    }

    // Close existing connection
    if (wsRef.current) {
      wsRef.current.close();
    }

    setConnectionState('connecting');

    try {
      // Connect to WebSocket endpoint
      const ws = new WebSocket(`${apiBaseUrl}/chat/ws/${sid}`);
      wsRef.current = ws;

      ws.onopen = () => {
        setConnectionState('connected');
        reconnectAttemptRef.current = 0;
      };

      ws.onmessage = (event) => {
        try {
          const msg: ServerMessage = JSON.parse(event.data);
          handleServerMessage(msg);
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };

      ws.onerror = () => {
        setConnectionState('error');
        onError?.('WebSocket connection error');
      };

      ws.onclose = (event) => {
        setConnectionState('disconnected');
        wsRef.current = null;

        // Attempt reconnection with exponential backoff
        if (event.code !== 1000 && reconnectAttemptRef.current < 5) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttemptRef.current), 30000);
          reconnectAttemptRef.current++;
          reconnectTimeoutRef.current = setTimeout(connect, delay);
        }
      };
    } catch (e) {
      setConnectionState('error');
      onError?.('Failed to create WebSocket connection');
    }
  }, [apiBaseUrl, sessionId, onError]);

  /** Disconnect from WebSocket */
  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    reconnectAttemptRef.current = 5; // Prevent reconnection
    if (wsRef.current) {
      wsRef.current.close(1000, 'User disconnected');
      wsRef.current = null;
    }
    setConnectionState('disconnected');
  }, []);

  /** Handle server messages */
  const handleServerMessage = useCallback((msg: ServerMessage) => {
    switch (msg.type) {
      case 'welcome':
        // Session established
        if (msg.session_id) {
          setSessionId(msg.session_id);
        }
        break;

      case 'message_start':
        // New message starting
        currentMessageIdRef.current = msg.message_id || generateId();
        messageBufferRef.current = '';
        citationsRef.current = [];
        setIsLoading(true);

        // Add placeholder message
        setMessages((prev) => [
          ...prev,
          {
            id: currentMessageIdRef.current!,
            role: 'assistant',
            content: '',
            citations: [],
            timestamp: new Date(),
            isStreaming: true,
          },
        ]);
        break;

      case 'content':
        // Streaming content chunk
        const chunk = msg.content || msg.data?.chunk || '';
        messageBufferRef.current += chunk;

        // Update streaming message
        setMessages((prev) =>
          prev.map((m) =>
            m.id === currentMessageIdRef.current
              ? { ...m, content: messageBufferRef.current }
              : m
          )
        );
        break;

      case 'citation':
        // Add citation
        const citation: Citation = msg.citation || {
          chapter: msg.data?.chapter || 0,
          section: msg.data?.section || '',
          heading: msg.data?.heading || '',
          quote: msg.data?.quote || '',
          link: msg.data?.link || '',
          relevance_score: msg.data?.relevance_score,
        };
        citationsRef.current.push(citation);

        // Update message with citations
        setMessages((prev) =>
          prev.map((m) =>
            m.id === currentMessageIdRef.current
              ? { ...m, citations: [...citationsRef.current] }
              : m
          )
        );
        break;

      case 'safety':
        // Safety disclaimer
        setMessages((prev) =>
          prev.map((m) =>
            m.id === currentMessageIdRef.current
              ? { ...m, hasSafetyDisclaimer: true }
              : m
          )
        );
        break;

      case 'done':
        // Message complete
        setMessages((prev) =>
          prev.map((m) =>
            m.id === currentMessageIdRef.current
              ? { ...m, isStreaming: false }
              : m
          )
        );
        setIsLoading(false);
        currentMessageIdRef.current = null;
        messageBufferRef.current = '';
        citationsRef.current = [];
        break;

      case 'error':
        // Handle error
        const errorMsg = msg.data?.message || 'An error occurred';
        onError?.(errorMsg);
        setIsLoading(false);

        // Update message to show error
        if (currentMessageIdRef.current) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === currentMessageIdRef.current
                ? {
                    ...m,
                    content: `Error: ${errorMsg}`,
                    isStreaming: false,
                  }
                : m
            )
          );
        }
        break;

      case 'pong':
        // Keep-alive response, no action needed
        break;
    }
  }, [onError]);

  /** Send a message */
  const sendMessage = useCallback(
    (content: string, sendOptions?: SendMessageOptions) => {
      if (!content.trim() || !wsRef.current || connectionState !== 'connected') {
        return;
      }

      // Add user message to history
      const userMessage: ChatMessage = {
        id: generateId(),
        role: 'user',
        content: content.trim(),
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMessage]);

      // Determine query type
      let queryType: QueryType = sendOptions?.queryType || 'global';
      if (sendOptions?.selectedText) {
        queryType = 'selection';
      } else if (sendOptions?.currentChapter || currentChapter) {
        queryType = 'page';
      }

      // Send to WebSocket - format matches backend ChatRequest schema
      const clientMessage = {
        message: content.trim(),
        query_type: queryType,
        persona: persona,
        current_chapter: sendOptions?.currentChapter || currentChapter || undefined,
        selected_text: sendOptions?.selectedText || undefined,
      };

      wsRef.current.send(JSON.stringify(clientMessage));
    },
    [connectionState, currentChapter, persona]
  );

  /** Clear message history */
  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  /** Update context when page changes (FR-031: Include page content for vague queries) */
  useEffect(() => {
    if (wsRef.current && connectionState === 'connected' && (currentChapter || currentPage || pageContent)) {
      const contextMessage: ClientMessage = {
        type: 'context',
        data: {
          current_chapter: currentChapter || null,
          current_page: currentPage,
          page_content: pageContent,
        },
      };
      wsRef.current.send(JSON.stringify(contextMessage));
    }
  }, [currentChapter, currentPage, pageContent, connectionState]);

  /** Cleanup on unmount */
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  /** Keep-alive ping every 30 seconds */
  useEffect(() => {
    if (connectionState !== 'connected') return;

    const pingInterval = setInterval(() => {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000);

    return () => clearInterval(pingInterval);
  }, [connectionState]);

  return {
    messages,
    isLoading,
    connectionState,
    persona,
    sessionId,
    sendMessage,
    setPersona,
    clearMessages,
    connect,
    disconnect,
  };
}
