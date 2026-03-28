import re
from collections import defaultdict
from datetime import date

# Simple NER without requiring torch
def load_ner_model():
    """Return a simple NER model (no actual model needed)"""
    return None

DOMAIN_KEYWORDS = {
    "Energy": ["energy", "energy sector", "energy systems"],
    "Oil & Gas": ["oil & gas", "oil gas", "oil", "gas", "petroleum"],
    "Power & Utilities": ["power-utilities", "utilities", "power grid", "electric utilities", "smart grid"],
    "Manufacturing": ["manufacturing", "industrial automation", "smart manufacturing"],
    "Retail / CPG": ["retail", "cpg", "consumer packaged goods", "consumer goods"],
}

AI_STACK_KEYWORDS = {
    "GenAI Frameworks": ["genai frameworks", "generative ai frameworks", "llm frameworks", "langchain", "raven", "lithic", "retrieval-augmented generation"],
    "Memory Systems": ["memory systems", "vector memory", "session memory", "rete memory"],
    "Token Management": ["token management", "tokenization", "context management", "context window", "context windows"],
    "Queuing": ["queuing", "queueing", "task queue", "message queue", "celery", "rabbitmq", "kafka"],
    "Governance": ["governance", "ai governance", "model governance", "data governance"],
    "AIOps": ["aiops"],
    "Cloud Execution": ["cloud enabled execution", "cloud-enabled execution", "cloud-native", "cloud execution", "cloud scale", "cloud orchestration"],
    "AI Agents": ["ai agents", "agentic"],
}


def _match_keyword_categories(text, category_map):
    """Return matching canonical categories based on keyword presence."""
    if not text:
        return []
    normalized = text.lower()
    matches = set()
    for category, keywords in category_map.items():
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, normalized):
                matches.add(category)
                break
    return sorted(matches)

def calculate_resume_score(text, extracted_data):
    """
    Calculate resume quality score based on multiple dimensions (0-100)
    Returns dict with overall score and dimension breakdown
    """
    
    scores = {}
    
    # 1. COMPLETENESS SCORE (Name, Email, Phone) - 0-100
    completeness = 0
    if extracted_data.get('NAME'):
        completeness += 25
    if extracted_data.get('EMAIL'):
        completeness += 25
    if extracted_data.get('PHONE'):
        completeness += 25
    if extracted_data.get('LOCATION'):
        completeness += 25
    scores['Completeness'] = completeness
    
    # 2. SKILLS SCORE - Based on number of skills extracted (0-100)
    skills_count = len(extracted_data.get('SKILL', []))
    skills_score = min(100, (skills_count / 15) * 100)  # 15+ skills = 100
    scores['Skills'] = round(skills_score)
    
    # 3. EDUCATION SCORE - Check for education level (0-100)
    education_score = 0
    edu_text = ' '.join(extracted_data.get('EDUCATION', ['']))
    if extracted_data.get('EDUCATION'):
        if re.search(r'\bPhD\b', edu_text, re.IGNORECASE):
            education_score = 95
        elif re.search(r'\bMaster|M\.Tech|MBA\b', edu_text, re.IGNORECASE):
            education_score = 85
        elif re.search(r'\bB\.Tech|Bachelor|BS|BA\b', edu_text, re.IGNORECASE):
            education_score = 75
        else:
            education_score = 50
    scores['Education'] = education_score
    
    # 4. EXPERIENCE SCORE - Check for work history keywords (0-100)
    experience_score = 0
    exp_keywords = ['Experience', 'Professional', 'Intern', 'Developer', 'Engineer', 
                    'Analyst', 'Manager', 'Intern', 'Associate', 'Senior', 'Lead']
    exp_matches = sum(1 for kw in exp_keywords if re.search(kw, text, re.IGNORECASE))
    
    # Count mentions of companies/positions
    position_patterns = len(re.findall(r'(?:Intern|Developer|Engineer|Analyst|Manager|Lead|Associate)', text, re.IGNORECASE))
    
    experience_score = min(100, (position_patterns / 3) * 100)  # 3+ positions = 100
    scores['Experience'] = round(experience_score)
    
    # 5. PROJECTS SCORE - Check for projects section (0-100)
    projects_score = 0
    if re.search(r'\bProject|Portfolio|GitHub|Github\b', text, re.IGNORECASE):
        projects_score = 40
    if extracted_data.get('URL'):  # Has GitHub/LinkedIn links
        projects_score += 30
    # Count project mentions
    project_mentions = len(re.findall(r'(?:Built|Developed|Created|Designed|Implemented)', text, re.IGNORECASE))
    projects_score += min(30, (project_mentions / 3) * 30)
    scores['Projects'] = min(100, round(projects_score))
    
    # 6. FORMAT & QUALITY SCORE - Resume length, structure (0-100)
    text_length = len(text)
    word_count = len(text.split())
    
    # Optimal resume: 400-800 words
    if 400 <= word_count <= 800:
        format_score = 90
    elif 200 <= word_count < 400:
        format_score = 70
    elif word_count < 200:
        format_score = 40
    else:  # >800 words
        format_score = 75
    
    # Check for well-organized sections
    sections = len(re.findall(r'^[A-Z][A-Z\s]+$', text, re.MULTILINE))
    if sections >= 5:
        format_score += 10
    
    scores['Format Quality'] = min(100, round(format_score))
    
    # CALCULATE OVERALL SCORE (weighted average)
    weights = {
        'Completeness': 0.15,
        'Skills': 0.20,
        'Education': 0.15,
        'Experience': 0.20,
        'Projects': 0.15,
        'Format Quality': 0.15
    }
    
    overall_score = sum(scores[dim] * weights[dim] for dim in scores)
    
    # Determine grade
    if overall_score >= 90:
        grade = "A+"
    elif overall_score >= 80:
        grade = "A"
    elif overall_score >= 70:
        grade = "B+"
    elif overall_score >= 60:
        grade = "B"
    elif overall_score >= 50:
        grade = "C"
    else:
        grade = "D"
    
    return {
        'overall_score': round(overall_score),
        'grade': grade,
        'percentile': round(min(100, (overall_score / 100) * 100)),
        'dimensions': scores
    }


