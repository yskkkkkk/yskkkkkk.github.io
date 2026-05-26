import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://yskkkkkk.github.io',
  integrations: [sitemap()],
});
