import os
import re
import json

def verify_latex_assets(compiled_tex: str):
    """
    Cross-checks the final compiled LaTeX paper draft against visual 
    and tabular manifests to print warnings if any references are missing.
    """
    missing_detected = False
    print("\n[Verification Pass] Running validation scan on compiled text...")
    
    # 1. Check Figures
    if os.path.exists("data/figure_manifest.json"):
        with open("data/figure_manifest.json", "r", encoding="utf-8") as f:
            fig_data = json.load(f)
            for fig in fig_data.get("figures", []):
                filenames = fig.get("filenames") or [fig.get("filename")]
                if filenames:
                    lbl = f"fig:{filenames[0].split('.')[0]}"
                    ref_macro = f"\\ref{{{lbl}}}"
                    if ref_macro not in compiled_tex:
                        print(f"  [!] Warning: Asset target '{lbl}' is not mentioned via \\ref{{{lbl}}} in the body text.")
                        missing_detected = True
                        
    # 2. Check Tables
    if os.path.exists("data/table_manifest.json"):
        with open("data/table_manifest.json", "r", encoding="utf-8") as f:
            tab_data = json.load(f)
            for tab in tab_data.get("tables", []):
                lbl = f"tab:{tab.get('label', '')}"
                ref_macro = f"\\ref{{{lbl}}}"
                if ref_macro not in compiled_tex:
                    print(f"  [!] Warning: Asset target '{lbl}' is not mentioned via \\ref{{{lbl}}} in the body text.")
                    missing_detected = True
                    
    if not missing_detected:
        print("  [✓] Success: All figures and tables verified as referenced inside the text body.")


def clean_markdown_artifacts(text: str) -> str:
    """Removes backtick environments accidentally wrapped by standard LLM text completions."""
    return re.sub(r'^```latex\n|^```\n|```$', '', text, flags=re.MULTILINE)

    
def filter_duplicate_citations(text: str) -> str:

    global_cited_history = set()

    def filter_first_citations(match):
        raw_keys_str = match.group(1)
        # Handle multi-key citations gracefully (e.g., \cite{key1, key2})
        individual_keys = [k.strip() for k in raw_keys_str.split(",") if k.strip()]
        unique_new_keys = []
        
        for key in individual_keys:
            if key not in global_cited_history:
                unique_new_keys.append(key)
                global_cited_history.add(key)
                
        # If all keys in this specific cite macro were already used earlier, remove the macro entirely
        if not unique_new_keys:
            return "" 
        return f"\\cite{{{', '.join(unique_new_keys)}}}"

    print("[Editorial Pass] Enforcing citation first-occurrence rule globally...")
    return re.sub(r'\\cite\s*\{([^}]+)\}', filter_first_citations, text)


def clean_and_escape_latex_prose(text: str) -> str:
    lines = text.split("\n")
    processed_lines = []

    for line in lines:
        # Pass structural block definitions completely through unchanged
        if any(line.strip().startswith(token) for token in ["\\begin", "\\end", "\\section", "\\subsection"]):
            processed_lines.append(line)
            continue

        # Step 1: Handle unescaped percent signs first
        # Replace % with \% only if it isn't already preceded by a backslash
        line = re.sub(r'(?<!\\)%', r'\\%', line)

        # Step 2: Fragment the line by math strings ($...$), LaTeX commands (\\ref{...}, \\cite{...}), 
        # and filesystem paths to isolate plain text words for underscore escaping.
        # This matches $...$, \command{...}, or paths like data/fig_table/...
        tokens = re.split(r'(\$[^\$]*\$|\\[a-zA-Z]+\{[^\}]*\}|data/fig_table/\S+)', line)
        
        for i in range(len(tokens)):
            if not tokens[i]:
                continue
            # If the token is NOT math, NOT a LaTeX command macro argument, and NOT a figure directory path:
            if not (tokens[i].startswith('$') or tokens[i].startswith('\\') or tokens[i].startswith('data/fig_table')):
                # Safely escape any unescaped underscore in plain text words
                tokens[i] = re.sub(r'(?<!\\)_', r'\\_', tokens[i])
                
        processed_lines.append("".join(tokens))

    return "\n".join(processed_lines)

def escape_text_underscores(text: str) -> str:
    lines = text.split("\n")
    processed_lines = []

    for line in lines:
        # 1. Skip completely if the line contains structural macros or file paths
        if any(token in line for token in ["\\ref{", "\\label{", "\\cite{", "\\includegraphics", "data/fig_table"]):
            processed_lines.append(line)
            continue
            
        # 2. Skip if it's part of an environment toggle or structural section header
        if any(line.strip().startswith(token) for token in ["\\begin", "\\end", "\\section", "\\subsection"]):
            processed_lines.append(line)
            continue

        # 3. For standard prose lines, separate math chunks ($...$) from normal text
        parts = re.split(r'(\$[^\$]*\$)', line)
        for i in range(len(parts)):
            # If it's a plain text chunk (not wrapped in dollars), escape raw underscores safely
            if not parts[i].startswith('$'):
                # Lookahead to verify it doesn't already have a backslash escape
                parts[i] = re.sub(r'(?<!\\)_', r'\\_', parts[i])
        
        processed_lines.append("".join(parts))

    return "\n".join(processed_lines)


def build_final_skeleton(skeleton: str, title: str, abstract: str, body: str) -> str:
    """Stitches structural layout replacements seamlessly into your master template skeleton."""
    # Strip any citations from the abstract layout safely
    clean_abstract = re.sub(r'\\cite\{[^}]*\}', '', abstract) if abstract else "Drafting processing placeholder abstract."
    
    final_tex = skeleton.replace("__PAPER_TITLE__", title)
    final_tex = final_tex.replace("__PAPER_ABSTRACT__", clean_abstract.strip())
    final_tex = final_tex.replace("__PAPER_BODY__", body)
    return final_tex
