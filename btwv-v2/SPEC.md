# Before They Went Viral — SPEC.md (v2)

## 1. Concept & Vision

**"Before They Went Viral"** is a discovery platform that surfaces the earliest signals of content, products, and trends about to explode — before the mainstream catches on. Each signal links to a deep-dive article (3-10 min read) explaining *why* it will go viral and *why we think so*.

The vibe is sharp, editorial, and data-driven — like a smart friend who always knows what's next before it hits your feed. Light mode, clean, trustworthy.

**Updated 2026-06-14:** Now with genre-based navigation, full article pages, About/Contact pages, and AdSense-ready structure.

---

## 2. Design Language

**Aesthetic Direction:** Clean editorial light mode — trustworthy, readable, AdSense-friendly. Think The Atlantic meets a modern web publication.

**Color Palette:**
- Background: `#ffffff`
- Surface: `#f5f5f5`
- Surface2: `#eeeeee`
- Border: `#e0e0e0`
- Primary Text: `#1a1a1a`
- Secondary Text: `#666666`
- Accent: `#ff6b35` (warm orange — urgency, early signals)
- Signal Green: `#16a34a`
- Signal Yellow: `#ca8a04`
- Signal Red: `#dc2626`

**Typography:**
- Headlines: `Space Grotesk` (bold, technical)
- Body: `IBM Plex Sans` (clean, readable)
- Monospace: `IBM Plex Mono` (data points, timestamps)

**Spatial System:**
- Base unit: 8px
- Card padding: 24px
- Section gaps: 48px
- Max content width: 720px (articles), 1200px (grid)

**Motion:**
- Cards: fade-in on load, lift on hover (translateY -2px)
- Tab switch: fade transition 200ms
- Article page: smooth scroll

---

## 3. Layout & Structure

### Pages

1. **index.html** — Main signals grid with genre tabs
2. **article-{id}.html** — Full article for each signal (3-10 min read)
3. **about.html** — About the project
4. **contact.html** — Contact page

### index.html Layout

**Header:**
- Logo: "Before They Went Viral" ⚡
- Nav: Home / About / Contact

**Hero:**
- Headline: "Spot what's next. Before it explodes."
- Subtext: "Early signals tracked across Tech, Sports, Culture & more."
- Stats: X signals tracked · Last updated: X

**Genre Tabs:**
- All · Tech · Sports · Culture · Viral · Music · Business · Gaming · AI

**Signal Grid:**
- 3-column responsive grid
- Cards sorted by signal score (hottest first)

**Footer:**
- "Updated daily by AI intelligence"
- Links: About · Contact · Privacy

### Article Page Layout

**Header:** Same nav as index

**Article Header:**
- Genre badge
- Headline
- Subheadline (1-sentence hook)
- Meta: Signal score · Read time · Date

**Article Body (3-10 min read):**
- "Why this will go viral" section
- "The signals" — key data points
- "What we're seeing" — analysis
- "Who should watch this" — audience
- Ad placeholder (middle of article)

**Footer:**
- "Back to signals" link
- Related articles

### About Page
- What this site is
- How we find signals
- The team
- FAQ

### Contact Page
- Contact form (name, email, message)
- Social links

---

## 4. Features & Interactions

### Genre Tabs
- Click tab → filters grid to that genre
- Active tab: accent underline + bold
- Smooth fade transition on filter

### Signal Cards (on index)
- Genre badge + source
- Headline (2 lines max)
- Description (2 lines max)
- Signal score pill (color-coded)
- Time ago
- "Read article →" link

### Signal Score Pills
- 0-30: Cold (gray)
- 31-60: Warming (yellow)
- 61-80: Hot (orange)
- 81-100: Exploding (red)

### Article Pages
- "Read article" goes to internal article page (not external)
- Each article: 600-1500 words (3-10 min read)
- Structured sections with headers
- Ad placeholders (2 per article)

### Search
- Real-time filter as user types
- Searches headline + description

### Daily Auto-Update (cron)
- I run a daily search across Reddit, X, Product Hunt, Google Trends, news
- Find 2-5 new signals per day
- Write article content for each
- Add to index.html signals array
- Redeploy

---

## 5. Component Inventory

### SignalCard
```
[Genre Badge] [Source]     2h ago
─────────────────────────────────────
Headline goes here, max 2 lines
Description text, max 2 lines...
─────────────────────────────────────
[Signal: 78] [~4 min read] [Read →]
```

### GenreTab
States: default (gray), active (accent underline), hover (darken)

### ArticlePage
- Header with nav
- Article header block
- Body with structured sections
- Ad placeholders (2)
- Footer with back link

### AboutPage / ContactPage
- Standard content pages
- Contact form with validation

---

## 6. Technical Approach

**Stack:** Plain HTML/CSS/JS — no framework needed.

**File Structure:**
```
before-they-went-viral/
  index.html          — main grid page
  about.html          — about page
  contact.html        — contact page
  article-{id}.html   — one per signal
  SPEC.md
```

**Signal Data Model:**
```javascript
{
  id: "sig-001",
  source: "reddit",
  sourceName: "r/ChatGPT",
  headline: "Headline here",
  description: "Description here",
  metric: "8.2k upvotes",
  signalScore: 94,
  genre: "AI",  // Tech|Sports|Culture|Viral|Music|Business|Gaming|AI
  timeAgo: "45 minutes ago",
  readTime: 4,  // minutes
  isNew: true
}
```

**Article Page Data Model (in HTML):**
```html
<article>
  <header>Genre · Read time · Date</header>
  <h1>Headline</h1>
  <section class="why-viral">Why this will go viral</section>
  <section class="the-signals">Key data points</section>
  <section class="analysis">What we're seeing</section>
  <section class="who-watch">Who should watch this</section>
</article>
```

**Deployment:**
- `CLOUDFLARE_API_TOKEN=*** wrangler pages deploy . --project-name=before-they-went-viral`

**Auto-Update Cron:**
- Daily cron job runs me (PuckwudgieBot) to search for new signals
- I write article content, update index.html, redeploy
- All automated once set up

---

## 7. Genre Categories

- **Tech** — Apps, AI, software, gadgets
- **Sports** — Athletes, teams, moments
- **Culture** — Internet trends, memes, social phenomena
- **Viral** — Content, videos, posts gaining massive traction
- **Music** — Artists, songs, albums
- **Business** — Startups, entrepreneurs, money moves
- **Gaming** — Games, streamers, esports
- **AI** — Artificial intelligence specific

---

## 8. AdSense Strategy

**Requirements:** 50+ articles, valuable content, good UX.

**Placements:**
- Header ad (auto)
- Middle of each article (manual placeholder)
- Footer ad (auto)
- Sidebar on desktop (index page)

**Article target:** 600-1500 words each for 3-10 min reads.

**Launch:** Start with 18 articles (current signals), add 2-5 daily via cron until 50+.
