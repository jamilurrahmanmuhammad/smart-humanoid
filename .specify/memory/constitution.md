<!--
  ============================================================================
  SYNC IMPACT REPORT
  ============================================================================
  Version Change: 1.1.0 → 1.1.1

  Modified Principles:
    - XII. Identity & Personalization: Added Reader Data Privacy subsection
    - XXI. Translation Governance: Added future language expansion roadmap
    - XXXVII. Content Review Gates: Added Accessibility Compliance gate

  Added Sections:
    - Reader Data Privacy (under XII. Identity & Personalization)
    - Accessibility Standards (new section after User Experience Consistency)

  Removed Sections: None

  Templates Requiring Updates:
    - .specify/templates/plan-template.md: ✅ Compatible
    - .specify/templates/spec-template.md: ✅ Compatible
    - .specify/templates/tasks-template.md: ✅ Compatible

  Follow-up TODOs: None
  ============================================================================
-->

# Smart Humanoid — Constitution

**Version 1.1.1 — December 2025**

---

## 1. Mission

We build an **intelligent multi-book educational ecosystem** that teaches people how to think, build, and create in the age of AI. Our platform delivers AI-native technical education through interactive books spanning Physical AI, Humanoid Robotics, AI Agents, STEM, Medical AI, Cybersecurity, Data Science, and Cloud Native Engineering.

Each book adapts to reader background, verifies every claim, and transforms passive reading into active capability building. The platform accumulates intelligence across books—skills, subagents, and learning patterns that compound over time.

This constitution governs how we design content, build technology, and deliver learning experiences across the entire ecosystem. Every decision—from a single sentence to a system architecture choice—MUST align with these principles.

---

## 2. The Author Identity

Every contributor operates as an **Educational Systems Architect**.

This identity combines:
- The precision of a robotics engineer
- The clarity of a technical writer
- The empathy of a patient teacher
- The rigour of a researcher
- The vision of a curriculum designer

We do not write content. We design structured learning experiences that build real capability. Every lesson MUST answer one question:

**"What can the reader do after learning this that they could not do before?"**

If the answer is unclear, the lesson is not ready.

---

## Core Principles

### I. Specification Before Implementation

Understanding precedes action. Before any code, command, or tool appears, the reader MUST understand:
- What we are building
- Why it matters
- What constraints exist
- How we will know it works

This develops judgement. Readers learn to think before they type—a skill that separates professionals from hobbyists.

### II. Progressive Mastery

Learning is a journey through four distinct phases. The reader never sees these labels, but every chapter MUST follow this rhythm:

**Phase 1 — Foundation**: Build mental models manually. Handle core concepts without AI assistance. Establish independent understanding that enables quality judgement later.

**Phase 2 — Collaboration**: Introduce AI as a thinking partner. Learn to ask precise questions, evaluate responses critically, challenge assumptions, and refine outputs through iteration. The reader MUST experience both AI providing genuine value and themselves correcting AI mistakes.

**Phase 3 — Amplification**: Transform repeated workflows into reusable intelligence: structured prompts, custom skills, subagents, automation patterns. This mirrors how professionals reduce cognitive load and scale their capability.

**Phase 4 — Integration**: Apply everything through a specification-first project. Begin with requirements, use accumulated tools, produce working outcomes. This is where learning becomes capability.

### III. Anti-Convergence

We reject generic technical education. No lecture-style explanations. No identical lesson structures. No toy projects disconnected from reality.

Each chapter MUST vary its approach:
- Discovery through exploration
- Scenario-based reasoning
- Learning from deliberate errors
- Specification-driven problem solving
- Real-world pattern application

Every chapter MUST feel alive.

### IV. Accumulated Intelligence

Nothing exists in isolation. Every chapter MUST build upon:
- Prior specifications and mental models
- Previously created tools and skills
- Earlier concepts and vocabulary
- Capabilities developed in previous lessons

The reader experiences a seamless progression where everything connects.

### V. Minimal Sufficient Content

We include only what advances capability. No summaries restating what was just read. No motivational padding. No "what you learned" sections.

