import os
import re
import json
from dotenv import load_dotenv
import langchain 
from langchain_community.cache import SQLiteCache 
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import EHEPPaperState
from src.prompts import (
    THEORIST_SYSTEM_PROMPT, 
    DETECTOR_SYSTEM_PROMPT,
    DATASETS_SYSTEM_PROMPT,
    RECONSTRUCTION_SYSTEM_PROMPT,
    SELECTION_SYSTEM_PROMPT,
    BACKGROUND_SYSTEM_PROMPT,
    SYSTEMATICS_SYSTEM_PROMPT,
    RESULTS_SYSTEM_PROMPT,
    CONCLUSION_SYSTEM_PROMPT,
    EDITORIAL_REVIEWER_SYSTEM_PROMPT,
    ABSTRACT_GENERATION_PROMPT
)
from src.rag_storage import retrieve_style_context_section_based
from src.editorial_tools import (
    clean_markdown_artifacts,
    filter_duplicate_citations,
    build_final_skeleton,
    verify_latex_assets,
    clean_and_escape_latex_prose
)
from src.asset_compiler import get_figure_block, get_table_block

load_dotenv()

ENABLE_EDITORIAL_LLM_POLISH = True

langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

# The multi-model hybrid assembly
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
claude_llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.0)
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

