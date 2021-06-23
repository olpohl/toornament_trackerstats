import unittest
#from trackernetwork import *
import toornament
import csv
import trackernetwork
from trackernetwork import *


# Basic data
# https://www.toornament.com/en_GB/tournaments/3356365864224243712/stages/
tournament_id = "4396607322092011520"  # 4396607322092011520 = Uniliga Sommer 2021
season = 17
get_and_show_all = True  # if true: gets all tournament data and displays in terminal

# Activate APIs
f = open("../config/api-key-toornament", "r")
api_key_toornament = f.read().splitlines()[0]
f = open("../config/api-key-trn", "r")
api_key_trn = f.read().splitlines()[0]
toornament_api = toornament.SyncViewerAPI(api_key_toornament)
trn_api = TrackernetAPI(api_key_trn)

# Get basic tournament data from toornament (tournament, stages, groups, divisions, teams, players)
my_tournament = toornament_api.get_tournament(tournament_id)
my_stages = toornament_api.get_stages(tournament_id)

if get_and_show_all:  # not needed for unit testing, but could be interesting nontheless sometimes
    for the_stage in my_stages:
        print('\n' + the_stage.name)
        print(the_stage.type)
        if the_stage.type == 'league' or the_stage.type == 'pools':
            if int(the_stage.settings['nb_groups']) < 50:
                r = toornament.Range(0, the_stage.settings['nb_groups'])
            else:
                print('Too many groups in stage!')
            my_groups = toornament_api.get_groups(tournament_id=tournament_id, range=r, stage_ids={the_stage.id})
            for the_group in my_groups:
                group_teams = []
                ranking_items = toornament_api.get_ranking_items(tournament_id, the_stage.id, range=toornament.Range(0,the_group.settings['size']), group_ids=[the_group.id])
                for the_item in ranking_items:
                    group_teams.append(toornament_api.get_participant(tournament_id, the_item.participant.id))
                print('\n---------------------')
                print(the_group.name)
                for the_team in group_teams:
                    if the_team.name == 'Uni Vechta Aquarobic Ultras':
                        print('\n' + the_team.name)
                        for the_player in the_team.lineup:
                            steam_id = the_player.custom_fields['steam_id']
                            xbox_id = the_player.custom_fields['xbox_live_gamertag']
                            psn_id = the_player.custom_fields['psn_id']
                            nintendo_id = the_player.custom_fields['nintendo_network_id']
                            epic_id = the_player.custom_fields['epic_id']

                            print(the_player.name)
                            #print(the_player.custom_fields['steam_id'])
                            #print(the_player.custom_fields['xbox_live_gamertag'])
                            #print(the_player.custom_fields['psn_id'])
                            #print(the_player.custom_fields['nintendo_network_id'])
                            #print(the_player.custom_fields['epic_id'])
        elif the_stage.type == 'double_elimination' or the_stage.type == 'single_elimination':
            print('...omitting tree stage...')  # TODO: read tree stages as well


class TestToornamentAPI(unittest.TestCase):
    def test_toornament_data(self):
        self.assertEqual(my_tournament.name, "Uniliga RL Sommer 21")
        self.assertEqual(my_tournament.size, 93)
        self.assertEqual(len(my_stages), 8)


# class TestTrackerAPI(unittest.TestCase):  # Currently TRN API is deactivated
#     def test_get_playerstats(self):
#         test_playername = 'BonsaiBrudi'
#         test_teamname = 'UED'
#         test_steam_id = '76561197970707838'
#         test_epic_id = '-'
#         test_xbox_id = '-'
#         test_psn_id = '-'
#         test_nintendo_id = '-'
#         test_season = 16
#         test_player = trackernetwork.Player(name=test_playername, steam_id=test_steam_id)
#         stats = trn_api.get_playerstats(test_player, season=test_season)
#         self.assertEqual(stats['mmr_1v1'], 1004)
#         self.assertEqual(stats['mmr_2v2'], 1472)
#         self.assertEqual(stats['mmr_3v3'], 1351)


class TestManualWebscraping(unittest.TestCase):  # TODO: test this
    def test_webscrape(self):
        test_playername = 'BonsaiBrudi'
        test_teamname = 'UED'
        test_steam_id = '76561197970707838'
        test_epic_id = '-'
        test_xbox_id = '-'
        test_psn_id = '-'
        test_nintendo_id = '-'
        test_season = 17
        test_player = trackernetwork.Player(name=test_playername, steam_id=test_steam_id)
        stats = test_player.webscrape_stats(season=test_season)
        self.assertTrue(stats['success'])
        self.assertEqual(stats['mmr_1v1'], 1026)  # TODO: needs to be adjusted to current values for every test
        self.assertEqual(stats['mmr_2v2'], 1291)
        self.assertEqual(stats['mmr_3v3'], 1283)

    def test_webscrape_fail(self):
        test_playername = 'Crave0209'
        test_teamname = 'HSW Enkelkinder'
        test_steam_id = '76561197960287930'
        test_epic_id = '-'
        test_xbox_id = '-'
        test_psn_id = '-'
        test_nintendo_id = '-'
        test_season = 17
        test_player = trackernetwork.Player(name=test_playername, steam_id=test_steam_id)
        stats = test_player.webscrape_stats(season=test_season)
        self.assertFalse(stats['success'])
        self.assertEqual(stats['mmr_1v1'], -1)
        self.assertEqual(stats['mmr_2v2'], -1)
        self.assertEqual(stats['mmr_3v3'], -1)
        count_failed_scrapes = 0
        print(count_failed_scrapes)
        count_failed_scrapes += not stats['success']
        print(count_failed_scrapes)


if __name__ == '__main__':
    unittest.main()
