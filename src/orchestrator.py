# src/orchestrator.py
from src.state import EHEPPaperState
from src.agents import (
    draft_introduction_section, 
    draft_experimental_setup, 
    draft_object_selection,
    draft_background_estimation,
    draft_statistical_interpretation,
    review_and_align_all_sections
)
from src.tools import save_latex_output

class EHEPPaperOrchestrator:
    def __init__(self, state: EHEPPaperState):
        self.state = state

    def run_workflow(self):
        print("="*50)
        print("[⚡] Starting Local Multi-Agent Drafting Pipeline")
        print("="*50)
        
        # 1. Domain specialists work independently on their milestones
        self.state.latex_introduction = draft_introduction_section(self.state)
        self.state.latex_detector_setup = draft_experimental_setup(self.state)
        self.state.latex_object_selection = draft_object_selection(self.state)
        self.state.latex_background_estimation = draft_background_estimation(self.state)
        self.state.latex_systematics = draft_statistical_interpretation(self.state)
        
        # 2. Central Editorial Reviewer resolves cross-references and merges
        polished_document = review_and_align_all_sections(self.state)
        
        # 3. Save the finalized macro document
        save_latex_output(filename="compiled_paper_draft.tex", content=polished_document)
        
        print("\n[✓] Pipeline execution finished. Check outputs/compiled_paper_draft.tex!")
        return self.state