def _normalize_skill(skill):
    """Normalize skill text for matching."""
    return re.sub(r'[^a-z0-9+#.]', '', skill.lower())


def _extract_experience_sections(text):
    """Return likely experience-only sections so education dates are ignored."""
    heading_pattern = re.compile(
        r'(?im)^\s*(work experience|professional experience|experience|employment history|internships?)\s*:?\s*$'
    )
    next_heading_pattern = re.compile(
        r'(?im)^\s*(skills|technical skills|projects|education|certifications|awards|summary|profile|objective|contact)\s*:?\s*$'
    )

    sections = []
    for match in heading_pattern.finditer(text):
        start = match.end()
        remaining = text[start:]
        next_heading = next_heading_pattern.search(remaining)
        end = start + next_heading.start() if next_heading else len(text)
        section_text = text[start:end].strip()
        if section_text:
            sections.append(section_text)
    return sections


def _parse_year_intervals(text):
    """Parse year ranges like 2021-2023 or Jan 2022 - Present."""
    current_year = date.today().year
    interval_pattern = re.compile(
        r'(?i)(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)?'
        r'[\s,/-]*'
        r'((?:19|20)\d{2})'
        r'\s*(?:to|\u2013|\u2014|-)'
        r'\s*(?:'
        r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)?[\s,/-]*'
        r'((?:19|20)\d{2}|present|current)'
        r')'
    )

    intervals = []
    for start, end in interval_pattern.findall(text):
        start_year = int(start)
        end_lower = end.lower()
        end_year = current_year if end_lower in {'present', 'current'} else int(end_lower)
        if end_year >= start_year:
            intervals.append((start_year, end_year))
    return intervals


def _merge_intervals(intervals):
    """Merge overlapping intervals and return total covered years."""
    if not intervals:
        return 0

    merged = []
    for start, end in sorted(intervals):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return sum(end - start for start, end in merged)


def _extract_years_required(job_description):
    """Extract the most relevant required experience from the JD."""
    matches = re.findall(
        r'(?i)(\d+)\s*(?:\+)?\s*years?(?:\s+of)?\s+(?:professional\s+)?(?:software\s+engineering|experience|exp)',
        job_description
    )
    return max((int(value) for value in matches), default=0)


