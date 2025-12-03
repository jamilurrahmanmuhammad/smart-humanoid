"""Safety guardrail checks service.

Detects safety-relevant content and injects disclaimers for physical robotics topics.

FR References:
- FR-021: Include safety disclaimers for physical robotics operations
- FR-022: Refuse or heavily qualify advice involving physical risks
- FR-023: Distinguish conceptual explanation from hardware readiness
- FR-024: Encourage cross-checking with official sources
"""

import re
from dataclasses import dataclass


@dataclass
class SafetyCheckResult:
    """Result from safety check analysis.

    Attributes:
        requires_disclaimer: Whether the content needs a safety disclaimer.
        category: The category of safety concern (e.g., "electrical", "mechanical").
        is_high_risk: Whether this is a high-risk request requiring refusal/strong warning.
        keywords_matched: List of safety keywords that triggered the check.
    """

    requires_disclaimer: bool
    category: str
    is_high_risk: bool
    keywords_matched: list[str]


# Safety keyword categories with their patterns
_SAFETY_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "safety_bypass": {
        # HIGH RISK - These trigger strong warnings
        "patterns": [
            r"\bbypass\b.*\b(safety|interlock|limit|stop)\b",
            r"\bdisable\b.*\b(safety|interlock|limit|stop|emergency)\b",
            r"\boverride\b.*\b(safety|limit|protection)\b",
            r"\bremove\b.*\b(safety|guard|interlock)\b",
            r"\bdeactivate\b.*\b(safety|protection)\b",
            r"\bemergency\s*stop\b.*\b(disable|bypass|remove)\b",
        ],
        "keywords": [
            "bypass", "disable safety", "override safety", "remove interlock",
            "disable interlock", "bypass limit", "defeat safety",
        ],
        "is_high_risk": True,
    },
    "electrical": {
        "patterns": [
            r"\b(rewire|rewiring)\b",
            r"\bvoltage\b",
            r"\bcurrent\b.*\b(adjust|change|modify|limit)\b",
            r"\bshort\s*circuit\b",
            r"\bpower\s*supply\b.*\b(modify|build|change)\b",
            r"\bbattery\b.*\b(connect|wire|mod)\b",
        ],
        "keywords": [
            "rewire", "voltage", "short circuit", "power supply",
            "amp", "amperage", "electrical connection",
        ],
        "is_high_risk": False,
    },
    "mechanical": {
        "patterns": [
            r"\btorque\b.*\b(adjust|change|limit|increase)\b",
            r"\bjoint\b.*\b(limit|force|torque)\b",
            r"\bmotor\b.*\b(control|direct|modify)\b",
            r"\bservo\b",
            r"\bactuator\b.*\b(control|modify)\b",
        ],
        "keywords": [
            "motor", "servo", "actuator", "torque", "joint limit",
            "gear", "pulley", "belt", "chain",
        ],
        "is_high_risk": False,
    },
    "physical_modification": {
        "patterns": [
            r"\b(modify|modifying)\b.*\bhardware\b",
            r"\bbuild\b.*\brobot\b",
            r"\bassemble\b",
            r"\bsolder\b",
            r"\bmount\b.*\b(motor|sensor|camera)\b",
        ],
        "keywords": [
            "rewire", "solder", "assemble", "mount", "install",
            "hardware modification", "physical setup",
        ],
        "is_high_risk": False,
    },
}

