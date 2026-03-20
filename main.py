import sys
from pathlib import Path

from worship_service import WorshipService



def process_template(worship_service: WorshipService): 
    contents = ""
    with open('template.txt', 'r', encoding='utf-8') as file:
        content = file.read()   
    output = content.replace("{{ Sermon }}", worship_service.title)
    output = output.replace("{{ Date }}", worship_service.full_date)
    output = output.replace("{{ YouTube }}", worship_service.youtube_slug)
    return output


def create_output_file(worship_service: WorshipService, content: str):
    output_path = Path("output/worship_{worship_service.sort_date}.txt")
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as file:
        file.write(content)


if __name__ == "__main__":
    title = ""
    date = ""
    yt_slug = ""

    if len(sys.argv) == 1:
        title = input("Enter sermon title: ")
        date = input("Date for worship: ")
        yt_slug = input("You Tube Slug: ")
    else:
        title = sys.argv[1]
        yt_slug = sys.argv[2]
        if len(sys.argv) == 4:
            date = sys.argv[3]
    
    worship_service = WorshipService(title, yt_slug, date)
    processed_template = process_template(worship_service)
    create_output_file(worship_service, processed_template)
    
