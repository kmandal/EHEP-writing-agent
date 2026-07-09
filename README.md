# High-Energy Physics Auto-Writer (EHEP-Compiler)

An advanced, multi-agent framework designed to synthesize, polish, and compile raw experimental data, collider metadata, and phenomenological notes into publication-ready LaTeX documents following rigorous journal styles (such as JHEP, PRD or CMS/ATLAS guidelines).

The pipeline orchestrates a hybrid assembly of state-of-the-art LLMs (GPT-4o-mini, Claude 4.6 Sonnet, and Gemini 2.5 flash) to handle everything from domain-specific text generation to hyper-precise LaTeX math typesetting and structural verification.

---

##  Key Features

*   **Multi-Model Hybrid Architecture:** 
    *   **GPT-4o-mini:** Powers the rapid parallel generation of raw physics sections based on specific metadata templates and RAG inputs.
    *   **Gemini 2.5 flash:** Synthesizes global document semantics to generate executive abstracts.
    *   **Claude 4.6 Sonnet:** Acts as a senior editorial layer, optimizing sentence structure, prose flow, and verifying high-precision mathematical typesetting.
*   **Context-Aware RAG Integration:** Automatically retrieves CMS-relevant style guides, experimental constraints, and linguistic conventions unique to the section being drafted.
*   **Robust LaTeX Compilation Safeguards:** Built-in sanitization routines handle unescaped operators (e.g., `<` or `>`), raw variable subscripts (e.g., `p_T`), and table dimension macro expansions for double-column layouts.
*   **Persistent Caching:** Utilizes an SQLite backend via LangChain to cache model outputs locally, minimizing API overhead and accelerating iteration speeds.

---

##  Project Architecture

```text
EHEP-writing-agent/
├── data/
│   ├── templates/               # LaTeX skeletons for target journals (jhep_skeleton.tex, etc.)
│   ├── sample_papers/           # Native source PDFs used to seed the RAG style repository
│   ├── cache_text/              # Cached plain-text extractions from reference source documents
│   ├── context_slides/          # Target input presentations or analysis meeting talk decks
│   ├── fig_table/               # Source assets for compilation layout verification
│   ├── analysis_input.md        # Main structural markdown document containing raw analysis input parameters
│   ├── ANMacros.tex             # Analysis notes macros and providecommand override rules
│   ├── figure_manifest.json     # Dynamic indexing map for targeting image labels
│   └── table_manifest.json      # Dynamic indexing map for structural statistical arrays
├── src/
│   ├── state.py                 # Central tracking object representing compiling manuscript state (EHEPPaperState)
│   ├── orchestrator.py          # Sequence engine executing multi-agent workflow updates
│   ├── agents.py                # Core agent configurations managing prompt construction loops
│   ├── prompts.py               # Strict domain-specific physics styling prompts and system guidelines
│   ├── rag_storage.py           # Local keyword proximity-search and PDF parsing extraction layers
│   ├── asset_compiler.py        # Injects figure assets and tabular matrices contextually into prose layout bounds
│   ├── editorial_tools.py       # Cleans markdown tokens, duplicate labels, and escapes mathematical prose typos
│   ├── bibliography_builder.py  # Automated script for downloading and building reference sets
│   ├── citation_utils.py        # Maps inline data anchors against precise target bibliography keys
│   ├── pdf_builder.py           # Handles compilation system pipelines to trigger pdflatex builds
│   └── slide_parser.py          # Extracts raw parameters out of contextual analysis briefings
├── outputs/                     # Target destination for compiled .tex and finalized draft outputs
├── .env.example                 # Example template showing environmental credentials layout
├── PaperPdfPublisher.py         # Autonomous utility script for packaging and staging build deployments
├── main.py                      # Main entrypoint script to execute the multi-agent orchestration sequence
├── requirements.txt             # Python dependency specification matrix
└── README.md                    # System documentation and deployment blueprints

```

## Setup and Installation

1. Clone the Repository

```
git clone [https://github.com/kmandal/EHEP-writing-agent.git](https://github.com/kmandal/EHEP-writing-agent.git)
cd EHEP-writing-agent

```
2. Set Up a Virtual Environment

