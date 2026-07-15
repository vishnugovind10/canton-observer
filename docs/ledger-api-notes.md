# JSON Ledger API notes

Status: **EXPERIMENTAL — not verified against LocalNet**.

The adapter is limited to `GET /v2/parties` and `POST /v2/state/active-contracts`. The latter accepts an event filter scoped to the subject party. No `/v2/commands/*`, package upload, party allocation, or topology mutation endpoint is implemented.

Digital Asset documents the [JSON Ledger API v2 service](https://docs.digitalasset.com/build/3.5/explanations/json-api/index.html), the [OpenAPI definition](https://docs.digitalasset.com/build/3.5/reference/json-api/openapi.html), and [LocalNet JSON API ports and authentication](https://docs.digitalasset.com/build/3.5/quickstart/configure/project-structure-overview.html). The blocking ACS endpoint is suitable for prototypes but the official documentation recommends WebSockets for production-scale reads.

The LocalNet test is marked `localnet` and skipped by default. It must not be unskipped until authentication, response decoding, ledger-offset capture, and the official Quickstart are exercised end to end.
