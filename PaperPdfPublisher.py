import os
from dotenv import load_dotenv
from src.pdf_builder import compile_tex_to_pdf
compile_tex_to_pdf("outputs/compiled_paper_draft.tex")