def _extract_years_from_resume(resume_text):
    """Estimate experience from explicit claims or actual work date ranges only."""
    explicit_matches = re.findall(
        r'(?i)(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?\s*(?:of|in)?\s*'
        r'(?:professional\s+|software\s+engineering\s+|work\s+)?(?:experience|exp)',
        resume_text
    )
    explicit_years = max((float(value) for value in explicit_matches), default=0)

    experience_sections = _extract_experience_sections(resume_text)
    search_text = '\n'.join(experience_sections) if experience_sections else resume_text
    interval_years = float(_merge_intervals(_parse_year_intervals(search_text)))

    years = max(explicit_years, interval_years)
    return round(years, 1) if years > 0 else 0


def _resume_has_ai_foundation(resume_skills_lower):
    """Check whether the resume shows clear AI/ML fundamentals."""
    ai_foundation = {
        'machinelearning', 'deeplearning', 'nlp', 'scikitlearn', 'tensorflow',
        'pytorch', 'keras', 'pandas', 'numpy', 'datascience', 'computervision'
    }
    return any(skill in ai_foundation for skill in resume_skills_lower)

def calculate_jd_match(resume_text, resume_skills, job_description, extracted_data=None):
    """
    Calculate how well resume matches a job description.
    Returns match percentage, matched skills, missing skills, and recommendations.
    """

    if not job_description or not resume_skills:
        return None

    extracted_data = extracted_data or {}

    skill_categories = {
        'Backend Languages': ['Python', 'Java', 'Go', 'C++', 'C#', 'PHP', 'Rust'],
        'Frontend': ['React', 'Vue', 'Angular', 'JavaScript', 'TypeScript', 'CSS', 'HTML'],
        'AI/ML': ['Machine Learning', 'Deep Learning', 'NLP', 'TensorFlow', 'PyTorch', 'Keras',
                  'Scikit-learn', 'Pandas', 'NumPy', 'LLM', 'AI', 'Generative AI', 'Transformers',
                  'Computer Vision', 'Data Science', 'Neural Networks', 'AI Agents'],
        'Data & Search': ['SQL', 'ElasticSearch', 'Solr', 'FAISS', 'Vector DB', 'Embedding'],
        'Cloud & DevOps': ['AWS', 'Google Cloud', 'Azure', 'Docker', 'Kubernetes', 'CI/CD', 'Jenkins'],
        'Databases': ['MySQL', 'PostgreSQL', 'MongoDB', 'Firebase', 'Redis', 'Cassandra'],
        'APIs & Services': ['REST API', 'GraphQL', 'gRPC', 'Microservices', 'API Gateway'],
        'Tools': ['Git', 'GitHub', 'Streamlit', 'Jupyter', 'Linux']
    }

    years_required = _extract_years_required(job_description)
    years_in_resume = _extract_years_from_resume(resume_text)

    resume_domains = set(extracted_data.get('DOMAIN', _match_keyword_categories(resume_text, DOMAIN_KEYWORDS)))
    resume_stack = set(extracted_data.get('AI_STACK', _match_keyword_categories(resume_text, AI_STACK_KEYWORDS)))
    jd_domains = set(_match_keyword_categories(job_description, DOMAIN_KEYWORDS))
    jd_stack = set(_match_keyword_categories(job_description, AI_STACK_KEYWORDS))

    required_categories = {}
    for category, skills in skill_categories.items():
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', job_description, re.IGNORECASE):
                required_categories.setdefault(category, []).append(skill)

    matched_skills = []
    matched_categories = set()
    resume_skills_lower = [_normalize_skill(skill) for skill in resume_skills]

    for category, req_skills in required_categories.items():
        for req_skill in req_skills:
            normalized_req_skill = _normalize_skill(req_skill)

            if normalized_req_skill in resume_skills_lower:
                matched_skills.append(req_skill)
                matched_categories.add(category)
                continue

            if category == 'AI/ML':
                if normalized_req_skill in {'ai', 'machinelearning', 'datascience', 'nlp'} and _resume_has_ai_foundation(resume_skills_lower):
                    matched_skills.append(req_skill)
                    matched_categories.add(category)
                elif normalized_req_skill in {'scikitlearn', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'keras'} and normalized_req_skill in resume_skills_lower:
                    matched_skills.append(req_skill)
                    matched_categories.add(category)

    matched_skills = sorted(set(skill.split('(')[0].strip() for skill in matched_skills))

    missing_skills = []
    for req_skills in required_categories.values():
        for req_skill in req_skills:
            if req_skill not in matched_skills and _normalize_skill(req_skill) not in resume_skills_lower:
                missing_skills.append(req_skill)
    missing_skills = sorted(set(missing_skills))

    total_required_skills = sum(len(skills) for skills in required_categories.values())
    skill_match_percentage = 50 if total_required_skills == 0 else round((len(matched_skills) / total_required_skills) * 100)

    if years_required > 0:
        experience_score = 100 if years_in_resume >= years_required else round((years_in_resume / years_required) * 100)
    else:
        experience_score = 80

    domain_matches = sorted(resume_domains & jd_domains)
    domain_missing = sorted(jd_domains - resume_domains)
    stack_matches = sorted(resume_stack & jd_stack)
    stack_missing = sorted(jd_stack - resume_stack)

    seniority_keywords = {
        'Junior|Entry|Intern|Graduate': 'Junior',
        'Lead|Principal|Architect|Manager|Head': 'Lead',
        'Senior|Staff': 'Senior'
    }

    jd_level = 'Mid'
    for pattern, level in seniority_keywords.items():
        if re.search(pattern, job_description, re.IGNORECASE):
            jd_level = level
            break

    overall_match = round((skill_match_percentage * 0.5) + (experience_score * 0.5))

    if overall_match >= 80:
        fit_level = "Excellent Fit"
    elif overall_match >= 60:
        fit_level = "Good Fit"
    else:
        fit_level = "Needs Work"

    recommendations = []
    if experience_score < 100:
        rec_years = years_required - years_in_resume
        if rec_years > 0:
            recommendations.append(f"Gain {rec_years}+ more years of experience or emphasize relevant project work")
        if years_in_resume == 0:
            recommendations.append("Add clear work dates or an explicit 'X years of experience' summary to improve matching accuracy")

    if skill_match_percentage < 80:
        top_missing = missing_skills[:3]
        if top_missing:
            recommendations.append(f"Learn: {', '.join(top_missing)}")

    if skill_match_percentage < 60:
        recommendations.append("Build projects using the required tech stack")
        recommendations.append("Focus on system design and architecture experience")

    if jd_level == 'Lead' and years_in_resume < 5:
        recommendations.append("Demonstrate technical leadership through mentoring or open-source contributions")

    if matched_skills:
        recommendations.append(f"Highlight your {matched_skills[0]} expertise and use cases")

    if jd_domains:
        if domain_matches:
            recommendations.append(f"Highlight your domain depth in {', '.join(domain_matches)}")
        else:
            recommendations.append(f"Showcase experience in the {', '.join(jd_domains)} domain(s)")

    if jd_stack:
        if stack_matches:
            recommendations.append(f"Call out hands-on work with {', '.join(stack_matches)}")
        else:
            recommendations.append(f"Gain experience with {', '.join(jd_stack)} to mirror the modern AI stack demands")

    if not recommendations:
        recommendations.append("Great match! Polish your resume and apply!")

    jd_found_skills = sorted({skill for skills in required_categories.values() for skill in skills})

    return {
        'overall_match': overall_match,
        'match_percentage': overall_match,
        'fit_level': fit_level,
        'skill_match_percentage': skill_match_percentage,
        'experience_score': experience_score,
        'experience_fit_score': experience_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills[:10],
        'jd_found_skills': jd_found_skills,
        'years_required': years_required,
        'years_in_resume': years_in_resume,
        'jd_level': jd_level,
        'seniority_level': jd_level,
        'required_categories': len(required_categories),
        'matched_categories': len(matched_categories),
        'domains_required': sorted(jd_domains),
        'domains_matched': domain_matches,
        'domains_missing': domain_missing,
        'stack_required': sorted(jd_stack),
        'stack_matched': stack_matches,
        'stack_missing': stack_missing,
        'recommendations': recommendations
    }


