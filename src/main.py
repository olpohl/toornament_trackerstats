# Retrieves player data about a tournament on toornament.com and then gets these players' data from trackernetwork
import trackernetwork
import toornament
import csv

tournament_id = "4396607322092011520"  # 4396607322092011520 = Uniliga Sommer 2021
season = 17

f = open("../config/api-key-toornament-toornament", "r")
api_key_toornament = f.readline()

f = open("../config/api-key-toornament-trn", "r")
api_key_trn = f.readline()

toornament_api = toornament.SyncViewerAPI(api_key_toornament)
trn_api = trackernetwork.Trackernet_api(api_key_trn)

tournament_stats = dict()

with open('toornament_data.csv', mode='w', encoding='UTF-8', newline='') as write_file:
    writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Player Name', 'Team Name', 'Stage', 'Group', 'Steam', 'Xbox', 'PSN', 'Nintendo', 'Epic',
                     '1v1', '2v2', '3v3'])

    toornament_api = toornament.SyncViewerAPI(api_key_toornament)
    my_tournament = toornament_api.get_tournament(tournament_id)

    nTeams = my_tournament.size
    my_stages = toornament_api.get_stages(tournament_id)

    last_group_size = 0
    this_group_size = 0

    my_teams = []
    nStart = 0
    nEnd = 49
    while nStart < nTeams:
        sub_range = toornament.Range(nStart, nEnd)
        my_teams.extend(toornament_api.get_participants(tournament_id, range=sub_range))
        nStart = nEnd + 1
        nEnd = min((nEnd+50), nTeams)

    for the_stage in my_stages:
        print('\n' + the_stage.name)
        if int(the_stage.settings['nb_groups']) < 50:
            r = toornament.Range(0, the_stage.settings['nb_groups'])
        else:
            print('Too many groups in stage!')
            # TODO: iterate in steps of 50

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

                    stats = trackernetwork.scrape_playerstats(steam_id, xbox_id, psn_id, nintendo_id, epic_id, season, the_player.name)

                    writer.writerow(
                        [the_player.name, the_team.name, the_stage.name, the_group.name,
                         steam_id, xbox_id, psn_id, nintendo_id, epic_id,
                         stats['mmr_1v1'], stats['mmr_2v2'], stats['mmr_3v3']])
            last_group_size = this_group_size + 1
            # TODO: Add average team stats

print('SCRAPING DONE!')
