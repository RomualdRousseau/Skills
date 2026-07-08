#!/usr/bin/env python3
import base64
import os
import sys

# Inline Metadata for UV to automatically fetch dependencies
# /// script
# dependencies = []
# ///

def get_base64_image(image_path):
    """Read a local image and return its base64 representation."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def main():
    if len(sys.argv) < 2:
        print("Usage: generate_svgs.py <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1]
    os.makedirs(output_dir, exist_ok=True)

    # Search for assets in typical relative locations
    logo_dir = "wiki/analyses"
    logo_path = os.path.join(logo_dir, "Servier_Logo_RVB.png")
    logo_sign_path = os.path.join(logo_dir, "Servier_Logo_Sign_RVB.png")
    logo_sign_blanc_path = os.path.join(logo_dir, "Servier_Logo_Sign_Blanc.png")
    symbole_blanc_path = os.path.join(logo_dir, "Servier_Symbole_Blanc.png")

    if not os.path.exists(logo_path):
        # Fallback to local script relative folder if run in isolated scopes
        logo_dir = os.path.join(os.path.dirname(__file__), "../assets")
        logo_path = os.path.join(logo_dir, "Servier_Logo_RVB.png")
        logo_sign_path = os.path.join(logo_dir, "Servier_Logo_Sign_RVB.png")
        logo_sign_blanc_path = os.path.join(logo_dir, "Servier_Logo_Sign_Blanc.png")
        symbole_blanc_path = os.path.join(logo_dir, "Servier_Symbole_Blanc.png")

    logo_b64 = get_base64_image(logo_path)
    logo_sign_b64 = get_base64_image(logo_sign_path)
    logo_sign_blanc_b64 = get_base64_image(logo_sign_blanc_path)
    symbole_blanc_b64 = get_base64_image(symbole_blanc_path)

    print(f"=== Hand-Crafted Vector SVG Generator ===")
    print(f"Destination: {output_dir}")

    # Helper for card shadow defs
    def get_defs():
        return """  <defs>
    <!-- Drop Shadow Filter for Cards -->
    <filter id="card-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#0f172a" flood-opacity="0.06" />
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.04" />
    </filter>
  </defs>"""

    # Helper for background sweeping arc
    def get_bg_arc(color="#e8edf9"):
        return f'  <ellipse cx="309" cy="846" rx="525" ry="450" fill="none" stroke="{color}" stroke-width="180" opacity="0.4" pointer-events="none"/>'

    # Helper for footer band
    def get_footer(index, context="Orbit - US IT Presentation"):
        return f"""  <!-- Footer Band -->
  <g id="footer">
    <rect x="0" y="984" width="1920" height="96" fill="#f8fafc"/>
    <line x1="0" y1="984" x2="1920" y2="984" stroke="#e2e8f0" stroke-width="2"/>
    
    <!-- Left Footer Details - Space buffer x=220 to prevent overlap -->
    <text x="72" y="1042" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="18" font-weight="bold" fill="#64748b">{index}</text>
    <text x="220" y="1042" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#64748b">{context}</text>
    
    <!-- Right Footer Servier Logo -->
    <image x="1655" y="1002" width="193" height="60" href="data:image/png;base64,{logo_b64}"/>
  </g>"""

    # Helper for header elements
    def get_header(title, subtitle, badge):
        return f"""  <!-- Slide Header -->
  <g id="header">
    <!-- Category Badge -->
    <rect x="1680" y="72" width="168" height="42" rx="6" fill="#f1f5f9" stroke="#e2e8f0" stroke-width="1.5"/>
    <text x="1764" y="98" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="16" font-weight="bold" fill="#1d2366" text-anchor="middle">{badge}</text>

    <!-- Main Title -->
    <text x="72" y="112" font-family="'Segoe UI', 'Arial', sans-serif" font-size="44" font-weight="800" fill="#1d2366" letter-spacing="-0.025em">{title}</text>
    
    <!-- Subtitle -->
    <text x="72" y="152" font-family="'Segoe UI', 'Arial', sans-serif" font-size="20" fill="#64748b">{subtitle}</text>
  </g>"""

    # Icons SVGs dict
    icons = {
        "database": """
      <ellipse cx="126" cy="364" rx="10" ry="4" fill="none" stroke="#ffffff" stroke-width="2"/>
      <path d="M116 364 L116 372 A10 4 0 0 0 136 372 L136 364" fill="none" stroke="#ffffff" stroke-width="2"/>
      <path d="M116 372 L116 380 A10 4 0 0 0 136 380 L136 372" fill="none" stroke="#ffffff" stroke-width="2"/>""",
        
        "layout": """
      <rect x="716" y="360" width="28" height="28" rx="3" fill="none" stroke="#ffffff" stroke-width="2"/>
      <line x1="716" y1="368" x2="744" y2="368" stroke="#ffffff" stroke-width="1.5"/>
      <line x1="726" y1="368" x2="726" y2="388" stroke="#ffffff" stroke-width="1.5"/>""",
        
        "microscope": """
      <path d="M1324 384 L1344 384 M1328 384 L1328 376 Q1328 368 1338 368 L1340 368" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <line x1="1334" y1="362" x2="1342" y2="370" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="1326" cy="362" r="3" fill="#ffffff"/>""",
        
        "trending-up": """
      <path d="M114 382 L124 370 L130 376 L138 362" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <path d="M132 362 L138 362 L138 368" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>""",
        
        "dna": """
      <path d="M718 362 Q726 374 730 374 T742 386" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <path d="M718 386 Q726 374 730 374 T742 362" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <line x1="722" y1="367" x2="722" y2="381" stroke="#ffffff" stroke-width="1.5" opacity="0.6"/>
      <line x1="730" y1="374" x2="730" y2="374" stroke="#ffffff" stroke-width="1.5" opacity="0.6"/>
      <line x1="738" y1="381" x2="738" y2="367" stroke="#ffffff" stroke-width="1.5" opacity="0.6"/>""",
        
        "star": """
      <polygon points="1334,357 1339,368 1351,370 1342,378 1344,390 1334,384 1324,390 1326,378 1317,370 1329,368" fill="#ffffff"/>""",
        
        "users": """
      <circle cx="120" cy="368" r="6" fill="none" stroke="#ffffff" stroke-width="2"/>
      <path d="M110 382 A10 10 0 0 1 130 382" fill="none" stroke="#ffffff" stroke-width="2"/>
      <circle cx="132" cy="364" r="5" fill="none" stroke="#ffffff" stroke-width="1.8"/>
      <path d="M125 378 A7 7 0 0 1 139 378" fill="none" stroke="#ffffff" stroke-width="1.8"/>""",
        
        "shield": """
      <path d="M730 357 L742 362 L742 373 Q742 382 730 387 Q718 382 718 373 L718 362 Z" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linejoin="round"/>""",
        
        "settings": """
      <circle cx="1334" cy="374" r="6" fill="none" stroke="#ffffff" stroke-width="2.5"/>
      <path d="M1334 358 L1334 362 M1334 386 L1334 390 M1318 374 L1322 374 M1346 374 L1350 374" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>""",
        
        "puzzle": """
      <path d="M720 370 A5 5 0 0 1 730 370 L736 370 L736 376 A5 5 0 0 1 736 386 L720 386 Z" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linejoin="round"/>""",
        
        "zap": """
      <polygon points="126,358 116,374 126,374 124,390 136,370 126,370" fill="#ffffff"/>""",
        
        "cpu": """
      <rect x="718" y="362" width="24" height="24" rx="4" fill="none" stroke="#ffffff" stroke-width="2.5"/>
      <line x1="712" y1="368" x2="718" y2="368" stroke="#ffffff" stroke-width="2"/>
      <line x1="712" y1="380" x2="718" y2="380" stroke="#ffffff" stroke-width="2"/>
      <line x1="742" y1="368" x2="748" y2="368" stroke="#ffffff" stroke-width="2"/>
      <line x1="742" y1="380" x2="748" y2="380" stroke="#ffffff" stroke-width="2"/>""",
        
        "git-branch": """
      <circle cx="1324" cy="364" r="3.5" fill="none" stroke="#ffffff" stroke-width="2"/>
      <circle cx="1324" cy="384" r="3.5" fill="none" stroke="#ffffff" stroke-width="2"/>
      <circle cx="1344" cy="364" r="3.5" fill="none" stroke="#ffffff" stroke-width="2"/>
      <path d="M1324 368 L1324 380 Q1324 374 1340 367" fill="none" stroke="#ffffff" stroke-width="2"/>""",
        
        "file-text": """
      <rect x="114" y="358" width="24" height="32" rx="3" fill="none" stroke="#ffffff" stroke-width="2"/>
      <line x1="120" y1="368" x2="132" y2="368" stroke="#ffffff" stroke-width="1.5"/>
      <line x1="120" y1="374" x2="132" y2="374" stroke="#ffffff" stroke-width="1.5"/>""",
        
        "code": """
      <path d="M716 370 L710 374 L716 378 M738 370 L744 374 L738 378 M730 364 L724 384" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>""",
        
        "check-circle": """
      <circle cx="1334" cy="374" r="14" fill="none" stroke="#ffffff" stroke-width="2.5"/>
      <path d="M1327 374 L1332 379 L1342 368" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>""",
        
        "book-open": """
      <path d="M112 364 Q124 360 124 384 L112 384" fill="none" stroke="#ffffff" stroke-width="2"/>
      <path d="M136 364 Q124 360 124 384 L136 384" fill="none" stroke="#ffffff" stroke-width="2"/>""",
        
        "git-commit": """
      <circle cx="730" cy="374" r="6" fill="none" stroke="#ffffff" stroke-width="2.5"/>
      <line x1="712" y1="374" x2="724" y2="374" stroke="#ffffff" stroke-width="2"/>
      <line x1="736" y1="374" x2="748" y2="374" stroke="#ffffff" stroke-width="2"/>""",
        
        "plus": """
      <line x1="112" y1="374" x2="136" y2="374" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
      <line x1="124" y1="362" x2="124" y2="386" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>""",
        
        "package": """
      <polygon points="730,358 744,365 744,381 730,388 716,381 716,365" fill="none" stroke="#ffffff" stroke-width="2"/>
      <line x1="730" y1="358" x2="730" y2="388" stroke="#ffffff" stroke-width="1.5"/>
      <line x1="730" y1="373" x2="744" y2="365" stroke="#ffffff" stroke-width="1.5"/>
      <line x1="730" y1="373" x2="716" y2="365" stroke="#ffffff" stroke-width="1.5"/>""",
        
        "upload-cloud": """
      <path d="M1324 380 A6 6 0 0 1 1334 374 A8 8 0 0 1 1344 380 L1348 380" fill="none" stroke="#ffffff" stroke-width="2.5"/>
      <path d="M1334 384 L1334 368 M1329 373 L1334 368 L1339 373" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>""",
        
        "history": """
      <path d="M120 360 A14 14 0 1 1 114 368" fill="none" stroke="#ffffff" stroke-width="2.5"/>
      <path d="M110 366 L114 368 L116 360" fill="none" stroke="#ffffff" stroke-width="2"/>
      <line x1="126" y1="368" x2="126" y2="374" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>""",
        
        "lock": """
      <rect x="718" y="368" width="24" height="20" rx="4" fill="none" stroke="#ffffff" stroke-width="2.5"/>
      <path d="M722 368 L722 362 A8 8 0 0 1 738 362 L738 368" fill="none" stroke="#ffffff" stroke-width="2"/>""",
        
        "network": """
      <rect x="1328" y="358" width="12" height="12" rx="2" fill="none" stroke="#ffffff" stroke-width="2"/>
      <rect x="1316" y="378" width="12" height="12" rx="2" fill="none" stroke="#ffffff" stroke-width="2"/>
      <rect x="1340" y="378" width="12" height="12" rx="2" fill="none" stroke="#ffffff" stroke-width="2"/>
      <path d="M1334 370 L1334 374 L1322 374 L1322 378 M1334 374 L1346 374 L1346 378" fill="none" stroke="#ffffff" stroke-width="2"/>""",
        
        "heart": """
      <path d="M730 382 Q742 370 742 364 A5 5 0 0 0 730 360 A5 5 0 0 0 718 364 Q718 370 730 382" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linejoin="round"/>""",
        
        "award": """
      <circle cx="1334" cy="366" r="10" fill="none" stroke="#ffffff" stroke-width="2.5"/>
      <polygon points="1328,376 1324,388 1334,382 1344,388 1340,376" fill="none" stroke="#ffffff" stroke-width="2"/>"""
    }

    # ==================== SLIDE 1 (TITLE) ====================
    print("Generating Slide 1 (Title)...")
    s1_logo = f'<image x="1560" y="960" width="288" height="60" href="data:image/png;base64,{logo_sign_blanc_b64}"/>' if logo_sign_blanc_b64 else ""
    s1 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Base Dark Background with rx=0 corners -->
  <rect x="0" y="0" width="1920" height="1080" rx="0" fill="#1d2366" stroke="#2c3385" stroke-width="2"/>
  
  <!-- Swept Accent Ring -->
  <ellipse cx="309" cy="846" rx="525" ry="450" fill="none" stroke="#2c3385" stroke-width="180" opacity="0.35" pointer-events="none"/>
  
  <!-- Metadata/Lab Reference -->
  <text x="144" y="320" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="20" font-weight="bold" fill="#ff5a24" letter-spacing="0.1em">ORBIT STRATEGIC BRIEFING • 2026</text>
  
  <!-- Main Title - Split into flat, non-overlapping text rows -->
  <text x="144" y="440" font-family="'Segoe UI', 'Arial', sans-serif" font-size="64" font-weight="800" fill="#ffffff" letter-spacing="-0.025em">Orbit: Scaling AI-Native</text>
  <text x="144" y="520" font-family="'Segoe UI', 'Arial', sans-serif" font-size="64" font-weight="800" fill="#ffffff" letter-spacing="-0.025em">Engineering for US IT</text>
  
  <!-- Subtitle - Split into flat, non-overlapping text rows -->
  <text x="144" y="620" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" fill="#cbd5e1" opacity="0.9">Transitioning Software Engineering from Syntax Labor to Intent Architecture.</text>
  <text x="144" y="660" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" fill="#cbd5e1" opacity="0.9">Fast, Governed, and Scaled Software Development via Skill Programming.</text>
  
  <!-- Footer Brand -->
  <g id="footer">
    <text x="144" y="1000" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="16" fill="#cbd5e1" opacity="0.6">JULY 2026 / STRATEGY SHEET</text>
    {s1_logo}
  </g>
</svg>"""
    with open(os.path.join(output_dir, "Slide1.svg"), "w", encoding="utf-8") as f:
        f.write(s1)

    # ==================== SLIDES 2, 5, 9, 13 (CHAPTER DIVIDERS) ====================
    chapters = [
        {"num": 2, "sec": "SECTION 01", "lbl": "THE CORE CHALLENGE", "title": "The Code Assistant Dilemma"},
        {"num": 5, "sec": "SECTION 02", "lbl": "ORBIT: THE OPERATING MODEL", "title": "A Unified Model for AI-Native Data Factories"},
        {"num": 9, "sec": "SECTION 03", "lbl": "US-IT EXECUTION PLAYBOOK", "title": "Implementation Details &amp; Roadmaps"},
        {"num": 13, "sec": "SECTION 04", "lbl": "THE METRICS", "title": "Enforcing Standards &amp; Measuring Success"}
    ]

    for chap in chapters:
        idx = chap["num"]
        print(f"Generating Slide {idx} (Chapter)...")
        logo_part = f'<image x="1560" y="960" width="288" height="60" href="data:image/png;base64,{logo_sign_b64}"/>' if logo_sign_b64 else ""
        s_chap = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Base Light Background with rx=0 corners -->
  <rect x="0" y="0" width="1920" height="1080" rx="0" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>
  {get_bg_arc("#e8edf9")}
  
  <!-- Section Badge -->
  <rect x="1680" y="72" width="168" height="42" rx="6" fill="#f1f5f9" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="1764" y="98" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="16" font-weight="bold" fill="#1d2366" text-anchor="middle">{chap['sec']}</text>
  
  <!-- Main Title Area -->
  <text x="144" y="440" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="20" font-weight="bold" fill="#ff5a24" letter-spacing="0.1em">{chap['lbl'].upper()}</text>
  <text x="144" y="540" font-family="'Segoe UI', 'Arial', sans-serif" font-size="56" font-weight="800" fill="#1d2366" letter-spacing="-0.025em">
    {chap['title']}
  </text>
  
  <!-- Footer Brand -->
  <g id="footer">
    <text x="144" y="1000" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="16" fill="#64748b">DATA - AI INNOVATION LAB</text>
    {logo_part}
  </g>
