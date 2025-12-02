"""OpenAI Agent configuration and runner.

Configures the agent with tools and system prompts for RAG-based Q&A.
"""

from dataclasses import dataclass
from typing import Any, AsyncIterator, Optional

from openai import OpenAI

from core.config import get_settings
from models.schemas import StreamChunk
from services.rag import RAGPipeline
from services.vector_store import SearchFilters


class AgentError(Exception):
    """Error during agent execution."""

    pass


@dataclass
class AgentTool:
    """Definition of an agent tool.

    Represents a function that the agent can call.
    """

    name: str
    description: str
    parameters: dict[str, Any]


# Global RAG pipeline instance for tool execution
_rag_pipeline: Optional[RAGPipeline] = None


def _get_rag_pipeline() -> RAGPipeline:
    """Get or create the global RAG pipeline instance."""
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline


async def search_book_content(
    query: str,
    chapter_id: Optional[int] = None,
    persona: Optional[str] = None,
) -> str:
    """Search textbook content for relevant information.

    Args:
        query: Search query string.
        chapter_id: Optional chapter ID to scope search.
        persona: Optional persona filter.

    Returns:
        Retrieved context string from the textbook.
    """
    pipeline = _get_rag_pipeline()

    filters = None
    if chapter_id or persona:
        filters = SearchFilters(chapter_id=chapter_id, persona=persona)

    result = await pipeline.query(query, filters=filters)

    if result.is_out_of_scope:
        return "I don't have information about this topic in the textbook."

    return result.context


def get_agent_tools() -> list[AgentTool]:
    """Get the list of tools available to the agent.

    Returns:
        List of AgentTool definitions.
    """
    return [
        AgentTool(
            name="search_book_content",
            description=(
                "Search the ROS 2 textbook for information about a topic. "
                "Use this to find relevant content to answer user questions."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for finding relevant content",
                    },
                    "chapter_id": {
                        "type": "integer",
                        "description": "Optional chapter ID to scope the search",
                    },
                    "persona": {
                        "type": "string",
                        "enum": ["Explorer", "Builder", "Engineer", "Default"],
                        "description": "Optional persona to filter content",
                    },
                },
                "required": ["query"],
            },
        ),
    ]


def _tools_to_openai_format(tools: list[AgentTool]) -> list[dict[str, Any]]:
    """Convert AgentTool list to OpenAI API format.

    Args:
        tools: List of AgentTool definitions.

    Returns:
        List of tool dicts in OpenAI format.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            },
        }
        for tool in tools
    ]


SYSTEM_PROMPT = """You are a helpful AI assistant for the "Smart Humanoid Robotics"
online textbook. Your role is to help students learn about ROS 2, robotics, and
physical AI.

Guidelines:
- Always use the search_book_content tool to find relevant information before answering
- Provide accurate information based on the textbook content
- Include citations when referencing specific sections
- If a question is outside the scope of the textbook, politely explain that
- Be encouraging and supportive in helping students learn
- Use clear, educational language appropriate for the learner

Remember: Only provide information that can be found in the textbook. Do not make up
information or provide content from other sources."""


class AgentRunner:
    """Runs the OpenAI agent with streaming support.

    Coordinates tool execution and response generation.

    NFR Reference: NFR-001 (streaming responses)
    """

    def __init__(self) -> None:
        """Initialize agent runner with OpenAI client."""
        settings = get_settings()

        self.model = settings.openai_model
        self._client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
        self._tools = get_agent_tools()

    async def run_stream(
        self,
        message: str,
        context: Optional[list[dict[str, str]]] = None,
        rag_context: Optional[str] = None,
    ) -> AsyncIterator[StreamChunk]:
        """Run the agent with streaming response.

        Args:
            message: User message to process.
            context: Optional conversation history.
            rag_context: Optional pre-retrieved RAG context.

        Yields:
            StreamChunk objects containing response content.

        Raises:
            AgentError: If agent execution fails.
        """
        try:
            async for chunk in self._create_stream(message, context, rag_context):
                # Process OpenAI chunk
                if chunk.choices and chunk.choices[0].delta:
                    delta = chunk.choices[0].delta
                    finish_reason = chunk.choices[0].finish_reason

                    if delta.content:
                        yield StreamChunk(
                            type="content",
                            content=delta.content,
                        )
                    elif finish_reason == "stop":
                        yield StreamChunk(
                            type="done",
                            content=None,
                        )
        except Exception as e:
            raise AgentError(f"Agent execution failed: {e}") from e

    async def _create_stream(
        self,
        message: str,
        context: Optional[list[dict[str, str]]] = None,
        rag_context: Optional[str] = None,
    ) -> AsyncIterator[Any]:
        """Create OpenAI streaming response.

        Args:
            message: User message.
            context: Conversation history.
            rag_context: Pre-retrieved context.

        Yields:
            OpenAI stream chunks.
        """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add context from RAG if provided
        if rag_context:
            messages.append({
                "role": "system",
                "content": f"Relevant textbook content:\n\n{rag_context}",
            })

        # Add conversation history
        if context:
            messages.extend(context)

        # Add current message
        messages.append({"role": "user", "content": message})

        # Create streaming response
        # Only provide tools when we don't have pre-retrieved context
        # If rag_context is provided, the model should use that context
        # rather than calling the search tool again
        create_kwargs = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }

        if not rag_context:
            # Only include tools when model needs to search for context
            create_kwargs["tools"] = _tools_to_openai_format(self._tools)

        stream = self._client.chat.completions.create(**create_kwargs)

        for chunk in stream:
            yield chunk
