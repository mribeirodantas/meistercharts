#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# This allows the generation even without X server running
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import csv
import argparse

########################################################################
# Copyright (©) 2016 Marcel Ribeiro Dantas                             #
#                                                                      #
# mribeirodantas at fedoraproject.org                                  #
#                                                                      #
# This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as              #
# published by the Free Software Foundation, either version 3 of the   #
# License, or (at your option) any later version.                      #
#                                                                      #
# This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         #
# GNU Affero General Public License for more details.                  #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with this program. If not, see <http://www.gnu.org/licenses/>. #
########################################################################

parser = argparse.ArgumentParser(description='Generate charts out of\
 MeisterTask exported CSVs', version='0.1')

parser.add_argument('-p', '--person', nargs=1, help='Data about a specific person')

group = parser.add_mutually_exclusive_group()
group.add_argument('-w', '--workload', action='store_true', help='Chart of workload')
group.add_argument('-t', '--tasks',  action='store_true', help='Chart of number of tasks')

group2 = parser.add_mutually_exclusive_group()
group2.add_argument('-th', '--hours',  action='store_true', help='Show time in hours')
group2.add_argument('-tm', '--minutes',  action='store_true', help='Show time in minutes')
group2.add_argument('-ts', '--seconds',  action='store_true', help='Show time in seconds')
parser.add_argument('filename', help='CSV filename')

args = vars(parser.parse_args())

if args['workload']:
    info = {}
    with open(args['filename'], 'rb') as csvfile:
      content = csv.DictReader(csvfile)
      for row in content:
        if row['First name'].decode('utf8') in info.keys():
          info[row['First name'].decode('utf8')] = info[row['First name'].decode('utf8')] + float(row['Hours'])
        else:
          info[row['First name'].decode('utf8')] = float(row['Hours'])

    # Plotting
    fig = plt.figure()
    plt.title("Tasks workload")
    plt.xlabel('Person')
    plt.ylabel('Amount of hours')

    width = 1/1.5
    y = info.values()
    N = len(y)
    x = range(N)

    my_xticks = info.keys()
    plt.xticks(x, my_xticks)

    plt.ylim([0,max(y)+1])

    # Add number of hours on top of bars
    for i, v in enumerate(y):
        plt.text(i, v + 0.25, str(v), color='blue', fontweight='bold')

    plt.bar(x, y, width, color="blue")

    fig.savefig('ch_chart.png')

elif args['tasks']:
    info = {}
    with open(args['filename'], 'rb') as csvfile:
      content = csv.DictReader(csvfile)
      for row in content:
        if row['First name'].decode('utf8') in info.keys():
          info[row['First name'].decode('utf8')].append(row['Notes'].decode('utf8'))
        else:
          info[row['First name'].decode('utf8')] = []
          info[row['First name'].decode('utf8')].append(row['Notes'].decode('utf8'))

    for user in info.keys():
      # Removing duplicated tasks
      info[user] = list(set(info[user]))
      # Getting number of tasks
      info[user] = len(info[user])

    # Plotting
    fig = plt.figure()
    plt.title('Number of tasks by person')
    plt.xlabel('Person')
    plt.ylabel('Number of tasks')

    width = 1/1.5
    y = info.values()
    N = len(y)
    x = range(N)

    my_xticks = info.keys()
    plt.xticks(x, my_xticks)

    plt.ylim([0,max(y)+1])

    # Add number of tasks on top of bars
    for i, v in enumerate(y):
        plt.text(i + 0.1, v + 0.1, str(v), color='blue', fontweight='bold')

    plt.bar(x, y, width, color="blue")

    fig.savefig('tasks_chart.png')
elif args['person']:
    time = 0
    with open(args['filename'], 'rb') as csvfile:
      content = csv.DictReader(csvfile)
      for row in content:
          name = row['First name'] + str(' ') + row['Last name']
          if args['person'][0] in name:
            time += float(row['Hours'])
    if args['minutes']:
        print time*60
    elif args['hours']:
        print time
    elif args['seconds']:
        print time*60*60
