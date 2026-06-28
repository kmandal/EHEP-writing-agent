from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class HEPContext(BaseModel):
    theory_framework: str = Field(..., description="The underlying BSM theory framework.")
    theory_citation: str = Field(default="", description="Strict citation key for the theory framework.")
    target_signal: str = Field(..., description="The specific signal process being probed.")
    signal_citation: str = Field(default="", description="Strict citation key for the signal process cross-section.")
    decay_topology: str = Field(..., description="The step-by-step decay final states.")
    motivation: str = Field(..., description="The theoretical problem solved or kinematic innovations.")

class ExperimentalSetup(BaseModel):
    collider_experiment: str = Field(..., description="e.g., Proton-Proton collisions at LHC, CMS Detector.")
    energy_sqrt_s: str = Field(..., description="Center of mass energy, e.g., 13 TeV.")
    luminosity: str = Field(..., description="Integrated luminosity profile, e.g., 138 fb^-1.")
    data_samples: str = Field(..., description="Primary dataset details across data-taking periods.")
    simulation_samples: str = Field(..., description="Generators used for signal, background, and detector simulation details.")

class SignalModeling(BaseModel):
    fastsim_grid: str = Field(..., description="Parameters governing the SMS grid points, mass variations, and step sizes.")

class ObjectSelection(BaseModel):
    event_reconstruction: str = Field(..., description="Core reconstruction algorithms utilized.")
    primary_vertex: str = Field(..., description="Primary vertex specifications.")
    muons: str = Field(..., description="Muon selection thresholds.")
    electrons: str = Field(..., description="Electron selection thresholds.")
    jets_btagging: str = Field(..., description="Jet definitions and b-tagging metrics.")
    met: str = Field(..., description="Missing transverse energy calculation nuances.")

class BackgroundEstimation(BaseModel):
    composition: str = Field(default="Not specified", description="Prompt backgrounds layout.")
    prompt_lepton_method: str = Field(default="Not specified", description="Methods for isolating prompt lepton estimations.")
    prompt_lepton_validation: str = Field(default="Not specified", description="Validation procedures for prompt setups.")
    fake_lepton_method: str = Field(default="Not specified", description="Data-driven fake rate implementation mechanics.")
    fake_lepton_validation: str = Field(default="Not specified", description="Validation closure and data validation sideband strategies.")

class StatisticalInterpretations(BaseModel):
    systematics_signal: str = Field(default="Not specified", description="Uncertainties on signal yields.")
    systematics_prompt_bkg: str = Field(default="Not specified", description="Uncertainties on prompt backgrounds.")
    systematics_fake_bkg: str = Field(default="Not specified", description="Uncertainties on fake/non-prompt backgrounds.")
    statistical_model: str = Field(default="Not specified", description="The specific test statistic, framework tools, and tracking targets like CLs.")

class EHEPPaperState(BaseModel):
    """
    The global shared memory state tracking the analysis parameters 
    along with the progressive generated LaTeX outputs for each section.
    """
    # Physics Metadata Parameters
    context: Optional[HEPContext] = None
    setup: Optional[ExperimentalSetup] = None
    signal: Optional[SignalModeling] = None
    objects: Optional[ObjectSelection] = None
    backgrounds: Optional[BackgroundEstimation] = None
    statistics: Optional[StatisticalInterpretations] = None
    
    # Paper Compilation State (Shared memory filled sequentially by sub-agents)
    latex_document_title: str = "Search for pair production of scalar top quarks in single lepton final state with compressed mass spectra"
    latex_abstract: str = ""
    latex_introduction: str = ""
    latex_detector_setup: str = ""
    latex_object_selection: str = ""
    latex_background_estimation: str = ""
    latex_systematics: str = ""
    latex_results: str = ""
