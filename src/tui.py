from textual.app import App, ComposeResult

from textual_plotext import PlotextPlot

from yahoo_fantasy_api import League, Team
from yahoo_oauth import OAuth2
from data_collection import *

class ScatterApp(App[None]):
    
    def compose(self) -> ComposeResult:
        yield PlotextPlot()

    def on_mount(self) -> None:
        plt = self.query_one(PlotextPlot).plt
        y = plt.sin()
        plt.scatter(y)
        plt.title("Scatter Plot")

class BarChartApp(App[None]):
    
    def compose(self) -> ComposeResult:
        yield PlotextPlot()

    def on_mount(self) -> None:
        languages = ["Python", "C++", "PHP", "Ruby", "Julia", "COBOL"]
        percentages = [14, 36, 11, 8, 7, 4]
        plt = self.query_one(PlotextPlot).plt
        y = plt.bar(languages, percentages)
        plt.scatter(y)
        plt.title("Programming Languages")

class WeeklyTotalsApp(App[None]):    

    def __init__(self, weekly_longs):
        self.weekly_longs = weekly_longs

    def compose(self) -> ComposeResult:
        yield PlotextPlot()
    
    def on_mount(self) -> None:
        for name, group in weekly_longs.groupby('name'):
            plt.plot(group['week'], group['points'], marker = 'o', label=name)

def main():
    oauth = OAuth2(None, None, from_file='../auth/oauth2yahoo.json')
    league = League(oauth, league_id='461.l.6288') #game_key.l.leauge_key
    team = get_team_from_num(oauth, 12, 7)
    weekly_totals = get_weekly_totals(league, team)
    weekly_longs = get_weekly_longs(weekly_totals)
    
    weeklyApp = WeeklyTotalsApp(weekly_longs)
    #weeklyApp.weekly_longs = weekly_longs
    
    weeklyApp.run() 


if __name__ == "__main__":

    main()

#    ScatterApp().run()
#    BarChartApp().run()
