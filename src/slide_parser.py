import os
import pypdf

def extract_slide_text(file_path: str, max_pages: int = None) -> str:
    """Extracts text lines from a presentation slide PDF up to a optional page cap."""
    if not os.path.exists(file_path):
        print(f"[Warning] Slide file not found: {file_path}")
        return ""
    
    text_content = []
    try:
        reader = pypdf.PdfReader(file_path)
        total_pages = len(reader.pages)
        pages_to_read = min(total_pages, max_pages) if max_pages else total_pages
        
        text_content.append(f"\n=========================================\nSOURCE SLIDE DECK: {os.path.basename(file_path)}\n=========================================")
        for i in range(pages_to_read):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text_content.append(f"[Slide {i+1}]\n{page_text}")
    except Exception as e:
        print(f"[Error] Failed to parse {file_path}: {str(e)}")
        
    return "\n\n".join(text_content)

def cache_all_context_slides(slides_dir: str = "data/context_slides") -> str:
    """Gathers and combines extracted text from all critical presentation slides."""
    combined_context = []
    
    # 1. Process electron presentation capped at first 6 slides
    elec_path = os.path.join(slides_dir, "Electrons_presentation-1.pdf")
    if os.path.exists(elec_path):
        combined_context.append(extract_slide_text(elec_path, max_pages=6))
        
    # 2. Process other decks completely
    other_decks = ["Softb_Presentation.pdf", "StopSearchStatusReport.pdf"]
    for deck in other_decks:
        deck_path = os.path.join(slides_dir, deck)
        if os.path.exists(deck_path):
            combined_context.append(extract_slide_text(deck_path))
            
    return "\n\n".join(combined_context)