Every chapter MUST end with **"Try With AI"**—a practical activity where readers engage, evaluate, iterate, and build.

---

## Content Integrity Standards

### VI. Citation Requirements (NON-NEGOTIABLE)

Every factual claim MUST be traceable to its source.

**Citation Format: IEEE Standard**
```
In-text: [1], [2], [3-5]

References:
[1] A. Author, "Title," Publication, vol. X, pp. Y-Z, Year. [Online]. Available: URL
```

**MUST Be Cited:**
- Statistics and numerical claims
- Hardware specifications and performance metrics
- Software version capabilities
- Research findings and benchmarks
- Code adapted from external sources
- API behaviours and limitations
- Pricing and availability information

**Exempt from Citation:**
- Original explanations written for this book
- Code created specifically for our lessons
- Universal programming concepts
- Logical reasoning and analysis

### VII. Source Verification Hierarchy

Not all sources carry equal weight. Verify claims against this hierarchy:

**Tier 1 — Authoritative**
- Official documentation (ROS 2, NVIDIA Isaac, Gazebo, Unity)
- Peer-reviewed publications (IEEE, ACM, robotics journals)
- Manufacturer specifications (NVIDIA, Intel, Unitree, Boston Dynamics)

**Tier 2 — Credible**
- Official tutorials and guides
- Conference presentations with named authors
- Established technical blogs with verifiable claims

**Tier 3 — Supplementary**
- Community documentation (wikis, forums)
- Video tutorials from recognized experts
- GitHub repositories with significant adoption

**Prohibited Sources:**
- Unverified forum posts or comments
- AI-generated content without independent verification
- Documentation older than 24 months for rapidly evolving technology
- Anonymous or unattributable claims

### VIII. Technical Accuracy

Code MUST work. Commands MUST execute. Examples MUST produce the stated results.

**Every code example requires:**
- Target operating system (Ubuntu 22.04 LTS as baseline)
- Software versions (ROS 2 Humble/Iron, Python 3.10+, CUDA version)
- Hardware requirements where applicable
- Expected output or observable behaviour
- Known limitations or edge cases

**Prohibited:**
- Hallucinated APIs or features
- Invented function signatures
- Speculative behaviour descriptions
- Untested command sequences

When uncertain, investigate. When investigation fails, state the limitation explicitly rather than guess.

### IX. Plagiarism Prevention (NON-NEGOTIABLE)

Plagiarism in any form is unacceptable. All content MUST be original or properly attributed.

**Definition — Plagiarism includes:**
- Copying text without quotation marks and citation
- Paraphrasing ideas without attribution
- Using code from external sources without credit
- Presenting AI-generated content as human-written without disclosure
- Reusing one's own published work without acknowledgment (self-plagiarism)
- Using images, diagrams, or media without permission or attribution

**Original Content Standards:**
- All explanatory text MUST be written originally for this work
- Paraphrasing requires genuine transformation of ideas, not word substitution
- Direct quotes require quotation marks AND citation
- Quotes exceeding 40 words require block formatting

**Code Attribution:**
- External code snippets require source link and license
- Adapted code MUST state "Adapted from [source]"
- AI-generated code MUST be reviewed, tested, and disclosed
- Standard library usage exempt; novel implementations require attribution

**Visual Content:**
- Original diagrams preferred
- External images require permission and attribution
- Screenshots of software interfaces permitted with tool acknowledgment
- No copyrighted material without explicit license

**Verification Process:**
- All content checked against plagiarism detection tools before publication
- Similarity reports reviewed for legitimate vs. problematic matches
- Technical terminology and code syntax excluded from similarity scoring
- Flagged content revised or properly attributed before approval

**Consequences:**
- Plagiarized content rejected without exception
- Repeated violations result in contributor removal
- Published plagiarism triggers immediate correction and public acknowledgment

---

## Technology Platform

### X. Content Delivery

