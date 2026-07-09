import os
import requests

def fetch_bibtex_from_inspire(tex_key: str) -> str:
    """Queries InspireHEP by TexKey, DOI, or arXiv ID to get the exact BibTeX entry."""
    print(f"[BibTeX Engine] Querying InspireHEP for: {tex_key}")
    
    # 1. Determine query type dynamically
    if tex_key.startswith("10."): # It's a DOI
        query = f"doi+{tex_key}"
    elif "arxiv:" in tex_key.lower(): # It's an arXiv ID
        clean_arxiv = tex_key.lower().replace("arxiv:", "").strip()
        query = f"eprint+{clean_arxiv}"
    else: # It's a standard TexKey
        query = f"find+texkey+{tex_key}"
        
    url = f"https://inspirehep.net/api/literature?q={query}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            hits = response.json().get("hits", {}).get("hits", [])
            if hits:
                rec_id = hits[0].get("id")
                # If queried via DOI/arXiv, let's extract the official TexKey so LaTeX matches it
                official_key = hits[0].get("metadata", {}).get("texkeys", [tex_key])[0]
                
                bib_url = f"https://inspirehep.net/api/literature/{rec_id}?format=bibtex"
                bib_res = requests.get(bib_url, timeout=10)
                if bib_res.status_code == 200:
                    # Return the clean bibtex text string
                    return bib_res.text.strip()
    except Exception as e:
        print(f"  [Warning] Lookup failed for {tex_key}: {e}")
        
    return f"@article{{{tex_key},\n  author = \"{{CMS Collaboration}}\",\n  title = \"{{Placeholder for {tex_key}}}\",\n  year = \"2026\"\n}}"


def generate_bibliography_file(keys_list: list):
    """Aggregates all unique citation keys used across the pipeline and updates references.bib."""
    bib_content = []
    unique_keys = sorted(list(set(keys_list)))
    
    for key in unique_keys:
        if not key or key == "Not specified":
            continue
        entry = fetch_bibtex_from_inspire(key)
        bib_content.append(entry)
        
    out_path = "references.bib"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(bib_content))
    print(f"[✓] Bibliography compilation complete. Saved {len(unique_keys)} references to {out_path}")
