"""Unit tests for persona adapter service.

TDD: Tests for T063-T070 - Persona-aware response adaptation.
"""

import pytest


class TestPersonaAdapter:
    """Tests for PersonaAdapter.get_system_prompt (T063-T064)."""

    @pytest.mark.unit
    def test_explorer_persona_produces_unique_prompt(self) -> None:
        """Explorer persona should produce distinct system prompt (FR-015, FR-016)."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()
        prompt = adapter.get_system_prompt(PersonaType.EXPLORER)

        # Explorer-specific characteristics
        assert "software" in prompt.lower() or "simulation" in prompt.lower()
        assert "analogy" in prompt.lower() or "analogies" in prompt.lower()

    @pytest.mark.unit
    def test_builder_persona_produces_unique_prompt(self) -> None:
        """Builder persona should produce distinct system prompt (FR-015, FR-016)."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()
        prompt = adapter.get_system_prompt(PersonaType.BUILDER)

        # Builder-specific characteristics
        assert "maker" in prompt.lower() or "arduino" in prompt.lower() or "raspberry" in prompt.lower()

    @pytest.mark.unit
    def test_engineer_persona_produces_unique_prompt(self) -> None:
        """Engineer persona should produce distinct system prompt (FR-015, FR-016)."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()
        prompt = adapter.get_system_prompt(PersonaType.ENGINEER)

        # Engineer-specific characteristics
        assert "technical" in prompt.lower() or "industrial" in prompt.lower()

    @pytest.mark.unit
    def test_default_persona_produces_balanced_prompt(self) -> None:
        """Default persona should produce balanced system prompt (FR-017)."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()
        prompt = adapter.get_system_prompt(PersonaType.DEFAULT)

        # Default should be balanced, accessible
        assert "balanced" in prompt.lower() or "accessible" in prompt.lower() or "general" in prompt.lower()

    @pytest.mark.unit
    def test_all_personas_produce_different_prompts(self) -> None:
        """Each persona should produce a distinct prompt (FR-016)."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()

        prompts = {
            persona: adapter.get_system_prompt(persona)
            for persona in PersonaType
        }

        # All prompts should be unique
        unique_prompts = set(prompts.values())
        assert len(unique_prompts) == len(PersonaType)


class TestPersonaPromptContent:
    """Tests for persona-specific prompt content (T065-T066)."""

    @pytest.mark.unit
    def test_explorer_uses_software_analogies(self) -> None:
        """Explorer prompt should encourage software analogies."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()
        prompt = adapter.get_system_prompt(PersonaType.EXPLORER)

        # Should mention software background, avoid hardware jargon
        assert any(term in prompt.lower() for term in [
            "software", "simulation", "programming", "code"
        ])

    @pytest.mark.unit
    def test_builder_uses_maker_examples(self) -> None:
        """Builder prompt should include maker-friendly examples."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()
        prompt = adapter.get_system_prompt(PersonaType.BUILDER)

        # Should mention maker context
        assert any(term in prompt.lower() for term in [
            "maker", "arduino", "raspberry", "diy", "hands-on", "practical"
        ])

    @pytest.mark.unit
    def test_engineer_provides_technical_depth(self) -> None:
        """Engineer prompt should provide full technical depth."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()
        prompt = adapter.get_system_prompt(PersonaType.ENGINEER)

        # Should mention technical depth, industrial context
        assert any(term in prompt.lower() for term in [
            "technical", "industrial", "professional", "detailed", "rigorous"
        ])

    @pytest.mark.unit
    def test_prompts_include_citation_requirement(self) -> None:
        """All prompts should include citation requirement."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()

        for persona in PersonaType:
            prompt = adapter.get_system_prompt(persona)
            # All prompts should mention citations/sources
            assert any(term in prompt.lower() for term in [
                "citation", "source", "reference", "cite"
            ]), f"{persona} prompt missing citation requirement"


class TestAgentPersonaIntegration:
    """Tests for persona integration with AgentRunner (T067-T068)."""

    @pytest.mark.unit
    def test_adapt_prompt_for_persona_returns_string(self) -> None:
        """adapt_prompt should return a formatted prompt string."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()
        base_prompt = "You are a helpful assistant."
        rag_context = "Some context from the textbook."

        result = adapter.adapt_prompt(
            base_prompt=base_prompt,
            persona=PersonaType.EXPLORER,
            rag_context=rag_context,
        )

        assert isinstance(result, str)
        assert len(result) > len(base_prompt)
        # Should include both base prompt and RAG context
        assert "assistant" in result.lower()

    @pytest.mark.unit
    def test_adapt_prompt_includes_rag_context(self) -> None:
        """adapt_prompt should include RAG context in output."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()
        rag_context = "ROS 2 uses DDS for communication."

        result = adapter.adapt_prompt(
            base_prompt="Base prompt",
            persona=PersonaType.DEFAULT,
            rag_context=rag_context,
        )

        # RAG context should be included
        assert "DDS" in result or "context" in result.lower()

    @pytest.mark.unit
    def test_adapt_prompt_handles_empty_context(self) -> None:
        """adapt_prompt should handle empty RAG context gracefully."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()

        result = adapter.adapt_prompt(
            base_prompt="Base prompt",
            persona=PersonaType.BUILDER,
            rag_context="",
        )

        # Should still return a valid prompt
        assert isinstance(result, str)
        assert len(result) > 0


class TestSessionPersonaPersistence:
    """Tests for session persona persistence (T069-T070).

    Note: Full session persistence requires database integration.
    These tests verify the PersonaAdapter handles session context.
    """

    @pytest.mark.unit
    def test_get_system_prompt_is_deterministic(self) -> None:
        """Same persona should always produce same prompt."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()

        prompt1 = adapter.get_system_prompt(PersonaType.EXPLORER)
        prompt2 = adapter.get_system_prompt(PersonaType.EXPLORER)

        assert prompt1 == prompt2

    @pytest.mark.unit
    def test_persona_adapter_is_stateless(self) -> None:
        """PersonaAdapter should not maintain state between calls."""
        from models.schemas import PersonaType
        from services.persona import PersonaAdapter

        adapter = PersonaAdapter()

        # Call with different personas
        explorer_prompt = adapter.get_system_prompt(PersonaType.EXPLORER)
        builder_prompt = adapter.get_system_prompt(PersonaType.BUILDER)

        # Calling explorer again should give same result
        explorer_prompt_again = adapter.get_system_prompt(PersonaType.EXPLORER)

        assert explorer_prompt == explorer_prompt_again
        assert explorer_prompt != builder_prompt
