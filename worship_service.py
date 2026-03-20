from datetime import datetime

class WorshipService:
    def __init__(self, title, date, youtube_slug):
        self.title = title
        self.youtube_slug = youtube_slug
        self.full_date = date
        self.date_formats(date)
    
    def date_formats(self, date):
        date_object = datetime.strptime(date, "%B %d, %Y")
        self.sort_date = date_object.strftime("%Y-%m-%d")

