# PRODUCT SPECIFICATION TEMPLATE

(Authoritative Source of Truth)

Purpose: Define exactly what the app is, what it does, and what it must not do.
This document overrides any assumptions by the AI.

### 1.1 Product Overview

Product Name:
<Exact product name>

One-Sentence Description:
<One precise sentence describing the product and its primary function>

Problem Statement:
<Clearly define the problem being solved. Include who experiences the problem and in what context>

Target Users:

Primary User: <Role, skill level, context>

Secondary User(s): <If any>

User Environment Assumptions:

Platform(s): <Web / iOS / Android / Desktop>

Devices: <Mobile / Desktop / Tablet>

Connectivity: <Online-only / Offline support / Hybrid>

Accessibility requirements: <WCAG level, if any>

### 1.2 Goals & Non-Goals
Product Goals (Must Achieve)

G1: <Specific, measurable goal>

G2: <Specific, measurable goal>

Explicit Non-Goals (Must NOT Do)

NG1: <Feature or behavior explicitly excluded>

NG2: <Out of scope functionality>

⚠️ Any feature not explicitly listed as a goal is considered out of scope.

### 1.3 Functional Requirements
Core Features
Feature 1: <Feature Name>

Description:
<Exact behavior in plain language>

Inputs:

<Input name>: <Type, format, constraints>

Outputs:

<Output name>: <Type, format, constraints>

User Flow:

<Step-by-step interaction>

<No skipped steps>

Edge Cases:

<What happens if input is missing>

<What happens if input is invalid>

(Repeat for each feature)

### 1.4 User Stories (Strict Format)
As a <specific user type>,
when I <specific action>,
the system MUST <specific outcome>,
so that <explicit benefit>.

Example:

As a first-time user,
when I submit the signup form with valid data,
the system MUST create an account and redirect me to onboarding,
so that I can start using the product immediately.

### 1.5 Data Requirements
Data Models
Model: <Model Name>
Field Name Type Required Constraints
id UUID Yes Auto-generated
name String Yes Max 100 chars
Data Storage

Database type: <SQL / NoSQL / In-memory>

Persistence rules: <What must be stored, what must not>

### 1.6 API & Integration Requirements (If Applicable)

External APIs used: <Name + purpose>

Authentication method: <OAuth, API key, none>

Rate limits: <Exact limits>

Failure handling: <Retry / fail fast / fallback>

### 1.7 Security & Compliance

Authentication: <Required / Not required>

Authorization: <Roles & permissions>

Data sensitivity: <PII, financial, none>

Compliance: <GDPR, SOC2, none>

### 1.8 Performance Constraints

Max response time: <e.g., 300ms>

Max payload size: <e.g., 1MB>

Concurrent users: <Number>

### 1.9 Acceptance Criteria (Mandatory)

For each feature:

Given <initial state>,
When <action>,
Then <verifiable outcome>.

No feature is complete without acceptance criteria.

### 1.10 Open Questions (Must Be Resolved Before Build)

Q1: <Unclear requirement>

Q2: <Decision needed>

2. AI INSTRUCTION / EXECUTION CONTRACT

(How the AI Must Behave)

Purpose: Remove guesswork, creativity drift, and hallucination.

2.1 AI Role Definition
You are acting as:
<Role: e.g., Senior Full-Stack Engineer with 10+ years experience>

Your primary objective is:
<e.g., Produce production-ready code that exactly matches the Product Specification>

You are NOT acting as:

- A product designer
- A business strategist
- A creative writer

2.2 Source of Truth Hierarchy
Priority Order (Highest → Lowest):

1. Product Specification Document
2. This AI Instruction Document
3. User follow-up instructions
4. General best practices

If a conflict exists, follow the higher-priority source.

2.3 Assumption Policy (Critical)
You MUST NOT make assumptions.

If information is missing, ambiguous, or conflicting:

- STOP
- List the exact missing information
- Ask targeted clarification questions

2.4 Output Requirements

For all outputs, you MUST:

Be explicit and deterministic

Avoid vague language

Avoid placeholders unless explicitly requested

Use consistent naming

Follow the specified tech stack exactly

Code Output Rules (If Applicable)

No pseudo-code unless explicitly requested

No unexplained abstractions

Comment complex logic

Match file structure exactly as specified

2.5 Error Handling Expectations
For every failure scenario:

- Describe the failure
- Define system behavior
- Ensure no silent failures

2.6 Validation & Self-Check

Before responding, the AI MUST internally verify:

 All requirements are satisfied

 No non-goals are violated

 No assumptions were introduced

 Output matches acceptance criteria

If any box cannot be checked, the AI must state why.

2.7 Communication Style Constraints

Tone: <Neutral / Technical / Concise>

No emojis

No marketing language

No opinions unless explicitly asked

No additional features or improvements unless requested

2.8 Change Management
If the user asks for a change:

- Identify affected sections
- Describe impact
- Do NOT implement until confirmed

3. OPTIONAL: AI TASK PROMPT TEMPLATE

Use this when issuing tasks:

TASK:
<What you want the AI to produce>

REFERENCES:

- Product Specification vX.X
- AI Instruction Contract vX.X

DELIVERABLE FORMAT:
<Exact format: code, markdown, table, etc>

CONSTRAINTS:

- <Time, performance, stack constraints>

STOP CONDITIONS:

- Stop and ask questions if any required information is missing
