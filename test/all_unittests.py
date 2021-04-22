import unittest
#from trackernetwork import *
import toornament
import csv
from trackernetwork import *

# For reference purposes:
# class TestStringMethods(unittest.TestCase):
#
#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
#
#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)



# Basic data
# https://www.toornament.com/en_GB/tournaments/3356365864224243712/stages/
tournament_id = "4396607322092011520"
f = open("../config/api-key-toornament.txt", "r")
api_key_toornament = f.readline()
f = open("../config/api-key-trn", "r")
api_key_trn = f.readline()
season = 17

connector = toornament.SyncViewerAPI(api_key_toornament)


class TestToornamentAPI(unittest.TestCase):
    with open('toornament_data.csv', mode='w', encoding='UTF-8', newline='') as write_file:
        writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Player Name', 'Team Name', 'Stage', 'Group', 'Steam', 'Xbox', 'PSN', 'Nintendo', 'Epic'])

        connector = toornament.SyncViewerAPI(api_key_toornament)
        my_tournament = connector.get_tournament(tournament_id)

        nTeams = my_tournament.size
        my_stages = connector.get_stages(tournament_id)

        last_group_size = 0
        this_group_size = 0

        my_teams = []
        nStart = 0
        nEnd = 49
        while (nStart < nTeams):
            sub_range = toornament.Range(nStart, nEnd)
            my_teams.extend(connector.get_participants(tournament_id, range=sub_range))
            nStart = nEnd + 1
            nEnd = min((nEnd+50), nTeams)

        for the_stage in my_stages:
            print('\n' + the_stage.name)
            if int(the_stage.settings['nb_groups']) < 50:
                r = toornament.Range(0, the_stage.settings['nb_groups'])
            else:
                print('Too many groups in stage!')
                # TODO: iterate in steps of 50

            my_groups = connector.get_groups(tournament_id=tournament_id, range=r, stage_ids={the_stage.id})

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
                        stats = scrape_playerstats(steam_id, xbox_id, psn_id, nintendo_id, epic_id, season)

                        writer.writerow(
                            [the_player.name, the_team.name, the_stage.name, the_group.name,
                             steam_id, xbox_id, psn_id, nintendo_id, epic_id])
                        print(the_player.name)
                        print(the_player.custom_fields['steam_id'])
                        print(the_player.custom_fields['xbox_live_gamertag'])
                        print(the_player.custom_fields['psn_id'])
                        print(the_player.custom_fields['nintendo_network_id'])
                        print(the_player.custom_fields['epic_id'])
                last_group_size = this_group_size + 1


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
