import sys
import argparse
from pathlib import Path
from datetime import datetime
from .database import init_db, save_to_database, get_all_sermons
from .worship_service import WorshipService
from .handlers.create_doc_handler import create_doc_handler

from config import OUPUT_LOCATION

def process_template(worship_service: WorshipService): 
    contents = ""
    with open('template.txt', 'r', encoding='utf-8') as file:
        content = file.read()   
    output = content.replace("{{ Sermon }}", worship_service.title)
    output = output.replace("{{ Date }}", worship_service.full_date)
    output = output.replace("{{ YouTube }}", worship_service.youtube_slug)
    return output


def create_output_file(worship_service: WorshipService, content: str):
    base_path = Path(OUPUT_LOCATION) / f"Worship - {worship_service.sort_date}" 
    base_path.mkdir(parents=True, exist_ok=True)
    output_path = base_path / f"worship_{worship_service.sort_date}.txt"
    with open(output_path, "w") as file:
        file.write(content)

def sort_sermons_key(sermon):
    """
    Custom sorting key: 
    1. 'next' strings go to the very top.
    2. Valid dates are sorted chronologically.
    3. Unparseable strings fall to the bottom.
    """
    date_str = sermon.date.lower().strip()
    
    if date_str == "next":
        # Return a time so far in the past it always comes first
        return datetime.min
    
    try:
        # Assuming YYYY-MM-DD format for actual dates
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        # If the date string format is weird, put it at the end
        return datetime.max

def handle_list_command():
    """Fetches, sorts, and prints upcoming sermons."""
    sermons = get_all_sermons()
    
    if not sermons:
        print("No sermons found in the database.")
        return

    # Sort the sermons using our custom key
    sorted_sermons = sorted(sermons, key=sort_sermons_key)

    print("\n=== Upcoming Services ===")
    print(f"{'ID':<15} | {'Date':<15} | {'Sermon Title':<25} | {'YouTube Link'}")
    print("-" * 80)
    
    for s in sorted_sermons:
        print(f"{s.id:<15} | {s.date:<15} | {s.title:<25} | {s.youtube_url}")

def main():
    init_db()
    parser = argparse.ArgumentParser(description="Worship Planning Document")
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
    
    # Create the parser for the 'new' command
    new_sermon_parser = subparsers.add_parser("new", help="Create a new sermon")
    new_sermon_parser.add_argument(
        "-s", "--sermon", 
        type=str, 
        required=True, 
        help="The sermon title (Required)"
    )
    new_sermon_parser.add_argument(
        "-y", "--youtube", 
        type=str, 
        required=True, 
        help="The YouTube Slug (Required)"
    )
    new_sermon_parser.add_argument(
        "-d", "--date", 
        type=str, 
        default="next", 
        help="The date for the entry (Optional, defaults to 'next')"
    )

    list_parser = subparsers.add_parser("list", help="List all upcoming services closest to top")

    create_doc_parser = subparsers.add_parser("create_doc", help="Creates a doc in downloads folder")
    create_doc_parser.add_argument('-d', type=str, default="next", help="The date for the entry (Optional, defaults to 'next')")

    args = parser.parse_args()
    
    match args.command:
        case "new":
            worship_service = WorshipService(args.sermon, args.youtube, args.date)
            # processed_template = process_template(worship_service)
            # # print(process_template)
            # create_output_file(worship_service, processed_template)
            save_to_database(
                sermon_title=args.sermon, 
                youtube_url=args.youtube, 
                date_value=worship_service.sort_date
            )

        case "list":
            handle_list_command()

        case "create_doc":
            create_doc_handler()

        case _:
            parser.print_help()




if __name__ == "__main__":
    main()
    # title = ""
    # date = ""
    # yt_slug = ""

    # if len(sys.argv) == 1:
    #     title = input("Enter sermon title: ")
    #     date = input("Date for worship: ")
    #     yt_slug = input("You Tube Slug: ")
    # else:
    #     title = sys.argv[1]
    #     yt_slug = sys.argv[2]
    #     if len(sys.argv) == 4:
    #         date = sys.argv[3]
    
    # worship_service = WorshipService(title, yt_slug, date)
    # processed_template = process_template(worship_service)
    # create_output_file(worship_service, processed_template)
    
