import trackernetwork
import toornament


# Toornament limits ranges to 50 per request.
# With this function we can cylce through larger ranges.
# TODO: Add delay, so we don't get blocked by toornament?
def get_full_range_with_fct(toornament_api, tournament_id, fct, n, *args, **kwargs):
    my_elements = []
    nStart = 0
    nEnd = 49
    while nStart < n:
        sub_range = toornament.Range(nStart, nEnd)
        my_elements.extend(toornament_api.fct(tournament_id=tournament_id, range=sub_range, stage_ids={the_stage.id}))
        nStart = nEnd + 1
        nEnd = min((nEnd + 50), n)