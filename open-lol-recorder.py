#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details <http://www.gnu.org/licenses/>.


import re
import urllib2
from time import sleep
import sys
import os

#Seconds to wait between summoners on the same cycle.
wait_between_sums = 5

#Seconds to wait at the end of a cycle.
wait_on_end = 120

def is_region(s):
    if len(s) > 1:
        return s in ('br', 'eune', 'euw', 'lan', 'las', 'na', 'oce', 'ru', 'tr',
                     'www')
    return False


#Only works with valid region codes. Returns a more readable region name.
def get_region_name(s):
    return {'br': 'Brazil',
            'eune': 'Europe Nordic',
            'euw': 'Europe West',
            'lan': 'Latin America North',
            'las': 'Latin America South',
            'na': 'North America',
            'oce': 'Oceanic',
            'ru': 'Russia',
            'tr': 'Turkey',
            'www': 'Korea'}[s]


#Check that string s is a possible summoner name at all.
#Only checks for length at the moment.
def is_valid_sum(s):
    return 0 < len(s) < 50


def get_url(url):
    return urllib2.urlopen(urllib2.Request(url)).read()


if __name__ == '__main__':
    summoners = []

    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                               'summoners.txt')) as f:
            for line in f:
                line = line.lower().strip()
                line = line.split(' ', 1)

                region = line[0]

                #Rename the Korea region out of convenience to match URL.
                if region == 'kr':
                    region = 'www'

                if is_region(region):
                    summoner = line[1].strip()
                    if is_valid_sum(summoner):
                        summoners.append([region, summoner])

    except IOError:
        print('\nERROR: Can\'t find summoners.txt file! Is it in the same'
              + ' directory as this script?\n')


    if len(summoners) > 0:
        print('\nChecking %d summoner(s):\n' % len(summoners))
        for sum in summoners:
            print('Region: ' + get_region_name(sum[0]) + '\nSummoner: ' +
                  sum[1] + '\n')

        #Main loop
        while True:
            for sum in summoners:
                prefix_url = 'http://' + sum[0] + '.op.gg/summoner/ajax/'
                spec_suffix = 'userName=' + sum[1].replace(' ', '+') + \
                              '&force=true'

                try:
                    initial_page = get_url(prefix_url + 'spectator/'
                                           + spec_suffix)
                except:
                    initial_page = '(ConnectionProblemException'

                if '(SummonerNotExistsException' in initial_page:
                    print('\nop.gg can\'t find the summoner name ' + sum[1])
                elif '(ConnectionProblemException' in initial_page:
                    print('\nThere may be an issue with your internet '
                          + 'connection to op.gg or your firewall settings.')
                #Hopefully this doesn't pick up false positives.
                #Page length seems like a reliable indicator though.
                elif len("".join(initial_page.split())) < 350:
                    print('\nop.gg can\'t find an active game for ' + sum[1])
                elif '"NowRecording' in initial_page:
                    print('\nop.gg is already recording ' + sum[1])
                else:
                    patt = re.compile('gameId=(\d+)\"')
                    print('\nA record request for %s is being sent.'
                          % sum[1])
                    try:
                        id = patt.search(initial_page).groups()[0]
                        rec_page = get_url(prefix_url +
                                           'requestRecording.json/gameId=%s'
                                           % id)

                    except:
                        pass

                sleep(wait_between_sums)
            print('\nChecking again in %d seconds.' % wait_on_end)
            sleep(wait_on_end)
    else:
        print(
            '\nNo summoners found in summoners.txt file! Please check that you'
            + 'correctly formatted your summoners.txt file.\n')
