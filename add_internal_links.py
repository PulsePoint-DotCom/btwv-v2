#!/usr/bin/env python3
"""Add internal links to BTWV article pages."""

import re
import os

# Signal map: sig-id -> (article filename, title snippet for matching)
SIGNALS = {
    "sig-001": ("article-sig-001.html", "OpenAI memory upgrade"),
    "sig-002": ("article-sig-002.html", "Lovable AI coding"),
    "sig-003": ("article-sig-003.html", "Nomad List AI stacks"),
    "sig-004": ("article-sig-004.html", "AI email assistant $4,200"),
    "sig-005": ("article-sig-005.html", "AI generated podcast"),
    "sig-006": ("article-sig-006.html", "Mistral Mesmer"),
    "sig-007": ("article-sig-007.html", "Sam Altman cryptic"),
    "sig-008": ("article-sig-008.html", "Nvidia DLSS 4"),
    "sig-009": ("article-sig-009.html", "AI faceless YouTube channel"),
    "sig-010": ("article-sig-010.html", "Fireship AI coding tools"),
    "sig-011": ("article-sig-011.html", "NBA AI injury predictor"),
    "sig-012": ("article-sig-012.html", "AI Billboard Hot 100"),
    "sig-013": ("article-sig-013.html", "Lex Fridman 1B downloads"),
    "sig-014": ("article-sig-014.html", "Steam AI game tags"),
    "sig-015": ("article-sig-015.html", "FIFA AI referee"),
    "sig-016": ("article-sig-016.html", "Spotify AI DJ"),
    "sig-017": ("article-sig-017.html", "Google sarcasm detector"),
    "sig-018": ("article-sig-018.html", "Marc Andreessen AI-native"),
    "sig-019": ("article-sig-019.html", "Nintendo Switch 2 AI upscaling"),
    "sig-020": ("article-sig-020.html", "TikTok breakup algorithm"),
    "sig-021": ("article-sig-021.html", "NFL AI play calling"),
    "sig-022": ("article-sig-022.html", "AI music theory TwoSet"),
    "sig-023": ("article-sig-023.html", "AI Oscar short film"),
    "sig-024": ("article-sig-024.html", "Roblox AI NPCs"),
}

# Categories for cross-linking
CATEGORIES = {
    "sig-001": "AI", "sig-002": "Tech", "sig-003": "Business",
    "sig-004": "Business", "sig-005": "Culture", "sig-006": "AI",
    "sig-007": "AI", "sig-008": "Gaming", "sig-009": "Business",
    "sig-010": "Tech", "sig-011": "Sports", "sig-012": "Music",
    "sig-013": "Culture", "sig-014": "Gaming", "sig-015": "Sports",
    "sig-016": "Music", "sig-017": "Tech", "sig-018": "Business",
    "sig-019": "Gaming", "sig-020": "Culture", "sig-021": "Sports",
    "sig-022": "Music", "sig-023": "Culture", "sig-024": "Gaming",
}

