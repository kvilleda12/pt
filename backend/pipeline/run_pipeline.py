from .scraper import download_research_papers, download_textbooks
import time

def main():
    """Runs the full end-to-end data gathering and processing pipeline."""
    start_time = time.time()
    print("=============================================")
    print("     STARTING DATA GATHERING PIPELINE      ")
    print("=============================================")

    # STAGE 1: Find and process textbooks
    download_textbooks()

    # STAGE 2: Find and process research papers
    download_research_papers()

    print(f"\n\n🏁 PIPELINE EXECUTION FINISHED in {time.time() - start_time:.2f} seconds.")
    print("=============================================")

if __name__ == "__main__":
    main()