# Retrieves player data about a tournament on toornament.com and then gets these players' data from trackernetwork
import trackernetwork
import toornament
import csv

# Basic data
# https://www.toornament.com/en_GB/tournaments/3356365864224243712/stages/
tournament_id = "4396607322092011520"  # 4396607322092011520 = Uniliga Sommer 2021
season = 17

# Activate APIs
f = open("../config/api-key-toornament", "r")
api_key_toornament = f.read().splitlines()[0]
f = open("../config/api-key-trn", "r")
api_key_trn = f.read().splitlines()[0]
toornament_api = toornament.SyncViewerAPI(api_key_toornament)
trn_api = trackernetwork.TrackernetAPI(api_key_trn)

# Get basic tournament data from toornament (tournament, stages, groups, divisions, teams, players)
my_tournament = toornament_api.get_tournament(tournament_id)

# Get stages data
my_stages = toornament_api.get_stages(tournament_id)
stages = []

# Go through: stages -> groups -> teams -> players and write player data into csv file
for the_stage in my_stages:
    print('\n' + the_stage.name)
    print(the_stage.type)
    groups = []
    if the_stage.type == 'league' or the_stage.type == 'pools':  # league/group phases are different from trees
        if int(the_stage.settings['nb_groups']) < 50:
            r = toornament.Range(0, the_stage.settings['nb_groups'])
        else:
            print('Too many groups in stage!')
        my_groups = toornament_api.get_groups(tournament_id=tournament_id, range=r, stage_ids={the_stage.id})

        for the_group in my_groups:
            print('\n---------------------')
            print('\n' + the_group.name)
            teams = []

            # Get teams in this group via ranking table
            group_teams = []
            ranking_items = toornament_api.get_ranking_items(tournament_id, the_stage.id,
                                                             range=toornament.Range(0, the_group.settings['size']),
                                                             group_ids=[the_group.id])
            for the_item in ranking_items:
                group_teams.append(toornament_api.get_participant(tournament_id, the_item.participant.id))
            for the_team in group_teams:
                print('\n' + the_team.name)
                # TODO: check if this team already exists in my_teams? Might mess up something with 1 team in 2 stages
                players = []
                #team_already_added = False
                #for t in my_teams:
                #    if the_team.name == t.name:
                #        team_already_added = True
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

                    stats = {"mmr_1v1": 0, "mmr_2v2": 0, "mmr_3v3": 0}
                    #trn_player = trackernetwork.Player(the_player.name, steam_id, xbox_id, psn_id, nintendo_id, epic_id)
                    #stats = trn_api.get_playerstats(trn_player, season)  # TRN-API for RL deactivated atm
                    # TODO: webscraping without API...

                    player = {"name": the_player.name,
                              "IDs": {"steam_id": steam_id,
                                      "xbox_id": xbox_id,
                                      "psn_id": psn_id,
                                      "nintendo_id": nintendo_id,
                                      "epic_id": epic_id},
                              "stats": {"mmr_1v1": stats['mmr_1v1'],
                                        "mmr_2v2": stats['mmr_2v2'],
                                        "mmr_3v3": stats['mmr_3v3']}
                              }
                    players.append(player)

                team = {"name": the_team.name,
                        "ID": the_team.id,
                        "players": players,
                        "stats": {"avg_mmr_1v1": 0, "avg_mmr_2v2": 0, "avg_mmr_3v3": 0}}  # TODO: average team stats
                teams.append(team)
            group = {"name": the_group.name, "ID": the_group.id, "teams": teams}
            groups.append(group)
    else:
        print("Skipping tree stage...")
        # TODO: tree stages...
    stage = {"name": the_stage.name,
             "ID": the_stage.id,
             "type": the_stage.type,
             "groups": groups}
    stages.append(stage)
tournament = {"name": my_tournament.name, "ID": tournament_id, "stages": stages}

print("Tournament data retrieved. Starting to write into csv-file...")

# Open csv-file to write into
with open("../output/toornament_data.csv", mode='w', encoding='UTF-8', newline='') as write_file:
    writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Stage', 'Group', 'Team', 'Player', 'Steam', 'Xbox', 'PSN', 'Nintendo', 'Epic',
                     '1v1', '2v2', '3v3'])
    for s in tournament["stages"]:
        for g in s["groups"]:
            for t in g["teams"]:
                for p in t["players"]:
                    writer.writerow([s["name"], g["name"], t["name"], p["name"],
                                    p["IDs"]["steam_id"], p["IDs"]["xbox_id"], p["IDs"]["psn_id"],
                                    p["IDs"]["nintendo_id"], p["IDs"]["epic_id"],
                                    p["stats"]["mmr_1v1"], p["stats"]["mmr_2v2"], p["stats"]["mmr_3v3"]])

print("DONE!")
