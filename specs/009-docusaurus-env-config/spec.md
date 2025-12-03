# Feature Specification: Docusaurus Environment Configuration

**Feature Branch**: `009-docusaurus-env-config`
**Created**: 2025-12-03
**Status**: Draft
**Input**: User description: "externalize the url and base url as configuration from the docusaurus configuration code, it should not be limited to a platform, rather the deployment engineer should be able to inject the environmental relevant url and base url."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy to Custom Domain (Priority: P1)

A deployment engineer needs to deploy the documentation site to a custom domain (e.g., `docs.company.com`) without modifying any source code. They should be able to provide the URL and base path through environment configuration at build time.

**Why this priority**: This is the core requirement - enabling platform-agnostic deployment. Without this, every deployment target requires code changes.

**Independent Test**: Can be fully tested by setting environment variables before build and verifying the generated site uses the configured values.

**Acceptance Scenarios**:

1. **Given** environment variables are set for URL and base URL, **When** the site is built, **Then** the built site uses the environment-provided values instead of hardcoded defaults.
2. **Given** no environment variables are set, **When** the site is built, **Then** the built site uses sensible default values that allow local development.
3. **Given** the URL environment variable is set to `https://docs.example.com`, **When** the site is built and deployed, **Then** all absolute URLs in the generated site point to `https://docs.example.com`.

---

### User Story 2 - Deploy to Subdirectory (Priority: P1)

A deployment engineer needs to deploy the site to a subdirectory path (e.g., `/docs/` or `/manual/`) on an existing domain. They should be able to configure this base path without code changes.

**Why this priority**: Equal priority to URL configuration as both are needed for most deployments.

**Independent Test**: Can be tested by setting base URL environment variable and verifying all asset paths and internal links use the configured base path.

**Acceptance Scenarios**:

1. **Given** base URL is set to `/manual/`, **When** the site is built, **Then** all internal links and asset paths are prefixed with `/manual/`.
2. **Given** base URL is set to `/` (root), **When** the site is built, **Then** the site works correctly at the domain root without any path prefix.
3. **Given** base URL contains trailing slash `/docs/`, **When** the site is built, **Then** the configuration is accepted and works correctly.

---

### User Story 3 - Multi-Environment Deployment (Priority: P2)

A DevOps team maintains multiple deployment environments (development, staging, production) each with different URLs. They should be able to use the same build process with different environment configurations.

**Why this priority**: Supports CI/CD workflows which are common but secondary to basic deployment capability.

**Independent Test**: Can be tested by running builds with different environment configurations and verifying each produces correctly configured output.

**Acceptance Scenarios**:

1. **Given** a CI/CD pipeline with environment-specific variables, **When** builds run for different environments, **Then** each build produces site configured for its target environment.
2. **Given** staging URL is `https://staging.example.com` and production is `https://docs.example.com`, **When** respective builds complete, **Then** each site's metadata and links reflect the correct environment.

---

### User Story 4 - Local Development (Priority: P2)

A developer needs to run the documentation site locally for development without setting up environment variables. The site should work out of the box with sensible defaults.

**Why this priority**: Developer experience is important but secondary to production deployment needs.

**Independent Test**: Can be tested by running `npm start` without any environment configuration and verifying the site runs correctly on localhost.

**Acceptance Scenarios**:

1. **Given** no environment variables are set, **When** a developer runs the local development server, **Then** the site loads correctly on localhost with default configuration.
2. **Given** environment variables are set for production, **When** a developer runs the local development server, **Then** the development server still works correctly (development mode may override production values).

---

### Edge Cases

- What happens when URL is provided without protocol (e.g., `example.com` instead of `https://example.com`)? System should validate and warn.
- What happens when base URL doesn't start with `/`? System should normalize or warn about invalid format.
- What happens when environment variables contain invalid characters or unexpected formats? System should fail build with clear error message.
- What happens when only one of URL or base URL is configured? System should allow partial configuration with sensible defaults for unset values.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST read the site URL from the `SITE_URL` environment variable at build time.
- **FR-002**: System MUST read the base URL path from the `BASE_URL` environment variable at build time.
- **FR-003**: System MUST provide sensible default values when environment variables are not set, allowing local development without configuration.
- **FR-004**: System MUST apply configured URL and base URL to all generated pages, links, and assets.
- **FR-005**: System MUST support both static builds and development server modes with the same configuration approach.
- **FR-006**: System MUST validate that configured URL is a valid URL format with protocol (http/https).
- **FR-007**: System MUST validate that base URL starts with a forward slash (`/`).
- **FR-008**: System MUST document the environment variables and their expected formats for deployment engineers.
- **FR-009**: System MUST fail the build with a clear error message if environment variables contain invalid values.

### Key Entities

- **Site URL**: The full canonical URL where the site will be deployed (e.g., `https://docs.example.com`). Used for absolute URLs, sitemaps, and social metadata.
- **Base URL**: The path prefix under which the site is served (e.g., `/docs/` or `/`). Used for all internal navigation and asset loading.
- **Environment Configuration**: The mechanism by which deployment engineers provide URL and base URL values externally, without modifying source code.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Deployment engineers can successfully deploy the site to any custom domain by setting environment variables, with zero source code changes required.
- **SC-002**: The same build process works for at least 3 different deployment targets (local, staging, production) by only changing environment variables.
- **SC-003**: Local development works without any environment configuration - developers can run `npm start` immediately after cloning.
- **SC-004**: Build fails with a clear, actionable error message within 5 seconds when invalid configuration values are provided.
- **SC-005**: All internal links and asset paths correctly reflect the configured base URL after deployment.
- **SC-006**: Documentation for environment configuration is complete and allows a new deployment engineer to deploy to a custom domain in under 10 minutes.

## Clarifications

### Session 2025-12-03

- Q: What should the environment variable names be? → A: `SITE_URL` and `BASE_URL` (matches spec terminology, self-documenting)

## Assumptions

- Docusaurus 3.x supports reading environment variables in configuration files (standard Node.js `process.env` access).
- Environment variable names: `SITE_URL` for the canonical site URL, `BASE_URL` for the path prefix.
- Default values for local development: URL = `http://localhost:3000`, Base URL = `/`.
- The existing GitHub Pages configuration (`organizationName`, `projectName`) can remain for backward compatibility but URL/baseUrl take precedence when set.
