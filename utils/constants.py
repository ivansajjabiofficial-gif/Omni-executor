"""
Constants and problem classification signals for Omni Executor.
"""

# Problem classification categories
PROBLEM_CATEGORIES = [
    "operational",
    "financial",
    "strategic",
    "organizational",
    "customer",
    "employee",
    "compliance",
    "risk",
    "growth",
    "automation",
    "productivity",
]

# Keywords that signal different problem categories
PROBLEM_SIGNALS = {
    "operational": [
        "process", "workflow", "inefficient", "slow", "bottleneck", 
        "delivery", "execution", "manual", "repetitive", "handoff"
    ],
    "financial": [
        "cost", "revenue", "budget", "profit", "expense", "margin",
        "cash flow", "pricing", "financial", "spending", "roi"
    ],
    "strategic": [
        "strategy", "direction", "vision", "market", "competitive",
        "positioning", "growth", "expansion", "innovation", "roadmap"
    ],
    "organizational": [
        "team", "organizational", "structure", "roles", "alignment",
        "conflict", "silos", "culture", "leadership", "governance"
    ],
    "customer": [
        "customer", "client", "user", "satisfaction", "retention",
        "churn", "experience", "feedback", "acquisition", "loyalty"
    ],
    "employee": [
        "employee", "staff", "talent", "retention", "turnover",
        "engagement", "morale", "skills", "training", "development"
    ],
    "compliance": [
        "compliance", "regulation", "audit", "legal", "policy",
        "governance", "control", "risk", "audit", "requirement"
    ],
    "risk": [
        "risk", "security", "data", "breach", "vulnerability",
        "threat", "exposure", "mitigation", "contingency", "disaster"
    ],
    "growth": [
        "growth", "scale", "expansion", "market", "new", "opportunity",
        "revenue", "product", "innovation", "launch"
    ],
    "automation": [
        "automation", "automate", "manual", "repetitive", "efficiency",
        "workflow", "integrate", "integration", "system", "tool"
    ],
    "productivity": [
        "productivity", "efficient", "speed", "time", "delay",
        "bottleneck", "wait", "queue", "capacity", "throughput"
    ],
}

# Severity indicators
CRITICAL_INDICATORS = [
    "losing", "bankruptcy", "shutdown", "compliance violation",
    "data breach", "critical outage", "customer loss", "revenue drop",
    "existential", "crisis", "emergency", "failing"
]

HIGH_INDICATORS = [
    "declining", "slow", "inefficient", "expensive", "conflict",
    "poor quality", "missed deadline", "customer complaint", "unhappy",
    "risk", "vulnerability"
]

# Urgency indicators
URGENT_INDICATORS = [
    "immediately", "now", "emergency", "crisis", "failing", "urgent",
    "asap", "within days", "critical", "must", "must-fix"
]

# Positive indicators for confidence
CONFIDENCE_BOOSTERS = [
    "data", "metrics", "numbers", "documented", "evidence",
    "tested", "measured", "validated", "analysis", "report"
]

# Business scale characteristics
SCALE_CHARACTERISTICS = {
    "Small Business": {
        "team_size": "1-50",
        "structure": "Flat, owner-driven",
        "processes": "Informal, flexible",
        "budget_constraint": "High",
        "change_speed": "Fast",
    },
    "Medium Business": {
        "team_size": "50-500",
        "structure": "Functional departments",
        "processes": "Documented but evolving",
        "budget_constraint": "Medium",
        "change_speed": "Medium",
    },
    "Large Company": {
        "team_size": "500-5000",
        "structure": "Divisional with departments",
        "processes": "Formal and documented",
        "budget_constraint": "Low",
        "change_speed": "Slow",
    },
    "Enterprise": {
        "team_size": "5000+",
        "structure": "Global matrix",
        "processes": "Highly formalized",
        "budget_constraint": "Very low",
        "change_speed": "Very slow",
    },
    "Agency": {
        "team_size": "10-200",
        "structure": "Project-based teams",
        "processes": "Client-driven",
        "budget_constraint": "Medium-High",
        "change_speed": "Medium",
    },
    "NGO": {
        "team_size": "5-100",
        "structure": "Mission-driven",
        "processes": "Purpose-aligned",
        "budget_constraint": "Very High",
        "change_speed": "Medium",
    },
    "Government": {
        "team_size": "Varies",
        "structure": "Hierarchical",
        "processes": "Policy-bound",
        "budget_constraint": "Medium",
        "change_speed": "Very slow",
    },
    "Institution": {
        "team_size": "Varies",
        "structure": "Academic/formal",
        "processes": "Tradition-bound",
        "budget_constraint": "Low-Medium",
        "change_speed": "Slow",
    },
}

# Timeline recommendations by severity and scale
TIMELINE_MATRIX = {
    ("Critical", "Small Business"): {"quick_wins": "24-48 hours", "phase1": "1 week", "full": "4 weeks"},
    ("Critical", "Medium Business"): {"quick_wins": "3 days", "phase1": "2 weeks", "full": "8 weeks"},
    ("Critical", "Large Company"): {"quick_wins": "1 week", "phase1": "4 weeks", "full": "16 weeks"},
    ("Critical", "Enterprise"): {"quick_wins": "1-2 weeks", "phase1": "6 weeks", "full": "6 months"},
    ("High", "Small Business"): {"quick_wins": "1 week", "phase1": "2 weeks", "full": "8 weeks"},
    ("High", "Medium Business"): {"quick_wins": "1 week", "phase1": "4 weeks", "full": "12 weeks"},
    ("High", "Large Company"): {"quick_wins": "2 weeks", "phase1": "6 weeks", "full": "6 months"},
    ("High", "Enterprise"): {"quick_wins": "2-3 weeks", "phase1": "8 weeks", "full": "9 months"},
    ("Medium", "Small Business"): {"quick_wins": "2 weeks", "phase1": "4 weeks", "full": "12 weeks"},
    ("Medium", "Medium Business"): {"quick_wins": "2 weeks", "phase1": "6 weeks", "full": "16 weeks"},
    ("Medium", "Large Company"): {"quick_wins": "3 weeks", "phase1": "8 weeks", "full": "9 months"},
    ("Medium", "Enterprise"): {"quick_wins": "1 month", "phase1": "12 weeks", "full": "12+ months"},
}

# Maturity model levels
MATURITY_LEVELS = [
    "Ad-Hoc (Level 1)",
    "Repeatable (Level 2)",
    "Defined (Level 3)",
    "Managed (Level 4)",
    "Optimized (Level 5)",
]

# Report section order
REPORT_SECTIONS = [
    "problem_summary",
    "current_state",
    "root_causes",
    "target_state",
    "priority_level",
    "recommended_actions",
    "quick_wins",
    "thirty_day_plan",
    "kpis",
    "risks",
    "automation",
    "governance",
    "final_recommendation",
    "assumptions",
]