</svg>"""
        with open(os.path.join(output_dir, f"Slide{idx}.svg"), "w", encoding="utf-8") as f:
            f.write(s_chap)

    # ==================== SLIDE 19 (CLOSING) ====================
    print("Generating Slide 19 (Closing)...")
    s19_symbol = f'<image x="824" y="404" width="272" height="272" href="data:image/png;base64,{symbole_blanc_b64}"/>' if symbole_blanc_b64 else ""
    s19 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <!-- Base Dark Blue Background with rx=0 corners -->
  <rect x="0" y="0" width="1920" height="1080" rx="0" fill="#1d2366" stroke="#2c3385" stroke-width="2"/>
  
  <!-- Swept Quarter-Circle Accent Ring -->
  <ellipse cx="309" cy="846" rx="525" ry="450" fill="none" stroke="#2c3385" stroke-width="180" opacity="0.35" pointer-events="none"/>
  
  <!-- Centered White Corporate Symbole -->
  {s19_symbol}
</svg>"""
    with open(os.path.join(output_dir, "Slide19.svg"), "w", encoding="utf-8") as f:
        f.write(s19)

    # ==================== SLIDES 3, 12, 14 ====================
    # Hand-crafted Slide 12 TIMELINE template generator
    print("Generating Slide 12 (Roadmap Timeline)...")
    s12 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {get_defs()}
  <!-- rx=0 outer slide border -->
  <rect x="0" y="0" width="1920" height="1080" rx="0" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>
  {get_bg_arc()}
  {get_header("Project Roadmap &amp; Timeline", "Our structured milestones leading to full operational launch and handover to Run mode.", "MILESTONES")}
  
  <line x1="288" y1="374" x2="1632" y2="374" stroke="#e2e8f0" stroke-width="6"/>

  <g id="timeline-cards">
    <g id="card-1">
      <rect x="72" y="320" width="568" height="480" rx="20" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" filter="url(#card-shadow)"/>
      <circle cx="126" cy="374" r="24" fill="#1d2366"/>
      <text x="126" y="374" font-family="'Segoe UI', 'Arial', sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle" dominant-baseline="central">1</text>
      <text x="102" y="440" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="18" font-weight="bold" fill="#1d2366">JULY 2026 (TODAY)</text>
      <text x="102" y="485" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1e293b">LLM Proxy &amp; Skill Kickoff</text>
      <text x="102" y="535" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Deploy Apigee + LiteLLM gateway.</text>
      <text x="102" y="563" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Kickoff the continuous build and</text>
      <text x="102" y="591" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">packaging of the centralized Skill</text>
      <text x="102" y="619" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Repository monorepo.</text>
    </g>

    <g id="card-2">
      <rect x="676" y="320" width="568" height="480" rx="20" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" filter="url(#card-shadow)"/>
      <circle cx="730" cy="374" r="24" fill="#ff5a24"/>
      <text x="730" y="374" font-family="'Segoe UI', 'Arial', sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle" dominant-baseline="central">2</text>
      <text x="706" y="440" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="18" font-weight="bold" fill="#ff5a24">AUGUST 2026</text>
      <text x="706" y="485" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1e293b">Ongoing Build &amp; Workshops</text>
      <text x="706" y="535" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Continuous development of the skill</text>
      <text x="706" y="563" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">repository. Running localized</text>
      <text x="706" y="591" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">biostatistics/Data IT workshops,</text>
      <text x="706" y="619" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">bootcamps, and masterclasses.</text>
    </g>

    <g id="card-3">
      <rect x="1280" y="320" width="568" height="480" rx="20" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" filter="url(#card-shadow)"/>
      <circle cx="1334" cy="374" r="24" fill="#059669"/>
      <text x="1334" y="374" font-family="'Segoe UI', 'Arial', sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle" dominant-baseline="central">3</text>
      <text x="1310" y="440" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="18" font-weight="bold" fill="#059669">SEPTEMBER 2026</text>
      <text x="1310" y="485" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1e293b">Live Run &amp; FinOps Rebilling</text>
      <text x="1310" y="535" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Final Skill Repo deployment completed.</text>
      <text x="1310" y="563" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Activate full FinOps direct chargeback</text>
      <text x="1310" y="591" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">model via SNOW. Transition project</text>
      <text x="1310" y="619" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">streams to active Run mode.</text>
    </g>
  </g>
  {get_footer("12")}
</svg>"""
    with open(os.path.join(output_dir, "Slide12.svg"), "w", encoding="utf-8") as f:
        f.write(s12)

    # ==================== GENERAL CONTENT SLIDES (SLIDES 4, 6, 7, 8, 10, 11, 15, 16, 17, 18) ====================
    content_slides = [
        # SLIDE 4 - Refactored flat bullets with zero nested tspans
        {
            "num": 4, "badge": "THE THREAT", 
            "title": "The Hard Truths: The Productivity Trap",
            "subtitle": "While code assistants offer rapid speed-up, they introduce severe risks to code security and overall engineering quality.",
            "cols": [
                {
                    "x": 72, "w": 856, "title": "Hallucination &amp; Seniority Gap", "icon": "trending-up", "icon_color": "#ff5a24",
                    "lines": [
                        "• Instant Errors (High Risk):",
                        "  Assistants are extremely fast to type, but also fast",
                        "  to hallucinate incorrect syntax, paths, and APIs.",
                        "• The Expertise Gap:",
                        "  Generating AI code actually requires higher professional",
                        "  expertise to review, debug, and secure boundaries."
                    ],
                    "line_styles": {0: "font-weight='bold' fill='#1d2366'", 3: "font-weight='bold' fill='#1d2366'"}
                },
                {
                    "x": 992, "w": 856, "title": "Fragmentation &amp; Security Risks", "icon": "shield", "icon_color": "#1d2366",
                    "lines": [
                        "• Lack of Guidelines (Fragmentation):",
                        "  Without shared centralized practices, squads develop",
                        "  isolated, fragile and fragmented local codebases.",
                        "• IP Leakage &amp; Shadow IT:",
                        "  Developers copying patient or corporate data into",
                        "  unsecured public chat windows, raising compliance risks."
                    ],
                    "line_styles": {0: "font-weight='bold' fill='#1d2366'", 3: "font-weight='bold' fill='#1d2366'"}
                }
            ]
        },
        # SLIDE 6
        {
            "num": 6, "badge": "THE MISSION",
            "title": "Orbit: Fast, Governed, At Scale",
            "subtitle": "Orbit is the comprehensive operating model designed to manage and run the AI-Native Data Factory.",
            "cards": [
                {
                    "num": "1", "num_color": "#1d2366", "title": "Fast", "date": "VELOCITY", "date_color": "#1d2366",
                    "lines": [
                        "Leveraging instant code generation, automated",
                        "GKE/ETL orchestration pipelines, and",
                        "specialized local scripts to speed up",
                        "scientific pipeline turnarounds."
                    ]
                },
                {
                    "num": "2", "num_color": "#ff5a24", "title": "Governed", "date": "COMPLIANCE", "date_color": "#ff5a24",
                    "lines": [
                        "Establishing strict, centralized multi-agent",
                        "guardrails and peer reviews to prevent",
                        "silent logic hijacking, prompt injections,",
                        "and invalid outputs."
                    ]
                },
                {
                    "num": "3", "num_color": "#4f46e5", "title": "At Scale", "date": "EXTENSIBILITY", "date_color": "#4f46e5", "dashed": True,
                    "lines": [
                        "Scaling AI-Native developer velocity across",
                        "US IT squads and global R&amp;D teams by",
                        "consolidating reusable skills within",
                        "our monorepo."
                    ]
                }
            ]
        },
        # SLIDE 7
        {
            "num": 7, "badge": "OPERATING LAYERS",
            "title": "Operating Tiers of the AI-Native Data Factory",
            "subtitle": "Enforcing safety, cost transparency, and seamless execution across all layers of the organization.",
            "cards": [
                {
                    "icon": "database", "title": "Infrastructure Tier", "date": "API GATEWAYS", "date_color": "#1d2366",
                    "lines": [
                        "Secure API gateways, model-agnostic proxying,",
                        "and active FinOps chargeback tracking across",
                        "the Data Platform."
                    ]
                },
                {
                    "icon": "shield", "title": "Governance Tier", "date": "PRE-COMMIT GATE", "date_color": "#ff5a24",
                    "lines": [
                        "Automated pre-commit hooks, git-integrated",
                        "static code reviews, and central skill registries",
                        "enforcing security rules."
                    ]
                },
                {
                    "icon": "settings", "title": "Execution Tier", "date": "SQUAD COMPATIBLE", "date_color": "#4f46e5", "dashed": True,
                    "lines": [
                        "Skill-oriented workspace integrations",
                        "(custom sub-agents, CLI skills, and IDE",
                        "configurations) for local developer efficiency."
                    ]
                }
            ]
        },
        # SLIDE 8
        {
            "num": 8, "badge": "PROGRAMMING MODEL",
            "title": "The Skill-Oriented Programming Model",
            "subtitle": "Decoupling stable core services from rapidly evolving specialized developer competencies.",
            "cards": [
                {
                    "icon": "database", "title": "Core Platform", "date": "GLOBAL FOUNDATION", "date_color": "#1d2366",
                    "lines": [
                        "Standardized platform services (logging,",
                        "telemetry, database hooks) managed globally",
                        "as highly stable packages."
                    ]
                },
                {
                    "icon": "puzzle", "title": "Extensible Skills", "date": "REUSABLE MODULES", "date_color": "#ff5a24",
                    "lines": [
                        "Domain-specific, reusable developer skills",
                        "(Preprocess, Pre-train, Query, Report)",
                        "packaged and shared globally."
                    ]
                },
                {
                    "icon": "star", "title": "Specialized US Skills", "date": "LOCAL US INNOVATION", "date_color": "#4f46e5", "dashed": True,
                    "lines": [
                        "Statistical programming, biometrics automation,",
                        "and local US IT R&amp;D pipelines maintained",
                        "locally by US champions."
                    ]
                }
            ]
        },
        # SLIDE 10
        {
            "num": 10, "badge": "HYBRID ARCHITECTURE",
            "title": "Commercial vs. Open Source Hybrid Model",
            "subtitle": "A routing strategy balancing high-reasoning intelligence against low-cost, bulk processing speeds.",
            "cards": [
                {
                    "icon": "zap", "title": "Premium Commercial", "date": "CLAUDE 3.5 / GEMINI PRO", "date_color": "#1d2366",
                    "lines": [
                        "Routing complex, high-reasoning tasks (e.g.",
                        "strategic design, multi-file code refactoring,",
                        "structural reviews) to premium models."
                    ]
                },
                {
                    "icon": "cpu", "title": "Lightweight Open Source", "date": "LLAMA 3 / LOCAL MODEL", "date_color": "#ff5a24",
                    "lines": [
                        "Routing routine, bulk tasks (simple unit",
                        "tests, syntax boilerplate, basic SQL queries)",
                        "to lightweight local/hosted models."
                    ]
                },
                {
                    "icon": "git-branch", "title": "Orchestration Routing", "date": "APIGEE + LITELLM", "date_color": "#4f46e5", "dashed": True,
                    "lines": [
                        "A smart, automated routing proxy dynamically",
                        "balancing cost, speed, and context limits in",
                        "real-time with zero developer overhead."
                    ]
                }
            ]
        },
        # SLIDE 11
        {
            "num": 11, "badge": "BLUEPRINT PLAYBOOK",
            "title": "SDLC Blueprint: Code Generation to Verification",
            "subtitle": "Enforcing code standards, security gates, and quality controls at every step of the development cycle.",
            "cards": [
                {
                    "icon": "file-text", "title": "Planning &amp; Intent", "date": "01. SPECIFICATION", "date_color": "#1d2366",
                    "lines": [
                        "Developer outlines specifications using clean",
                        "Markdown prompts. High-reasoning model drafts",
                        "design logic and test plans before coding."
                    ]
                },
                {
                    "icon": "code", "title": "Coding &amp; Formatting", "date": "02. INTEGRATION", "date_color": "#ff5a24",
                    "lines": [
                        "Developer iterates code safely. Automated formatters",
                        "(Black, Ruff, Prettier) run continuously to",
                        "enforce strict visual compliance."
                    ]
                },
                {
                    "icon": "check-circle", "title": "Gating &amp; Pre-Commit", "date": "03. VERIFICATION", "date_color": "#4f46e5", "dashed": True,
                    "lines": [
                        "Pre-commit hooks run automated unit tests and",
                        "strict security/license linters. No unverified",
                        "or unformatted code is staged."
                    ]
                }
            ]
        },
        # SLIDE 15
        {
            "num": 15, "badge": "SKILL PLATFORM",
            "title": "The \"One Ring\" Skill Repository",
            "subtitle": "Consolidating all developer prompt capabilities, sub-agents, and CLI extensions in a unified registry.",
            "cards": [
                {
                    "icon": "book-open", "title": "Universal Catalog", "date": "01. DISCOVER", "date_color": "#1d2366",
                    "lines": [
                        "A single centralized, indexed skill registry",
                        "where every team catalogs their custom",
                        "sub-agents, prompts, and CLI extensions."
                    ]
                },
                {
                    "icon": "shield", "title": "Strict Verification", "date": "02. COMPATIBILITY", "date_color": "#ff5a24",
                    "lines": [
                        "All skills pass mandatory security sandboxing,",
                        "unit-testing suites, and semantic reviews",
                        "before becoming discoverable."
                    ]
                },
                {
                    "icon": "git-commit", "title": "Versioned Deployment", "date": "03. RELIABILITY", "date_color": "#4f46e5", "dashed": True,
                    "lines": [
                        "Every skill is fully versioned, allowing teams",
                        "to reference stable skill releases (@v1.2)",
                        "with zero breakages in live runs."
                    ]
                }
            ]
        },
        # SLIDE 16
        {
            "num": 16, "badge": "DEVELOPER LIFECYCLE",
            "title": "Standardizing the Skill Development Lifecycle",
            "subtitle": "Streamlining prompt engineering and skill deployment through an automated pipeline.",
            "cards": [
                {
                    "icon": "plus", "title": "1. Skill Creation", "date": "LOCAL WORKSPACE", "date_color": "#1d2366",
                    "lines": [
                        "Developer creates a new reusable CLI skill or",
                        "sub-agent prompt template in the local",
                        "environment."
                    ]
                },
                {
                    "icon": "package", "title": "2. Packaging", "date": "GLOBAL MONOREPO", "date_color": "#ff5a24",
                    "lines": [
                        "The skill is compiled, sandboxed, and pushed",
                        "to the staging branch of the global",
                        "monorepo."
                    ]
                },
                {
                    "icon": "upload-cloud", "title": "3. Deployment", "date": "AUTOMATED REGISTRY", "date_color": "#4f46e5", "dashed": True,
                    "lines": [
                        "The global CI/CD pipeline triggers tests,",
                        "signs the package, and publishes it to the",
                        "active skill registry."
                    ]
                }
            ]
        },
        # SLIDE 17
        {
            "num": 17, "badge": "GOVERNANCE OUTCOMES",
            "title": "Traceability &amp; Lineage Compliance",
            "subtitle": "Enforcing perfect clinical compliance, data isolation, and total structural auditability.",
            "cards": [
                {
                    "icon": "history", "title": "Prompt Traceability", "date": "REPLAY AUDITS", "date_color": "#1d2366",
                    "lines": [
                        "Every LLM interaction is indexed with metadata",
                        "(prompt hash, model version, system context)",
                        "for absolute behavioral replay."
                    ]
                },
                {
                    "icon": "lock", "title": "Data Sandboxing", "date": "ZERO CLOUD LEAKAGE", "date_color": "#ff5a24",
                    "lines": [
                        "Strict local routing pathways guarantee no private",
                        "patient datasets or clinical records leak to",
                        "external public models."
                    ]
                },
                {
                    "icon": "network", "title": "Dependency Lineage", "date": "SBOM VERIFICATION", "date_color": "#4f46e5", "dashed": True,
                    "lines": [
                        "Automatic SBOM (Software Bill of Materials)",
                        "compilation for all AI-generated code, mapping",
                        "exactly what was created and verified."
                    ]
                }
            ]
        },
        # SLIDE 18
        {
            "num": 18, "badge": "TRANSFORMATION",
            "title": "US-IT Participation: Driving the Transformation",
            "subtitle": "Building localized skill clusters, localized biostatistics tools, and training super-champions.",
            "cards": [
                {
                    "icon": "users", "title": "1. Joint Bootcamps", "date": "TALENT ACCELERATION", "date_color": "#1d2366",
                    "lines": [
                        "Hands-on collaborative bootcamps for",
                        "biostatisticians and Data IT squads, teaching",
                        "prompt engineering and skill programming."
                    ]
                },
                {
                    "icon": "heart", "title": "2. Pair Programming", "date": "CO-DEVELOP AUTOMATIONS", "date_color": "#ff5a24",
                    "lines": [
                        "Global core team members pair-program with",
                        "local US engineers to co-develop specialized",
                        "biometrics scripts."
                    ]
                },
                {
                    "icon": "award", "title": "3. Active Contribution", "date": "GLOBAL ACKNOWLEDGEMENT", "date_color": "#4f46e5", "dashed": True,
                    "lines": [
                        "Empowering US developers to become core",
                        "contributors, packaging local accomplishments",
                        "into global extensible skills."
                    ]
                }
            ]
        }
    ]

    for s in content_slides:
        idx = s["num"]
        print(f"Generating Slide {idx} (Content)...")
        
        s_body = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
{get_defs()}
  <!-- rx=0 base slide frame outer border -->
  <rect x="0" y="0" width="1920" height="1080" rx="0" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>
{get_bg_arc()}
{get_header(s['title'], s['subtitle'], s['badge'])}
"""

        if "cols" in s:
            s_body += "\n  <!-- 2-Column Container Grid -->\n  <g id='columns'>"
            for col in s["cols"]:
                cx = col["x"]
                cw = col["w"]
                s_body += f"""
    <g id="col-{col['title'].split()[0]}">
      <rect x="{cx}" y="320" width="{cw}" height="480" rx="20" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" filter="url(#card-shadow)"/>"""
                
                icon_path = icons[col["icon"]]
                s_body += f"""
      <rect x="{cx + 30}" y="350" width="48" height="48" rx="8" fill="{col['icon_color']}"/>
      {icon_path}
      <text x="{cx + 96}" y="382" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1d2366">{col['title']}</text>"""
                
                # Apply optional bold/color row-by-row line styles (preventing nested tspan bugs!)
                line_styles = col.get("line_styles", {})
                for dy, line in enumerate(col["lines"]):
                    line_style = line_styles.get(dy, "")
                    if line_style:
                        s_body += f'\n      <text x="{cx + 30}" y="{445 + dy*40}" font-family="\'Segoe UI\', \'Arial\', sans-serif" font-size="18" {line_style}>{line}</text>'
                    else:
                        s_body += f'\n      <text x="{cx + 30}" y="{445 + dy*40}" font-family="\'Segoe UI\', \'Arial\', sans-serif" font-size="18" fill="#475569">{line}</text>'
                
                s_body += "\n    </g>"
            s_body += "\n  </g>"

        elif "cards" in s:
            card_w = 568
            spacing = 36
            
            s_body += "\n  <!-- 3-Card Container Grid -->\n  <g id='cards'>"
            for i, card in enumerate(s["cards"]):
                card_x = 72 + i * (card_w + spacing)
                dashed_style = 'stroke-dasharray="8,6" stroke="#a5b4fc"' if card.get("dashed") else 'stroke="#e2e8f0"'
                s_body += f"""
    <g id="card-{i+1}">
      <rect x="{card_x}" y="320" width="{card_w}" height="480" rx="20" fill="#ffffff" {dashed_style} stroke-width="2" filter="url(#card-shadow)"/>"""
                
                cx = card_x + 54
                if "num" in card:
                    s_body += f"""
      <circle cx="{cx}" cy="374" r="24" fill="{card['num_color']}"/>
      <text x="{cx}" y="374" font-family="'Segoe UI', 'Arial', sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle" dominant-baseline="central">{card['num']}</text>"""
                elif "icon" in card:
                    rect_color = "#1d2366" if i == 0 else ("#ff5a24" if i == 1 else "#4f46e5")
                    icon_path = icons[card["icon"]]
                    s_body += f"""
      <rect x="{card_x + 30}" y="350" width="48" height="48" rx="8" fill="{rect_color}"/>
      {icon_path}"""
                
                title_x = card_x + 96 if ("num" in card or "icon" in card) else card_x + 30
                s_body += f'\n      <text x="{title_x}" y="{382}" font-family="\'Segoe UI\', \'Arial\', sans-serif" font-size="24" font-weight="bold" fill="#1d2366">{card["title"]}</text>'
                s_body += f'\n      <text x="{card_x + 30}" y="{440}" font-family="\'JetBrains Mono\', \'Courier New\', monospace" font-size="18" font-weight="bold" fill="{card["date_color"]}">{card["date"]}</text>'
                
                for dy, line in enumerate(card["lines"]):
                    s_body += f'\n      <text x="{card_x + 30}" y="{485 + dy*28}" font-family="\'Segoe UI\', \'Arial\', sans-serif" font-size="18" fill="#475569">{line}</text>'
                
                s_body += "\n    </g>"
            s_body += "\n  </g>"

        s_body += f"\n{get_footer(str(idx))}\n</svg>"
        with open(os.path.join(output_dir, f"Slide{idx}.svg"), "w", encoding="utf-8") as f:
            f.write(s_body)

    # Re-write Slide 3 specifically so we retain its exact handcrafted state (and eliminate nested tspans!)
    print("Regenerating Slide 3...")
    s3_handcrafted = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <!-- Drop Shadow Filter for Cards -->
    <filter id="card-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#0f172a" flood-opacity="0.06" />
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.04" />
    </filter>
  </defs>

  <!-- Base White Background with rx=0 corners and border -->
  <rect x="0" y="0" width="1920" height="1080" rx="0" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>

  <!-- Background Swept Accent Ring (Quarter-Circle Arc) -->
  <ellipse cx="309" cy="846" rx="525" ry="450" fill="none" stroke="#e8edf9" stroke-width="180" opacity="0.4" pointer-events="none"/>

  <!-- Slide Header -->
  <g id="header" transform="translate(0, 0)">
    <!-- Category Badge 'DEMAND BOOM' -->
    <rect x="1680" y="72" width="168" height="42" rx="6" fill="#f1f5f9" stroke="#e2e8f0" stroke-width="1.5"/>
    <text x="1764" y="98" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="16" font-weight="bold" fill="#1d2366" text-anchor="middle">DEMAND BOOM</text>

    <!-- Main Title -->
    <text x="72" y="112" font-family="'Segoe UI', 'Arial', sans-serif" font-size="44" font-weight="800" fill="#1d2366" letter-spacing="-0.025em">Coding Revolution: From Syntax to Intent</text>
    
    <!-- Subtitle -->
    <text x="72" y="152" font-family="'Segoe UI', 'Arial', sans-serif" font-size="20" fill="#64748b">AI assistants are shifting software production from manual typing ("Syntax Labor") to high-level guidelines ("Intent Architecture").</text>
  </g>

  <!-- Content Cards Grid -->
  <g id="content-cards">
    <!-- ================= CARD 1 ================= -->
    <g id="card-1">
      <rect x="72" y="320" width="568" height="480" rx="20" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" filter="url(#card-shadow)"/>
      <rect x="102" y="350" width="48" height="48" rx="8" fill="#1d2366"/>
      <ellipse cx="126" cy="364" rx="10" ry="4" fill="none" stroke="#ffffff" stroke-width="2"/>
      <path d="M116 364 L116 372 A10 4 0 0 0 136 372 L136 364" fill="none" stroke="#ffffff" stroke-width="2"/>
      <path d="M116 372 L116 380 A10 4 0 0 0 136 380 L136 372" fill="none" stroke="#ffffff" stroke-width="2"/>
      <text x="166" y="382" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1d2366">Data &amp; Operations</text>
      <!-- Flattened rows preventing overlapping tspan bugs -->
      <text x="102" y="445" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" font-weight="bold" fill="#1d2366">Data Engineers, Data Ops, and Analysts demand</text>
      <text x="102" y="473" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">assistants to automate complex ETL pipelines,</text>
      <text x="102" y="501" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">manage GKE/SQL queries, and accelerate</text>
      <text x="102" y="529" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">infrastructure deployments.</text>
    </g>

    <!-- ================= CARD 2 ================= -->
    <g id="card-2">
      <rect x="676" y="320" width="568" height="480" rx="20" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" filter="url(#card-shadow)"/>
      <rect x="706" y="350" width="48" height="48" rx="8" fill="#ff5a24"/>
      <rect x="716" y="360" width="28" height="28" rx="3" fill="none" stroke="#ffffff" stroke-width="2"/>
      <line x1="716" y1="368" x2="744" y2="368" stroke="#ffffff" stroke-width="1.5"/>
      <line x1="726" y1="368" x2="726" y2="388" stroke="#ffffff" stroke-width="1.5"/>
      <text x="770" y="382" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1d2366">Designers, Front &amp; PO</text>
      <!-- Flattened rows preventing overlapping tspan bugs -->
      <text x="706" y="445" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" font-weight="bold" fill="#1d2366">Front-End, UX, and Product Owners use</text>
      <text x="706" y="473" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">assistants to prototype user interfaces, auto-generate</text>
      <text x="706" y="501" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">front-end frameworks, and scaffold JIRA story</text>
      <text x="706" y="529" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">logic directly.</text>
    </g>

    <!-- ================= CARD 3 ================= -->
    <g id="card-3">
      <rect x="1280" y="320" width="568" height="480" rx="20" fill="#ffffff" stroke="#a5b4fc" stroke-width="2" stroke-dasharray="8,6" filter="url(#card-shadow)"/>
      <rect x="1310" y="350" width="48" height="48" rx="8" fill="#4f46e5"/>
      <path d="M1324 384 L1344 384 M1328 384 L1328 376 Q1328 368 1338 368 L1340 368" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <line x1="1334" y1="362" x2="1342" y2="370" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="1326" cy="362" r="3" fill="#ffffff"/>
      <text x="1374" y="382" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1d2366">Specialized US R&amp;D</text>
      <!-- Flattened, line-by-line hierarchal rows preventing overlapping tspan bugs -->
      <text x="1310" y="445" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" font-weight="bold" fill="#1d2366">Statistical Programmers and Computational</text>
      <text x="1310" y="473" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Chemists collaborate with local US IT</text>
      <text x="1310" y="501" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" font-weight="bold" fill="#4f46e5">Champion Shailendra Phadke to define</text>
      <text x="1310" y="529" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">and package specialized biometrics skills.</text>
    </g>
  </g>
  {get_footer("3")}
</svg>"""
    with open(os.path.join(output_dir, "Slide3.svg"), "w", encoding="utf-8") as f:
        f.write(s3_handcrafted)

    # Re-write Slide 14 specifically so we retain its exact handcrafted state (and eliminate nested tspans!)
    print("Regenerating Slide 14...")
    s14_handcrafted = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <!-- Drop Shadow Filter for Cards -->
    <filter id="card-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#0f172a" flood-opacity="0.06" />
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.04" />
    </filter>
  </defs>

  <!-- Base White Background with rx=0 corners and border -->
  <rect x="0" y="0" width="1920" height="1080" rx="0" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>

  <!-- Background Swept Accent Ring (Quarter-Circle Arc) -->
  <ellipse cx="309" cy="846" rx="525" ry="450" fill="none" stroke="#e8edf9" stroke-width="180" opacity="0.4" pointer-events="none"/>

  <!-- Slide Header -->
  <g id="header" transform="translate(0, 0)">
    <!-- Category Badge 'KPI METRICS' -->
    <rect x="1680" y="72" width="168" height="42" rx="6" fill="#f1f5f9" stroke="#e2e8f0" stroke-width="1.5"/>
    <text x="1764" y="98" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="16" font-weight="bold" fill="#1d2366" text-anchor="middle">KPI METRICS</text>

    <!-- Main Title -->
    <text x="72" y="112" font-family="'Segoe UI', 'Arial', sans-serif" font-size="44" font-weight="800" fill="#1d2366" letter-spacing="-0.025em">Velocity, Acceleration, and DORA Measures</text>
    
    <!-- Subtitle -->
    <text x="72" y="152" font-family="'Segoe UI', 'Arial', sans-serif" font-size="20" fill="#64748b">Evaluating Project Orbit's impact on software engineering output and scientific discovery pipelines.</text>
  </g>

  <!-- Content Cards Grid -->
  <g id="content-cards">
    <!-- ================= CARD 1 ================= -->
    <g id="card-1">
      <rect x="72" y="320" width="568" height="480" rx="20" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" filter="url(#card-shadow)"/>
      <rect x="102" y="350" width="48" height="48" rx="8" fill="#1d2366"/>
      <path d="M114 382 L124 370 L130 376 L138 362" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <path d="M132 362 L138 362 L138 368" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <text x="166" y="382" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1d2366">Delivery Velocity</text>
      <!-- Flattened rows preventing overlapping tspan bugs -->
      <text x="102" y="445" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Aiming for &gt;25% improvement in</text>
      <text x="102" y="473" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" font-weight="bold" fill="#1d2366">Lead Time and Deployment Frequency.</text>
      <text x="102" y="501" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Tracks individual and team build velocity automatically</text>
      <text x="102" y="529" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">using secure Git and Jira telemetry endpoints.</text>
    </g>

    <!-- ================= CARD 2 ================= -->
    <g id="card-2">
      <rect x="676" y="320" width="568" height="480" rx="20" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" filter="url(#card-shadow)"/>
      <rect x="706" y="350" width="48" height="48" rx="8" fill="#ff5a24"/>
      <path d="M718 362 Q726 374 730 374 T742 386" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <path d="M718 386 Q726 374 730 374 T742 362" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <line x1="722" y1="367" x2="722" y2="381" stroke="#ffffff" stroke-width="1.5" opacity="0.6"/>
      <line x1="730" y1="374" x2="730" y2="374" stroke="#ffffff" stroke-width="1.5" opacity="0.6"/>
      <line x1="738" y1="381" x2="738" y2="367" stroke="#ffffff" stroke-width="1.5" opacity="0.6"/>
      <text x="770" y="382" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1d2366">R&amp;D Acceleration</text>
      <text x="706" y="445" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">Drastically shrinking pipeline-building timelines</text>
      <text x="706" y="473" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">for genomic alignment, statistical modeling,</text>
      <text x="706" y="501" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">and computational simulations. Empowering</text>
      <text x="706" y="529" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">biostatisticians to compile reproducible</text>
      <text x="706" y="557" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">pipelines in minutes.</text>
    </g>

    <!-- ================= CARD 3 ================= -->
    <g id="card-3">
      <rect x="1280" y="320" width="568" height="480" rx="20" fill="#ffffff" stroke="#a5b4fc" stroke-width="2" stroke-dasharray="8,6" filter="url(#card-shadow)"/>
      <rect x="1310" y="350" width="48" height="48" rx="8" fill="#4f46e5"/>
      <polygon points="1334,357 1339,368 1351,370 1342,378 1344,390 1334,384 1324,390 1326,378 1317,370 1329,368" fill="#ffffff"/>
      <text x="1374" y="382" font-family="'Segoe UI', 'Arial', sans-serif" font-size="24" font-weight="bold" fill="#1d2366">US IT Leadership</text>
      <!-- Flattened rows preventing overlapping tspan bugs -->
      <text x="1310" y="445" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" font-weight="bold" fill="#4f46e5">US IT Champion Shailendra Phadke</text>
      <text x="1310" y="473" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">(Statistical Programming) spearheads the definition</text>
      <text x="1310" y="501" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">of specialized local R&amp;D biometrics skills,</text>
      <text x="1310" y="529" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">bridging the gap between local US projects and</text>
      <text x="1310" y="557" font-family="'Segoe UI', 'Arial', sans-serif" font-size="18" fill="#475569">our global repo.</text>
    </g>
  </g>
  {get_footer("14")}
</svg>"""
    with open(os.path.join(output_dir, "Slide14.svg"), "w", encoding="utf-8") as f:
        f.write(s14_handcrafted)

    print(f"\n✓ Successfully compiled and wrote all 19 hand-crafted vector SVGs to {output_dir}")

if __name__ == "__main__":
    main()
