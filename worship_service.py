from datetime import datetime, timedelta

class WorshipService:
    def __init__(self, title, youtube_slug, date=""):
        self.title = title
        self.youtube_slug = youtube_slug
        self.date_formats(date)
    
    def date_formats(self, date):
        if date == "":
            today = datetime.now()
            days_until_sunday = (6 - today.weekday())
            if days_until_sunday <= 0:
                days_until_sunday += 7
            next_sunday = today + timedelta(days=days_until_sunday)
            self.sort_date = next_sunday.strftime("%Y-%m-%d")
            self.full_date = next_sunday.strftime("%B %d, %Y")
        else:   
            self.full_date = date
            date_object = datetime.strptime(date, "%B %d, %Y")
            self.sort_date = date_object.strftime("%Y-%m-%d")

