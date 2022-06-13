import requests
from datetime import datetime

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse


def index(request):
    persons = []
    response = requests.get('https://hs-resume-data.herokuapp.com/v3/candidates/all_data_b1f6-acde48001122')
    candidates = response.json()
    for person in candidates:
        history = []
        total_jobs = len(person['experience'])
        i = 0
        for job in person['experience']:
            # fetch history of jobs
            i += 1
            end_date = job['end_date']
            start_date = job['start_date']
            title = job['title']
            history.append(f'Worked as: {title}, From {start_date}  To {end_date}')
            
            # if the end date doesn't align with next job say how many days break there was
            if i < total_jobs:
                # i
                format_str = '%b/%d/%Y'
                next_date = person['experience'][i]['start_date']
                dt1 = datetime.strptime(end_date, format_str)
                dt2 = datetime.strptime(next_date, format_str)
                days_apart = (dt2 - dt1).days
                
                if 1 < days_apart < 31:
                    divider, term = 1, 'days'
                elif 31 <= days_apart < 365:
                    divider, term = 30, 'months'
                elif 365 <= days_apart:
                    divider, term = 365, 'years'

                # if more then 1 day gap add this to history
                if 1 < days_apart:
                    history.append(f'Gap between jobs: { days_apart//divider } { term }')
                
        p = {
            'name': person['contact_info']['name']['formatted_name'],
            'history': history
        }
        persons.append(p)
        
        
    data = {
        'candidates': persons,
        'version': '1.2.2'
    }
    context = {"data": data}
    return JsonResponse(context)