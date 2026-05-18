import sys
import argparse
from pathlib import Path

from worship_service import WorshipService

from config import output_location

def process_template(worship_service: WorshipService): 
    contents = ""
    with open('template.txt', 'r', encoding='utf-8') as file:
        content = file.read()   
    output = content.replace("{{ Sermon }}", worship_service.title)
    output = output.replace("{{ Date }}", worship_service.full_date)
    output = output.replace("{{ YouTube }}", worship_service.youtube_slug)
    return output


def create_output_file(worship_service: WorshipService, content: str):
    base_path = Path(output_location) / f"Worship - {worship_service.sort_date}" 
    base_path.mkdir(parents=True, exist_ok=True)
    output_path = base_path / f"worship_{worship_service.sort_date}.txt"
    with open(output_path, "w") as file:
        file.write(content)

def main():

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

    # 5. Parse the arguments
    args = parser.parse_args()

    # Demonstration of how to access the parsed data
    if args.command == "new":
        print(f"Command executed: {args.command}")
        print(f"Sermon:           {args.sermon}")
        print(f"YouTube:          {args.youtube}")
        print(f"Date:             {args.date}")
    
    match args.command:
        case "new":
            worship_service = WorshipService(args.sermon, args.youtube, args.date)
            processed_template = process_template(worship_service)
            # print(process_template)
            create_output_file(worship_service, processed_template)




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
    
