import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import EHEPPaperState
from src.prompts import (
    THEORIST_SYSTEM_PROMPT, 
    EXPERIMENTALIST_SYSTEM_PROMPT, 
    RECONSTRUCTION_SYSTEM_PROMPT,
    BACKGROUND_SYSTEM_PROMPT,
    STATISTICIAN_SYSTEM_PROMPT,
    EDITORIAL_REVIEWER_SYSTEM_PROMPT
)

load_dotenv()

# Instantiating a LangChain model automatically triggers LangSmith tracing!
# To swap backends later, use 'from langchain_openai import ChatOpenAI'
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0
)

def draft_introduction_section(state: EHEPPaperState) -> str:
    print("\n[🤖] LangChain -> Generating Introduction (Theorist)...")
    
    prompt = f"""
    Please draft the formal LaTeX code for the Introduction section. 
    You must incorporate the following verified analysis parameters exactly:
    - Theory Framework: {state.context.theory_framework} \\cite{{{state.context.theory_citation}}}
    - Target Signal: {state.context.target_signal} \\cite{{{state.context.signal_citation}}}
    - Decay Topology: {state.context.decay_topology}
    - Scientific Motivation: {state.context.motivation}
    """
    
    messages = [
        SystemMessage(content=THEORIST_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content

def draft_experimental_setup(state: EHEPPaperState) -> str:
    print("[🤖] LangChain -> Generating Detector Setup (Experimentalist)...")
    prompt = f"Draft the Experimental Setup using these targets: {state.setup.collider_experiment}, {state.setup.luminosity}."
    messages = [
        SystemMessage(content=EXPERIMENTALIST_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    return response.content

def draft_object_selection(state: EHEPPaperState) -> str:
    print("[🤖] LangChain -> Generating Object Selection (Reconstruction)...")
    prompt = f"Draft selection rules using thresholds: {state.objects.muons}, {state.objects.electrons}."
    messages = [
        SystemMessage(content=RECONSTRUCTION_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    return response.content


def draft_background_estimation(state: EHEPPaperState) -> str:
    print("[🤖] LangChain -> Generating Background Estimation (Background Specialist)...")
    
    # We pass the newly mapped state fields directly into the generation prompt
    prompt = f"""
    Please draft the formal LaTeX code for the Background Estimation section. 
    You must incorporate the following analysis methodology parameters:
    - Prompt Lepton Background Composition & Origin: {state.backgrounds.composition}
    - Estimation Method for Prompt Backgrounds: {state.backgrounds.prompt_lepton_method}
    - Validation Strategy for Prompt Backgrounds: {state.backgrounds.prompt_lepton_validation}
    - Non-prompt/Fake Lepton Background Estimation Method: {state.backgrounds.fake_lepton_method}
    - Validation and Closure Tests for Non-prompt Backgrounds: {state.backgrounds.fake_lepton_validation}
    
    Output ONLY valid LaTeX code starting with a logical section macro (\\section{{Background Estimation}}).
    """
    
    messages = [
        SystemMessage(content=BACKGROUND_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content

def draft_statistical_interpretation(state: EHEPPaperState) -> str:
    print("[🤖] LangChain -> Generating Statistical Interpretations (Statistician)...")
    
    prompt = f"""
    Please draft the formal LaTeX code for the Systematic Uncertainties and Statistical Interpretation sections.
    You must incorporate the following exact parameters from the LHC statistical configuration:
    - Systematic Uncertainties affecting Signals: {state.statistics.systematics_signal}
    - Systematic Uncertainties affecting Estimated Prompt Backgrounds: {state.statistics.systematics_prompt_bkg}
    - Systematic Uncertainties affecting Non-prompt/Fake Backgrounds: {state.statistics.systematics_fake_bkg}
    - Statistical Model & Likelihood Profiling Configuration: {state.statistics.statistical_model}
    
    Output ONLY valid LaTeX code starting with an appropriate section macro (such as \\section{{Systematic Uncertainties}} or \\section{{Statistical Interpretation}}).
    """
    
    messages = [
        SystemMessage(content=STATISTICIAN_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content

def review_and_align_all_sections(state: EHEPPaperState) -> str:
    print("\n[✍️] LangChain -> Editorial Reviewer balancing transitions...")
    
    # We pass all previously generated text blocks directly to the editor model
    review_prompt = f"""
    You are looking at the standalone LaTeX code sections generated by separate specialists. 
    Review them collectively, adjust the wording of paragraph transitions so they read like a cohesive paper, 
    ensure LaTeX labels align smoothly, and output the polished, consolidated source text.

    --- SECTION 1: INTRODUCTION ---
    {state.latex_introduction}

    --- SECTION 2: EXPERIMENTAL APPARATUS ---
    {state.latex_detector_setup}

    --- SECTION 3: PARTICLE RECONSTRUCTION & SELECTION ---
    {state.latex_object_selection}

   --- SECTION 4: BACKGROUND ESTIMATION ---
    {state.latex_background_estimation}

    --- SECTION 5: SYSTEMATIC UNCERTAINTIES & STATISTICAL INTERPRETATION ---
    {state.latex_systematics}
    """
    
    messages = [
        SystemMessage(content=EDITORIAL_REVIEWER_SYSTEM_PROMPT),
        HumanMessage(content=review_prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content