| Component | Technology | Purpose |
|-----------|------------|---------|
| Publishing Platform | Docusaurus 3.x | Interactive book rendering |
| Deployment | GitHub Pages / Vercel | Global content delivery |
| Version Control | Git + GitHub | Content versioning and collaboration |
| Content Development | Claude Code + Spec-Kit Plus | AI-assisted authoring workflow |

### XI. Intelligent Assistant

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend Framework | FastAPI | API layer and business logic |
| Vector Database | Qdrant Cloud | Semantic search over content |
| Relational Database | Neon Serverless Postgres | User data, preferences, history |
| AI Integration | OpenAI Agents SDK | Conversational capabilities |
| Embeddings | text-embedding-3-small | Content vectorization |

**Assistant Capabilities:**
- Answer questions grounded exclusively in book content
- Respond to queries about user-selected text passages
- Maintain conversation context within sessions
- Gracefully decline out-of-scope questions
- Response latency target: under 3 seconds

### XII. Identity & Personalization

| Component | Technology | Purpose |
|-----------|------------|---------|
| Authentication | Better-Auth | Secure signup and signin |
| Session Management | JWT | Stateless authentication |
| Profile Storage | Postgres | User background and preferences |

**User Onboarding Data:**
- Software development experience level
- Hardware/electronics background
- Robotics familiarity
- Learning objectives
- Preferred pace

**Reader Data Privacy:**

We respect reader privacy and handle personal data responsibly. The platform collects only data necessary for personalization and learning progress tracking. Readers control their data and can request deletion at any time.

**Privacy Principles:**
- Data collection MUST be transparent and consent-based
- Personal data MUST be encrypted at rest and in transit
- Reader profiles MUST NOT be shared with third parties without explicit consent
- Users MUST have access to export or delete their data
- Analytics MUST be aggregated and anonymized where possible
- Minors' data MUST comply with COPPA and equivalent regulations
- Privacy policy MUST be accessible and written in plain language

### XIII. Adaptive Content

The platform adapts content based on reader background:

**Learning Paths:**
- **Explorer**: Software background only, simulation-focused
- **Builder**: Some embedded/hardware experience
- **Engineer**: Full hardware access, sim-to-real focus

**Per-Chapter Features:**
- Personalization: Adjust depth and examples based on user profile
- Translation: Render content in Urdu (and future languages)
- Difficulty indicators visible to user

### XIV. Infrastructure Principles

- API keys and secrets via environment variables only
- No hardcoded credentials in any repository
- User data encrypted at rest
- PII collected only with explicit consent
- Content under permissive licensing (MIT/Apache 2.0 for code)

---

## Platform Intelligence Framework

### XV. Reusable Subagents

The platform brain consists of specialized subagents that accumulate intelligence across books.

**Subagent Categories:**
- **Content Agents**: Generate, review, and refine educational content
- **Code Agents**: Write, test, and validate code examples
- **Research Agents**: Gather and verify technical information
- **Translation Agents**: Localize content while preserving technical accuracy
- **Personalization Agents**: Adapt content to reader profiles

**Governance Rules:**
- Every subagent MUST have a defined scope and capability boundary
- Subagents MUST NOT make decisions outside their declared competency
- All subagent outputs MUST be traceable to their source agent
- Subagent failures MUST degrade gracefully with clear error messages

### XVI. Skill Libraries

Skills are reusable intelligence modules shared across books and agents.

**Skill Structure:**
```
skill/
├── manifest.yaml      # Name, version, dependencies, capabilities
├── prompts/           # Structured prompts for the skill
├── validators/        # Output validation rules
├── tests/             # Skill verification tests
└── examples/          # Usage examples
```

**Skill Requirements:**
- Every skill MUST have a semantic version (MAJOR.MINOR.PATCH)
- Skills MUST declare their dependencies explicitly
- Skills MUST include validation rules for their outputs
- Skills MUST be independently testable
- Skills MUST NOT have circular dependencies

**Cross-Book Skill Sharing:**
- Skills developed in one book MUST be available to other books
- Book-specific customizations MUST NOT break shared skill contracts
- Skill updates MUST maintain backward compatibility within MAJOR version

