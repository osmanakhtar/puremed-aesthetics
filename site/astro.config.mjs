import { defineConfig } from 'astro/config';

export default defineConfig({
  build: {
    // Single-file HTML pages: the Stage review tool on the Pi serves prototype
    // pages standalone and cannot serve extracted /_astro/*.css files.
    inlineStylesheets: 'always',
  },
});
