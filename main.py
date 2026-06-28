import os
import re
from src.state import (
    EHEPPaperState, HEPContext, ExperimentalSetup, 
    SignalModeling, ObjectSelection, BackgroundEstimation, StatisticalInterpretations
)
from src.orchestrator import EHEPPaperOrchestrator

def read_markdown_file(file_path: str) -> str:
    """Reads the raw text contents of the input file securely."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing analysis input file: {os.path.abspath(file_path)}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_field(content: str, keywords: list) -> str:
    """
    Scans the entire text line by line to locate the given keywords 
    and extracts the bracketed content safely.
    """
    for line in content.split('\n'):
        if any(kw.lower() in line.lower() for kw in keywords):
            match = re.search(r'\[(.*)\]', line)
            if match:
                return match.group(1).strip()
    return "Not specified"

def parse_analysis_markdown(file_path: str) -> EHEPPaperState:
    """Parses individual blocks from the markdown file directly via sequential text mapping."""
    content = read_markdown_file(file_path)
    
    # Direct Extraction via exact field keywords
    context_model = HEPContext(
        theory_framework=extract_field(content, ["Theory / Model Framework"]),
        theory_citation=extract_field(content, ["Theory Framework Citation Key"]),
        target_signal=extract_field(content, ["Target Signal Process"]),
        signal_citation=extract_field(content, ["Target Signal Citation Key"]),
        decay_topology=extract_field(content, ["Decay Topology & Final State"]),
        motivation=extract_field(content, ["Physics Motivation"])
    )

    setup_model = ExperimentalSetup(
        collider_experiment=extract_field(content, ["Collider & Experiment"]),
        energy_sqrt_s=extract_field(content, ["Center-of-Mass Energy"]),
        luminosity=extract_field(content, ["Integrated Luminosity"]),
        data_samples=extract_field(content, ["Primary Dataset"]),
        simulation_samples=extract_field(content, ["Simulation Samples"])
    )

    signal_model = SignalModeling(
        fastsim_grid=extract_field(content, ["Signal SMS Grid"])
    )

    objects_model = ObjectSelection(
        event_reconstruction=extract_field(content, ["Core Reconstruction Algorithm"]),
        primary_vertex=extract_field(content, ["Primary Interaction Vertex Criteria"]),
        muons=extract_field(content, ["Muon Identification"]),
        electrons=extract_field(content, ["Electron Identification"]),
        jets_btagging=extract_field(content, ["Jet Clustering"]),
        met=extract_field(content, ["Missing Transverse Momentum"])
    )

    
    backgrounds_model = BackgroundEstimation(
        composition=extract_field(content, ["Background souurce and composition"]),
        prompt_lepton_method=extract_field(content, ["Prompt Lepton Background Estimation Strategy"]),
        prompt_lepton_validation=extract_field(content, ["Prompt Lepton Background Estimation Method Validation"]),
        fake_lepton_method=extract_field(content, ["Non-prompt Lepton Background Estimation Strategy"]),
        fake_lepton_validation=extract_field(content, ["Non-prompt Lepton Background Validation with MC closure test and data validation"])
    )

    statistics_model = StatisticalInterpretations(
        systematics_signal=extract_field(content, ["Systematic Uncertainties (on Signals)"]),
        systematics_prompt_bkg=extract_field(content, ["Systematic Uncertainties (on estimated background )"]),
        systematics_fake_bkg=extract_field(content, ["Non-prompt lepton background"]),
        statistical_model=extract_field(content, ["LHC Statistical Framework Configuration"])
    )

    return EHEPPaperState(
        context=context_model,
        setup=setup_model,
        signal=signal_model,
        objects=objects_model,
        backgrounds=backgrounds_model,
        statistics=statistics_model
    )

def main():
    print("="*60)
    print("🚀 INITIALIZING AGENTIC EHEP PAPER GENERATION ENGINE")
    print("="*60)
    
    input_file = "data/analysis_input.md"
    
    try:
        # Parse text directly using the absolute file path location
        paper_state = parse_analysis_markdown(input_file)
        print("\n[✓] SUCCESS: All analysis metadata parsed smoothly into active RAM.")
        print(f"    Loaded Theory Framework: {paper_state.context.theory_framework}")
        print(f"    Loaded Experiment Config: {paper_state.setup.collider_experiment}")
        print(f"    Loaded Event Object Description: {paper_state.objects.event_reconstruction}")
        print(f"    Loaded Background Estimation Methods: {paper_state.backgrounds.composition}")
        print(f"    Loaded Systematics and Statistical Interpretation: {paper_state.statistics.statistical_model}")
        
        # Initialize the local orchestrator with the parsed state configuration
        orchestrator = EHEPPaperOrchestrator(state=paper_state)
        
        # Run workflow: Drafting -> Reviewing -> Exporting Compiled Code
        orchestrator.run_workflow()
        
        print("\n" + "="*20 + " WORKFLOW CYCLE COMPLETE " + "="*20)
        
    except Exception as e:
        print(f"\n[X] CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    main()