### XVII. Intelligence Versioning & Interoperability

**Version Policy:**
- MAJOR: Breaking changes to skill/agent contracts
- MINOR: New capabilities, backward compatible
- PATCH: Bug fixes, documentation updates

**Interoperability Rules:**
- All agents and skills MUST communicate via defined interfaces
- Interface changes MUST follow deprecation policy (minimum 1 version warning)
- Cross-book intelligence MUST use the shared skill registry
- Version conflicts MUST be resolved at build time, not runtime

**Skill Registry:**
- Central registry of all available skills across the ecosystem
- Skills MUST be registered before use in any book
- Registry tracks usage, versions, and dependencies

---

## RAG Assistant Governance

### XVIII. Answer Grounding & Traceability

Every assistant response MUST be grounded in book content.

**Grounding Requirements:**
- Responses MUST cite specific sections, chapters, or passages
- No claims without traceable source in the indexed content
- Out-of-scope questions MUST receive explicit "I don't have information about this in the book" responses
- Hallucination risk MUST be mitigated through retrieval-first architecture

**Traceability Format:**
```
[Answer text]

📚 Sources:
- Chapter X, Section Y: "relevant quote"
- Chapter Z, Section W: "supporting information"
```

### XIX. Multi-Source Citation in Responses

Assistant responses that synthesize multiple sources MUST cite all contributing passages.

**Multi-Citation Rules:**
- When combining information from multiple chapters, cite each source
- Conflicting information across sources MUST be flagged to the user
- Citation order MUST reflect relevance to the query
- Maximum 5 citations per response to maintain readability

**Citation Quality:**
- Citations MUST link to the exact location in the book
- Quote extracts MUST be verbatim (no paraphrasing in citations)
- Citations MUST include chapter number, section title, and paragraph reference

### XX. Context Stitching & Lineage

The assistant MUST maintain coherent context across multi-turn conversations.

**Context Management:**
- Conversation history MUST be preserved within session
- Context window MUST prioritize recent exchanges and user-selected text
- When context exceeds limits, summarize earlier turns rather than truncate
- Cross-chapter queries MUST stitch relevant content coherently

**Lineage Tracking:**
- Every response MUST track which content chunks contributed to it
- Lineage data MUST be available for debugging and quality analysis
- Content updates MUST trigger re-indexing of affected responses

---

## Multilingual Quality Framework

### XXI. Translation Governance

All translations MUST preserve technical accuracy while achieving linguistic naturalness.

**Translation Principles:**
- Technical meaning takes precedence over literal translation
- Domain-specific terms follow the Terminology Dictionary (Section XXII)
- Translations MUST be reviewed by native speakers with technical background
- Machine translation outputs MUST be human-verified before publication

**Translation Workflow:**
1. Machine translation of source content
2. Technical accuracy review by domain expert
3. Linguistic review by native speaker
4. Consistency check against Terminology Dictionary
5. Final approval and publication

**Language Expansion Roadmap:**

Urdu is the first supported translation language. The platform is designed for multi-language expansion:

**Current:** Urdu (اردو)
**Planned Phase 2:** Arabic (العربية), Hindi (हिन्दी)
**Planned Phase 3:** Spanish (Español), French (Français), Chinese (中文)
**Future:** Community-driven language additions following the Translation Governance framework

Each new language MUST:
- Have a dedicated Terminology Dictionary
- Pass native speaker + technical expert review
- Support appropriate text direction (RTL/LTR)
- Maintain parity with English source content

### XXII. Terminology Dictionary

A centralized dictionary governs translation of technical terms across all languages.

**Dictionary Structure:**
| English Term | Urdu Translation | Transliteration | Notes |
|--------------|------------------|-----------------|-------|
| kinematics | حرکیات | harakiyaat | Motion study |
| torque | گردشی قوت | gardishi quwwat | Rotational force |
| SLAM | سلیم | SLAM | Keep acronym, explain in context |

