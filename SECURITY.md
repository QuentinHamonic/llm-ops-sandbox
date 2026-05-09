# Security Policy

LLM Ops Sandbox is a local learning project for observable LLM serving. It is not a production security product.

Security matters anyway: the project is designed to avoid secrets in the repository, avoid prompt/data leakage, and keep operational behavior explicit.

## Supported versions

| Version | Supported |
| --- | --- |
| `v0.x` | Best-effort security fixes while the project is in active development |
| `v1.x` | Planned future stable support |

## Reporting a vulnerability

If this repository is hosted on GitHub, use private vulnerability reporting when available.

If private reporting is not available, open a minimal public issue that says a security concern exists, without exploit details, secrets, logs, tokens, payloads, or private data.

Do not publish:

- working exploit steps;
- credentials, API keys or tokens;
- private prompts or model outputs;
- personal data;
- infrastructure details that are not already public.

Expected response for a learning project:

- acknowledge the report when seen;
- reproduce the issue locally if possible;
- document the impact;
- fix or document the limitation;
- add a regression test when the issue is code-related.

## Security boundaries

Current version:

- runs locally by default;
- exposes a mock LLM backend by default;
- can call a local Ollama server when configured;
- exposes Prometheus metrics;
- has no authentication layer;
- is not intended to be exposed directly to the public internet.

Do not deploy this project on a public network without adding authentication, rate limiting, TLS termination, secret management, logging policy, and hardening.

## Secrets policy

Never commit:

- `.env`;
- tokens;
- passwords;
- private keys;
- cloud credentials;
- production URLs;
- real customer, employer or personal data.

Use environment variables and local `.env` files for local configuration. Keep `.env.example` safe, fake and minimal.

## Data and logging policy

The project should not log prompt bodies, generated replies, authorization headers, cookies or secrets.

Metrics labels must stay low-cardinality and must not contain user text, prompts, model output, IP addresses, emails, names, tokens or identifiers.

If future tracing or structured logging is added, it must include a privacy review before being committed.

## Dependency policy

- Prefer official images and well-known packages.
- Pin container image versions where practical.
- Keep the dependency list small.
- Document new external services before adding them.
- Treat LLM backends and generated outputs as untrusted.

## Responsible defaults

The default backend is `mock` so the API can be tested without external calls or model downloads.

Any future backend that sends data outside the local machine must be opt-in, documented clearly, and disabled by default.
