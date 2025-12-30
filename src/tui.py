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
        super().__init__()
        self.weekly_longs = weekly_longs
        #print(self.weekly_longs)

    def compose(self) -> ComposeResult:
        yield PlotextPlot(id="plot")
    
    def on_mount(self) -> None:
        plot = self.query_one("#plot", PlotextPlot)
        plt = plot.plt

        #plt.clear_figures()
        #plt.clear_data()
    
        for name, group in self.weekly_longs.groupby("name"):
            plt.plot(
                group["week"].tolist(),
                group["points"].tolist(),
                marker="dot",
                label=name,
            )

        plot.refresh()    

    #def on_mount(self) -> None:
        #for name, group in weekly_longs.groupby('name'):
        #    plt.plot(group['week'], group['points'], marker = 'o', label=name)
        #plt = self.query_one(PlotextPlot).plt
        #print(self.weekly_longs)
        #y = plt.scatter(self.weekly_longs)
        #plt.scatter(y)

def main():
    oauth = OAuth2(None, None, from_file='../auth/oauth2yahoo.json')
    league = League(oauth, league_id='461.l.6288') #game_key.l.leauge_key
    team = get_team_from_num(oauth, 12, 7)
    weekly_totals = get_weekly_totals(league, team)
    weekly_longs = get_weekly_longs(weekly_totals)
    
    weeklyApp = WeeklyTotalsApp(weekly_longs)
    
    team_stats = get_team_yearly_stats(league, team)
    wrs = get_position_stats(team_stats, 'WR')
    wr_weekly = get_weekly_totals(league, wrs)
    wr_longs = get_weekly_longs(wr_weekly)
    
    wrsApp = WeeklyTotalsApp(wr_longs)
    
    weeklyApp.run() 
    wrsApp.run()


if __name__ == "__main__":

    main()

#    ScatterApp().run()
#    BarChartApp().run()