# Disclaimer templates by category
_DISCLAIMER_TEMPLATES: dict[str, str] = {
    "safety_bypass": """
**IMPORTANT SAFETY WARNING**: I cannot provide instructions for bypassing, disabling, or removing safety systems. Safety mechanisms exist to prevent injury and equipment damage. Attempting to circumvent them can result in:

- Serious personal injury
- Damage to expensive equipment
- Voiding warranties and violating regulations

If you believe a safety system is malfunctioning, please consult your equipment manual or contact a qualified technician.
""".strip(),
    "electrical": """
**Safety Note**: This response discusses electrical systems. Before attempting any electrical work on real hardware:

- Verify all information against official documentation
- Ensure power is disconnected before making changes
- Use appropriate safety equipment (insulated tools, safety glasses)
- Consult an instructor or qualified technician if unsure

This explanation is for educational and conceptual understanding. Always verify procedures before attempting on actual hardware.
""".strip(),
    "mechanical": """
**Safety Note**: This response involves mechanical systems. Before working with real hardware:

- Ensure the robot is powered off and secured
- Verify torque and force limits from official specifications
- Use appropriate personal protective equipment
- Consult official manuals for your specific hardware

This information is for learning purposes. Always verify with official documentation before attempting on real hardware.
""".strip(),
    "physical_modification": """
**Safety Note**: This response discusses physical hardware operations. Before attempting any modifications:

- Review official documentation for your specific equipment
- Consult with an instructor or experienced mentor
- Ensure you have appropriate safety equipment
- Start with simulation or disconnected hardware when possible

This explanation is for conceptual understanding. Always verify procedures and consult official sources before working on actual hardware.
""".strip(),
    "default": """
**Safety Note**: This topic involves physical robotics operations. Please:

- Verify all information against official documentation
- Consult your instructor or equipment manuals
- Use appropriate safety precautions

This response is for educational purposes. Always consult official sources before attempting procedures on real hardware.
""".strip(),
}


class SafetyChecker:
    """Checks content for safety concerns and generates appropriate disclaimers.

    FR References:
    - FR-021: Safety disclaimers for physical robotics operations
    - FR-022: Refuse/qualify advice involving physical risks
    - FR-023: Distinguish conceptual from hardware-ready
    - FR-024: Encourage cross-checking with official sources
    """

    def __init__(self, enabled: bool = True) -> None:
        """Initialize SafetyChecker.

        Args:
            enabled: Whether safety checking is enabled. Defaults to True.
        """
        self._enabled = enabled
        self._compiled_patterns: dict[str, list[re.Pattern]] = {}

        # Pre-compile regex patterns for efficiency
        for category, config in _SAFETY_KEYWORDS.items():
            self._compiled_patterns[category] = [
                re.compile(pattern, re.IGNORECASE)
                for pattern in config["patterns"]
            ]

    def check(self, text: str) -> SafetyCheckResult:
        """Check text for safety concerns.

        Args:
            text: The text to analyze for safety keywords.

        Returns:
            SafetyCheckResult with analysis details.
        """
        if not self._enabled:
            return SafetyCheckResult(
                requires_disclaimer=False,
                category="",
                is_high_risk=False,
                keywords_matched=[],
            )

        text_lower = text.lower()
        matched_keywords: list[str] = []
        matched_category: str = ""
        is_high_risk: bool = False

        # Check each category
        for category, config in _SAFETY_KEYWORDS.items():
            # Check regex patterns
            for pattern in self._compiled_patterns[category]:
                if pattern.search(text):
                    matched_category = category
                    is_high_risk = config["is_high_risk"]
                    # Extract matched text as keyword
                    match = pattern.search(text)
                    if match:
                        matched_keywords.append(match.group(0).lower())

            # Check simple keywords
            for keyword in config["keywords"]:
                if keyword.lower() in text_lower:
                    if not matched_category:
                        matched_category = category
                        is_high_risk = config["is_high_risk"]
                    matched_keywords.append(keyword.lower())

            # If we found a high-risk match, prioritize it
            if is_high_risk:
                break

        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in matched_keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)

        return SafetyCheckResult(
            requires_disclaimer=len(unique_keywords) > 0,
            category=matched_category,
            is_high_risk=is_high_risk,
            keywords_matched=unique_keywords,
        )

    def get_disclaimer(self, result: SafetyCheckResult) -> str:
        """Get the appropriate disclaimer for a safety check result.

        Args:
            result: The SafetyCheckResult from a check() call.

        Returns:
            Disclaimer text to include in the response.
        """
        if not result.requires_disclaimer:
            return ""

        # Use category-specific template or default
        template = _DISCLAIMER_TEMPLATES.get(
            result.category,
            _DISCLAIMER_TEMPLATES["default"],
        )

        return template
