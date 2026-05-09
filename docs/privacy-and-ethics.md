# Privacy and Ethics

LLM Ops Sandbox is designed as a public, neutral and professional learning project for LLM operations.

The project should demonstrate technical competence without exposing private work, personal context, employer data, user data, or hidden dependencies on third-party AI services.

## Principles

### Local-first by default

The default backend is `mock`. It does not call a model, an API provider or an external service.

Ollama is optional and expected to run locally. Future vLLM support should follow the same local/self-hosted principle.

Any backend that sends prompts or outputs to a third-party service must be opt-in, documented, and disabled by default.

### Data minimization

The project should use synthetic examples only.

Do not commit:

- personal conversations;
- real user prompts;
- real model outputs containing private data;
- employer or customer data;
- private infrastructure names;
- credentials or secrets.

### No prompt leakage through observability

Metrics are for service behavior, not content inspection.

Allowed metrics:

- request count;
- latency;
- error count;
- backend status;
- token or generation statistics when available and non-sensitive.

Forbidden metrics labels:

- prompt text;
- generated reply text;
- emails;
- names;
- IP addresses;
- session identifiers;
- tokens or API keys.

The API enforces this principle with regression tests: prompt content and unmatched raw paths must not appear in `/metrics`.

### Logs must stay boring

Logs should help operate the service without exposing content.

Do not log prompt bodies, generated replies, authorization headers, cookies, secrets or personal identifiers.

If future debugging requires temporary sensitive logs, they must stay local, be disabled by default, and never be committed.

### Transparency over magic

The project should make its limits visible:

- mock backend by default;
- no authentication yet;
- no production hardening yet;
- no GPU monitoring yet;
- no claim of production readiness before the relevant versions are complete.

This is more ethical than pretending the sandbox is a production platform.

### Human responsibility with AI assistance

AI can help generate code, documentation and tests, but the maintainer remains responsible for:

- architecture;
- validation;
- security review;
- privacy review;
- tests;
- documentation;
- known limitations.

Generated code is not accepted blindly.

### Sustainability and resource awareness

LLM serving can be expensive in compute and energy.

The project should prefer:

- small local models for demos;
- explicit resource requests when Kubernetes is added;
- measurement before optimization claims;
- honest documentation of GPU and compute limits.

## Practical checklist

Before committing a new feature, ask:

- Does this send data outside the local machine?
- Does this log prompts, outputs or identifiers?
- Does this add a secret or private endpoint?
- Does this increase monitoring cardinality with user-controlled data?
- Is the behavior documented in README, architecture, runbook or roadmap?
- Can the feature be tested with synthetic data?

If the answer is unclear, stop and document the decision before implementation.
