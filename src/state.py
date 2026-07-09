from pydantic import BaseModel, Field
from typing import Optional

class Section1Introduction(BaseModel):
    theory_model_framework: str = Field(..., description="BSM framework details (SUSY, MSSM, etc.).")
    physics_motivation_innovation: str = Field(..., description="Innovations like compressed spectra and dark matter relic density.")
    target_signal_process: str = Field(..., description="The specific signal process targeted (e.g., pp -> t~ t~*).")
    decay_topology_final_state: str = Field(..., description="4-body decay details yielding 1 lepton + jets + MET.")
    collider_experiment: str = Field(default="CMS Detector", description="LHC collider and experiment.")
    center_of_mass_energy: str = Field(default="13 TeV", description="Sqrts parameter.")
    integrated_luminosity_data_period: str = Field(..., description="Integrated luminosity mapping over data taking years.")

class Section2DetectorSetUpTriggerSystem(BaseModel):
    detector_component: str = Field(..., description="Physical descriptions of sub-detectors (Tracker, ECAL, HCAL, Muon system).")
    trigger_setup: str = Field(..., description="Two layer trigger system specifications (L1 and HLT).")

class Section3DatasetsSimulatedSamples(BaseModel):
    data_samples: str = Field(..., description="UltraLegacy datasets and integrated luminosity profile.")
    signal_grid_modeling: str = Field(..., description="SMS parameters, mass grids, parameters m_s and neutralino mass steps.")
    simulation_samples_mc: str = Field(..., description="Generators used (MadGraph5, PYTHIA, FastSim, Geant4) and pileup modeling.")

class Section4EventReconstructionObjectIdentification(BaseModel):
    event_reconstruction: str = Field(..., description="Particle flow algorithm and standard physics objects.")
    primary_vertex_pv: str = Field(..., description="Primary Vertex fit requirements and selection rule.")
    leptons: str = Field(..., description="Lepton strategy and hybrid isolation criteria rules.")
    muons: str = Field(..., description="Muon pT, eta, isolation, and vertex impact parameter cuts.")
    standard_electrons: str = Field(..., description="Standard electron selection thresholds.")
    low_p_t_electrons: str = Field(..., description="Specialized low pT electron selection with BDT scores.")
    electron_combination: str = Field(..., description="Overlap resolution strategy between standard and low pT collections.")
    jets_b_tagging: str = Field(..., description="anti-kt R=0.4 jet criteria and DeepCSV working points.")
    missing_transverse_momentum: str = Field(..., description="Type-1 corrected PF MET nuances.")
    soft_b: str = Field(..., description="Identification of low pT b-quarks via secondary vertex reconstruction.")

class Section5EventSelectionCriteriaAnalysisStrategy(BaseModel):
    primary_trigger_paths: str = Field(..., description="Primary HLT trigger path paths.")
    data_quality_requirement: str = Field(..., description="MET filters, L1 prefire, and HEM failure adjustments.")
    event_weight_for_fullsim_mc_samples: str = Field(..., description="Correction scale factors for FullSim background simulation.")
    event_weight_for_fastsim_mc_signal_samples: str = Field(..., description="FastSim vs FullSim calibration scale factors.")
    preselection_baseline: str = Field(..., description="Baseline kinematic selection triggers (MET, HT, jet/lepton vetoes).")
    search_signal_regions_sr: str = Field(..., description="SR1, SR2, and SR3 categorization logic based on b-jet multiplicity.")
    search_bins: str = Field(..., description="Binning schema detailing the 108 categories across CT, MT, and lepton pT.")

class Section6BackgroundEstimationMethods(BaseModel):
    background_composition: str = Field(..., description="Prompt vs non-prompt background breakdowns.")
    estimation_methodology: str = Field(..., description="Summary of simulation vs data-driven pathways.")
    prompt_lepton_background_estimation: str = Field(..., description="Simultaneous profile likelihood fit across CRs and SRs and validation tests.")
    non_prompt_lepton_background_estimation: str = Field(..., description="Data-driven ABCD method using tight-to-loose ratios from MR applied to AR.")

class Section7SystematicUncertainties(BaseModel):
    systematic_uncertainties_experimental: str = Field(..., description="Experimental nuisance impacts.")
    systematic_uncertainties_theoretical: str = Field(..., description="Theoretical scaling and modeling nuisance shapes.")
    systematic_uncertainties_limited_statistics: str = Field(..., description="MC sample count limit uncertainties.")
    systematic_uncertainties_on_signals: str = Field(..., description="Percentage impacts on signal yields.")
    systematic_uncertainties_on_estimated_background: str = Field(..., description="Percentage impacts on background models including prompt normalization and closure errors.")

class Section8ResultsInterpretations(BaseModel):
    total_estimated_backgrounds_and_observed_data_comparison: str = Field(..., description="Summary of SM yield agreement with data.")
    evaluating_constraints_on_signal_model_parameter: str = Field(..., description="Statistical test statistics, profile likelihood configurations, and limits.")
    limit_report: str = Field(..., description="Final 95% CL mass limits for the scalar top and LSP.")

class Section9SummaryConclusion(BaseModel):
    summary: str = Field(..., description="High level summary of the analysis characteristics.")
    conclusion: str = Field(..., description="Final limits statement and context comparison within LHC physics.")

class EHEPPaperState(BaseModel):
    """
    The updated linear shared-memory state configuration.
    Classes directly mirror sections inside analysis_input.md.
    """
    # Section Metadata Models
    sec1_intro: Optional[Section1Introduction] = None
    sec2_detector: Optional[Section2DetectorSetUpTriggerSystem] = None
    sec3_datasets: Optional[Section3DatasetsSimulatedSamples] = None
    sec4_objects: Optional[Section4EventReconstructionObjectIdentification] = None
    sec5_selection: Optional[Section5EventSelectionCriteriaAnalysisStrategy] = None
    sec6_backgrounds: Optional[Section6BackgroundEstimationMethods] = None
    sec7_systematics: Optional[Section7SystematicUncertainties] = None
    sec8_results: Optional[Section8ResultsInterpretations] = None
    sec9_conclusion: Optional[Section9SummaryConclusion] = None
    
    # Core state parameters...
    target_journal: str = Field(default="JHEP", description="Target journal layout style (e.g., JHEP, PRD, EPJC)")
    latex_document_title: str = "Search for pair production of scalar top quarks in single lepton final state with compressed mass spectra"
    # Sequential LaTeX Generation Pipeline Buffers
    latex_abstract: str = ""
    latex_introduction: str = ""
    latex_detector_setup: str = ""
    latex_datasets_samples: str = ""
    latex_object_selection: str = ""
    latex_event_selection: str = ""
    latex_background_estimation: str = ""
    latex_systematics: str = ""
    latex_results: str = ""
    latex_summary_conclusion: str = ""
