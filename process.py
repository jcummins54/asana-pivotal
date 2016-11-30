import csv
import sys
import os
from datetime import datetime

if len(sys.argv) < 2:
    print 'This script requires an input filename and optional output filename (defaults to "output.csv")'
    exit()

inputfile = str(sys.argv[1])
outputfile = str(sys.argv[2]) if len(sys.argv) > 2 else 'output.csv'


try:
    os.remove(outputfile)
except OSError:
    pass


def change_date(date_str):
    if date_str == '':
        return date_str
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")


with open(outputfile, 'a+') as csvfileout:
    writer = csv.writer(csvfileout, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['Id', 'Title', 'Labels', 'Iteration', 'Iteration Start', 'Iteration End', 'Type', 'Estimate',
                     'Current State', 'Created at', 'Accepted at', 'Deadline', 'Requested By', 'Description', 'URL',
                     'Owned By'])

    '''
    Pivotal headers:

    [0'Id', 1'Title', 2'Labels', 3'Iteration', 4'Iteration Start', 5'Iteration End', 6'Type', 7'Estimate',
     8'Current State', 9'Created at', 10'Accepted at', 11'Deadline', 12'Requested By', 13'Description', 14'URL',
     15'Owned By']

    Asana headers:

    [0'Task ID', 1'Created At', 2'Completed At', 3'Last Modified', 4'Name', 5'Assignee', 6'Due Date', 7'Tags', 8'Notes',
     9'Projects', 10'Parent Task', 11'Steps to Reproduce', 12'Client Name/ ID', 13'Expected Behavior', 14'Urgent?',
     15'URL of Widget']
    '''

    with open(inputfile, 'rb') as csvfilein:
        reader = csv.reader(csvfilein, delimiter=',', quotechar='"')
        is_first = True
        for row in reader:
            if is_first:
                is_first = False
                continue

            created_at = change_date(row[1])
            accepted_at = change_date(row[2])

            if row[6] == '':
                deadline = ''
            elif datetime.now() > datetime.strptime(row[6], "%Y-%m-%d"):
                print 'Past deadline found, removing deadline from task: ' + row[4]
                deadline = ''
            else:
                deadline = change_date(row[6])

            description = row[8]

            if accepted_at != '':
                status = 'accepted'
                estimate = 3
            else:
                status = 'unscheduled'
                estimate = ''

            try:
                if row[11] != '':
                    if description != '':
                        description += '\n\n'
                    description += row[11]
            except IndexError:
                pass

            try:
                requested_by = row[12]
            except IndexError:
                requested_by = ''

            try:
                owned_by = row[15]
            except IndexError:
                owned_by = ''

            mapped_row = [row[0], row[4], row[7], '', '', '', 'feature', estimate, status, created_at, accepted_at,
                          deadline, requested_by, description, owned_by, row[5]]
            # print(mapped_row)
            writer.writerow(mapped_row)

