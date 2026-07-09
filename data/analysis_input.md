# EHEP Analysis Input Metadata: Prompt Scalar Top Search

## 1. Introduction
* **Theory / Model Framework:** [Suppersymmetry (SUSY) :CITE:{10.1142/9789812839657_0001, 10.1103/PhysRevD.31.1581}, Minimal Supersymmetric Standard Model (MSSM), R-parity :CITE:{10.1016/0370-2693(78)90858-4} conserving scenario, Natural SUSY :CITE:{arXiv:1110.6926, arXiv:1110.6670, arXiv:1212.6847}]
* **Physics Motivation and Innovation:** [Higgs discovery :CITE:{arXiv:1207.7214, arXiv:1207.7235, arXiv:1303.4571}, addressing the gauge hierarchy problem via natural SUSY, treating neutralino as lightest supersymmetric paticle (LSP) in R-parity conserving model, making netralino as a dark matter candidate :CITE:{Balazs:2004ae}, accounting for observed relic density via stop-neutralino co-annihilation in compressed mass spectra; exploring challenging compressed phase space to probe if susy is hidden in this less explored territory]
* **Target Signal Process:** [Under simplified model :CITE:{10.1007/JHEP04(2014)117, 10.1103/PhysRevD.79.075020} consideration, Pair production of scalar top quarks (pp -> t~ t~*)]
* **Decay Topology and Final State:** [Each scalar top (stop) undergoes 4-body decay to a bottom quark, pair of ferimions and a neutralino (t~ -> b + ff' + chi_1^0), for one stop, this pair of fermions are lepton and neutrino, leading to a final state of one lepton + jets + missing transverse momentum (E_T^miss), these jets include b-tagged jets]
* **Collider Experiment:** [Proton-proton collisions at LHC, CMS Detector]
* **Center-of-Mass Energy (\sqrt{s}):** [13 TeV]
* **Integrated Luminosity (\int L dt) and data taking period:** [138 fb^-1 for full Run 2 data during the year of 2016, 2017 and 2018]


## 2. Detector SetUp & Trigger System
* **Detector component:** [The CMS experiment :CITE:{10.1088/1748-0221/3/08/S08004} structure, Sub-detectors: Tracker, ECAL, HCAL and Muon system] 
* **Trigger setup:** [Data acquisition, Two layer trigger structure: hardwar based level one trigger :CITE:{arXiv:2006.10165}, and software based high level trigger :CITE:{arXiv:1609.02366}]


## 3. Datasets & Simulated samples
* **Data Samples:** [Run2 UltraLegacy data samples corresponding to an integrated luminosity of 35.9 fb^−1 , 41.5 fb^−1 , and 59.8 fb^−1 for 2016, 2017 and 2018 data taking periods respectively, MET primary datasets]
* **Signal Grid Modeling:** [Under simplified model spectra (SMS) consideration, stop decays to 4-body final state with 100% BR. In such a simplified model, there are only two parameters to account for: the stop mass m_s which defines the production cross section and the neutralino mass that affects strongly the final state kinematics, Instead of the latter, the mass difference between the stop and the neutralino \Delta m  can also be used, which is then assumed to be ≤ 80 GeV for compressed signal search, for the signal grid, signal points are defined with following parameters: m_s is sampled in 25 GeV steps between 250 GeV and 1100 GeV while the mass difference was sampled in about 5 GeV steps between 10-30 GeV and in steps of 10 GeV between 30-80 GeV]
* **Simulation Samples (MC):** [For signal,generated with MadGraph5_aMC@NLO :CITE:{arXiv:1405.0301} followed by decay, hadronization and showering in PYTHIA :CITE:{arXiv:1410.3012} and a modeling of the detector response and reconstruction with the CMS FastSim package :CITE:{10.1088/1742-6596/331/3/032049, 10.1088/1742-6596/513/2/022012}. For background MC processes, generated with MadGraph except for single top where POWHEG :CITE:{arXiv:0907.4076, arXiv:1009.2450} is used and then hadronization and showering in PYTHIA followed by Geant4 :CITE:{10.1016/S0168-9002(03)01368-8} full simulation, Additional minimum bias interactions (”pileup”) were also simulated and mixed with all simulated samples]


## 4. Event Reconstruction & Object Identification
* **Event reconstruction:** [Particle flow (PF) algorithm :CITE:{arXiv:1706.04965}, Standard physics objects]
* **Primary Vertex (PV):** [Fit quality: N_dof >= 5, fiducial volume: |z| < 24 cm, PV with largest quadratic sum of the transverse momenta is chosen]
* **Leptons:** [Muon :CITE:{arXiv:1804.04528}, combination of standard GED electron :CITE:{arXiv:2012.06888}, and low p_T electron collection, Hybrid Isolation critearia: Iso = Relative Isolation * p_T (Iso_abs)if p_T =< 12 GeV else  Relative Isolation (Iso_rel)]
* **Muons:** [p_T > 3 GeV, |eta| < 2.4, Iso_abs < 2.4 GeV, Iso_rel <0.2, Muon POG recommended Loose working points, dxy <0.02 cm, dz < 0.1 cm]
* **Standard Electrons:** [p_T > 5 GeV, |eta| < 2.5, Iso_abs < 2.4 GeV, Iso_rel <0.2, loose ID, dxy <0.02 cm, dz < 0.1 cm] 
* **Low P_T Electrons:** [p_T > 3 GeV, |eta| < 2.5, Iso_abs < 2.4 GeV, Iso_rel <0.2, MVA ID; BDT score >2.5, dxy <0.02 cm, dz < 0.1 cm]
* **Electron combination:** [For p_T > 5 GeV, prefer standard electron rosolving overlap between standard and low p_T electron, for p_T < 5 GeV, autometically chose low p_T electron]
* **Jets and b-tagging:** [anti-k_t algorithm :CITE:{arXiv:0802.1189} with R=0.4, p_T > 20 GeV, |eta| < 2.4, JetMET POG recommended ID, JES and JER correction :CITE:{arXiv:1607.03663}, DeepCSV algorithm medium working point :CITE:{arXiv:1712.07158}]
* **Missing Transverse Momentum (E_T^miss or MET):** [Type-1 corrected PF E_T^miss :CITE:{arXiv:1903.06078}]
* **Soft b:** [ b quark with p_T< 20 GeV, not captured by standard b-jet tagging algorithm, identified secondary vertex (SV) :CITE:{10.1007/JHEP03(2011)136} as soft b if SV satisfy certain selection criterion]

## 5. Event Selection Criteria & Analysis Strategy
* **Primary Trigger Paths:** [HLT_PFMET120_PFMHT120_IDTight]
* **Data Quality requirement:** [MET filters, L1 prefire for partial 2016. 2017 data, HEM 15/16 failure for partial 2018 data]
* **Event weight for fullsim MC samples:** [Event pileup reweighting, L1 prefire reweight, HEM reweight, Lepton p_T rewight for W+jets sample, Lepton SF, B-jet tagging SF, Trigger SF]
* **Event weight for fastsim MC signal samples:** [Trigger efficiency, Lepton fastsim-fullsim SF]
* **Preselection Baseline:** [At least 1 selected lepton, at least one ISR jet: leading jet with p_T>100 GeV, MET > 200 GeV, HT > 300 GeV, N_hard-jet =< 2; hard jet: p_T>60 GeV, E_T^miss > 250 GeV, Min(\Delta \Phi (MET, jet))>0.5, Extra lepton (p_T>20 GeV) veto, Hadronic Tau veto]
* **Search / Signal Regions (SR):** [Additional selection after preselection: MET>300GeV and lepton p_T < 50 GeV N_hard b-jet==0; hard b-jet: b-jet woth p_T>60GeV, catergorized into three regions based on b-jet and soft b multiplicity]
  * *SR1 (0 b-jet):* [Target very compressed signal scenario, to reduce W_jets background extra cuts, lepton |\eta|<1.5 and HT > 400 GeV applied, if ISR jet p_T>375 GeV, N_softb==0 required]
  * *SR2 (>= 1 b-jet):* [Targets high \Delta M signals, ISR jet p_T threshold is tightened to 325 GeV]
  * *SR3 (>= 1 soft b):* [Targets all signal points, N_b-jet ==0, ISR jet p_T > 325 GeV]
* **Search bins:** [Each SR is futher divided in the bin of MT, lepton p_T and a bew variable called CT, In total 108 search bins]
  * *CT:* [Two version of CT; for SR1, CT1 defined as min(MET, HT-100), for SR2 and SR3, CT2 defined as min(MET, p_T(ISR jet)-100), Each SR is splitted bins of 300 < CT < 400 GeV and CT > 400 GeV, labeled as ’X’ and ’Y’, respectively]
  * *MT(Transverse mass of lepton):* [ Each CT region is devided into four parts: ’a’: MT < 60 GeV, ’b’: 60 < MT < 95 GeV, ’c’: 95 < MT < 130 GeV, and ’d’: MT > 130 GeV]
  * *Lepton p_T:* [Events are further subdivided according to lepton p_T into five  bins: 3-5, 5-12, 12-20, 20-30, and 30-50 GeV, referred to as 'VL', 'L', 'M', 'H', and 'VH', respectively, Very low lepton p_T bin, 3-5 is not included in 'c' and 'd' MT subregions]



## 6. Background Estimation Methods
* **Background composition:** [Among the SM background the dominant one is W+jets, Next part equally shared by ttbar and dibosn (VV), contribution from Z+jets and QCD multijets is small except low p_T SR bins, Background from other sources like single top (tW), Drell Yan (DY) and ttV are samll, the backfround processes divided into two categories depending on the origin of the reocnstructed lepton;If the lepton comes from the prompt decay of W, Z or τ, it goes to the prompt lepton background category, and the remaining leptons, called non-prompt, belong to the fake lepton background]
* **Estimation methodology:** [Prompt lepton background is estimated from MC because of well-modeled simulation of electro-weak processes, Fake lepton backgrounde is etimated utilizing a data-driven method]
* **Prompt lepton background Estimation:**
  * *Method:* [ Estimated from simulation scaled to the data normalization measured in control regions (CR), CR has exactly same kinematic selections as of SR except for lepton p_T > 5o GeV, One CR bin is assigned for all lepton p_T SR bins inside a given MT bin, Technically, simultaneous Profile Likelihood Fit across CRs and SRs using normalization factors, All SM processes contributing to the prompt lepton background exibit similar shape in lepton p_T distribution indicating all of them could be corrected with a single normalixation factor, However, due to the difference in uncertainties associated with each proceses, we group them into three: W + jets, tt̄, and ’Other prompt’ where Other Prompt consists of tW, VV, DY, and ttV processes. We use a single normalization factor for all these three categories]
  * *Validation:* [Validation tests are performed in 2 validation regions associated to control/search region pairs, This is achieved by
performing a control-region-only fit in each validation region and then comparing the data and prediction in the ’search region’ part of the validation region, First validation region is defined in CT side bin; 200 < CT < 300 GeV, second validation region is defined defined by altering the hard b-tag jet (p_T > 60 GeV) requirements by selecting N_b−jet(hard) ≥ 1]
* **Non-prompt lepton background Estimation:**
  * *Method:* [ Utilizing ABCD method, SR contribution (A) estimated from the data in application region (B) by weighting with fake rate or tigh-to-loose ratio (C/D) which is measured from data in measurement region, fake rate is the probability of a fake or non-prompt lepton being selected as an analysis lepton, i.e., passing the analysis lepton selection (aka tight selection), fake rate is calculated as the fraction of events containing a tight lepton to the events with loose-not-tight lepton, i.e., a lepton passes the loose criteria but but fails the tight selection, loose criteria for muons: Iso_abs < 24 GeV, Iso_rel <2, no upper cut on dz, loose criteria for standard electrons: Iso_abs < 24 GeV, Iso_rel <2, cut-based-veto ID, no upper cut on dz, loose criteria for low p_T electrons: Iso_abs < 24 GeV, Iso_rel <2, BDT score > 3, no upper cut on dz, all other criterion are same as tight ones, MR refion selection: MET < 50 GeV, one loose lepton, Transverse Mass(MT) < 40 GeV N_jets(p_T > 40 GeV) >=1, N_b−jet(hard) = 0, In the measurement region, due to trigger efficiency and prescale considerations, different datasets and trigger paths are employed for the fake rate measurement, ensuring an unbiased and efficient selection across the full lepton p_T spectrum, fake rate is measured seperately for muon and electron (seperating by lepton type) and after subtracting prompt lepton contribution from data, application region (AR) has excatly same selection criterion as of SR except for lepton selection condition where leptons are required to pass the loose and fail the tight criteria, each SR bin has its correcpoding AR bin, while weighting the AR data by tight-to-loose ratio, prompt lepton contribution is also subtracted from the AR data]
  * *Validation:* [Two types of validation test: simultion based closure test and data calidation test, closure test performed with Z+jets and QCD MC samples by comparing the predicted yield obtained utilizing the medthod with the direct yield obtained using MC truth information, data validation is done in MET side band validation region (VR); 200 < MET < 300 GeV) by forming psedo SR-AR pair and using tight-to-loose ratio obtained from MR data]

## 7. Systematic Uncertainties
* **Systematic Uncertainties (Experimental):** [luminosity, pilup and L1 prefire weight and due to several object selections in the analysis]
* **Systematic Uncertainties (Theoretical):** [MC cross section, renormalization/Factorization scales, parton sdistribution functions (PDFs) modeling]
* **Systematic Uncertainties (Limited statistics):** [one of the major source of uncertainties is due to the limitation of MC statistics]
* **Systematic Uncertainties (on Signals):** [Integrated luminosity: 1.2-2.5%, Pileup 1-2%, Jet Energy Corrections (JEC): 2-5%, b-tagging efficiency scale factors: 1-3%, lepton efficiency SF: 1-2%, ISR jet multiplicity correction: 1%, L1 prefire correction: 1-2%, PDF uncertainties: <1%, Renormalization and factorization uncertainties: <1%, MC cross-section: 2-5%, Trigger efficiency and SF: 1-3%, Statistical uncertainty due to limited MC sample]
* **Systematic Uncertainties (on estimated background ):** * *Prompt lepton background:* [ntegrated luminosity: 1.2-2.5%, Pileup 1-2%, Jet Energy Corrections (JEC): 2-5%, b-tagging efficiency scale factors: 1-3%, lepton efficiency SF: 1-2%, ISR jet multiplicity correction: 1%, L1 prefire correction: 1-2%, MC cross-section: 2-5%, Trigger SF: 1-2%, Statistical uncertainty due to limited MC sample, uncertainty on normalization factor] * *Non-prompt lepton background:* [uncertainty from the closure test: 1-20%, uncertainty from data validation 1-40%]


## 8. Results  & Interpretations
* **Total estimated backgrounds and observed data comaparison:** [Estimated SM processes contribution consitent with observed data, No excess found]
* ** Evaluating constraints on Signal model parameter:** [Utilizing LHC Statistical Framework Configuration and CMS combine tool]
  * *Statistical Model:* [Profile Likelihood Ratio test statistic utilizing Nuisance Parameters (NP) with Gaussian/Lognormal priors]
  * *Exclusion limit:* ["Limit Setting" using the CL_s method to extract 95% CL upper limits on scalar top production cross-sections]
* ** Limit report:** * [Excluded Stop mass upto 750 GeV and LSP mass upto 500 GeV]

## 9. Summary & Conclusion
* ** Summary:** * [Search for scalar top quark with compressed mass spectra in single lepton final state, Full run 2 ultra legacy data samples used, Addition of new objects such as low p_T electron and tagged SV as soft b, revised background estimation method] 
* ** Conclusion:** * [No excess observed beyong SM, Excuded Stop mass upto 750 GeV and LSP upto 500 GeV, among thr best limit within CMS and ATLAS in compressed mass spectra]

