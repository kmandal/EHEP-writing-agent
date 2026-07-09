import os
import re
from src.state import (
    EHEPPaperState,
    Section1Introduction,
    Section2DetectorSetUpTriggerSystem,
    Section3DatasetsSimulatedSamples,
    Section4EventReconstructionObjectIdentification,
    Section5EventSelectionCriteriaAnalysisStrategy,
    Section6BackgroundEstimationMethods,
    Section7SystematicUncertainties,
    Section8ResultsInterpretations,
    Section9SummaryConclusion
)
from src.orchestrator import EHEPPaperOrchestrator
from src.bibliography_builder import generate_bibliography_file
from src.citation_utils import should_skip_bibtex_generation, generate_phrase_citation_dict
from src.rag_storage import convert_sample_pdfs_to_text

def read_markdown_file(file_path: str) -> str:
    """Reads the raw text contents of the input file securely."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing analysis input file: {os.path.abspath(file_path)}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_and_build_bibliography(markdown_content: str):
    """
    Exclusively parses keys securely wrapped inside the explicit :CITE:{...} brace blocks.
    Skips API interaction if a validated references.bib file is already cached.
    """
    if should_skip_bibtex_generation("references.bib"):
        return

    print("[Engine] Local cache invalid or missing. Scanning input metadata for strict brace-enclosed citation anchors...")
    extracted_keys = []

    # Find everything inside :CITE:{...} or :cite:{...}
    brace_matches = re.findall(r'(?:CITE|cite)\s*:\s*\{([^}]+)\}', markdown_content)
    for match in brace_matches:
        parts = re.split(r'[,\s]+', match)
        for part in parts:
            clean_part = part.strip().strip('.').strip(')').strip('(')
            if clean_part and len(clean_part) > 2:
                if clean_part.lower() not in {"minimal", "standard", "accounting", "and"}:
                    extracted_keys.append(clean_part)

    unique_keys = sorted(list(set(extracted_keys)))
    print(f"[Engine] Found {len(unique_keys)} unique validated citation keys.")
    if unique_keys:
        generate_bibliography_file(unique_keys)

def segment_markdown_by_sections(content: str) -> dict:
    sections = {}
    current_section = None
    current_lines = []
    
    for line in content.split('\n'):
        match = re.match(r'^##\s+(\d+)\.', line)
        if match:
            if current_section is not None:
                sections[current_section] = '\n'.join(current_lines)
            current_section = int(match.group(1))
            current_lines = [line]
        else:
            if current_section is not None:
                current_lines.append(line)
                
    if current_section is not None:
        sections[current_section] = '\n'.join(current_lines)
        
    return sections

def extract_field_from_block(block_text: str, markers: list) -> str:
    """
    Robust field content extractor tailored for EHEP markdown parameters.
    Matches the marker by ignoring markdown formatting (*, **), spacing, and case, and cleanly extracts whatever text is captured inside the brackets [...].
    Returns an empty string "" if the marker has no brackets or if brackets are empty.
    """
    for marker in markers:
        #Clean the marker text from regex special characters
        escaped_marker = re.escape(marker.strip())
        
        #Build a regex that permits arbitrary markdown symbols (*, _) and spaces around the marker name and then catches everything inside the subsequent brackets [...]
        pattern = (
            r'(?:^|\n)[*_\s]*' +                 # Optional bullet points and bolding markdown starts
            escaped_marker +                     # The literal parameter key name
            r'[*_\s:]*' +                        # Trailing markdown emphasis closures and colons
            r'(?:\s*\[([^\]]*)\]|\s*(.*))'       # Capture either content inside [...] or any remaining text if no brackets
        )
        
        match = re.search(pattern, block_text, flags=re.IGNORECASE)
        if match:
            # If group(1) matched, it found [...]. If group(2) matched, there were no brackets.
            val = match.group(1) if match.group(1) is not None else match.group(2)
            val = val.strip() if val else ""
            
            # Additional safety: Clean up any hanging bracket typos if group 2 caught anything messy
            if val.startswith('['): val = val[1:]
            if val.endswith(']'): val = val[:-1]
            
            return val.strip()
            
    return ""
    

def parse_analysis_markdown(file_path: str) -> EHEPPaperState:
    """
    Parses metadata headers from analysis_input.md and instantiates the exact fields expected by the Pydantic schemas.
    """
    raw_content = read_markdown_file(file_path)
    sections = segment_markdown_by_sections(raw_content)
    
    # --- Section 1 ---
    s1 = sections.get(1, "")
    sec1_model = Section1Introduction(
        theory_model_framework=extract_field_from_block(s1, ["Theory / Model Framework:"]),
        physics_motivation_innovation=extract_field_from_block(s1, ["Physics Motivation and Innovation:"]),
        target_signal_process=extract_field_from_block(s1, ["Target Signal Process:"]),
        decay_topology_final_state=extract_field_from_block(s1, ["Decay Topology and Final State:"]),
        integrated_luminosity_data_period=extract_field_from_block(s1, ["Collider Experiment:", "Center-of-Mass Energy (\\sqrt{s}):", "Integrated Luminosity (\\int L dt) and data taking period:"])
    )

    # --- Section 2 ---
    s2 = sections.get(2, "")
    sec2_model = Section2DetectorSetUpTriggerSystem(
        detector_component=extract_field_from_block(s2, ["Detector component:"]),
        trigger_setup=extract_field_from_block(s2, ["Trigger setup:"])
    )

    # --- Section 3 ---
    s3 = sections.get(3, "")
    sec3_model = Section3DatasetsSimulatedSamples(
        data_samples=extract_field_from_block(s3, ["Data Samples:"]),
        signal_grid_modeling=extract_field_from_block(s3, ["Signal Grid Modeling:"]),
        simulation_samples_mc=extract_field_from_block(s3, ["Simulation Samples (MC):"])
    )

    # --- Section 4 ---
    s4 = sections.get(4, "")
    sec4_model = Section4EventReconstructionObjectIdentification(
        event_reconstruction=extract_field_from_block(s4, ["Event reconstruction:"]),
        primary_vertex_pv=extract_field_from_block(s4, ["Primary Vertex (PV):"]),
        leptons=extract_field_from_block(s4, ["Leptons:"]),
        muons=extract_field_from_block(s4, ["Muons:"]),
        standard_electrons=extract_field_from_block(s4, ["Standard Electrons:"]),
        low_p_t_electrons=extract_field_from_block(s4, ["Low P_T Electrons:"]),
        electron_combination=extract_field_from_block(s4, ["Electron combination:"]),
        jets_b_tagging=extract_field_from_block(s4, ["Jets and b-tagging:"]),
        missing_transverse_momentum=extract_field_from_block(s4, ["Missing Transverse Momentum (E_T^miss or MET):"]),
        soft_b=extract_field_from_block(s4, ["Soft b:"])
    )

    # --- Section 5 ---
    s5 = sections.get(5, "")
    sec5_model = Section5EventSelectionCriteriaAnalysisStrategy(
        primary_trigger_paths=extract_field_from_block(s5, ["Primary Trigger Paths:"]),
        data_quality_requirement=extract_field_from_block(s5, ["Data Quality requirement:"]),
        event_weight_for_fullsim_mc_samples=extract_field_from_block(s5, ["Event weight for fullsim MC samples:"]),
        event_weight_for_fastsim_mc_signal_samples=extract_field_from_block(s5, ["Event weight for fastsim MC signal samples:"]),
        preselection_baseline=extract_field_from_block(s5, ["Preselection Baseline:"]),
        search_signal_regions_sr=extract_field_from_block(s5, ["Search / Signal Regions (SR):", "SR1 (0 b-jet):", "SR2 (>= 1 b-jet):", "SR3 (>= 1 soft b):"]),
        search_bins=extract_field_from_block(s5, ["Search bins:", "CT:", "MT(Transverse mass of lepton):", "Lepton p_T:"])
    )

    # --- Section 6 ---
    s6 = sections.get(6, "")
    sec6_model = Section6BackgroundEstimationMethods(
        background_composition=extract_field_from_block(s6, ["Background composition:"]),
        estimation_methodology=extract_field_from_block(s6, ["Estimation methodology:"]),
        prompt_lepton_background_estimation=extract_field_from_block(s6, ["Prompt lepton background Estimation:", "Method:", "Validation:"]),
        non_prompt_lepton_background_estimation=extract_field_from_block(s6, ["Non-prompt lepton background Estimation:", "Method:", "Validation:"])
    )
    
    # --- Section 7 ---
    s7 = sections.get(7, "")
    sec7_model = Section7SystematicUncertainties(
        systematic_uncertainties_experimental=extract_field_from_block(s7, ["Systematic Uncertainties (Experimental):"]),
        systematic_uncertainties_theoretical=extract_field_from_block(s7, ["Systematic Uncertainties (Theoretical):"]),
        systematic_uncertainties_limited_statistics=extract_field_from_block(s7, ["Systematic Uncertainties (Limited statistics):"]),
        systematic_uncertainties_on_signals=extract_field_from_block(s7, ["Systematic Uncertainties (on Signals):"]),
        systematic_uncertainties_on_estimated_background=extract_field_from_block(s7, ["Systematic Uncertainties (on estimated background ):", "Prompt lepton background:", "Non-prompt lepton background:"])
    )
    
    # --- Section 8 ---
    s8 = sections.get(8, "")
    sec8_model = Section8ResultsInterpretations(
        total_estimated_backgrounds_and_observed_data_comparison=extract_field_from_block(s8, ["Total estimated backgrounds and observed data comaparison:"]),
        evaluating_constraints_on_signal_model_parameter=extract_field_from_block(s8, ["Evaluating constraints on Signal model parameter:", "Statistical Model:"]),
        limit_report=extract_field_from_block(s8, ["Exclusion limit:", "Limit report:"])
    )


    # --- Section 9 ---
    s9 = sections.get(9, "")
    sec9_model = Section9SummaryConclusion(
        summary=extract_field_from_block(s9, ["Summary:"]),
        conclusion=extract_field_from_block(s9, ["Conclusion:"])
    )

    return EHEPPaperState(
        sec1_intro=sec1_model,
        sec2_detector=sec2_model,
        sec3_datasets=sec3_model,
        sec4_objects=sec4_model,
        sec5_selection=sec5_model,
        sec6_backgrounds=sec6_model,
        sec7_systematics=sec7_model,
        sec8_results=sec8_model,
        sec9_conclusion=sec9_model
    )


def main():
    print("="*60)
    print("🚀 INITIALIZING AGENTIC EHEP PAPER GENERATION ENGINE")
    print("="*60)
    
    input_file = "data/analysis_input.md"
    
    try:
        raw_markdown = read_markdown_file(input_file)
        
        # 1: INITIALIZE LOCAL TEXT RAG CACHE
        print("[RAG Setup] Checking and building local CMS style text caches...")
        convert_sample_pdfs_to_text(pdf_dir="data/sample_papers", output_dir="data/cache_text")
        
        # 2. Run the safe checked bibliography generation
        extract_and_build_bibliography(raw_markdown)
        
        # 3. Extract the phrase-to-citation dictionary mapping
        phrase_citation_dict = generate_phrase_citation_dict(input_file, "references.bib")
        print(f"[Engine] Compiled Phrase-to-Citation Map containing {len(phrase_citation_dict)} specific anchor markers.")
        
        # 4. Parse input markdown configurations into memory state
        paper_state = parse_analysis_markdown(input_file)
        print("\n[✓] SUCCESS: Hierarchical data parsed into memory without schema conflicts.")
        
        # 5. Instantiate the agent Orchestrator, passing the phrase map as an option
        orchestrator = EHEPPaperOrchestrator(paper_state, phrase_citation_map=phrase_citation_dict)
        final_paper_path = orchestrator.run_workflow()
        
        print("\n==================== WORKFLOW CYCLE COMPLETE ====================")
        print(f"[🎉] Target compiled document saved successfully at: {final_paper_path}")
        
    except Exception as e:
        print(f"\n[❌] CRITICAL RUNTIME ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
