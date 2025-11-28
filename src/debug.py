import logging
from yahoo_oauth import OAuth2
from yahoo_fantasy_api import Team

#enable debug logging
logging.basicConfig(level=logging.DEBUG)

my_team_code = "461.l.6288.t.4"
oauth = OAuth2(None, None, from_file='../auth/oauth2yahoo.json')
curr_week = 11
team = Team(oauth, team_key=my_team_code)
roster = team.roster(week=curr_week)
