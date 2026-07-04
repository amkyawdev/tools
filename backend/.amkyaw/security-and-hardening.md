---
name: security-and-hardening
description: Hardens code against vulnerabilities.
---

# Security and Hardening

Security-first development. Every external input is hostile, every secret is sacred.

## Three-Tier System
- Always: validate input, parameterize queries, encode output, HTTPS, hash passwords, security headers, httpOnly cookies, npm audit
- Ask first: new auth flows, sensitive data, external integrations, CORS changes, file uploads
- Never: commit secrets, log sensitive data, trust client validation, eval()/innerHTML with user data, expose stack traces

## OWASP Prevention: Injection (parameterized queries), Broken Auth (bcrypt + secure sessions), XSS (framework escaping), Broken Access Control (check ownership), Security Misconfig (helmet + CSP), SSRF (allowlist + DNS check)

## AI/LLM: Treat model output as untrusted, never prompt-as-security-boundary, scope tool permissions