# EHEP Analysis Input Metadata: Prompt Scalar Top Search

## 1. HEP Context & Phenomenology
* **Theory / Model Framework:** [Suppersymmetry (SUSY), Minimal Supersymmetric Standard Model (MSSM), R-parity conserving simplified model, Natural SUSY]
* **Theory Framework Citation Key:** [Martin:1997un]
* **Target Signal Process:** [Pair production of scalar top quarks (pp -> t~ t~*)]
* **Target Signal Citation Key:** [CMS-SUS-21-002]
* **Decay Topology & Final State:** [Each scalar top (stop) undergoes 4-body decay to a bottom quark, pair of ferimions and a neutralino (t~ -> b + ff' + chi_1^0), for one stop, this pair of fermions are lepton and neutrino, leading to a final state of one lepton + jets + missing transverse momentum (E_T^miss), these jets include b-tagged jets]
* **Physics Motivation & Innovation:** [Addressing the gauge hierarchy problem via natural SUSY, treating neutralino as lightest supersymmetric paticle (LSP) in R-parity conserving model, making netralino as a dark matter candidate, accounting for observed relic density via stop-neutralino co-annihilation in compressed mass spectra; exploring challenging compressed phase space to probe if susy is hidden in this less explored territory]

## 2. Experimental Setup & Datasets
* **Collider & Experiment:** [Proton-proton collisions at LHC, CMS Detector]
* **Center-of-Mass Energy (\sqrt{s}):** [13 TeV]
* **Integrated Luminosity (\int L dt) & data taking period:** [138 fb^-1 for full Run 2 data during the year of 2016, 2017 and 2018]
* **Data Samples:** [Run2 UltraLegacy data samples corresponding to an integrated luminosity of 35.9 fb^−1 , 41.5 fb^−1 , and 59.8 fb^−1 for 2016, 2017 and 2018 data taking periods respectively, MET primary datasets]
* **Simulation Samples (MC):** [For signal,generated with MadGraph5_aMC@NLO followed by decay, hadronization and showering in PYTHIA and a modeling of the detector response and reconstruction with the CMS FastSim package, For background MC processes, generated with MadGraph except for single top where POWHEG is used and then hadronization and showering in PYTHIA followed by Geant4 full simulation, Additional minimum bias interactions (”pileup”) were also simulated and mixed with all simulated samples]

## 3. Signal Modeling
* **FastSim Signal Grid:** [Under simplified model spectra (SMS) consideration, stop decays to 4-body final state with 100% BR. In such a simplified model, there are only two parameters to account for: the stop mass m_s which defines the production cross section and the neutralino mass that affects strongly the final state kinematics, Instead of the latter, the mass difference between the stop and the neutralino \Delta m  can also be used, which is then assumed to be ≤ 80 GeV for compressed signal search, for the signal grid, signal points are defined with followinf parameters: m_s is sampled in 25 GeV steps between 250 GeV and 1100 GeV while the mass differ-
ence was sampled in about 5 GeV steps between 10-30 GeV and in steps of 10 GeV between 30-80 GeV, the fast Geant4 simulation is used for grid signal points production]

## 4. Object Identification & Selection Criteria
* **Event reconstruction:** [Particle flow (PF) algorithm, Standrard physics objects following the reccomendation from POG]
* **Primary Vertex (PV):** [Fit quality: N_dof >= 5, fiducial volume: |z| < 24 cm, PV with largest quadratic sum of the transverse momenta is chosen]
* **Leptons :** [Muon, combination of standard GED electron and low p_T electron collection, Hybrid Isolation critearia: Iso = Relative Isolation * p_T (Iso_abs)if p_T =< 12 GeV else  Relative Isolation (Iso_rel)]
* **Muons :** [p_T > 3 GeV, |eta| < 2.4, Iso_abs < 2.4 GeV, Iso_rel <0.2, Muon POG recommended Loose working points, dxy <0.02 cm, dz < 0.1 cm]
* **Standard Electrons :** [p_T > 5 GeV, |eta| < 2.5, Iso_abs < 2.4 GeV, Iso_rel <0.2, loose ID, dxy <0.02 cm, dz < 0.1 cm]
* **Low P_T Electrons :** [p_T > 3 GeV, |eta| < 2.5, Iso_abs < 2.4 GeV, Iso_rel <0.2, MVA ID; BDT score >2.5, dxy <0.02 cm, dz < 0.1 cm]
* **Electron combination :** [For p_T > 5 GeV, prefer standard electron rosolving overlap between standard and low p_T electron, for p_T < 5 GeV, autometically chose low p_T electron]
* **Jets & b-tagging:** [anti-k_t algorithm with R=0.4, p_T > 20 GeV, |eta| < 2.4, JetMET POG recommended ID, JES and JER correction; DeepCSV algorithm medium working point]
* **Missing Transverse Momentum (E_T^miss or MET):** [Type-1 corrected PF E_T^miss]

## 5. Event Selection Criteria & event weight
* **Primary Trigger Paths:** [HLT_PFMET120_PFMHT120_IDTight]
* **Data Quality requirement:** [MET filters, L1 prefire for partial 2016. 2017 data, HEM 15/16 failure for partial 2018 data]
* **Event weight for fullsim MC samples:** [Event pileup reweighting, L1 prefire reweight, HEM reweight, Lepton p_T rewight for W+jets sample, Lepton SF, B-jet tagging SF, Trigger SF]
* **Event weight for fastsim MC signal samples:** [Trigger efficiency, Lepton fastsim-fullsim SF]

## 6. Analysis Strategy & Phase Space Mapping
* **Preselection Baseline:** [e.g., At least 1 isolated lepton, >= 4 jets, E_T^miss > 250 GeV]
* **Search / Signal Regions (SR):** * *SR1 (Low \Delta m):* [Define cuts: e.g., low b-jet multiplicity, specific M_T2 thresholds]
  * *SR2 (High \Delta m):* [Define cuts: e.g., high p_T jets, explicit top-tagged jets]
* **Control Regions (CR):**
  * *ttbar CR:* [e.g., Inverting b-tagging or lepton requirements to isolate ttbar process]
  * *W+jets CR:* [e.g., Requiring 0 b-tagged jets and specific transverse mass M_T window]

## 7. Background Estimation Methods
* **Background composition:** [Among the SM background the dominant one is W+jets, Next part equally shared by ttbar and dibosn (VV), contribution from Z+jets and QCD multijets is small except low p_T SR bins, Background from other sources like single top (tW), Drell Yan (DY) and ttV are samll, the backfround processes divided into two categories depending on the origin of the reocnstructed lepton;If the lepton comes from the prompt decay of W, Z or τ, it goes to the prompt lepton background category, and the remaining leptons, called non-prompt, belong to the fake lepton background]
* **Estimation Methodology:** [Prompt lepton background is estimated from MC because of well-modeled simulation of electro-weak processes, Fake lepton backgrounde is etimated utilizing a data-driven method]
* **Prompt lepton background Estimation:** * *Method:* [ Estimated from simulation scaled to the data normalization measured in control regions; Technically, simultaneous Profile Likelihood Fit across CRs and SRs using normalization factors, All SM processes contributing to the prompt lepton background exibit similar shape in lepton p_T distribution indicating all of them could be corrected with a single normalixation factor, However, due to the difference in uncertainties associated with each proceses, we group them into three: W + jets, tt̄, and ’Other prompt’ where Other Prompt consists of tW, VV, DY, and ttV processes. We use a single normalization factor for all these three categories]  * *Validation:* [Validation tests are performed in 2 validation regions associated to control/search region pairs, This is achieved by
performing a control-region-only fit in each validation region and then comparing the data and prediction in the ’search region’ part of the validation region, First validation region is defined in CT side bin; 200 < CT < 300 GeV, second validation region is defined defined by altering the hard b-tag jet (p_T > 60 GeV) requirements by selecting N_b−jet(hard) ≥ 1]
* **Non-prompt lepton background Estimation:** * *Method:* [ Utilizing ABCD method, SR contribution (A) estimated from the data in application region (B) by weighting with fake rate or tigh-to-loose ratio (C/D) which is measured from data in measurement region, fake rate is the probability of a fake or non-prompt lepton being selected as an analysis lepton, i.e., passing the analysis lepton selection (aka tight selection), fake rate is calculated as the fraction of events containing a tight lepton to the events with loose-not-tight lepton, i.e., a lepton passes the loose criteria but but fails the tight selection, loose criteria for muons: Iso_abs < 24 GeV, Iso_rel <2, no upper cut on dz, loose criteria for standard electrons: Iso_abs < 24 GeV, Iso_rel <2, cut-based-veto ID, no upper cut on dz, loose criteria for low p_T electrons: Iso_abs < 24 GeV, Iso_rel <2, BDT score > 3, no upper cut on dz, all other criterion are same as tight ones, MR refion selection: MET < 50 GeV, one loose lepton, Transverse Mass(MT) < 40 GeV N_jets(p_T > 40 GeV) >=1, N_b−jet(hard) = 0, In the measurement region, due to trigger efficiency and prescale considerations, different datasets and trigger paths are employed for the fake rate measurement, ensuring an unbiased and efficient selection across the full lepton p_T spectrum, fake rate is measured seperately for muon and electron (seperating by lepton type) and after subtracting prompt lepton contribution from data, application region (AR) has excatly same selection criterion as of SR except for lepton selection condition where leptons are required to pass the loose and fail the tight criteria, each SR bin has its correcpoding AR bin, while weighting the AR data by tight-to-loose ratio, prompt lepton contribution is also subtracted from the AR data]  * *Validation:* [Two types of validation test: simultion based closure test and data calidation test, closure test performed with Z+jets and QCD MC samples by comparing the predicted yield obtained utilizing the medthod with the direct yield obtained using MC truth information, data validation is done in MET side band validation region (VR); 200 < MET < 300 GeV) by forming psedo SR-AR pair and using tight-to-loose ratio obtained from MR data]

## 8. Statistical Interpretations & Uncertainties
* **Systematic Uncertainties (Experimental):** [luminosity, pilup and L1 prefire weight and due to several object selections in the analysis]
* **Systematic Uncertainties (Theoretical):** [MC cross section, renormalization/Factorization scales, parton sdistribution functions (PDFs) modeling]
* **Systematic Uncertainties (Limited statistics):** [one of the major source of uncertainties is due to the limitation of MC statistics]
* **Systematic Uncertainties (on Signals):** [Integrated luminosity: 1.2-2.5%, Pileup 1-2%, Jet Energy Corrections (JEC): 2-5%, b-tagging efficiency scale factors: 1-3%, lepton efficiency SF: 1-2%, ISR jet multiplicity correction: 1%, L1 prefire correction: 1-2%, PDF uncertainties: <1%, Renormalization and factorization uncertainties: <1%, MC cross-section: 2-5%, Trigger efficiency and SF: 1-3%, Statistical uncertainty due to limited MC sample]
* **Systematic Uncertainties (on estimated background ):** * *Prompt lepton background:* [ntegrated luminosity: 1.2-2.5%, Pileup 1-2%, Jet Energy Corrections (JEC): 2-5%, b-tagging efficiency scale factors: 1-3%\
, lepton efficiency SF: 1-2%, ISR jet multiplicity correction: 1%, L1 prefire correction: 1-2%, MC cross-section: 2-5%, Trigger SF: 1-2%, Statistical uncertainty due to limited MC sample, uncertainty on normalization factor] * *Non-prompt lepton background:* [uncertainty from the closure test: 1-20%, uncertainty from data validation 1-40%]
* **LHC Statistical Framework Configuration:** * *Statistical Model:* Profile Likelihood Ratio test statistic utilizing Nuisance Parameters (NP) with Gaussian/Lognormal priors. * *Tools:* CMS combine Tool
  * *Result Track Target:* ["Limit Setting" using the CL_s method to extract 95% CL upper limits on cross-sections]
  * *Key Diagnostic Metrics:* [ Post-fit NP pulls (\hat{\theta} - \theta_0)/\sigma_\theta, and NP impact checks on signal strength \hat{\mu}]