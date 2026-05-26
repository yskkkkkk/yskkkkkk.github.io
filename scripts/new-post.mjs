#!/usr/bin/env node

/**
 * Usage:
 *   node scripts/new-post.mjs "포스트 제목"
 *   node scripts/new-post.mjs "포스트 제목" --date 2026-05-26
 */

import { writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const BLOG_DIR = join(__dirname, '../src/content/blog');

function toSlug(title) {
  return title
    .toLowerCase()
    .replace(/[^\w\s가-힣]/g, '')  // 특수문자 제거, 한글·영문·숫자·공백 유지
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

function today() {
  return new Date().toISOString().split('T')[0];
}

function parseArgs(args) {
  const title = args.find((a) => !a.startsWith('--')) ?? '';
  const dateIdx = args.indexOf('--date');
  const date = dateIdx !== -1 ? args[dateIdx + 1] : today();
  return { title, date };
}

const { title, date } = parseArgs(process.argv.slice(2));

if (!title) {
  console.error('Error: 포스트 제목을 입력해주세요.');
  console.error('  Usage: node scripts/new-post.mjs "포스트 제목"');
  process.exit(1);
}

const slug = toSlug(title) || `post-${date}`;
const filename = `${slug}.md`;
const filepath = join(BLOG_DIR, filename);

if (existsSync(filepath)) {
  console.error(`Error: 이미 존재하는 파일입니다 → ${filename}`);
  process.exit(1);
}

const template = `---
title: "${title}"
pubDate: ${date}
description: ""
tags: []
heroImage: ""
---

`;

if (!existsSync(BLOG_DIR)) {
  mkdirSync(BLOG_DIR, { recursive: true });
}

writeFileSync(filepath, template, 'utf-8');
console.log(`✓ Created: src/content/blog/${filename}`);
