import json

from rdwn_selenium import AddNewEvent

calendar_app = AddNewEvent()

if __name__ == '__main__':
    calendar_app.go_to_calendar()
    with open('games.json', encoding='utf-8') as json_file:
        file = json.load(json_file)
        for i in file:
            calendar_app.expand_and_add_taxonomy(file[i]['title'],
                                                 file[i]['organization'],
                                                 file[i]['description'])
            calendar_app.add_title(file[i]['title'])
            calendar_app.add_date(file[i]['date_start'],
                                  file[i]['date_end'],
                                  file[i]['time_start'],
                                  file[i]['time_end'],
                                  file[i]['color'])
            calendar_app.save()
            print(f'==================================== \n'
                  f'{file[i]["title"]} ADDED TO CALENDAR \n'
                  f'====================================')
            calendar_app.next_add()
    calendar_app.close_session()