# Related signals for each article (format: (sig-id, display title, context))
RELATED = {
    "sig-001": [
        ("sig-006", "Mistral's Mesmer model", "AI"),
        ("sig-007", "Sam Altman's cryptic post", "AI"),
        ("sig-017", "Google's sarcasm detector", "AI"),
    ],
    "sig-002": [
        ("sig-010", "Fireship's AI coding comparison", "Tech"),
        ("sig-004", "AI email assistant breakdown", "Business"),
        ("sig-009", "AI faceless YouTube channel", "Business"),
    ],
    "sig-003": [
        ("sig-018", "Marc Andreessen on AI-native startups", "Business"),
        ("sig-004", "Developer $4.2k/mo AI assistant", "Business"),
        ("sig-001", "ChatGPT memory upgrade", "AI"),
    ],
    "sig-004": [
        ("sig-001", "OpenAI's memory upgrade", "AI"),
        ("sig-006", "Mistral Mesmer model", "AI"),
        ("sig-009", "AI faceless YouTube channel", "Business"),
    ],
    "sig-005": [
        ("sig-012", "AI song on Billboard Hot 100", "Culture"),
        ("sig-022", "AI music theory explainer", "Music"),
        ("sig-023", "AI Oscar short film", "Culture"),
    ],
    "sig-006": [
        ("sig-001", "ChatGPT memory upgrade", "AI"),
        ("sig-007", "Sam Altman cryptic post", "AI"),
        ("sig-017", "Google sarcasm detector", "AI"),
    ],
    "sig-007": [
        ("sig-001", "OpenAI memory upgrade", "AI"),
        ("sig-006", "Mistral Mesmer model", "AI"),
        ("sig-018", "Marc Andreessen AI-native startups", "Business"),
    ],
    "sig-008": [
        ("sig-019", "Nintendo Switch 2 AI upscaling", "Gaming"),
        ("sig-014", "Steam AI game tags", "Gaming"),
        ("sig-024", "Roblox AI NPCs", "Gaming"),
    ],
    "sig-009": [
        ("sig-005", "AI-generated podcast", "Culture"),
        ("sig-002", "Lovable AI coding tool", "Tech"),
        ("sig-012", "AI song on Billboard", "Music"),
    ],
    "sig-010": [
        ("sig-002", "Lovable AI coding tool", "Tech"),
        ("sig-004", "AI email assistant", "Business"),
        ("sig-017", "Google sarcasm detector", "Tech"),
    ],
    "sig-011": [
        ("sig-015", "FIFA AI referee system", "Sports"),
        ("sig-021", "NFL AI play calling", "Sports"),
        ("sig-008", "Nvidia DLSS 4 gaming", "Gaming"),
    ],
    "sig-012": [
        ("sig-022", "AI music theory explainer", "Music"),
        ("sig-005", "AI-generated podcast", "Culture"),
        ("sig-016", "Spotify AI DJ", "Music"),
    ],
    "sig-013": [
        ("sig-007", "Sam Altman cryptic post", "AI"),
        ("sig-001", "ChatGPT memory upgrade", "AI"),
        ("sig-005", "AI-generated podcast", "Culture"),
    ],
    "sig-014": [
        ("sig-008", "Nvidia DLSS 4", "Gaming"),
        ("sig-019", "Nintendo Switch 2 AI upscaling", "Gaming"),
        ("sig-024", "Roblox AI NPCs", "Gaming"),
    ],
    "sig-015": [
        ("sig-011", "NBA AI injury predictor", "Sports"),
        ("sig-021", "NFL AI play calling", "Sports"),
        ("sig-017", "Google sarcasm detector", "Tech"),
    ],
    "sig-016": [
        ("sig-012", "AI song on Billboard Hot 100", "Music"),
        ("sig-022", "AI music theory explainer", "Music"),
        ("sig-005", "AI-generated podcast", "Culture"),
    ],
    "sig-017": [
        ("sig-001", "OpenAI memory upgrade", "AI"),
        ("sig-006", "Mistral Mesmer model", "AI"),
        ("sig-007", "Sam Altman cryptic post", "AI"),
    ],
    "sig-018": [
        ("sig-003", "Nomad List AI stacks by city", "Business"),
        ("sig-004", "Developer $4.2k/mo AI assistant", "Business"),
        ("sig-009", "AI faceless YouTube channel", "Business"),
    ],
    "sig-019": [
        ("sig-008", "Nvidia DLSS 4", "Gaming"),
        ("sig-014", "Steam AI game tags", "Gaming"),
        ("sig-024", "Roblox AI NPCs", "Gaming"),
    ],
    "sig-020": [
        ("sig-023", "AI Oscar short film", "Culture"),
        ("sig-005", "AI-generated podcast", "Culture"),
        ("sig-013", "Lex Fridman 1B downloads", "Culture"),
    ],
    "sig-021": [
        ("sig-011", "NBA AI injury predictor", "Sports"),
        ("sig-015", "FIFA AI referee system", "Sports"),
        ("sig-008", "Nvidia DLSS 4 gaming", "Gaming"),
    ],
    "sig-022": [
        ("sig-012", "AI song on Billboard Hot 100", "Music"),
        ("sig-016", "Spotify AI DJ", "Music"),
        ("sig-005", "AI-generated podcast", "Culture"),
    ],
    "sig-023": [
        ("sig-005", "AI-generated podcast", "Culture"),
        ("sig-020", "TikTok breakup algorithm", "Culture"),
        ("sig-012", "AI song on Billboard", "Music"),
    ],
    "sig-024": [
        ("sig-008", "Nvidia DLSS 4", "Gaming"),
        ("sig-014", "Steam AI game tags", "Gaming"),
        ("sig-019", "Nintendo Switch 2 AI upscaling", "Gaming"),
    ],
}

def get_related_html(sig_id):
    """Generate the related signals HTML."""
    if sig_id not in RELATED:
        return ""
    links = RELATED[sig_id]
    items_html = ""
    for rel_sig, title, cat in links:
        fname = SIGNALS[rel_sig][0]
        items_html += f'      <li><a href="{fname}">{title}</a> <span>{cat} · Signal {rel_sig.replace("sig-", "")}</span></li>\n'
    return f"""
  <div class="related-signals">
    <h3>Related Signals</h3>
    <ul class="related-list">
{items_html}    </ul>
  </div>"""

RELATED_CSS = """
    .related-signals { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin: 40px 0; }
    .related-signals h3 { font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 700; margin: 0 0 16px; }
    .related-list { list-style: none; margin: 0; padding: 0; }
    .related-list li { margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid var(--border); }
    .related-list li:last-child { margin-bottom: 0; padding-bottom: 0; border-bottom: none; }
    .related-list a { font-weight: 500; }
    .related-list span { display: block; font-size: 0.8rem; color: var(--text-sec); margin-top: 2px; }
"""

def process_article(filepath, sig_id):
    """Add internal links and CSS to an article."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has related-signals section
    if 'related-signals' in content:
        print(f"  SKIP {sig_id} (already has related signals)")
        return

    related_html = get_related_html(sig_id)
    if not related_html:
        print(f"  SKIP {sig_id} (no related defined)")
        return

    # Inject CSS before </style>
    if '</style>' in content and '.related-signals' not in content:
        content = content.replace('</style>', RELATED_CSS + '\n  </style>')

    # Add related signals section after the first ad-placeholder (between sections)
    marker = '<div class="ad-placeholder">📢 Advertisement</div>'
    if marker in content:
        parts = content.split(marker, 2)
        if len(parts) >= 2:
            new_content = parts[0] + marker + related_html + ''.join(parts[1:])
        else:
            new_content = content
    else:
        # Try inserting before footer
        footer_marker = '<footer>'
        if footer_marker in content:
            parts = content.split(footer_marker, 1)
            new_content = parts[0] + related_html + '\n' + footer_marker + parts[1]
        else:
            new_content = content + related_html

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  UPDATED {sig_id}")

def main():
    base = "/Users/masonbacotti/projects/before-they-went-viral"
    for sig_id, (fname, title) in SIGNALS.items():
        filepath = os.path.join(base, fname)
        if os.path.exists(filepath):
            process_article(filepath, sig_id)
        else:
            print(f"  MISSING {sig_id}: {fname}")

if __name__ == "__main__":
    main()
