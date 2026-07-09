import os
import time
from src.state import EHEPPaperState
from src.agents import EHEPAgents
from src.asset_compiler import get_section_asset_manifests

class EHEPPaperOrchestrator:
    def __init__(self, state: EHEPPaperState, phrase_citation_map: dict = None):
        self.state = state
        self.phrase_citation_map = phrase_citation_map or {}

    def run_workflow(self) -> str:
        print("\n" + "="*60)
        print("[Orchestrator] Launching High-Precision Paper Generation Pipeline")
        print("="*60)

        # Initialize the singular agent cluster instance
        agents = EHEPAgents()

        # Load asset manifest mappings dynamically from src/asset_compiler.py
        asset_manifests = get_section_asset_manifests()

        def build_section_grounding(section_name_json: str, state_key: str) -> str:
            grounding = ""
            
            # 1. Section Citations
            section_citations = {}
            if section_name_json in self.phrase_citation_map:
                section_citations = self.phrase_citation_map[section_name_json]
            elif isinstance(self.phrase_citation_map, dict) and not any(isinstance(v, dict) for v in self.phrase_citation_map.values()):
                section_citations = self.phrase_citation_map

            if section_citations:
                grounding += "\n\n[STRICT INLINE CITATION GROUNDING MATRIX]\n"
                grounding += "You MUST explicitly integrate the following LaTeX citations into your prose text.\n"
                grounding += "Whenever your description touches upon or implies the scientific concept in the 'Phrase anchor', you MUST append its exact citation macro literal:\n"
                for phrase, cite_cmd in section_citations.items():
                    grounding += f"  - Phrase anchor: '{phrase}' ➔ You MUST use exactly: {cite_cmd}\n"
                grounding += "CRITICAL: Do NOT invent, shorten, or modify these citation keys. Place them naturally near their matching phrase context.\n"

            # 2. Section Assets (Split Figures and Tables completely to prevent prose mixups)
            assets = asset_manifests.get(state_key, [])
            if assets:
                figures = [a for a in assets if a['type'].lower() == 'figure']
                tables = [a for a in assets if a['type'].lower() == 'table']
                
                if figures or tables:
                    grounding += "\n\n[STRICT INLINE ASSET RE-REFERENCING MATRIX]\n"
                    grounding += "The following visual/data elements belong to this section. Introduce and reference them naturally using standard LaTeX macros:\n"
                
                if figures:
                    grounding += "  --- FIGURES ---\n"
                    for fig in figures:
                        grounding += f"  - For Figure label '{fig['label']}', introduce its physics contents or distribution trends naturally in the text using exactly: \\ref{{{fig['label']}}} (e.g., '...is shown in Fig.~\\ref{{{fig['label']}}}' or '...as illustrated in Fig.~\\ref{{{fig['label']}}}'). Do NOT call a Figure a Table.\n"
                
                if tables:
                    grounding += "  --- TABLES ---\n"
                    for tab in tables:
                        grounding += f"  - For Table label '{tab['label']}', describe the summarized values or selection cuts naturally in the text using exactly: \\ref{{{tab['label']}}} (e.g., '...are summarized in Table~\\ref{{{tab['label']}}}' or '...is detailed in Table~\\ref{{{tab['label']}}}'). Do NOT call a Table a Figure.\n"
                
                grounding += "CRITICAL: Integrate these references smoothly into the body narrative where the specific physics check happens. Do not pile them at the absolute end.\n"

            return grounding


        # --- Section 1: Introduction ---
        print("[Orchestrator] Executing Section 1: Introduction Agent...")
        introduction_grounding = build_section_grounding("Introduction", "latex_introduction")
        self.state = agents.draft_introduction(self.state, introduction_grounding)
        

        # --- Section 2: Detector Setup ---
        print("[Orchestrator] Executing Section 2: Detector Setup and Trigger Agent...")
        detector_grounding = build_section_grounding("Detector Setup and Trigger System", "latex_detector_setup")
        self.state = agents.draft_detector_setup(self.state, detector_grounding)
        

        # --- Section 3: Datasets & Samples ---
        print("[Orchestrator] Executing Section 3: Datasets and Simulated Samples Agent...")
        datasets_grounding = build_section_grounding("Datasets and Simulated Samples", "latex_datasets_samples")
        self.state = agents.draft_datasets_samples(self.state, datasets_grounding)
        

        # --- Section 4: Object Identification ---
        print("[Orchestrator] Executing Section 4: Event Reconstruction and Object ID Agent...")
        reco_grounding = build_section_grounding("Event Reconstruction and Object Identification", "latex_object_selection")
        self.state = agents.draft_object_selection(self.state, reco_grounding)
        

        # --- Section 5: Event Selection & Strategy ---
        print("[Orchestrator] Executing Section 5: Event Selection and Analysis Strategy Agent...")
        selection_grounding = build_section_grounding("Event Selection and Analysis Strategy", "latex_event_selection")
        self.state = agents.draft_event_selection(self.state, selection_grounding)
        

        # --- Section 6: Background Estimation ---
        print("[Orchestrator] Executing Section 6: Background Estimation Methods Agent...")
        bg_grounding = build_section_grounding("Background Estimation Methods", "latex_background_estimation")
        self.state = agents.draft_background_estimation(self.state, bg_grounding)
        

        # --- Section 7: Systematic Uncertainties ---
        print("[Orchestrator] Executing Section 7: Systematic Uncertainties Agent...")
        sys_grounding = build_section_grounding("Systematic Uncertainties", "latex_systematics")
        self.state = agents.draft_systematics(self.state, sys_grounding)
        

        # --- Section 8: Results & Interpretations ---
        print("[Orchestrator] Executing Section 8: Results and Statistical Interpretations Agent...")
        results_grounding = build_section_grounding("Results and Statistical Interpretations", "latex_results")
        self.state = agents.draft_results(self.state, results_grounding)
        

        # --- Section 9: Summary & Conclusion ---
        print("[Orchestrator] Executing Section 9: Summary and Conclusion Agent...")
        conclusion_grounding = build_section_grounding("Summary and Conclusion", "latex_summary_conclusion")
        self.state = agents.draft_summary_conclusion(self.state, conclusion_grounding)
        

        # --- Abstract Synthesis Step ---
        print("\n[Orchestrator] Invoking Abstract Agent for multi-model document summary extraction...")
        self.state = agents.generate_document_abstract(self.state)
            
        # --- Master Modular Compilation Pass ---
        print("\n[Orchestrator] Running compilation assembly and modular section polishing...")
        final_tex = agents.compile_and_polish(self.state)
        
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "compiled_paper_draft.tex")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_tex)
            
        return output_path
