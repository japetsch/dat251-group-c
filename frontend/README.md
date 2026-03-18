# Blood app frontend

This frontend uses SvelteKit. It is important to distinguish this from (standalone) Svelte.
The most major difference is the inclusion of a *file-based routing* system, as well as
*server-side rendering*.

`npm` is the package manager for the project. It normally comes installed together with Node.js.
Refer to the available scripts in [package.json](./package.json) for tasks to run on the code. Scripts are ran with `npm run [script-name]`.

| Component          | Purpose                                                                  |
|--------------------|--------------------------------------------------------------------------|
| npm                | Package manager, project task runner (like Gradle or uv)                 |
| Svelte             | Building reactive User Interfaces                                        |
| SvelteKit          | Adding file-based routing, server-side rendering to Svelte               |
| Tailwind CSS       | Standardized CSS classes, preventing duplicated or conflicting CSS code  |
| vite               | Web assets bundler, development server                                   |
| TypeScript         | Type hints in JavaScript, type checking                                  |
| svelte-check       | Analyzing code for errors (semantics, accessibility, etc.)               |
| Prettier           | Code formatting                                                          |
| openapi-typescript | Generating TypeScript types from the backend's OpenAPI spec              |
| openapi-fetch      | Generating code for backend interaction, coupled with openapi-typescript |
| vitest             | Integration testing for web UIs, coupled with vite                       |

## Running the frontend

1. Make sure the backend is running on http://localhost:8000
2. (First time, and on changes in dependencies only): `npm install`
3. `npm run dev`
4. Frontend should be running at http://localhost:5173

## CI and workflow for committing code

The CI is configured to run the following scripts from [package.json](./package.json):

- `generate-api`: backend and frontend are in agreement on what features the backend makes available
- `build`: verify that the code builds properly
- `check`: run the `svelte-check` program, checking TypeScript types, semantic errors, accessibility, etc.
- `test`: run the tests
- `check-format`: check that code is formatted properly

Failure in any script (except `check-format`) blocks the building of a Docker image.

Because of this validation, it is recommended you try to run all tasks,
as well as `npm run format` before committing.

IMO, failing `svelte-check` or `tests` are acceptable on a feature branch though.

## Routing structure

As of writing, the following is the file tree under `src/routes`.
It is subject to change, but the overall structure will likely remain.

```
src/routes
├── (app)
│   ├── +layout.svelte
│   ├── app.css
│   ├── appointment
│   │   ├── list
│   │   │   ├── +page.svelte
│   │   │   └── +page.ts
│   │   └── new
│   │       ├── +page.svelte
│   │       └── +page.ts
│   └── dashboard
│       └── +page.svelte
├── +page.svelte
└── page.test.ts
```

SvelteKit will use this file tree to decide what URLs in the application will look like.
It uses the entire path of directories under `src/routes`, excluding directories with names in parentheses.
There's a fair bit of more information in the docs: [https://svelte.dev/docs/kit/routing](https://svelte.dev/docs/kit/routing)

For example, http://localhost:5173/apppointment/new refers to the file under `(app)/appointment/new/+page.svelte`.
Notice how `(app)` is excluded from the URL.

Another example, http://localhost:5173 is just `+page.svelte` at the top of `src/routes`.

The idea behind the `(app)` directory is locating every route that requires being logged in the same place.
`(app)/+layout.svelte` runs as a wrapper for all pages within `(app)`, and can be used to provide common structure
(navbar, auth, etc.)
