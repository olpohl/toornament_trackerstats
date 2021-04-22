import unittest
#from trackernetwork import *
import toornament
import csv
from trackernetwork import *


# Basic data
# https://www.toornament.com/en_GB/tournaments/3356365864224243712/stages/
tournament_id = "4396607322092011520"  # 4396607322092011520 = Uniliga Sommer 2021
season = 17

# Activate APIs
f = open("../config/api-key-toornament", "r")
api_key_toornament = f.readline()
f = open("../config/api-key-trn", "r")
api_key_trn = f.readline()
toornament_api = toornament.SyncViewerAPI(api_key_toornament)
trn_api = Trackernet_api(api_key_trn)

# Get basic tournament data from toornament (tournament, stages, groups, divisions, teams, players)
my_tournament = toornament_api.get_tournament(tournament_id)
my_stages = toornament_api.get_stages(tournament_id)
my_teams = []
nStart = 0
nEnd = 49
while nStart < my_tournament.size:
    sub_range = toornament.Range(nStart, nEnd)
    my_teams.extend(toornament_api.get_participants(tournament_id, range=sub_range))
    nStart = nEnd + 1
    nEnd = min((nEnd+50), my_tournament.size)

last_group_size = 0
this_group_size = 0
for the_stage in my_stages:
    print('\n' + the_stage.name)
    if int(the_stage.settings['nb_groups']) < 50:
        r = toornament.Range(0, the_stage.settings['nb_groups'])
    else:
        print('Too many groups in stage!')
    my_groups = toornament_api.get_groups(tournament_id=tournament_id, range=r, stage_ids={the_stage.id})
    for the_group in my_groups:
        print('\n' + the_group.name)
        this_group_size = this_group_size + the_group.settings['size']
        group_teams = my_teams[last_group_size:this_group_size]
        for the_team in group_teams:
            print(the_team.name)
            for the_player in the_team.lineup:
                steam_id = the_player.custom_fields['steam_id']
                xbox_id = the_player.custom_fields['xbox_live_gamertag']
                psn_id = the_player.custom_fields['psn_id']
                nintendo_id = the_player.custom_fields['nintendo_network_id']
                epic_id = the_player.custom_fields['epic_id']

                print(the_player.name)
                print(the_player.custom_fields['steam_id'])
                print(the_player.custom_fields['xbox_live_gamertag'])
                print(the_player.custom_fields['psn_id'])
                print(the_player.custom_fields['nintendo_network_id'])
                print(the_player.custom_fields['epic_id'])
        last_group_size = this_group_size + 1


class TestToornamentAPI(unittest.TestCase):
    def test_toornament_data(self):
        self.assertEqual(my_tournament.name, "Uniliga Sommer RL 2021")
        self.assertEqual(my_tournament.size, 93)
        self.assertEqual(len(my_stages), 8)


class TestStatsScrape(unittest.TestCase):
    def test_playerscrape(self):
        playername = 'BonsaiBrudi'
        teamname = 'UED'
        steam_id = '76561197970707838'
        epic = '-'
        xbox = '-'
        psn = '-'
        nintendo = '-'
        test_season = 16
        stats = scrape_playerstats(steam_id=steam_id, season=test_season)
        self.assertEqual(stats['mmr_1v1'], 1004)
        self.assertEqual(stats['mmr_2v2'], 1472)
        self.assertEqual(stats['mmr_3v3'], 1351)


if __name__ == '__main__':
    unittest.main()
