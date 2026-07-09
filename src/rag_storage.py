import os
import re
from pypdf import PdfReader

def convert_sample_pdfs_to_text(pdf_dir="data/sample_papers", output_dir="data/cache_text"):
    """
    Scans the local PDF folder, extracts raw strings, 
    and caches them as simple .txt files for fast lookup.
    """
    if not os.path.exists(pdf_dir):
        print(f"[⚠️] Reference directory '{pdf_dir}' not found. Skipping extraction.")
        return
        
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            txt_filename = filename.replace(".pdf", ".txt")
            txt_path = os.path.join(output_dir, txt_filename)
            
            if os.path.exists(txt_path):
                continue
                
            print(f"[📄] Extracting text from reference: {filename}...")
            try:
                reader = PdfReader(pdf_path)
                full_text = []
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        full_text.append(text)
                
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(full_text))
                print(f"[✓] Cached plain text to: {txt_path}")
            except Exception as e:
                print(f"[X] Failed to extract {filename}: {str(e)}")



def parse_document_into_sections(text: str) -> dict:
    """
    Step 1: Implements the user's sequential workflow:
    - Strips the reference section first.
    - Loops over section counters to extract text blocks line-by-line.
    - Builds a clean section-to-text dictionary.
    """
    sections = {}
    
    # --- 1. STRIP THE REFERENCE SECTION ---
    # Find common final structural cutoff flags in CMS papers
    cutoff_keywords = [
        "\nReferences\n", "\nBibliography\n", 
        "\nThe CMS Collaboration\n", "\nThe ATLAS Collaboration\n"
    ]
    
    clean_text = text
    for keyword in cutoff_keywords:
        idx = clean_text.find(keyword)
        if idx != -1:
            clean_text = clean_text[:idx] # Drop everything below the references
            break

    # --- 2. DEFINE THE EXPECTED LINUISTIC SECTION FLOW ---
    # Mapping agentic keys to standard CMS paper heading names/numbers
    section_markers = [
        ("introduction", ["1 Introduction"]),
        ("detector", ["2 The CMS detector", "2 The detector setup", "2 Experimental setup"]),
        ("simulation", ["3 Data and simulated samples", "3 Simulated event samples", "3 Simulated samples"]),
        ("reconstruction", ["4 Event reconstruction", "4 Object reconstruction", "4 Event reconstruction"]),
        ("selection", ["5 Event selection", "5 Search strategy"]),
        ("background", ["6 Background estimation", "6 Background prediction", "6 Backgrounds"]),
        ("systematics", ["7 Summary of Systematic uncertainties", "7 Systematic uncertainties"]),
        ("results", ["8 Results and interpretation", "8 Results"]),
        ("conclusion", ["9 Summary", "9 Summary and conclusion", "9 Conclusions"])
    ]

    # --- 3. LOOP AND CAPTURE CONTINUOUS BLOCKS UNTIL THE NEXT HEADING ---
    lines = clean_text.split("\n")
    current_key = None
    current_block = []

    for line in lines:
        stripped_line = line.strip()
        found_new_section = False
        
        # Check if this line matches any of our target headers
        for key, headers in section_markers:
            if any(stripped_line.lower().startswith(h.lower()) for h in headers):
                # We hit a new section! Save the accumulated text from the previous section first
                if current_key and current_block:
                    sections[current_key] = "\n".join(current_block)
                
                # Reset tracking variables for the new section
                current_key = key
                current_block = []
                found_new_section = True
                break
        
        # If it's standard prose text, keep adding it to the currently open section block
        if not found_new_section and current_key is not None:
            current_block.append(line)

    # Save the very final section (Conclusion) after the loop exits
    if current_key and current_block:
        sections[current_key] = "\n".join(current_block)

    return sections


