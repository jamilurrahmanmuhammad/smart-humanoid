"""Unit tests for safety guardrails service.

TDD: Tests for T071-T078 - Safety guardrails for physical robotics topics.
"""

import pytest


class TestSafetyKeywordDetection:
    """Tests for SafetyChecker keyword detection (T071-T072)."""

    @pytest.mark.unit
    def test_detects_rewiring_keywords(self) -> None:
        """Should detect keywords related to rewiring (FR-021)."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        # Questions about rewiring should trigger safety
        result = checker.check("How do I rewire my robot's motor?")
        assert result.requires_disclaimer is True
        # Rewire is classified as electrical (it involves wiring)
        assert result.category in ["electrical", "physical_modification"]

    @pytest.mark.unit
    def test_detects_bypassing_safety_keywords(self) -> None:
        """Should detect keywords about bypassing safety systems (FR-022)."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result = checker.check("How can I bypass the safety interlock?")
        assert result.requires_disclaimer is True
        assert result.is_high_risk is True

    @pytest.mark.unit
    def test_detects_motor_control_keywords(self) -> None:
        """Should detect keywords about motor control (FR-021)."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result = checker.check("How do I control the servo motor directly?")
        assert result.requires_disclaimer is True

    @pytest.mark.unit
    def test_detects_power_related_keywords(self) -> None:
        """Should detect keywords about power systems (FR-021)."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result = checker.check("What voltage should I use for the power supply?")
        assert result.requires_disclaimer is True

    @pytest.mark.unit
    def test_no_detection_for_conceptual_questions(self) -> None:
        """Should not flag purely conceptual questions (FR-023)."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result = checker.check("What is the difference between ROS 1 and ROS 2?")
        assert result.requires_disclaimer is False

    @pytest.mark.unit
    def test_case_insensitive_detection(self) -> None:
        """Keyword detection should be case-insensitive."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result1 = checker.check("REWIRE the motor")
        result2 = checker.check("ReWiRe the motor")

        assert result1.requires_disclaimer is True
        assert result2.requires_disclaimer is True


class TestDisclaimerInjection:
    """Tests for SafetyChecker disclaimer injection (T073-T074)."""

    @pytest.mark.unit
    def test_get_disclaimer_returns_string(self) -> None:
        """get_disclaimer should return a non-empty string."""
        from services.safety import SafetyChecker, SafetyCheckResult

        checker = SafetyChecker()

        result = SafetyCheckResult(
            requires_disclaimer=True,
            category="physical_modification",
            is_high_risk=False,
            keywords_matched=["motor"],
        )

        disclaimer = checker.get_disclaimer(result)

        assert isinstance(disclaimer, str)
        assert len(disclaimer) > 0

    @pytest.mark.unit
    def test_high_risk_disclaimer_is_stronger(self) -> None:
        """High-risk content should get a stronger disclaimer (FR-022)."""
        from services.safety import SafetyChecker, SafetyCheckResult

        checker = SafetyChecker()

        normal_result = SafetyCheckResult(
            requires_disclaimer=True,
            category="physical_modification",
            is_high_risk=False,
            keywords_matched=["motor"],
        )

        high_risk_result = SafetyCheckResult(
            requires_disclaimer=True,
            category="safety_bypass",
            is_high_risk=True,
            keywords_matched=["bypass", "interlock"],
        )

        normal_disclaimer = checker.get_disclaimer(normal_result)
        high_risk_disclaimer = checker.get_disclaimer(high_risk_result)

        # High risk disclaimer should mention refusing or not providing instructions
        # (this is more important than length)
        assert any(term in high_risk_disclaimer.lower() for term in [
            "cannot", "refuse", "strongly", "dangerous", "do not"
        ])
        # High risk should be more emphatic (different content, not just longer)
        assert high_risk_disclaimer != normal_disclaimer

    @pytest.mark.unit
    def test_disclaimer_mentions_safety(self) -> None:
        """All disclaimers should mention safety (FR-021)."""
        from services.safety import SafetyChecker, SafetyCheckResult

        checker = SafetyChecker()

        result = SafetyCheckResult(
            requires_disclaimer=True,
            category="electrical",
            is_high_risk=False,
            keywords_matched=["voltage"],
        )

        disclaimer = checker.get_disclaimer(result)

        assert "safety" in disclaimer.lower() or "safe" in disclaimer.lower()

    @pytest.mark.unit
    def test_disclaimer_recommends_verification(self) -> None:
        """Disclaimers should recommend verifying with official sources (FR-024)."""
        from services.safety import SafetyChecker, SafetyCheckResult

        checker = SafetyChecker()

        result = SafetyCheckResult(
            requires_disclaimer=True,
            category="physical_modification",
            is_high_risk=False,
            keywords_matched=["motor"],
        )

        disclaimer = checker.get_disclaimer(result)

        # Should mention verification/official sources
        assert any(term in disclaimer.lower() for term in [
            "verify", "official", "manual", "instructor", "consult", "documentation"
        ])


