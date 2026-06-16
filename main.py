import os
import re
from src.state import (
    EHEPPaperState, HEPContext, ExperimentalSetup, 
    SignalModeling, ObjectSelection, BackgroundEstimation, StatisticalInterpretations
)

def read_markdown_file(file_path: str) -> str:
    """Reads the raw text contents of the input file securely."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing analysis input file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_bracket_content(section_text: str, label_keywords: list) -> str:
    """
    Finds bullet lines containing specific keywords and extracts 
    the text wrapped inside the [...] brackets.
    """
    for line in section_text.split('\n'):
        if any(kw.lower() in line.lower() for kw in label_keywords):
            # Regex to find everything between the first '[' and the last ']'
            match = re.search(r'\[(.*)\]', line)
            if match:
                return match.group(1).strip()
    return "Not specified"

def parse_analysis_markdown(file_path: str) -> EHEPPaperState:
    """Parses individual blocks from the markdown file into validated Pydantic models."""
    content = read_markdown_file(file_path)
    
    # Split the document by the numbered Markdown headers
    # e.g., '## 1. HEP Context & Phenomenology'
    sections = re.split(r'##\s+\d+\.', content)
    
    # Map section fragments into a structured dictionary
    section_map = {}
    for sec in sections:
        lines = sec.strip().split('\n')
        if not lines or lines[0] == '':
            continue
        header_title = lines[0].lower()
        section_map[header_title] = sec

    # Helper function to match fuzzy section headers
    def find_section_text(keyword: str) -> str:
        for title, text in section_map.items():
            if keyword in title:
                return text
        return ""

    # 1. Parse Context Block
    context_text = find_section_text("context")
    context_mod = HEPContext(
        theory_framework=extract_bracket_content(context_text, ["framework"]),
        target_signal=extract_bracket_content(context_text, ["target signal"]),
        decay_topology=extract_bracket_content(context_text, ["decay topology"]),
        motivation=extract_bracket_content(context_text, ["motivation"])
    )

    # 2. Parse Experimental Setup Block
    setup_text = find_section_text("experimental")
    setup_mod = ExperimentalSetup(
        collider_experiment=extract_bracket_content(setup_text, ["collider"]),
        energy_sqrt_s=extract_bracket_content(setup_text, ["energy"]),
        luminosity=extract_bracket_content(setup_text, ["luminosity"]),
        data_samples=extract_bracket_content(setup_text, ["data samples"]),
        simulation_samples=extract_bracket_content(setup_text, ["simulation"])
    )

    # 3. Parse Signal Modeling Block
    signal_text = find_section_text("signal")
    signal_mod = SignalModeling(
        fastsim_grid=extract_bracket_content(signal_text, ["fastsim"])
    )

    # 4. Parse Object Selection Block
    obj_text = find_section_text("object")
    obj_mod = ObjectSelection(
        event_reconstruction=extract_bracket_content(obj_text, ["reconstruction"]),
        primary_vertex=extract_bracket_content(obj_text, ["primary vertex"]),
        muons=extract_bracket_content(obj_text, ["muons"]),
        electrons=extract_bracket_content(obj_text, ["electrons"]),
        jets_btagging=extract_bracket_content(obj_text, ["jets"]),
        met=extract_bracket_content(obj_text, ["missing transverse"])
    )

    # 5. Parse Background Estimation Block
    bkg_text = find_section_text("background")
    bkg_mod = BackgroundEstimation(
        composition=extract_bracket_content(bkg_text, ["composition"]),
        prompt_lepton_method=extract_bracket_content(bkg_text, ["prompt lepton method"]),
        prompt_lepton_validation=extract_bracket_content(bkg_text, ["prompt lepton validation"]),
        fake_lepton_method=extract_bracket_content(bkg_text, ["fake lepton method"]),
        fake_lepton_validation=extract_bracket_content(bkg_text, ["fake lepton validation"])
    )

    # 6. Parse Statistical Context Block
    stat_text = find_section_text("statistical")
    stat_mod = StatisticalInterpretations(
        systematics_signal=extract_bracket_content(stat_text, ["uncertainties (on signals)"]),
        systematics_prompt_bkg=extract_bracket_content(stat_text, ["prompt lepton background"]),
        systematics_fake_bkg=extract_bracket_content(stat_text, ["non-prompt lepton background"]),
        statistical_model=extract_bracket_content(stat_text, ["statistical model"])
    )

    # Instantiate the global EHEPPaperState with all sub-modules populated dynamically
    global_state = EHEPPaperState(
        context=context_mod,
        setup=setup_mod,
        signal=signal_mod,
        objects=obj_mod,
        backgrounds=bkg_mod,
        statistics=stat_mod
    )
    
    return global_state

def main():
    print("="*60)
    print("Executing Automated Dynamic Metadata Ingestion Engine...")
    print("="*60)
    
    input_file = "data/analysis_input.md"
    
    try:
        # Run parsing framework
        paper_state = parse_analysis_markdown(input_file)
        
        print("\n[✓] SUCCESS: All analysis metadata compiled into global state memory.")
        print("-" * 60)
        print(f"Validated Working Title : {paper_state.latex_document_title}")
        print(f"Target Collider/Detector: {paper_state.setup.collider_experiment}")
        print(f"Luminosity Phase Space  : {paper_state.setup.luminosity}")
        print(f"Trigger Paths Isolated  : {paper_state.objects.event_reconstruction}")
        print(f"Muon Selection Window   : {paper_state.objects.muons}")
        print(f"Electron Crossover Cut  : {paper_state.objects.electrons}")
        print(f"Jet Energy Corrections  : {paper_state.objects.jets_btagging}")
        print(f"Fake-Lepton Method      : {paper_state.backgrounds.fake_lepton_method}")
        print(f"Statistical Framework   : {paper_state.statistics.statistical_model}")
        print("-" * 60)
        
    except Exception as e:
        print(f"\n[X] CRITICAL INGESTION ERROR: {str(e)}")

if __name__ == "__main__":
    main()