SECTION_ALIASES = {
    'summary': ['summary', 'professional summary', 'profile', 'objective', 'about'],
    'skills': ['skills', 'technical skills', 'core competencies', 'technologies', 'tech stack'],
    'experience': ['experience', 'work experience', 'professional experience', 'employment history', 'internship', 'internships'],
    'education': ['education', 'academic background', 'qualification', 'qualifications'],
    'projects': ['projects', 'personal projects', 'academic projects', 'key projects'],
    'certifications': ['certifications', 'certificates', 'licenses'],
}

SKILL_ALIASES = {
    'Python': ['python'],
    'Java': ['java'],
    'JavaScript': ['javascript', 'js'],
    'TypeScript': ['typescript', 'ts'],
    'SQL': ['sql', 'mysql', 'postgresql', 'postgres', 'sqlite'],
    'HTML': ['html', 'html5'],
    'CSS': ['css', 'css3'],
    'React': ['react', 'react.js', 'reactjs'],
    'Node.js': ['node', 'node.js', 'nodejs'],
    'Angular': ['angular'],
    'Vue': ['vue', 'vue.js', 'vuejs'],
    'Django': ['django'],
    'Flask': ['flask'],
    'FastAPI': ['fastapi'],
    'Streamlit': ['streamlit'],
    'Pandas': ['pandas'],
    'NumPy': ['numpy'],
    'Scikit-learn': ['scikit-learn', 'sklearn'],
    'TensorFlow': ['tensorflow'],
    'PyTorch': ['pytorch'],
    'Keras': ['keras'],
    'NLP': ['nlp', 'natural language processing'],
    'Machine Learning': ['machine learning', 'ml'],
    'Deep Learning': ['deep learning', 'dl'],
    'Generative AI': ['generative ai', 'genai'],
    'LLM': ['llm', 'large language model', 'large language models'],
    'AI': ['artificial intelligence', 'ai'],
    'Computer Vision': ['computer vision'],
    'SQL Server': ['sql server'],
    'MongoDB': ['mongodb', 'mongo'],
    'Redis': ['redis'],
    'Docker': ['docker'],
    'Kubernetes': ['kubernetes', 'k8s'],
    'AWS': ['aws', 'amazon web services'],
    'Azure': ['azure'],
    'Google Cloud': ['google cloud', 'gcp'],
    'Git': ['git'],
    'GitHub': ['github'],
    'Linux': ['linux'],
    'REST API': ['rest api', 'restful api', 'rest'],
    'GraphQL': ['graphql'],
    'FAISS': ['faiss'],
    'Embeddings': ['embedding', 'embeddings'],
    'Power BI': ['power bi'],
    'Tableau': ['tableau'],
    'Excel': ['excel'],
    'Communication': ['communication', 'communicator'],
    'Leadership': ['leadership', 'technical leadership', 'mentoring'],
    'Problem Solving': ['problem solving', 'problem-solving'],
    'Teamwork': ['teamwork', 'collaboration', 'cross-functional'],
}