**Dictionary Rules:**
- Every technical term MUST have an approved translation before use
- New terms MUST be proposed and reviewed before addition
- Contested translations MUST be resolved by domain + language experts
- Dictionary updates MUST propagate to all published content

**Prohibited Practices:**
- Ad-hoc translation of technical terms
- Inconsistent terminology across chapters
- Literal translations that lose technical meaning
- Mixing translation styles within a single book

### XXIII. Urdu Linguistics Quality Assurance

Urdu content MUST meet linguistic and typographic standards.

**Typographic Requirements:**
- Right-to-left (RTL) rendering MUST be correct throughout
- Code blocks MUST remain left-to-right within RTL context
- Nastaliq script preferred for body text where rendering supports it
- Mixed English-Urdu text MUST handle bidirectional flow correctly

**Linguistic Standards:**
- Formal register appropriate for educational content
- Avoid regional dialects; use standard Urdu
- Technical explanations MUST be clear to Pakistani and Indian Urdu readers
- Diacritical marks (اعراب) optional but consistent within each book

**Quality Gates for Urdu:**
- [ ] RTL rendering verified across all browsers
- [ ] Code blocks display correctly in RTL context
- [ ] Terminology matches Dictionary
- [ ] Native speaker review completed
- [ ] Technical accuracy preserved from English source

---

## Embodied Intelligence Safety

### XXIV. LLM-to-Robot Safety Guardrails

When LLMs generate commands for physical robots, safety MUST be enforced at multiple layers.

**Command Validation:**
- All LLM-generated robot commands MUST pass through a safety validator
- Commands affecting physical actuators MUST be bounded within safe ranges
- Emergency stop capability MUST be available at all times
- Unknown or ambiguous commands MUST default to safe state (no action)

**Safety Layers:**
1. **LLM Layer**: Prompt engineering to avoid dangerous outputs
2. **Validation Layer**: Rule-based filtering of generated commands
3. **Execution Layer**: Hardware-enforced limits on actuator ranges
4. **Monitoring Layer**: Real-time anomaly detection during execution

**Prohibited LLM Behaviours:**
- Generating commands that exceed hardware specifications
- Bypassing safety interlocks
- Executing sequences without human confirmation for high-risk actions
- Operating in unknown environments without explicit safety assessment

### XXV. Voice Command Safety

Voice-to-action pipelines MUST include safety verification before execution.

**Voice Command Pipeline:**
```
Voice Input → Speech Recognition → Intent Parsing → Safety Check → Execution
```

**Safety Requirements:**
- Ambiguous voice commands MUST request clarification before acting
- High-risk commands MUST require explicit confirmation
- Misheard commands MUST fail safely (no action on uncertainty)
- Background noise handling MUST NOT trigger unintended actions

**Confirmation Thresholds:**
| Risk Level | Action Type | Confirmation Required |
|------------|-------------|----------------------|
| Low | Navigation, observation | None |
| Medium | Object manipulation | Verbal confirmation |
| High | Tool use, lifting | Verbal + visual confirmation |
| Critical | Emergency, shutdown | Dual confirmation |

### XXVI. VLA Misinterpretation Handling

Vision-Language-Action models can misinterpret scenes. The system MUST handle these gracefully.

**Misinterpretation Mitigation:**
- VLA outputs MUST include confidence scores
- Low-confidence actions MUST trigger human verification
- Scene changes during execution MUST pause and re-evaluate
- Object misidentification MUST not result in dangerous actions

**Fallback Hierarchy:**
1. Re-query VLA with additional context
2. Request human clarification
3. Execute safe default behaviour
4. Full stop and await human intervention

**Logging Requirements:**
- All VLA decisions MUST be logged with input, output, and confidence
- Misinterpretations MUST be flagged for model improvement
- Safety incidents MUST trigger immediate review

### XXVII. Motion Planning Fallbacks

Motion planning failures MUST not result in dangerous robot states.

**Fallback Strategies:**
- **Path blocked**: Stop, re-plan, or request assistance
- **Joint limit reached**: Reverse to safe position
- **Collision detected**: Emergency stop, assess, report
- **Communication lost**: Execute safe shutdown sequence

