from .scraper import download_and_process_source
from .pdf_processor import run_pdf_processing
import time

def main():
    """Runs the full end-to-end data gathering and processing pipeline."""
    start_time = time.time()
    print("=============================================")
    print("     STARTING DATA GATHERING PIPELINE      ")
    print("=============================================")

    # STAGE 1: Scrape new sources from the web, download, and update DB
    download_and_process_source()

    print("\n---------------------------------------------")

    # STAGE 2: Process all PDFs in `file_sources` to extract images
    run_pdf_processing()

    print(f"\n\n🏁 PIPELINE EXECUTION FINISHED in {time.time() - start_time:.2f} seconds.")
    print("=============================================")


if __name__ == "__main__":
    main()