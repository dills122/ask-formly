# pnpm + Nx Formly source fixture

Two applications (`admin`, `portal`) and four libraries (`forms`, `form-helpers`,
`fields`, `validation`), with root/base and per-project TypeScript configurations.
Membership comes from `pnpm-workspace.yaml`, including an excluded package.

The admin supplier route renders a component that assigns a fields factory result
in `ngOnInit`. That factory imports a nested configuration from another library.
The leaf uses a custom Material field, wrapper and validator registered through a
third library, with validation implemented in the fourth. Portal registers the
same field name independently, to detect accidental cross-app connections.

`nx-project-graph.json` is a real Nx 23.3.0 export captured on 2026-10-15. Offline
tests import it with the root TypeScript compiler. `pnpm-lock.yaml` supports the
separate real-install qualification, which regenerates the Nx graph and also
checks package exports with TypeScript path aliases removed.

This fixture tests source discovery and tracing. Its build target is a metadata
stub; it is not a browser/AOT qualification application. See the repository's
[development instructions](../../../docs/development.md#exact-pnpm-nx-formly-fixture).