DEGREE_KEYWORDS = [
    'b.tech', 'm.tech', 'bachelor', 'master', 'phd', 'mba', 'b.e', 'm.e',
    'b.sc', 'm.sc', 'bs', 'ms', 'bca', 'mca', 'associate'
]

JOB_TITLE_KEYWORDS = [
    'engineer', 'developer', 'analyst', 'scientist', 'intern', 'consultant',
    'manager', 'lead', 'architect', 'specialist', 'associate'
]


def _normalize_resume_text(text):
    """Normalize OCR/PDF text while preserving useful line breaks."""
    if not text:
        return ""

    replacements = {
        '\u00a0': ' ',
        '\u200b': '',
        '\u2013': '-',
        '\u2014': '-',
        '\u2022': '\n- ',
        '\uf0b7': '\n- ',
        '\r': '\n',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = [line.strip(' -|\t') for line in text.split('\n')]
    return '\n'.join(line for line in lines if line.strip())


def _top_lines(text, limit=12):
    """Return the first meaningful lines from the resume."""
    return [line.strip() for line in text.split('\n') if line.strip()][:limit]


def _looks_like_section_heading(line):
    """Detect likely resume section headings."""
    cleaned = re.sub(r'[^A-Za-z ]', '', line).strip()
    lowered = cleaned.lower()
    if lowered in {alias for aliases in SECTION_ALIASES.values() for alias in aliases}:
        return True
    return bool(cleaned and len(cleaned.split()) <= 4 and cleaned.upper() == cleaned)


def _extract_sections(text):
    """Split resume text into semantic sections."""
    sections = {}
    current_section = 'header'
    buffer = []

    def flush():
        content = '\n'.join(buffer).strip()
        if content:
            sections.setdefault(current_section, []).append(content)

    section_name_map = {}
    for canonical, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            section_name_map[alias] = canonical

    for raw_line in text.split('\n'):
        line = raw_line.strip()
        normalized_line = re.sub(r'[:\s]+$', '', line.lower())
        if normalized_line in section_name_map or _looks_like_section_heading(line):
            flush()
            buffer = []
            current_section = section_name_map.get(normalized_line, normalized_line)
            continue
        buffer.append(line)
    flush()

    return {key: '\n'.join(value).strip() for key, value in sections.items()}


def _extract_urls(text):
    """Extract URLs from text."""
    pattern = r'(?:https?://|www\.)[^\s,|]+'
    return sorted(set(match.rstrip('.,);') for match in re.findall(pattern, text, re.IGNORECASE)))


def _extract_email_list(text):
    """Extract and deduplicate emails."""
    return sorted(set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)))


