import json

from rdwn_selenium import AddNewEvent

calendar_app = AddNewEvent()

if __name__ == '__main__':
    calendar_app.go_to_calendar()
    with open('data.json', encoding='utf-8') as json_file:
        file = json.load(json_file)
        for i in file:
            calendar_app.expand_and_add_taxonomy(file[i]['title'],
                                                 file[i]['organization'],
                                                 file[i]['description'])
            calendar_app.add_title(file[i]['title'])
    calendar_app.close_session()
