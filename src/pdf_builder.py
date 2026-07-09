import os
import re
import shutil
import subprocess
import urllib.request


def ensure_jhep_style(output_dir: str = "outputs"):
    """
    Downloads the official JHEP.bst style file if missing locally.Uses the official live SISSA repository link to avoid 404 errors.
    Change the journal according to the target one.
    """
    target_path = os.path.join(output_dir, "JHEP.bst")
    if not os.path.exists(target_path):
        print("[PDF Builder] JHEP.bst style file missing. Downloading official tracking layout...")
        url = "https://jhep.sissa.it/jhep/help/JHEP/TeXclass/DOCS/JHEP.bst"
        try:
            # Add a basic User-Agent header to prevent automated scraping blocks from academic servers
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req) as response:
                with open(target_path, 'wb') as f:
                    f.write(response.read())
            
            # Secure copy to root directory for global pipeline access
            shutil.copy(target_path, "JHEP.bst")
            print("[PDF Builder] JHEP.bst successfully cached locally from SISSA.")
        except Exception as e:
            print(f"[⚠️ Warning] Could not download JHEP.bst: {e}. LaTeX may fall back to default styling.")


def sanitize_bib_file(bib_path: str):
    """
    Safely removes or escapes characters like raw '%' in bib databases that cause BibTeX to hit fatal syntax crashes.
    """
    if not os.path.exists(bib_path):
        return
    print(f"[PDF Builder] Sanitizing bibliography entries inside: {bib_path}")
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Escape % characters to \% unless they are already escaped
    sanitized = re.sub(r'(?<!\\)%', r'\\%', content)
    
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(sanitized)
    print(f"[✓] Bibliography database sanitized cleanly.")

def compile_tex_to_pdf(tex_path: str, output_dir: str = "outputs") -> bool:
    """
    Synchronized, multi-pass LaTeX compilation pipeline.
    Executes pdflatex -> bibtex -> pdflatex -> pdflatex sequentially, managing local directory dependencies and style paths cleanly.
    """
    if not os.path.exists(tex_path):
        print(f"[❌ PDF Builder] Source file not found: {tex_path}")
        return False
        
    print("\n" + "="*50)
    print("🚀 INITIALIZING SYNCHRONIZED MULTI-PASS LATEX PIPELINE")
    print("="*50)
    
    #1: Initialize folders and styles
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(tex_path))[0]
    root_dir = os.getcwd()
    
    ensure_jhep_style(output_dir)

    #2: Synchronize and sanitize reference data
    dest_bib = os.path.join(output_dir, "references.bib")
    if os.path.exists("references.bib"):
        shutil.copy("references.bib", dest_bib)
    elif os.path.exists("data/references.bib"):
        shutil.copy("data/references.bib", dest_bib)
        
    sanitize_bib_file(dest_bib)

    #3: Check for local style files and sync them to outputs
    if os.path.exists("JHEP.bst"):
        shutil.copy("JHEP.bst", os.path.join(output_dir, "JHEP.bst"))

    pdflatex_cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={output_dir}",
        tex_path
    ]
    
    try:
        #PASS 1: Generate auxiliary file hooks ---
        print("[PDF Builder] Pass 1/4: Running pdflatex (Creating layout markers)...")
        subprocess.run(pdflatex_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        #PASS 2: Compile references via BibTeX ---
        print("[PDF Builder] Pass 2/4: Running bibtex (Resolving citations)...")
        env = os.environ.copy()
        env["BSTINPUTS"] = f".:{root_dir}:{output_dir}:"
        env["BIBINPUTS"] = f".:{root_dir}:{output_dir}:"
        
        bib_result = subprocess.run(
            ["bibtex", base_name], 
            cwd=output_dir,
            env=env,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        
        # Safe Style Fallback check: If bibtex failed because of missing style file, patch it to 'unsrt'
        bib_output = bib_result.stdout if bib_result.stdout else ""
        if bib_result.returncode != 0 and "I couldn't open style file" in bib_output:
            print("[⚠️ Style Patch] JHEP style missing in environment. Auto-switching document to standard 'unsrt' style fallback...")
            aux_path = os.path.join(output_dir, f"{base_name}.aux")
            if os.path.exists(aux_path):
                with open(aux_path, "r", encoding="utf-8") as f:
                    aux_content = f.read()
                aux_content = re.sub(r'\\bibstyle\{.*?\}', r'\\bibstyle{unsrt}', aux_content)
                with open(aux_path, "w", encoding="utf-8") as f:
                    f.write(aux_content)
                subprocess.run(["bibtex", base_name], cwd=output_dir, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        
        #PASS 3: Bind structural bibliography markers ---
        print("[PDF Builder] Pass 3/4: Running pdflatex (Injecting references)...")
        subprocess.run(pdflatex_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        #PASS 4: Final layout and reference reconciliation ---
        print("[PDF Builder] Pass 4/4: Running pdflatex (Final cross-reference alignment)...")
        subprocess.run(pdflatex_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
        if os.path.exists(pdf_path):
            print(f"\n[✓] SUCCESS: PDF compiled cleanly at: {pdf_path}")
            print("="*50 + "\n")
            return True
        else:
            print("[❌ PDF Builder] Compilation completed but PDF file was not generated.")
            return False
            
    except Exception as e:
        print(f"[❌ PDF Builder Error] Critical runtime error: {str(e)}")
        return False
