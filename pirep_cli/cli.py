"""
cli.py: Entry point for the PIREP CLI application.
Handles argument parsing, user interaction, and main program flow.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import argparse
    from models import get_pirep_data, format_pirep
    from db_ops import save_pirep, list_pireps
except ImportError as import_err:
    raise ImportError(f"Import error in cli.py: {import_err}. Make sure all dependencies are installed and you are running from the project root.") from import_err

def main():
    """
    Main entry point for the PIREP CLI application.
    Parses command-line arguments and handles user actions for saving or listing PIREPs.
    """
    parser = argparse.ArgumentParser(description="PIREP CLI - Create and manage Pilot Reports (PIREPs)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--save', action='store_true', help='Create and save a new PIREP')
    group.add_argument('--list', action='store_true', help='List all saved PIREPs')
    args = parser.parse_args()

    if args.save:
        print("PIREP Creator - Enter aviation weather report details")
        pirep_data = get_pirep_data()
        pirep_str = format_pirep(pirep_data)
        print("\nGenerated PIREP:")
        print(pirep_str)
        try:
            save_pirep(pirep_data)
            print("PIREP saved to database.db")
        except (IOError, OSError, ValueError) as e:
            print(f"Error saving PIREP: {e}")
    elif args.list:
        try:
            pireps = list_pireps()
            if not pireps:
                print("No PIREPs found in the database.")
            else:
                box_width = 78
                # Unicode box drawing characters for a solid table
                H = '\u2500'  # ─
                V = '\u2502'  # │
                TL = '\u250c' # ┌
                TR = '\u2510' # ┐
                BL = '\u2514' # └
                BR = '\u2518' # ┘
                LT = '\u251c' # ├
                RT = '\u2524' # ┤
                TT = '\u252c' # ┬
                BT = '\u2534' # ┴
                CROSS = '\u253c' # ┼'
                # ANSI escape code for bold yellow text
                HIGHLIGHT = '\033[1;33m'
                RESET = '\033[0m'
                # Table header
                print(f"{TL}{H*box_width}{TR}")
                print(f"{V} {'PIREP LIST':^{box_width}} {V}")
                print(f"{LT}{H*box_width}{RT}")
                for idx, pirep_str in enumerate(pireps, 1):
                    lines = pirep_str.split("\n")
                    # Highlight the PIREP label
                    print(f"{V} {HIGHLIGHT}{'PIREP ' + str(idx) + ':':<{box_width}}{RESET} {V}")
                    for line in lines:
                        # Highlight field names (before the first colon)
                        if ':' in line:
                            field, rest = line.split(':', 1)
                            field = f"{HIGHLIGHT}{field}:{RESET}"
                            content = field + rest
                        else:
                            content = line
                        for wrapped in [content[i:i+box_width] for i in range(0, len(content), box_width)]:
                            print(f"{V} {wrapped:<{box_width}} {V}")
                    if idx < len(pireps):
                        print(f"{LT}{H*box_width}{RT}")
                print(f"{BL}{H*box_width}{BR}")
        except (IOError, OSError, ValueError) as e:
            print(f"Error listing PIREPs: {e}")
