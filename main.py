"""
main.py
=======
CLI Entry point for NavigatorCrew.
"""

import argparse
from src.crew import build_crew
from src.config import logger

def main():
    parser = argparse.ArgumentParser(description="NavigatorCrew CLI")
    parser.add_argument("--dry-run", action="store_true", help="Simulate run without API calls")
    args = parser.parse_args()
    
    logger.info("Building NavigatorCrew...")
    crew, accountant = build_crew()
    
    if args.dry_run:
        logger.info("Dry run complete. No tasks executed.")
        return
        
    logger.info("Starting Research Run...")
    result = crew.kickoff()
    
    accountant.finalize(crew.usage_metrics)
    accountant.save_report("outputs/token_report.md")
    
    print("\n" + "="*50)
    print("RESEARCH COMPLETE")
    print(f"Tokens Spent: {accountant.total.total_tokens}")
    print("Report saved to outputs/token_report.md")
    print("="*50)

if __name__ == "__main__":
    main()
