import os
import json

def get_figure_block(section_name: str) -> str:
    manifest_path = "data/figure_manifest.json"
    if not os.path.exists(manifest_path):
        return ""
        
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        fig_blocks = []
        for fig in data.get("figures", []):
            if fig.get("section") != section_name:
                continue
                
            placement = fig.get('placement', 'htbp') # defaulting to standard flexible placement
            caption = fig.get('caption', '')
            
            # Check if this figure config is single image or a side-by-side array
            filenames = fig.get('filenames')
            if not filenames:
                # Fallback check if it was named singular "filename" in json
                filenames = [fig.get('filename')] if fig.get('filename') else []
                
            if len(filenames) == 1:
                # Standard single plot environment
                block = f"""
                \\begin{{figure}}[{placement}]
                \\centering
                \\includegraphics[width=0.48\\textwidth]{{data/fig_table/{filenames[0]}}}
                \\caption{{{caption}}}
                \\label{{fig:{filenames[0].split('.')[0]}}}
                \\end{{figure}}
                """
            elif len(filenames) > 1:
                # Side-by-Side multi-plot environment using elegant standard width allocation
                block = []
                block.append(f"\\begin{{figure}}[{placement}]")
                block.append("  \\centering")
                for fname in filenames:
                    block.append(f"  \\includegraphics[width=0.45\\textwidth]{{data/fig_table/{fname}}}")
                block.append(f"  \\caption{{{caption}}}")
                block.append(f"  \\label{{fig:{filenames[0].split('.')[0]}_multi}}")
                block.append("\\end{figure}")
                block = "\n".join(block)
                
            fig_blocks.append(block)
        return "\n".join(fig_blocks)
    except Exception as e:
        return f"% Error loading figure manifest: {str(e)}\n"
    
def get_table_block(section_name: str) -> str:
    """
    Scans data/table_manifest.json for references matching the active section,
    compiles the underlying flat txt matrix files, and returns complete booktabs structures.
    """
    manifest_path = "data/table_manifest.json"
    if not os.path.exists(manifest_path):
        return ""
        
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        table_blocks = []
        for tab in data.get("tables", []):
            if tab.get("section") != section_name:
                continue
                
            file_path = os.path.join("data/fig_table", tab.get("filename", ""))
            caption = tab.get("caption", "")
            label = tab.get("label", "")
            
            # Use your custom table converter function cleanly
            compiled_tex_table = compile_txt_table_to_latex(file_path, caption, label)
            if compiled_tex_table:
                table_blocks.append(compiled_tex_table)
                
        return "\n".join(table_blocks)
    except Exception as e:
        print(f"[⚠️ Asset Compiler] Error embedding tables for {section_name}: {e}")
        return ""

def compile_txt_table_to_latex(file_path: str, caption: str, label: str) -> str:
    """Reads a pipeline text table separated by '|' and returns a booktabs LaTeX table."""
    if not os.path.exists(file_path):
        return f"% Table data missing at {file_path}\n"
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
    if not lines:
        return ""
    
    # Parse headers and rows
    headers = [h.strip() for h in lines[0].split("|")]
    rows = []
    for line in lines[1:]:
        rows.append([r.strip() for r in line.split("|")])
        
    # Build column alignment string (e.g., lllp{6cm})
    align_str = "l" * (len(headers) - 1) + "p{6cm}"
    
    tex = []
    tex.append(r"\begin{table*}[ht!]")
    tex.append(r"\centering")
    tex.append(r"\resizebox{\textwidth}{!}")
    tex.append(f"\\caption{{{caption}}}")
    tex.append(f"\\label{{tab:{label}}}")
    tex.append(f"\\begin{{tabular}}{{{align_str}}}")
    tex.append(r"\toprule")
    tex.append(" & ".join([f"\\textbf{{{h}}}" for h in headers]) + r" \\")
    tex.append(r"\midrule")
    
    for row in rows:
        # Escape raw percentage signs in text lines safely if not already done
        escaped_row = [item.replace("%", r"\%") if "%" in item and "\\" not in item else item for item in row]
        tex.append(" & ".join(escaped_row) + r" \\")
        
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}")
    tex.append(r"\end{table*}")
    
    return "\n".join(tex)


def get_section_asset_manifests() -> dict:
    """
    Reads data/figure_manifest.json and data/table_manifest.json
    and maps available labels and captions by their target section keys.
    """
    asset_instructions = {
        "latex_introduction": [],
        "latex_detector_setup": [],
        "latex_datasets_samples": [],
        "latex_object_reconstruction": [],
        "latex_event_selection": [],
        "latex_background_estimation": [],
        "latex_systematics": [],
        "latex_results": [],
        "latex_summary_conclusion": []
    }
    
    # 1. Map Figures
    fig_path = os.path.join("data", "figure_manifest.json")
    if os.path.exists(fig_path):
        try:
            with open(fig_path, "r", encoding="utf-8") as f:
                fig_data = json.load(f)
                for fig in fig_data.get("figures", []):
                    sec = fig.get("section")
                    if sec in asset_instructions:
                        # Determine label format matching asset_compiler.py
                        filenames = fig.get("filenames")
                        if not filenames:
                            filenames = [fig.get("filename")] if fig.get("filename") else []
                        if filenames:
                            lbl = f"fig:{filenames[0].split('.')[0]}"
                            asset_instructions[sec].append({"type": "Figure", "label": lbl, "caption": fig.get("caption", "")})
        except Exception as e:
            print(f"[!] Error parsing figure manifest: {e}")

    # 2. Map Tables
    tab_path = os.path.join("data", "table_manifest.json")
    if os.path.exists(tab_path):
        try:
            with open(tab_path, "r", encoding="utf-8") as f:
                tab_data = json.load(f)
                for tab in tab_data.get("tables", []):
                    # Table sections use "Systematics", map to the state naming convention
                    sec_raw = tab.get("section", "")
                    sec = "latex_systematics" if "systemat" in sec_raw.lower() else sec_raw
                    if sec in asset_instructions:
                        lbl = f"tab:{tab.get('label', '')}"
                        asset_instructions[sec].append({"type": "Table", "label": lbl, "caption": tab.get("caption", "")})
        except Exception as e:
            print(f"[!] Error parsing table manifest: {e}")
            
    return asset_instructions
