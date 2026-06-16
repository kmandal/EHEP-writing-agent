from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class HEPContext(BaseModel):
    theory_framework: str = Field(..., description="The underlying BSM theory framework, e.g., MSSM Natural SUSY.")
    target_signal: str = Field(..., description="The specific signal process being probed, e.g., stop pair production.")
    decay_topology: str = Field(..., description="The step-by-step decay final states including specific physics objects.")
    motivation: str = Field(..., description="The theoretical problem solved or the kinematic phase space innovation.")

class ExperimentalSetup(BaseModel):
    collider_experiment: str = Field(..., description="e.g., Proton-Proton collisions at LHC, CMS Detector.")
    energy_sqrt_s: str = Field(..., description="Center of mass energy, e.g., 13 TeV.")
    luminosity: str = Field(..., description="Integrated luminosity profile, e.g., 138 fb^-1.")
    data_samples: str = Field(..., description="Primary dataset details across data-taking periods.")
    simulation_samples: str = Field(..., description="Generators used for signal, background, and detector simulation details.")

class SignalModeling(BaseModel):
    fastsim_grid: str = Field(..., description="Parameters governing the SMS grid points, mass variations, and step sizes.")

class ObjectSelection(BaseModel):
    event_reconstruction: str = Field(..., description="Reconstruction algorithms used, e.g., Particle Flow.")
    primary_vertex: str = Field(..., description="Cuts and configuration for defining the primary interaction vertex.")
    muons: str = Field(..., description="Transverse momentum, isolation, and impact parameter cuts for muons.")
    electrons: str = Field(..., description="Standard and low-pT hybrid electron selection and ID scores.")
    jets_btagging: str = Field(..., description="Jet clustering algorithm, pT thresholds, jet energy corrections and b-tagging working points.")
    met: str = Field(..., description="Missing transverse momentum corrections and filtering.")

class BackgroundEstimation(BaseModel):
    composition: str = Field(..., description="Dominant, sub-dominant, prompt, and non-prompt background breakdowns.")
    prompt_lepton_method: str = Field(..., description="Profile likelihood fit strategy across control and search regions.")
    prompt_lepton_validation: str = Field(..., description="Validation region definitions and extrapolation testing.")
    fake_lepton_method: str = Field(..., description="Data-driven ABCD/fake-rate method matrix details.")
    fake_lepton_validation: str = Field(..., description="Simulation closure and data validation sideband strategies.")

class StatisticalInterpretations(BaseModel):
    systematics_signal: str = Field(..., description="Uncertainties on signal yields.")
    systematics_prompt_bkg: str = Field(..., description="Uncertainties on prompt backgrounds.")
    systematics_fake_bkg: str = Field(..., description="Uncertainties on fake/non-prompt backgrounds.")
    statistical_model: str = Field(..., description="The specific test statistic, framework tools, and tracking targets like CLs.")

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