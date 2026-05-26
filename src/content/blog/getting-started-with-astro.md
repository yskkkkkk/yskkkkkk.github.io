---
title: 'Getting Started with Astro'
description: 'Astro is a modern static site generator with a focus on performance. Learn how to set up your first Astro project.'
pubDate: 2026-05-25
tags: ['astro', 'web', 'tutorial']
---

Astro is a web framework designed for content-driven websites. It ships zero JavaScript by default and only hydrates interactive components when needed — a concept called **Islands Architecture**.

## Why Astro?

- **Fast by default** — static HTML with no client-side JS unless you need it
- **Bring your own framework** — use React, Vue, Svelte, or just plain HTML
- **Content collections** — type-safe Markdown/MDX management
- **Great DX** — file-based routing, component syntax, TypeScript support

## Quick setup

```bash
npm create astro@latest
cd my-blog
npm run dev
```

That's all it takes to get a development server running at `localhost:4321`.

## Content Collections

One of Astro's best features is typed content collections. Define a schema in `src/content/config.ts` and get full TypeScript inference when querying your Markdown files.

```typescript
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
  }),
});
```

More posts coming soon!