class TestSafetyCategoryClassification:
    """Tests for safety category classification (T075-T076)."""

    @pytest.mark.unit
    def test_classifies_electrical_category(self) -> None:
        """Should classify electrical safety questions."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result = checker.check("What happens if I short circuit the battery?")
        assert result.requires_disclaimer is True
        assert result.category in ["electrical", "physical_modification"]

    @pytest.mark.unit
    def test_classifies_mechanical_category(self) -> None:
        """Should classify mechanical safety questions."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result = checker.check("How do I adjust the joint torque limits?")
        assert result.requires_disclaimer is True
        assert result.category in ["mechanical", "physical_modification"]

    @pytest.mark.unit
    def test_classifies_high_risk_bypass(self) -> None:
        """Should classify safety bypass as high risk."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result = checker.check("disable the emergency stop")
        assert result.is_high_risk is True
        assert result.category == "safety_bypass"

    @pytest.mark.unit
    def test_returns_matched_keywords(self) -> None:
        """Should return the keywords that triggered detection."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result = checker.check("How do I rewire the motor and adjust voltage?")

        assert len(result.keywords_matched) > 0
        # Should include at least one of the triggering keywords
        assert any(kw in ["rewire", "motor", "voltage"] for kw in result.keywords_matched)


class TestConceptualVsHardwareDistinction:
    """Tests for distinguishing conceptual vs hardware readiness (T077-T078, FR-023)."""

    @pytest.mark.unit
    def test_conceptual_flag_in_disclaimer(self) -> None:
        """Disclaimer should distinguish conceptual understanding from hardware readiness."""
        from services.safety import SafetyChecker, SafetyCheckResult

        checker = SafetyChecker()

        result = SafetyCheckResult(
            requires_disclaimer=True,
            category="physical_modification",
            is_high_risk=False,
            keywords_matched=["motor"],
        )

        disclaimer = checker.get_disclaimer(result)

        # Should mention that this is for understanding, not direct application
        assert any(phrase in disclaimer.lower() for phrase in [
            "conceptual", "understanding", "educational", "learning",
            "real hardware", "actual hardware", "before attempting"
        ])

    @pytest.mark.unit
    def test_safety_check_result_structure(self) -> None:
        """SafetyCheckResult should have all required fields."""
        from services.safety import SafetyCheckResult

        result = SafetyCheckResult(
            requires_disclaimer=True,
            category="test",
            is_high_risk=False,
            keywords_matched=["test"],
        )

        assert hasattr(result, "requires_disclaimer")
        assert hasattr(result, "category")
        assert hasattr(result, "is_high_risk")
        assert hasattr(result, "keywords_matched")

    @pytest.mark.unit
    def test_no_disclaimer_result_has_empty_keywords(self) -> None:
        """When no safety concern, keywords_matched should be empty."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        result = checker.check("Explain the concept of nodes in ROS 2")

        assert result.requires_disclaimer is False
        assert result.keywords_matched == []


class TestSafetyCheckerConfiguration:
    """Tests for SafetyChecker configuration options."""

    @pytest.mark.unit
    def test_safety_checker_can_be_disabled(self) -> None:
        """SafetyChecker should respect enabled flag."""
        from services.safety import SafetyChecker

        checker = SafetyChecker(enabled=False)

        result = checker.check("How do I rewire the motor?")

        # When disabled, should not flag anything
        assert result.requires_disclaimer is False

    @pytest.mark.unit
    def test_safety_checker_enabled_by_default(self) -> None:
        """SafetyChecker should be enabled by default."""
        from services.safety import SafetyChecker

        checker = SafetyChecker()

        # Should detect safety keywords when enabled
        result = checker.check("rewire the motor")
        assert result.requires_disclaimer is True