class EHEPAgents:
    def __init__(self):
        print("[System Initialization] EHEP High-Precision Writing Agents Initialized.")

    def _build_agent_prompt(self, section_title: str, state_data: str, grounding: str, target_section: str) -> str:
        """Helper to inject dynamic RAG style context and metadata cleanly into the human block."""
        style_guidance = retrieve_style_context_section_based(target_section=target_section)
        
        prompt = (
            f"You are drafting the formal LaTeX text for the section: {section_title}.\n\n"
            f"[CRITICAL LAYOUT RULE]\n"
            f"1. Do NOT output any '\\section{{...}}' header command. Start directly with the text body.\n\n"
            f"2. CRITICAL MATH COMPILATION RULES:\n"
            f"   - NEVER use unescaped mathematical operators like '<' or '>' directly in prose text. You must wrap them inside math mode delimiters (e.g., use '$M_\\mathrm{{T}} < 40\\,\\text{{GeV}}$' instead of 'MT < 40 GeV').\n"
            f"   - NEVER output raw variable underscores or subscripts like 'p_T' or 'E_T^miss' directly in plain text. This crashes the compiler with a 'Missing $ inserted' error.\n"
            f"[CMS RELEVANT RAG STYLE GUIDANCE]\n"
            f"{style_guidance}\n\n"
            f"[ANALYSIS INPUT DATA METADATA]\n"
            f"{state_data}\n\n"
            f"{grounding}\n\n"
            f"Output ONLY valid LaTeX markup content."
        )
        return prompt

    def draft_introduction(self, state: EHEPPaperState, grounding: str) -> EHEPPaperState:
        print("[Agent] Drafting Introduction Section...")
        prompt = self._build_agent_prompt(
            section_title="Introduction",
            state_data=str(state.sec1_intro),
            grounding=grounding,
            target_section="introduction"
        )
        messages = [SystemMessage(content=THEORIST_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        state.latex_introduction = llm.invoke(messages).content
        return state

    def draft_detector_setup(self, state: EHEPPaperState, grounding: str) -> EHEPPaperState:
        print("[Agent] Drafting Detector Setup Section...")
        prompt = self._build_agent_prompt(
            section_title="Detector Setup and Trigger System",
            state_data=str(state.sec2_detector),
            grounding=grounding,
            target_section="cms detector"
        )
        messages = [SystemMessage(content=DETECTOR_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        state.latex_detector_setup = llm.invoke(messages).content
        return state

    def draft_datasets_samples(self, state: EHEPPaperState, grounding: str) -> EHEPPaperState:
        print("[Agent] Drafting Datasets and Samples Section...")
        prompt = self._build_agent_prompt(
            section_title="Datasets and Simulated Samples",
            state_data=str(state.sec3_datasets),
            grounding=grounding,
            target_section="datasets"
        )
        messages = [SystemMessage(content=DATASETS_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        state.latex_datasets_samples = llm.invoke(messages).content
        return state

    def draft_object_selection(self, state: EHEPPaperState, grounding: str) -> EHEPPaperState:
        print("[Agent] Drafting Object Selection Section...")
        prompt = self._build_agent_prompt(
            section_title="Event Reconstruction and Object Identification",
            state_data=str(state.sec4_objects),
            grounding=grounding,
            target_section="reconstruction"
        )
        messages = [SystemMessage(content=RECONSTRUCTION_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        state.latex_object_selection = llm.invoke(messages).content
        return state

    def draft_event_selection(self, state: EHEPPaperState, grounding: str) -> EHEPPaperState:
        print("[Agent] Drafting Event Selection Section...")
        prompt = self._build_agent_prompt(
            section_title="Event Selection and Analysis Strategy",
            state_data=str(state.sec5_selection),
            grounding=grounding,
            target_section="event selection"
        )
        messages = [SystemMessage(content=SELECTION_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        state.latex_event_selection = llm.invoke(messages).content
        return state

    def draft_background_estimation(self, state: EHEPPaperState, grounding: str) -> EHEPPaperState:
        print("[Agent] Drafting Background Estimation Section...")
        prompt = self._build_agent_prompt(
            section_title="Background Estimation Methods",
            state_data=str(state.sec6_backgrounds),
            grounding=grounding,
            target_section="background" 
        )
        messages = [SystemMessage(content=BACKGROUND_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        state.latex_background_estimation = llm.invoke(messages).content
        return state

    def draft_systematics(self, state: EHEPPaperState, grounding: str) -> EHEPPaperState:
        print("[Agent] Drafting Systematic Uncertainties Section...")
        prompt = self._build_agent_prompt(
            section_title="Systematic Uncertainties",
            state_data=str(state.sec7_systematics),
            grounding=grounding,
            target_section="systematic" 
        )
        messages = [SystemMessage(content=SYSTEMATICS_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        state.latex_systematics = llm.invoke(messages).content
        return state

    def draft_results(self, state: EHEPPaperState, grounding: str) -> EHEPPaperState:
        print("[Agent] Drafting Results Section...")
        prompt = self._build_agent_prompt(
            section_title="Results and Statistical Interpretations",
            state_data=str(state.sec8_results),
            grounding=grounding,
            target_section="results"
        )
        messages = [SystemMessage(content=RESULTS_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        state.latex_results = llm.invoke(messages).content
        return state

    def draft_summary_conclusion(self, state: EHEPPaperState, grounding: str) -> EHEPPaperState:
        print("[Agent] Drafting Summary and Conclusion Section...")
        prompt = self._build_agent_prompt(
            section_title="Summary and Conclusion",
            state_data=str(state.sec9_conclusion),
            grounding=grounding,
            target_section="conclusion"
        )
        messages = [SystemMessage(content=CONCLUSION_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        state.latex_summary_conclusion = llm.invoke(messages).content
        return state

    def generate_document_abstract(self, state: EHEPPaperState) -> EHEPPaperState:
        print("[Abstract Agent] Synthesizing comprehensive executive abstract via Gemini...")
        full_context = f"""
        Introduction: {state.latex_introduction}
        Strategy: {state.latex_event_selection}
        Backgrounds: {state.latex_background_estimation}
        Results: {state.latex_results}
        Conclusion: {state.latex_summary_conclusion}
        """
        messages = [
            SystemMessage(content=ABSTRACT_GENERATION_PROMPT),
            HumanMessage(content=f"Draft Context:\n{full_context}")
        ]
        response = gemini_llm.invoke(messages)
        state.latex_abstract = response.content.strip() if not isinstance(response.content, list) else "".join([b.text for b in response.content]).strip()
        return state

    def process_section_modular(self, section_name: str, raw_prose: str) -> str:
        """Refines grammar, micro-flow, and math typesetting without modification of scientific context."""
        if not raw_prose or not raw_prose.strip():
            return ""
            
        if not ENABLE_EDITORIAL_LLM_POLISH:
            print(f"[Modular Polisher] Bypassing Claude Pass for: {section_name}")
            return raw_prose
            
        print(f"[Modular Polisher] Refining grammar and LaTeX math notation for section: {section_name} via Claude...")
        
        messages = [
            SystemMessage(content=EDITORIAL_REVIEWER_SYSTEM_PROMPT),
            HumanMessage(content=f"Raw text to polish:\n{raw_prose}")
        ]
        
        response = claude_llm.invoke(messages)
        if isinstance(response.content, list):
            text_content = "".join([block.text if hasattr(block, 'text') else str(block) for block in response.content])
        else:
            text_content = response.content

        return text_content.strip()

    def compile_and_polish(self, state: EHEPPaperState) -> str:
        journal_key = state.target_journal.lower() 
        template_path = f"data/templates/{journal_key}_skeleton.tex"
        with open(template_path if os.path.exists(template_path) else "data/templates/jhep_skeleton.tex", "r", encoding="utf-8") as f:
            skeleton = f.read()

        macro_path = "data/ANMacros.tex"
        analysis_macros = ""
        if os.path.exists(macro_path):
            with open(macro_path, "r", encoding="utf-8") as mf:
                raw_macros = mf.read()
            analysis_macros = re.sub(r'\\newcommand\{\\(met|pt|GeV|TeV|ttbar|fb|mt)\}', r'\\providecommand{\\\1}', raw_macros)
        
        preamble_injection = f"\n\\usepackage{{xspace}}\n{analysis_macros}\n"
        begin_doc_token = "\\begin{document}"
        if begin_doc_token in skeleton:
            skeleton = skeleton.replace(begin_doc_token, preamble_injection + "\n" + begin_doc_token)

        # Execute safe non-RAG editorial adjustments
        intro_prose = self.process_section_modular("latex_introduction", state.latex_introduction)
        intro_assets = get_figure_block("latex_introduction") + get_table_block("Introduction")

        detector_prose = self.process_section_modular("latex_detector_setup", state.latex_detector_setup)
        detector_assets = get_figure_block("latex_detector_setup") + get_table_block("Detector Setup and Trigger System")

        datasets_prose = self.process_section_modular("latex_datasets_samples", state.latex_datasets_samples)
        datasets_assets = get_figure_block("latex_datasets_samples") + get_table_block("Datasets and Simulated Samples")

        reco_prose = self.process_section_modular("latex_object_selection", state.latex_object_selection)
        reco_assets = get_figure_block("latex_object_selection") + get_table_block("Event Reconstruction and Object Identification")

        selection_prose = self.process_section_modular("latex_event_selection", state.latex_event_selection)
        selection_assets = get_figure_block("latex_event_selection") + get_table_block("Event Selection and Analysis Strategy")

        bg_prose = self.process_section_modular("latex_background_estimation", state.latex_background_estimation)
        bg_assets = get_figure_block("latex_background_estimation") + get_table_block("Background Estimation Methods")

        sys_prose = self.process_section_modular("latex_systematics", state.latex_systematics)
        sys_assets = get_figure_block("latex_systematics") + get_table_block("Systematic Uncertainties")

        results_prose = self.process_section_modular("latex_results", state.latex_results)
        results_assets = get_figure_block("latex_results") + get_table_block("Results and Statistical Interpretations")

        conclusion_prose = self.process_section_modular("latex_summary_conclusion", state.latex_summary_conclusion)
        conclusion_assets = get_figure_block("latex_summary_conclusion") + get_table_block("Summary and Conclusion")


        body_segments = [
            "\\section{Introduction}", intro_prose, intro_assets,
            "\\section{Detector Setup and Trigger System}", detector_prose, detector_assets,
            "\\section{Datasets and Simulated Samples}", datasets_prose, datasets_assets,
            "\\section{Event Reconstruction and Object Identification}", reco_prose, reco_assets,
            "\\section{Event Selection and Analysis Strategy}", selection_prose, selection_assets,
            "\\section{Background Estimation Methods}", bg_prose, bg_assets,
            "\\section{Systematic Uncertainties}", sys_prose, sys_assets,
            "\\section{Results and Statistical Interpretations}", results_prose, results_assets,
            "\\section{Summary and Conclusion}", conclusion_prose, conclusion_assets
        ]

        polished_body = "\n\n".join([seg.strip() for seg in body_segments if seg.strip()])
        polished_body = clean_markdown_artifacts(polished_body)
        polished_body = filter_duplicate_citations(polished_body)
        polished_body = clean_and_escape_latex_prose(polished_body)
        polished_body += f"\n\n\\bibliographystyle{{{state.target_journal}}}\n"

        safe_abstract = clean_and_escape_latex_prose(state.latex_abstract)

        final_tex = build_final_skeleton(
            skeleton=skeleton,
            title=state.latex_document_title,
            abstract=safe_abstract,
            body=polished_body
        )
        
        verify_latex_assets(final_tex)
        return final_tex
