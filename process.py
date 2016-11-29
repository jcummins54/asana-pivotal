import csv
import logging
from datetime import datetime

logging.basicConfig(filename='output.log', level=logging.DEBUG)
logging.debug('foo')


def change_date(date_str):
    if date_str == '':
        return date_str
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")


with open('output.csv', 'a+') as csvfileout:
    writer = csv.writer(csvfileout, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['Id', 'Title', 'Labels', 'Iteration', 'Iteration Start', 'Iteration End', 'Type', 'Estimate',
                     'Current State', 'Created at', 'Accepted at', 'Deadline', 'Requested By', 'Description', 'URL',
                     'Owned By'])

    '''
    Asana headers to map:

    [0'Task ID', 1'Created At', 2'Completed At', 3'Last Modified', 4'Name', 5'Assignee', 6'Due Date', 7'Tags', 8'Notes',
     9'Projects', 10'Parent Task', 11'Steps to Reproduce', 12'Client Name/ ID', 13'Expected Behavior', 14'Urgent?',
     15'URL of Widget']
    '''

    with open('Sprint_15_Juster.csv', 'rb') as csvfilein:
        reader = csv.reader(csvfilein, delimiter=',', quotechar='"')
        is_first = True
        for row in reader:
            if is_first:
                is_first = False
                continue

            created_at = change_date(row[1])
            accepted_at = change_date(row[2])
            deadline = change_date(row[6])
            description = row[8]

            if accepted_at != '':
                status = 'accepted'
                estimate = 1
            else:
                status = 'unscheduled'
                estimate = ''

            if row[11] != '':
                if description != '':
                    description += '\n\n'
                description += row[11]
            mapped_row = [row[0], row[4], row[7], '', '', '', 'feature', estimate, status, created_at, accepted_at,
                         deadline, row[12], description, row[15], row[5]]
            print(mapped_row)
            writer.writerow(mapped_row)