def _extract_phone_list(text):
    """Extract and normalize phone numbers."""
    candidates = re.findall(r'(?:\+?\d[\d\s().-]{8,}\d)', text)
    phones = []
    for candidate in candidates:
        digits = re.sub(r'\D', '', candidate)
        if 10 <= len(digits) <= 13:
            phones.append(candidate.strip())
    return sorted(set(phones))


def _extract_profile_link(urls, keyword):
    """Return a profile URL containing the given keyword."""
    for url in urls:
        if keyword in url.lower():
            return url
    return ""


def _extract_name_from_header(text, emails):
    """Extract a likely candidate name from the resume header."""
    exclusions = {
        'resume', 'curriculum vitae', 'profile', 'summary', 'objective',
        'skills', 'experience', 'education', 'project', 'certification'
    }
    for line in _top_lines(text):
        lowered = line.lower()
        if any(token in lowered for token in exclusions):
            continue
        if emails and any(email.lower() in lowered for email in emails):
            continue
        if re.search(r'\d|@|https?://|www\.', line, re.IGNORECASE):
            continue
        words = re.findall(r"[A-Za-z][A-Za-z'.-]+", line)
        if 2 <= len(words) <= 4:
            return ' '.join(word.capitalize() for word in words)
    return ""


def _extract_location_from_header(text):
    """Extract a likely location from the header area."""
    for line in _top_lines(text):
        parts = [part.strip() for part in re.split(r'[|]', line) if part.strip()]
        for part in parts:
            if re.search(r'@|\d|https?://|www\.', part, re.IGNORECASE):
                continue
            if re.search(r'\b(?:india|gurgaon|delhi|noida|bangalore|bengaluru|hyderabad|mumbai|pune|lucknow|chennai|kolkata)\b', part, re.IGNORECASE):
                return part
            if ',' in part:
                return part
    return ""


def _collect_skill_candidates(text):
    """Extract skills from section text and whole-resume aliases."""
    normalized_text = f" {text.lower()} "
    found = []

    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = r'(?<![A-Za-z0-9])' + re.escape(alias.lower()) + r'(?![A-Za-z0-9])'
            if re.search(pattern, normalized_text):
                found.append(canonical)
                break
    return sorted(set(found))


def _extract_skills_from_skill_section(skill_text):
    """Extract additional skills directly from a labeled skills section."""
    if not skill_text:
        return []

    skills = []
    for raw_line in skill_text.split('\n'):
        line = re.sub(r'(?i)^(technical skills|skills|technologies|tech stack)\s*:?\s*', '', raw_line).strip()
        if not line:
            continue

        for token in re.split(r'[,|;/]+', line):
            cleaned = token.strip(' -')
            lowered = cleaned.lower()
            if not cleaned or len(cleaned) > 35:
                continue
            if len(cleaned.split()) > 4:
                continue
            if re.search(r'^\d+$|^www\.|https?://|@', cleaned, re.IGNORECASE):
                continue

            canonical = None
            for skill_name, aliases in SKILL_ALIASES.items():
                alias_forms = {skill_name.lower(), *[alias.lower() for alias in aliases]}
                if lowered in alias_forms:
                    canonical = skill_name
                    break

            if canonical:
                skills.append(canonical)
            elif re.search(r'[A-Za-z+#.]', cleaned):
                skills.append(cleaned)

    return sorted(set(skills))


def _extract_skills_from_sections(sections, text):
    """Prioritize the skills section and backfill from resume-wide matching."""
    skill_text = sections.get('skills', '')
    combined_text = '\n'.join(filter(None, [skill_text, text]))
    skills = set(_collect_skill_candidates(combined_text))
    skills.update(_extract_skills_from_skill_section(skill_text))
    return sorted(skills)