**Planning Constraints:**
- All motion plans MUST include collision checking
- Plans MUST respect velocity and acceleration limits
- Dynamic obstacles MUST trigger re-planning
- Workspace boundaries MUST be enforced at planning level

**Human Override:**
- Human operators MUST be able to override automated motion at any time
- Override commands take precedence over planned motions
- Override events MUST be logged for safety analysis

---

## Multi-Book Ecosystem

### XXVIII. Ecosystem Architecture

The platform is a multi-book ecosystem, not a single book.

**Current and Planned Books:**
- Physical AI & Humanoid Robotics (current)
- AI Agents & Agentic Systems
- O/A-Level STEM Series
- Medical AI
- Cybersecurity
- Data Science & Analytics
- Cloud Native Engineering

**Ecosystem Principles:**
- Each book operates independently but shares platform infrastructure
- Books MUST NOT have hard dependencies on other books' content
- Cross-book references MUST be explicit and versioned
- Platform updates MUST NOT break individual books

### XXIX. Cross-Book Intelligence

Intelligence accumulates across the ecosystem.

**Shared Resources:**
- Skill libraries available to all books
- Subagents deployable across books
- Terminology dictionaries unified across domains where applicable
- User profiles portable between books

**Intelligence Flow:**
- Skills developed in one book MAY be promoted to ecosystem-level
- Ecosystem skills MUST be more general than book-specific variants
- Book-specific skills MUST NOT override ecosystem defaults without explicit configuration

**User Learning Continuity:**
- User progress in one book informs personalization in other books
- Completed skills transfer across books
- Learning path recommendations consider multi-book journey

### XXX. Book-Specific Customization

Each book MAY customize within ecosystem constraints.

**Allowed Customizations:**
- Book-specific terminology additions (must not conflict with ecosystem dictionary)
- Book-specific learning paths
- Book-specific UI themes (within brand guidelines)
- Book-specific assistant personality tuning

**Prohibited Customizations:**
- Overriding ecosystem safety rules
- Breaking shared skill contracts
- Inconsistent authentication flows
- Divergent citation formats

---

## User Experience Consistency

### XXXI. UI Component Standards

All books MUST use consistent UI components.

**Standard Components:**
| Component | Behaviour | Location |
|-----------|-----------|----------|
| Personalize Button | Opens personalization dialog | Chapter header |
| Translate Button | Toggles Urdu translation | Chapter header |
| Try With AI | Opens guided AI activity | Chapter footer |
| Ask Assistant | Opens RAG chat interface | Floating button |
| Progress Indicator | Shows chapter completion | Navigation sidebar |

**Component Rules:**
- Components MUST behave identically across all books
- Visual styling MAY vary within brand guidelines
- Interaction patterns MUST NOT vary between books
- New components MUST be approved at ecosystem level

### XXXII. Interaction Patterns

User interactions MUST be predictable across books.

**Standard Patterns:**
- **Personalization flow**: Background questions → preference storage → content adaptation
- **Translation flow**: Button click → loading state → translated content → toggle back
- **AI chat flow**: Question input → grounded response → source citations → follow-up
- **Progress tracking**: Section completion → chapter completion → module completion

**Consistency Requirements:**
- Loading states MUST use consistent indicators
- Error states MUST use consistent messaging patterns
- Success states MUST use consistent feedback
- Navigation MUST follow consistent information architecture

### XXXIII. Cross-Book Navigation

Users navigating between books MUST experience seamless transitions.

**Navigation Standards:**
- Ecosystem home provides access to all books
- User authentication persists across books
- Reading history is accessible from any book
- Recommendations surface relevant content from other books

**Cross-Reference Handling:**
- Links to other books MUST open in consistent manner
- Cross-book citations MUST be clearly marked
- Return navigation MUST be obvious and functional

---

## Accessibility Standards

### XXXIV. Inclusive Design Principles

The platform MUST be accessible to readers with disabilities, following WCAG 2.1 AA guidelines as a minimum standard.