# =========================================================================
# Step 2: TARGETED DICTIONARY RETRIEVAL FUNCTION
# =========================================================================
def retrieve_style_context_section_based(target_section: str, cache_dir="data/cache_text", window_lines=20) -> str:
    """
    Accesses the parsed section dictionary and retrieves a specified window
    of pristine paragraph text to feed directly into the agent.
    """
    if not os.path.exists(cache_dir):
        return ""
        
    extracted_snippets = []
    normalized_key = target_section.lower().strip()
    
    # Map input request variants smoothly to our dictionary keys
    key_mapping = {
        "introduction": "introduction", "detector": "detector", "cms detector": "detector",
        "simulation": "simulation", "monte carlo": "simulation", "datasets": "simulation",
        "reconstruction": "reconstruction", "objects": "reconstruction",
        "event selection": "selection", "selection": "selection",
        "background": "background", "background estimation": "background",
        "systematic": "systematics", "systematic uncertainties": "systematics",
        "results": "results", "summary": "conclusion", "conclusion": "conclusion", "summary and conclusion": "conclusion"
    }
    
    lookup_key = key_mapping.get(normalized_key, normalized_key)
    
    for filename in os.listdir(cache_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(cache_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                full_text = f.read()
                
            # Generate the dictionary using your workflow strategy
            document_sections = parse_document_into_sections(full_text)
            
            if lookup_key in document_sections:
                section_text = document_sections[lookup_key]
                all_lines = section_text.split("\n")
                
                # Filter out empty space fragments and numerical citations
                prose_lines = [l.strip() for l in all_lines if l.strip() and not re.match(r'^\s*\[\d+\]', l)]
                
                # Take the chosen text volume allocation window
                content_lines = prose_lines[:window_lines]
                cleaned_block = " ".join(content_lines)
                cleaned_block = re.sub(r'\s+', ' ', cleaned_block)[:2000]
                
                extracted_snippets.append(f"--- Style Context from {filename} [{lookup_key.upper()} SECTION] ---\n{cleaned_block}")
                
    return "\n\n".join(extracted_snippets[:2])


# =========================================================================
# STRATEGY 2: SENTENCE / LONG-PHRASE PROXIMITY MATCHING RAG EXTRACTOR
# =========================================================================
def retrieve_style_context_phrase_based(target_phrase: str, cache_dir="data/cache_text", window_lines=8) -> str:
    """
    Normalizes a long prompt sentence or phrase and matches it against the 
    reference files using whitespace-insensitive substring signatures. 
    Gathers a targeted surrounding contextual line window.
    """
    if not os.path.exists(cache_dir) or not target_phrase.strip():
        return ""
        
    extracted_snippets = []
    
    # Clean the input target sentence to make it robust against raw line-break mismatches
    clean_target = re.sub(r'\s+', ' ', target_phrase.strip().lower())
    
    # If the sentence is extremely long, pull its core component to maximize search hits
    if len(clean_target.split()) > 10:
        clean_target = " ".join(clean_target.split()[:7])

    # Transform phrase tokens into a flexible regex pattern allowing intermediate spacing/newlines
    search_pattern = re.escape(clean_target).replace(r'\ ', r'\s+')
    
    for filename in os.listdir(cache_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(cache_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Reassemble document text with indices to accurately pin down line hits
            full_doc_text = "".join(lines)
            match = re.search(search_pattern, full_doc_text, re.IGNORECASE)
            
            if match:
                # Character offset tracking to map the match back to specific line numbers
                matched_char_index = match.start()
                preceding_text = full_doc_text[:matched_char_index]
                hit_line_number = preceding_text.count("\n")
                
                # Gather surrounding line padding window
                start_idx = max(0, hit_line_number - 2)
                end_idx = min(len(lines), hit_line_number + window_lines)
                
                context_block = "".join(lines[start_idx:end_idx]).strip()
                context_block = re.sub(r'\s+', ' ', context_block)
                
                extracted_snippets.append(f"--- Style Context via Proximity Search from {filename} ---\n{context_block}")
                
                # Exit early for this file once a high-quality neighborhood hit is achieved
                if len(extracted_snippets) >= 2:
                    break
                    
    return "\n\n".join(extracted_snippets[:2])