def _extract_summary_section(sections, text):
    """Extract summary from explicit sections or fallback intro."""
    for key in ('summary', 'profile', 'objective', 'about'):
        if sections.get(key):
            return [sections[key].split('\n\n')[0][:400]]

    intro_lines = []
    for line in _top_lines(text, limit=20):
        if _looks_like_section_heading(line):
            break
        if len(line.split()) >= 8 and not re.search(r'@|https?://|\d{10,}', line):
            intro_lines.append(line)
    if intro_lines:
        return [' '.join(intro_lines)[:400]]
    return []


def _extract_education_entries(sections, text):
    """Extract richer education entries."""
    source = sections.get('education', text)
    entries = []
    for line in source.split('\n'):
        lowered = line.lower()
        if not any(keyword in lowered for keyword in DEGREE_KEYWORDS):
            continue
        cleaned = line.strip(' -')
        if cleaned:
            entries.append(cleaned)
    return list(dict.fromkeys(entries))[:5]


def _extract_project_entries(sections):
    """Extract project lines from the projects section."""
    source = sections.get('projects', '')
    entries = []
    for line in source.split('\n'):
        stripped = line.strip(' -')
        if len(stripped.split()) >= 2:
            entries.append(stripped)
    return list(dict.fromkeys(entries))[:8]


def _extract_experience_entries(sections, text):
    """Extract likely experience lines with role/date signals."""
    source = sections.get('experience', text)
    entries = []
    for line in source.split('\n'):
        stripped = line.strip(' -')
        lowered = stripped.lower()
        has_title = any(keyword in lowered for keyword in JOB_TITLE_KEYWORDS)
        has_date = bool(re.search(r'(19|20)\d{2}|present|current', lowered))
        if stripped and (has_title or has_date):
            entries.append(stripped)
    return list(dict.fromkeys(entries))[:10]

def extract_entities(text, ner_model):
    """Extract structured resume entities with section-aware parsing."""
    normalized_text = _normalize_resume_text(text)
    sections = _extract_sections(normalized_text)
    results = defaultdict(list)

    emails = _extract_email_list(normalized_text)
    phones = _extract_phone_list(normalized_text)
    urls = _extract_urls(normalized_text)
    linkedin = _extract_profile_link(urls, 'linkedin.com/in')
    github = _extract_profile_link(urls, 'github.com')
    name = _extract_name_from_header(normalized_text, emails)
    location = _extract_location_from_header(normalized_text)
    summary = _extract_summary_section(sections, normalized_text)
    skills = _extract_skills_from_sections(sections, normalized_text)
    education = _extract_education_entries(sections, normalized_text)
    experience = _extract_experience_entries(sections, normalized_text)
    projects = _extract_project_entries(sections)

    if name:
        results['NAME'] = [name]
    if emails:
        results['EMAIL'] = emails
    if phones:
        results['PHONE'] = phones
    if location:
        results['LOCATION'] = [location]
    if urls:
        results['URL'] = urls
    if linkedin:
        results['LINKEDIN'] = [linkedin]
    if github:
        results['GITHUB'] = [github]
    if summary:
        results['SUMMARY'] = summary
    if skills:
        results['SKILL'] = skills
    if education:
        results['EDUCATION'] = education
    if experience:
        results['EXPERIENCE'] = experience
    if projects:
        results['PROJECT'] = projects

    return dict(results)


ROLE_TEMPLATES = {
    'Machine Learning Engineer': ['Python', 'Machine Learning', 'Scikit-learn', 'Pandas', 'NumPy', 'NLP', 'LLM'],
    'AI Engineer': ['Python', 'Generative AI', 'LLM', 'NLP', 'Embeddings', 'FastAPI'],
    'Data Scientist': ['Python', 'Machine Learning', 'Pandas', 'NumPy', 'SQL', 'Scikit-learn'],
    'Data Analyst': ['SQL', 'Python', 'Pandas', 'Excel', 'Power BI', 'Tableau'],
    'Backend Engineer': ['Python', 'Java', 'SQL', 'FastAPI', 'REST API', 'Docker', 'Git'],
    'Full Stack Developer': ['JavaScript', 'React', 'Node.js', 'HTML', 'CSS', 'SQL', 'Git'],
    'Frontend Developer': ['React', 'JavaScript', 'TypeScript', 'HTML', 'CSS'],
}


def _count_quantified_mentions(text):
    """Count lines with metrics, percentages, or measurable impact."""
    patterns = [
        r'\b\d+(?:\.\d+)?%',
        r'\b\d+(?:\.\d+)?\s*(?:x|k|m|million|billion|hours|days|users|clients|projects)\b',
    ]
    return sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in patterns)


