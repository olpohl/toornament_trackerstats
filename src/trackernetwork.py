import os
import platform
import requests
import json

# Contains functions to access trackernetwork.com to scrape player data like MMR

#f = open("../config/api-key-toornament-trn", "r")
#api_key_trn = f.readline()

trn_api_url = "https://public-api.tracker.gg/v2/rocket-league/standard/profile"
season_url = "segments/playlist?season="  # Add season-number to this

# TODO: let Player_TRN inherit from toornament.ParticipantPlayer?
class Player:
    def __init__(self, name='-', steam_id='-', xbox_id='-', psn_id='-', nintendo_id='-', epic_id='-', best_id='-'):
        self.name = name
        self.best_id = None
        self.best_platform = None
        self.stats = {"mmr_1v1": "-", "mmr_2v2": "-", "mmr_3v3": "-"}
        self.all_ids = dict()
        self.set_ids(steam_id, xbox_id, psn_id, nintendo_id, epic_id, best_id)

    def set_ids(self, steam_id='-', xbox_id='-', psn_id='-', nintendo_id='-', epic_id='-', best_id='-'):
        self.all_ids["steam"] = steam_id
        self.all_ids["xbox"] = xbox_id
        self.all_ids["psn"] = psn_id
        self.all_ids["nintendo"] = nintendo_id
        self.all_ids["epic"] = epic_id
        if best_id != '-':
            self.determine_best_id()
        else:
            self.best_id = best_id
            self.best_platform = '-'

    def determine_best_id(self):
        # If Steam-ID is available for this player, this should be used. If not, use another ID available.
        if len(self.steam_id) > 4:
            self.best_platform = "steam"
            self.best_id = self.steam_id
        elif self.epic_id != '-' and self.epic_id != 'n/a' and self.epic_id != '/':
            self.best_platform = "epic"
            self.best_id = self.epic_id
        elif self.xbox_id != '-' and self.xbox_id != 'n/a' and self.xbox_id != '/':
            self.best_platform = "xbox"
            self.best_id = self.xbox_id
        elif self.psn_id != '-' and self.psn_id != 'n/a' and self.psn_id != '/':
            self.best_platform = "psn"
            self.best_id = self.psn_id
        elif self.nintendo_id != '-' and self.nintendo_id != 'n/a' and self.nintendo_id != '/':
            self.best_platform = "nintendo"
            self.best_id = self.psn_id
        else:
            self.best_platform = '-'
            self.best_id = '-'
            print(f"Player {self.name} has no valid ID!")
            return False
        return True

    def get_stats(self, trn_api, season=17):
        self.stats = trn_api.get_playerstats(self, season)


class Trackernet_api():
    def __init__(self, api_key_trn):
        self.api_key_trn = api_key_trn

    def get_playerstats(self, player, season=17):
        if (player.best_platform != '-') & (player.best_id != '-'):
            url = f"{trn_api_url}/{player.best_platform}/{player.best_id}/{season_url}{str(season)}"
            print(f"Scraping player MMR for {player.name}")
            req = requests.get(url, headers={"TRN-Api-Key": self.api_key_trn})
            if req.status_code == 200:
                stats_dict_list = json.loads(req.content.decode('utf-8'))['data']

                data_1v1 = next((item for item in stats_dict_list if item['metadata']['name'] == "Ranked Duel 1v1"), None)
                data_2v2 = next((item for item in stats_dict_list if item['metadata']['name'] == "Ranked Doubles 2v2"), None)
                data_3v3 = next((item for item in stats_dict_list if item['metadata']['name'] == "Ranked Standard 3v3"), None)
                # data_s3v3 = next((item for item in stats_dict_list if item['metadata']['name'] == "Ranked Solo Standard 3v3"), None)
                # data_casual = next((item for item in stats_dict_list if item['metadata']['name'] == "Un-Ranked"), None)
                # data_hoops = next((item for item in stats_dict_list if item['metadata']['name'] == "Hoops"), None)
                # data_rumble = next((item for item in stats_dict_list if item['metadata']['name'] == "Rumble"), None)
                # data_dropshot = next((item for item in stats_dict_list if item['metadata']['name'] == "Dropshot"), None)
                # data_snowday = next((item for item in stats_dict_list if item['metadata']['name'] == "Snowday"), None)
                # data_tournaments = next((item for item in stats_dict_list if item['metadata']['name'] == "Tournament Matches"), None)

                if data_1v1 is not None:
                    stats_1v1 = data_1v1['stats']
                    player.stats['mmr_1v1'] = stats_1v1['rating']['value']
                else:
                    player.stats['mmr_1v1'] = 0

                if data_2v2 is not None:
                    stats_2v2 = data_2v2['stats']
                    player.stats['mmr_2v2'] = stats_2v2['rating']['value']
                else:
                    player.stats['mmr_2v2'] = 0

                if data_3v3 is not None:
                    stats_3v3 = data_3v3['stats']
                    player.stats['mmr_3v3'] = stats_3v3['rating']['value']
                else:
                    player.stats['mmr_3v3'] = 0

                # stats_s3v3 = data_s3v3['stats']
                # stats_casual = data_casual['stats']
                # stats_hoops = data_hoops['stats']
                # stats_rumble = data_rumble['stats']
                # stats_dropshot = data_dropshot['stats']
                # stats_snowday = data_snowday['stats']
                # stats_tournaments = data_tournaments['stats']

            else:
                print(f'Bad request! Response was{str(req.status_code)}')

        else:
            print(f"No valid player ID found for {player.name}")

        return player.stats
