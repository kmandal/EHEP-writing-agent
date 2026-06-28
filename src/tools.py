import os

def save_latex_output(filename: str, content: str, output_dir: str = "outputs") -> str:
    """
    Saves the generated LaTeX code block safely to a designated local directory.
    Creates the directory if it does not already exist.
    """
    # Ensure the directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[📂] Created local output storage directory: {output_dir}/")
        
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[💾] SUCCESS: Content written permanently to target file -> {file_path}")
    return file_path