def infer_role_matches(extracted_data):
    """Infer likely role matches from extracted resume signals."""
    skills = set(extracted_data.get('SKILL', []))
    experience_bonus = min(len(extracted_data.get('EXPERIENCE', [])) * 5, 15)
    project_bonus = min(len(extracted_data.get('PROJECT', [])) * 4, 12)

    role_matches = []
    for role, required_skills in ROLE_TEMPLATES.items():
        matched = [skill for skill in required_skills if skill in skills]
        if len(matched) < 2:
            continue
        score = round((len(matched) / len(required_skills)) * 100)
        score = min(100, score + experience_bonus + project_bonus)
        role_matches.append({
            'role': role,
            'score': score,
            'matched_skills': matched,
            'missing_skills': [skill for skill in required_skills if skill not in skills][:4],
        })

    return sorted(role_matches, key=lambda item: item['score'], reverse=True)[:4]


def generate_ai_feedback(resume_text, extracted_data):
    """Generate feedback from the actual extracted resume content."""
    skills = extracted_data.get('SKILL', [])
    experience = extracted_data.get('EXPERIENCE', [])
    projects = extracted_data.get('PROJECT', [])
    summary = extracted_data.get('SUMMARY', [])
    education = extracted_data.get('EDUCATION', [])
    urls = extracted_data.get('URL', [])

    completeness_fields = ['NAME', 'EMAIL', 'PHONE', 'SKILL', 'EDUCATION']
    present_fields = sum(1 for field in completeness_fields if extracted_data.get(field))
    completeness_score = round((present_fields / len(completeness_fields)) * 100)

    section_count = sum(1 for field in ['SUMMARY', 'SKILL', 'EXPERIENCE', 'PROJECT', 'EDUCATION'] if extracted_data.get(field))
    readability_score = min(100, 40 + section_count * 10 + min(len(skills), 20))
    impact_score = min(100, 30 + _count_quantified_mentions(resume_text) * 15 + min(len(projects), 3) * 10)

    strengths = []
    improvements = []
    missing_sections = []

    if len(skills) >= 10:
        strengths.append(f"Strong technical coverage with {len(skills)} identified skills")
    else:
        improvements.append("Add a richer, clearly labeled skills section with core tools, frameworks, and platforms")

    if experience:
        strengths.append(f"Experience section detected with {len(experience)} role or timeline entries")
    else:
        missing_sections.append("Work Experience")
        improvements.append("Add a dedicated work experience section with role, company, and dates")

    if projects:
        strengths.append(f"Project work is present with {len(projects)} extracted project entries")
    else:
        missing_sections.append("Projects")
        improvements.append("Add 2-3 strong projects with technologies, outcomes, and links")

    if summary:
        strengths.append("Professional summary is present and gives quick context")
    else:
        missing_sections.append("Professional Summary")
        improvements.append("Add a 2-3 line summary tailored to your target role")

    if education:
        strengths.append("Education details were extracted cleanly")
    else:
        missing_sections.append("Education")

    if _count_quantified_mentions(resume_text) == 0:
        improvements.append("Use quantified achievements such as percentages, scale, or impact metrics")
    else:
        strengths.append("Resume includes measurable impact indicators")

    if not urls:
        improvements.append("Add GitHub, LinkedIn, or portfolio links to strengthen credibility")

    if skills and len(skills) <= 5:
        improvements.append("Separate programming languages, frameworks, tools, and databases so more skills are picked up clearly")

    if experience and not any(re.search(r'(19|20)\d{2}|present|current', item, re.IGNORECASE) for item in experience):
        improvements.append("Include clear dates for each experience entry so the system can estimate experience more accurately")

    action_plan = []
    if not summary:
        action_plan.append("Write a short summary aligned to the kind of roles you want")
    if _count_quantified_mentions(resume_text) == 0:
        action_plan.append("Rewrite experience and project bullets with metrics and outcomes")
    if len(skills) < 8:
        action_plan.append("Expand the skills section with frameworks, cloud tools, databases, and tooling")
    if not projects:
        action_plan.append("Add project highlights that demonstrate real applied work")

    return {
        'completeness_score': completeness_score,
        'readability_score': readability_score,
        'impact_score': impact_score,
        'strengths': strengths[:5],
        'improvements': improvements[:5],
        'missing_sections': missing_sections[:5],
        'action_plan': action_plan[:4],
    }
