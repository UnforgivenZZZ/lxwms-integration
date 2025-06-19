import os
from PyPDF2 import PdfMerger

def combine_pdfs(input_dir, output_file):
    """
    Combine all PDF files in a directory into one PDF
    
    Args:
        input_dir (str): Path to directory containing PDFs
        output_file (str): Output PDF file path
    """
    merger = PdfMerger()
    
    # Get sorted list of PDF files
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    pdf_files.sort()  # Sort alphabetically
    
    # Validate input
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to merge:")
    
    # Add each PDF to the merger
    for filename in pdf_files:
        filepath = os.path.join(input_dir, filename)
        try:
            merger.append(filepath)
            print(f"- Added: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    # Write output file
    try:
        merger.write(output_file)
        merger.close()
        print(f"\nSuccessfully created combined PDF: {output_file}")
        print(f"Total pages combined: {len(merger.pages)}")
    except Exception as e:
        print(f"\nError creating output file: {str(e)}")

if __name__ == "__main__":
    # Configuration - modify these paths as needed
    PDF_DIRECTORY = "/Users/magadaddy/Downloads/reshi"  # Replace with your input directory
    OUTPUT_PDF = "combined.pdf"                # Output filename
    
    combine_pdfs(PDF_DIRECTORY, OUTPUT_PDF)