**Visual Accessibility:**
- All text MUST have sufficient colour contrast (minimum 4.5:1 ratio)
- Content MUST be readable when zoomed to 200%
- Colour MUST NOT be the only means of conveying information
- High-contrast mode MUST be available
- Dark mode MUST maintain accessibility standards

**Cognitive Accessibility:**
- Dyslexia-friendly font options MUST be available
- Line spacing and paragraph width MUST be adjustable
- Complex diagrams MUST have text alternatives
- Navigation MUST be consistent and predictable
- Reading progress MUST be clearly indicated

**Motor Accessibility:**
- All interactive elements MUST be keyboard accessible
- Focus indicators MUST be visible
- Touch targets MUST be minimum 44x44 pixels
- No time-limited interactions without extension options

**Screen Reader Support:**
- All content MUST be navigable via screen reader
- Images MUST have descriptive alt text
- Code blocks MUST be properly labelled
- Interactive elements MUST have ARIA labels where needed
- Reading order MUST be logical

**Accessibility Quality Gates:**
- [ ] WCAG 2.1 AA compliance verified
- [ ] Screen reader testing completed
- [ ] Keyboard navigation tested
- [ ] Colour contrast validated
- [ ] Zoom functionality verified

---

## Content Architecture

### XXXV. Domain Structure

The curriculum covers Physical AI and Humanoid Robotics. The module structure is adapted from the Panaversity Physical AI & Humanoid Robotics course [1].

**Module 1: The Robotic Nervous System**
ROS 2 middleware, nodes, topics, services, actions. Python integration via rclpy. URDF for robot description. Foundation for all robot communication.

**Module 2: The Digital Twin**
Physics simulation with Gazebo. Visualization with Unity. Sensor simulation: LiDAR, depth cameras, IMUs. Environment building and testing.

**Module 3: The AI-Robot Brain**
NVIDIA Isaac Sim for photorealistic simulation. Isaac ROS for hardware-accelerated perception. VSLAM, navigation, and path planning. Sim-to-real transfer techniques.

**Module 4: Vision-Language-Action**
Voice command processing with Whisper. LLM integration for cognitive planning. Natural language to ROS 2 action translation. The convergence of language models and robotics.

### XXXVI. Chapter Structure

Every chapter MUST contain these elements (invisible scaffolding to reader):

**Opening:**
- Clear learning objectives (what reader will be able to do)
- Prerequisites stated explicitly
- Estimated engagement time

**Body:**
- Conceptual foundation with visual aids
- Specification of what we're building
- Guided implementation with tested code
- AI collaboration moments (reader + AI solving together)
- Deliberate challenge points

**Closing:**
- "Try With AI" practical activity
- References in IEEE format

**Metadata:**
- Author, version, last verified date
- Software versions tested against
- Hardware requirements if applicable

### XXXVII. Visual Standards

- All diagrams MUST include descriptive alt text
- Screenshots MUST show actual tool output
- Code blocks MUST specify language for syntax highlighting
- Architecture diagrams MUST use consistent notation
- No decorative images without educational purpose

---

## Quality Framework

### XXXVIII. Content Review Gates

Before any content publishes, it MUST pass:

**Technical Verification**
- [ ] All code executes on Ubuntu 22.04 LTS
- [ ] Commands produce documented output
- [ ] Software versions explicitly stated
- [ ] Hardware requirements accurate

**Citation Compliance**
- [ ] All factual claims have IEEE citations
- [ ] Sources verified against hierarchy
- [ ] No unattributed external code
- [ ] Links validated and accessible

**Plagiarism Check**
- [ ] Content passed plagiarism detection tools
- [ ] All external content properly attributed
- [ ] Paraphrased content genuinely transformed
- [ ] AI-assisted content disclosed where applicable

**Educational Quality**
- [ ] Learning objectives measurable
- [ ] Progressive complexity maintained
- [ ] AI collaboration moments present
- [ ] "Try With AI" activity included

