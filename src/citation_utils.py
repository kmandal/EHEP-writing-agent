import re
import os
import json

def should_skip_bibtex_generation(bib_file: str) -> bool:
    """
    Returns True if references.bib exists and does not contain placeholders.
    """
    if not os.path.exists(bib_file):
        return False
    with open(bib_file, "r", encoding="utf-8") as f:
        content = f.read()
    if "Placeholder" in content or "placeholder" in content:
        return False
    print(f"[BibTeX Guard] Secure and clean local {bib_file} found. Skipping InspireHEP API pass.")
    return True

def generate_phrase_citation_dict(markdown_path: str, bib_path: str) -> dict:
    """
    Parses the markdown file by first cleanly splitting content into section text buckets,
    then running your verified Version 1 regex backward-parsing engine inside each block.
    """
    section_map = {}
    
    if not os.path.exists(markdown_path) or not os.path.exists(bib_path):
        print(f"[!] Warning: Missing paths: md={markdown_path}, bib={bib_path}")
        return section_map

    # --- 1. Pure Version 1 .bib Database Lookup Cache ---
    bib_database = {}
    current_key = None
    
    with open(bib_path, "r", encoding="utf-8") as f:
        for line in f:
            match_entry = re.match(r'@\w+\s*\{\s*([^,]+),', line)
            if match_entry:
                current_key = match_entry.group(1).strip()
                bib_database[current_key.lower()] = current_key
            
            # DOI lookup
            match_doi = re.search(r'doi\s*=\s*["\{]([^"\}]+)["\}]', line, re.IGNORECASE)
            if match_doi and current_key:
                bib_database[match_doi.group(1).strip().lower()] = current_key

            # eprint/arXiv lookup
            match_eprint = re.search(r'eprint\s*=\s*["\{]([^"\}]+)["\}]', line, re.IGNORECASE)
            if match_eprint and current_key:
                bib_database[match_eprint.group(1).strip().lower()] = current_key
                # strip out any 'arXiv:' literal prefixes to handle raw numbers
                clean_eprint = match_eprint.group(1).lower().replace("arxiv:", "").strip()
                bib_database[clean_eprint] = current_key

    # --- 2. Normalized Section Heading Helper ---
    def normalize_section_heading(raw_title: str) -> str:
        t = raw_title.lower()
        if "intro" in t:
            return "Introduction"
        if "detector" in t or "trigger" in t:
            return "Detector Setup and Trigger System"
        if "dataset" in t or "sample" in t or "simulat" in t:
            return "Datasets and Simulated Samples"
        if "reconstruction" in t or "object" in t or "identification" in t:
            return "Event Reconstruction and Object Identification"
        if "event selection" in t or "strategy" in t or "search region" in t:
            return "Event Selection and Analysis Strategy"
        if "background" in t or "estimation" in t:
            return "Background Estimation Methods"
        if "systematic" in t or "uncertaint" in t:
            return "Systematic Uncertainties"
        if "result" in t or "statistical" in t or "interpretation" in t:
            return "Results and Statistical Interpretations"
        if "summary" in t or "conclusion" in t:
            return "Summary and Conclusion"
        return None

    # Pre-initialize sections to maintain paper layout sequence
    standard_sections = [
        "Introduction", "Detector Setup and Trigger System", "Datasets and Simulated Samples",
        "Event Reconstruction and Object Identification", "Event Selection and Analysis Strategy",
        "Background Estimation Methods", "Systematic Uncertainties",
        "Results and Statistical Interpretations", "Summary and Conclusion"
    ]
    for sec in standard_sections:
        section_map[sec] = {}

    # Read the full markdown file content
    with open(markdown_path, "r", encoding="utf-8") as f:
        full_content = f.read()

    # --- 3. Robust Section Content Division ---
    # Split content cleanly by any line starting with one or more '#'
    parts = re.split(r'(^#+\s+.*)', full_content, flags=re.MULTILINE)
    
    # re.split captures the delimiter too, so elements alternate between:
    # [leading_text, '# Header 1', 'content 1', '# Header 2', 'content 2', ...]
    current_section_name = None

    for idx, part in enumerate(parts):
        part_str = part.strip()
        if not part_str:
            continue
            
        # If it's a section header line
        if part_str.startswith('#'):
            raw_title = part_str.lstrip('#').strip()
            current_section_name = normalize_section_heading(raw_title)
        else:
            # It's a text block context belonging to the active section
            if not current_section_name:
                continue
                
            section_text = part_str
            
            # --- 4. Exact Version 1 Extraction Pattern over Section Text ---
            stop_words = {"and", "or", "in", "with", "via", "under", "over", "where", "using", "for", "at", "by", "from", "of", "to", "on", "as"}
            
            matches = re.finditer(r'([^\]\n]{1,120})\s*(?:CITE|cite)\s*:\s*\{([^}]+)\}', section_text)
                        
            for m in matches:
                raw_text_before = m.group(1)
                raw_citations = m.group(2)
                
                if not raw_text_before:
                    continue

                clean_text = re.sub(r'(?:CITE|cite)\s*:\s*\{[^}]+\}', '', raw_text_before)
                phrase_parts = re.split(r'[\[,;\*]', clean_text)
                prose_before = phrase_parts[-1].strip()
                if prose_before.endswith(':'):
                    prose_before = prose_before[:-1].strip()

                words = prose_before.split()
                # Keep a maximum of 3 words to evaluate
                target_words = words[-3:] if len(words) >= 3 else words
                filtered_words = []
                # Exact v1 Logic: Read backwards and break immediately if encountering a stop word
                for word in reversed(target_words):
                    clean_word = re.sub(r'[^\w\s-]', '', word).lower().strip()
                    if clean_word in stop_words:
                        break
                    filtered_words.insert(0, word)

                # Fallback safeguard from v1 if immediately preceded by a stop word
                if not filtered_words:
                    filtered_words = target_words

                phrase_key = " ".join(filtered_words).strip()
                if not phrase_key or len(phrase_key) < 2:
                    continue
                
                # Resolve tags using your correct v1 database keys
                raw_keys = [k.strip() for k in raw_citations.split(",") if k.strip()]
                resolved_keys = []
                
                for rk in raw_keys:
                    clean_id = rk.replace("arXiv:", "").replace("arxiv:", "").strip().lower()
                    if clean_id in bib_database:
                        resolved_keys.append(bib_database[clean_id])
                    elif rk.lower() in bib_database:
                        resolved_keys.append(bib_database[rk.lower()])
                    else:
                        resolved_keys.append(rk)

                if resolved_keys:
                    unique_keys = list(dict.fromkeys(resolved_keys))
                    cite_macro = f"\\cite{{{', '.join(unique_keys)}}}"
                    
                    # Store under the current section context
                    section_map[current_section_name][phrase_key] = cite_macro
                    print(f"  [{current_section_name}] Extracted: '{phrase_key}' ➔ {cite_macro}")

    # Remove completely empty sections to keep json clean
    final_section_map = {k: v for k, v in section_map.items() if v}

    # --- 5. Save output snapshots ---
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    for target_path in [os.path.join(output_dir, "phrase_citation_map.json"), "phrase_citation_map.json"]:
        with open(target_path, "w", encoding="utf-8") as jf:
            json.dump(final_section_map, jf, indent=2)

    print(f"\n[✓] Segmented citation mapping saved successfully!")
    return final_section_map
