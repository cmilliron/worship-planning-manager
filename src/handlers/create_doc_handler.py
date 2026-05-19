from ..database import get_next_sermon, SermonEntry
from ..worship_service import WorshipService
from config import OUPUT_LOCATION

def process_template(worship_service: WorshipService): 
    with open('template.txt', 'r', encoding='utf-8') as file:
        content = file.read()   
    output = content.replace("{{ Sermon }}", worship_service.title)
    output = output.replace("{{ Date }}", worship_service.full_date)
    output = output.replace("{{ YouTube }}", worship_service.youtube_slug)
    return output


def create_output_file(worship_service: WorshipService, content: str):
    base_path = OUPUT_LOCATION / f"Worship - {worship_service.sort_date}" 
    base_path.mkdir(parents=True, exist_ok=True)
    output_path = base_path / f"worship_{worship_service.sort_date}.txt"
    with open(output_path, "w") as file:
        file.write(content)

def create_doc_handler():
    next_service = get_next_sermon()
    worship_service = WorshipService(next_service.title, next_service.youtube_url, next_service.date) # type: ignore
    content = process_template(next_service)
    create_output_file(worship_service, content)