```
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt

```

3. Configure Environment Variables

Move the template environment file to an active configuration deployment file and populate your respective model keys:

```
mv .env.example .env

```

Open .env and add your environment credentials:

```
# Language Model API Configuration
ANTHROPIC_API_KEY="your-anthropic-api-key"
OPENAI_API_KEY="your-openai-api-key"
GEMINI_API_KEY="your-google-api-key"

# LangSmith Observability Tracking (Convenient for multi-agent debugging)
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
LANGCHAIN_API_KEY="your-langsmith-key"
LANGCHAIN_PROJECT="EHEP-writing-agent"

```

## Usage

To execute the entire multi-agent workflow, run the main engine entry point:

```
python main.py

```


Advanced Editorial Polishing Toggle (src/agents.py):

ENABLE_EDITORIAL_LLM_POLISH (Boolean): Set to True to route raw drafted text through the Claude editorial layer for advanced grammar correction and typesettin		polish. Toggle to False to compile raw drafts directly and save API credits during rapid debugging.


## How It Works: The Iterative State-Agent Pipeline

The core framework relies on a centralized state object (EHEPPaperState). Rather than a strict one-way chain, the orchestrator drives a forward-and-update feedback cycle. Every agent reads current parameters from the state, runs its specialized model operations, and actively writes its results back onto the shared state graph.

```text

          ┌─────────────────────────────────────────────────────────┐
          │                  Central State Graph                    │
          │                  (EHEPPaperState)                       │
          └─────────────────────────────────────────────────────────┘
             │ ▲                      │ ▲                      │ ▲
     (Reads  │ │ (Updates     (Reads  │ │ (Updates     (Reads  │ │ (Updates
      Input) │ │  Drafts)      State) │ │  Abstract)    State) │ │  Polish)
             ▼ │                      ▼ │                      ▼ │
 ┌──────────────────────┐  ┌──────────────────────┐  ┌─────────────────────┐
 │  GPT-4o-mini Layer   │  │ Gemini 1.5 Flash Lyr │  │ Claude 3.5 Sonnet   │
 │                      │  │                      │  │                     │
 │ Ingests context data │  │ Reads whole state to │  │ Runs grammar review,│
 │ & writes raw drafts  │  │ synthesize abstract  │  │ math validation,    │
 │ of physics sections  │  │ context parameters   │  │ and asset embedding │
 └──────────────────────┘  └──────────────────────┘  └─────────────────────┘
                                                                │
                                                                ▼
                                                     ┌─────────────────────┐
                                                     │ Sanitization Engine │
                                                     │ & Tex Compiler Pass │
                                                     └─────────────────────┘
                                                                │
                                                                ▼
                                                    [outputs/compiled_paper]

```


Dynamic Section Grounding & Drafting: The orchestrator reads baseline data from data/analysis_input.md. For each individual paper section, it bundles citation anchors and figure metrics, passing them into the respective GPT-4o-mini drafting agent. The agent drafts the specialized physics prose and updates the corresponding section fields in the EHEPPaperState.

Abstract Assembly: Once the core body sections are compiled into the state, Gemini 1.5 Flash consumes the full integrated context to construct an authoritative, single-paragraph executive abstract, updating the state directly.

Refinement & Typesetting Review: The orchestrator loops over the completed sections in the state, sending the text blocks into Claude 3.5 Sonnet to iron out grammatical flow and verify that math parameters (like subscripts or limit operators) are structurally secure inside native LaTeX math mode boundaries before committing the polished text back to the state.

Asset Synthesis & Compilation: The final text is parsed to resolve macro alignments against ANMacros.tex, wide tabular matrices are automatically scaled into double-column formatting spans (\begin{table*}), and the output is compiled to disk inside outputs/.



## Data Safety & Confidentiality

This framework is built with data segregation in mind. No training pipelines are coupled to your inference calls. Your underlying frontier research data, data points, and experimental metadata remain contained within your isolated runtime memory space and local cache database (.langchain.db).

## License

This project is licensed under the MIT License.