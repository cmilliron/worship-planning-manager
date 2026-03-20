from worship_service import WorshipService

def process_template(worship_service: WorshipService): 
    contents = ""
    with open('template.txt', 'r', encoding='utf-8') as file:
        content = file.read()   
    output = content.replace("{{ Title }}", worship_service.title)
    output = output.replace("{{ Date }}", worship_service.full_date)
    output = output.replace("{{ YouTube }}", worship_service.youtube_slug)
    return output


def create_output_file(worship_service: WorshipService, content: str):
    with open(f"output/worship_{worship_service.sort_date}.txt", "w") as file:
        file.write(content)


if __name__ == "__main__":
    title = input("Enter sermon title: ")
    date = input("Date for worship: ")
    yt_slug = input("You Tube Slug: ")
    worship_service = WorshipService(title, date, yt_slug)
    processed_template = process_template(worship_service)
    