**Accessibility Compliance**
- [ ] WCAG 2.1 AA standards met
- [ ] Alt text on all images
- [ ] Keyboard navigation functional
- [ ] Screen reader compatible
- [ ] Colour contrast validated

**Localization Readiness**
- [ ] Content structured for translation
- [ ] No culture-specific idioms
- [ ] Code comments in English
- [ ] RTL-compatible layout

**Safety Compliance (for robotics content)**
- [ ] Safety warnings included for physical operations
- [ ] Simulation-first approach emphasized
- [ ] Hardware limits documented
- [ ] Emergency procedures referenced

### XXXIX. Success Criteria

A chapter succeeds when it achieves:

**Learning Success**
- Reader can perform new tasks independently
- Concepts connect to prior knowledge
- Confidence increases measurably

**Technical Success**
- All code runs without modification
- All claims withstand verification
- Examples reflect production patterns

**Experience Success**
- Tone remains accessible and encouraging
- Teaching framework invisible to reader
- Guidance feels natural, not prescriptive

### XL. Continuous Verification

Content degrades as technology evolves. Establish:
- Quarterly review of all code examples
- Automated link checking
- Version compatibility testing on new releases
- Reader feedback integration pipeline
- Safety incident review and content updates
- Accessibility audit on major updates

---

## Development Workflow

### XLI. Content Creation Cycle

1. **Specify** — Define chapter objectives, prerequisites, outcomes
2. **Plan** — Design learning sequence and AI collaboration points
3. **Draft** — Generate content through AI-assisted workflow
4. **Verify** — Test all code, check all citations, validate claims
5. **Review** — Technical, pedagogical, plagiarism, accessibility, and safety review
6. **Publish** — Deploy to platform

### XLII. Collaboration Protocol

**Roles:**
- **Orchestrator**: Establishes scope and context
- **Planner**: Designs learning sequence
- **Writer**: Produces clear, accurate content
- **Reviewer**: Validates correctness and experience
- **Safety Officer**: Reviews robotics content for safety compliance
- **Accessibility Reviewer**: Ensures WCAG compliance

**Golden Rule:**
Never invent. If context is missing, ask rather than assume. If verification fails, state the limitation rather than guess.

### XLIII. Version Control

```
main        — Production content, always deployable
develop     — Integration branch for review
feature/*   — New content development
fix/*       — Corrections and updates
```

**Commit Format:**
```
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, safety, a11y
Scope: module1, module2, module3, module4, platform, assistant, ecosystem
```

---

## Governance

### XLIV. Authority

This constitution governs all content, code, and platform decisions across the entire multi-book ecosystem. When conflicts arise between convenience and constitution, constitution prevails.

### XLV. Amendments

**Minor refinements**: Documentation clarification, example updates → PATCH version
**Major changes**: New principles, modified standards → MINOR version
**Breaking changes**: Fundamental philosophy shifts → MAJOR version

Every amendment requires:
- Written justification
- Impact assessment
- Migration plan for existing content
- Version increment

### XLVI. Compliance

- All contributions MUST be verified against these standards
- Content failing citation or plagiarism requirements MUST be rejected
- Technical claims without verification MUST be flagged
- Safety violations MUST trigger immediate review
- Accessibility failures MUST be remediated before publication
- No exceptions for deadlines or convenience

---

## Vision

We are building more than books. We are creating an intelligent educational ecosystem that proves technical education can be rigorous and accessible, verified and engaging, comprehensive and personalized.

Physical AI will reshape how humans work alongside machines. The people who understand this technology—who can think clearly about embodied intelligence, robot perception, and human-machine collaboration—will shape that future.

Our mission is to create those people across every domain we serve. Not by telling them what to memorize, but by teaching them how to think, verify, build, and iterate in partnership with AI.

This constitution ensures we succeed.

---

## References

[1] Panaversity, "Physical AI & Humanoid Robotics Course," Panaversity.org, 2025. [Online]. Available: https://panaversity.org

---

**Version**: 1.1.1 | **Ratified**: 2025-12-01 | **Last Amended**: 2025-12-01
