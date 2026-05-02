import json
from pathlib import Path

from pdf_reader import extract_pdf_pages
from chunker import create_chunks_for_pdf

INPUT_DIR = Path(r"C:\Users\SHASHANK\Desktop\Current Projects\Python\Embedding-vectorDB-chunking\pdf-chunker\input-pdfs")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "chunks.json"

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input_pdfs/")
        return
    all_chunks = []

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")
        pages = extract_pdf_pages(pdf_path)

        chunks = create_chunks_for_pdf(
            pdf_path=pdf_path,
            pages=pages,
            chunk_size=300,
            overlap=60,
        )

        all_chunks.extend(chunks)
        print(f"Created {len(chunks)} chunks from {pdf_path.name}")

        output_data = [chunk.model_dump() for chunk in all_chunks]
        with open(OUTPUT_FILE,"w", encoding="utf-8") as file:
             json.dump(output_data, file, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(all_chunks)} chunks to {OUTPUT_FILE}")
    
if __name__ == "__main__":
   main()

