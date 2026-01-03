from textual.app import App, ComposeResult
from textual.widgets import Select, Static
from textual_plotext import PlotextPlot
from textual.containers import Container
from yahoo_fantasy_api import League, Team
from yahoo_oauth import OAuth2
#import sys
#sys.path.append('../')
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
    
    CSS = """
    Screen {
        layout: vertical;
    }

    #controls {
        height: 3;
    }

    #plots {
        layout: horizontal;
        height: 1fr;
    }

    PlotextPlot {
        width: 1fr;
    }
    """

    def __init__(self, weekly_longs, league, team, projections):
        super().__init__()
        self.get_longs_by_position = get_weekly_longs_by_position
        self.get_margin_longs = get_margin_longs_by_position
        self.weekly_longs = None
        self.league = league
        self.team = team
        self.projections = projections
        #print(self.weekly_longs)

    def compose(self) -> ComposeResult:
        yield Static("Filter by Position", id="controls")

        yield Select(
            options=[
              
                ("Quarterbacks", "QB"),
                ("Wide Receivers", "WR"),
                ("Running Backs", "RB"),
                ("Tight Ends", "TE"),
                ("WR/RB", "W/R"),
                ("WR/RB/TE", "W/R/T"),
                ("Kickers", "K"),
                ("Team Defense", "DEF"),
                ("Defensive Backs", "DB"),
                ("Defensive Linemen", "DL"),
                ("Linebackers", "LB")
            
            ],
            value="QB",
            id="position_select",
        )
        with Container(id="plots"):
            yield PlotextPlot(id="points_plot")
            yield PlotextPlot(id="margin_plot")
    
    def on_mount(self) -> None:
        #self.update_plots("ALL")
        pass

    def on_select_changed(self, event:Select.Changed) -> None:
        position = event.value
        if not position:
            return
        if event.select.id == "position_select":
            self.update_plots(event.value)

    def update_plots(self, position: str) -> None:
        points_plot = self.query_one("#points_plot", PlotextPlot)
        margin_plot = self.query_one("#margin_plot", PlotextPlot)
        
        self._draw_points(points_plot, position)
        self._draw_margin(margin_plot, position)

    def _draw_points(self, plot: PlotextPlot, position: str) -> None:
        plt = plot.plt

        # reset graph when swapping
        plt.clear_figure()
        plt.clear_data()
        
        weekly_longs = self.get_longs_by_position(self.league, self.team, position)
    
        for name, group in weekly_longs.groupby("name"):
            plt.plot(
                group["week"].tolist(),
                group["points"].tolist(),
                marker="dot",
                label=name,
            )
        
        plt.ylim(weekly_longs["points"].min(), weekly_longs["points"].max() + 5)
        plot.refresh()    

    def _draw_margin(self, plot: PlotextPlot, position: str) -> None:
        plt = plot.plt

        # reset graph when swapping
        plt.clear_figure()
        plt.clear_data()

        weekly_margin_longs = self.get_margin_longs(self.league, self.team, position, self.projections)
        
        for name, group in weekly_margin_longs.groupby("name"):
            plt.bar(
                group["week"],
                group["margin"],
                label=name,
            )

        #self.hline(0)
        plt.ylim(weekly_margin_longs["margin"].min() - 5, weekly_margin_longs["margin"].max() + 5)
        plot.refresh()

        

def main():
    oauth = OAuth2(None, None, from_file='../auth/oauth2yahoo.json')
    league = League(oauth, league_id='461.l.6288') #game_key.l.leauge_key
    team = get_team_from_num(oauth, 12, 7)
    projections = pd.read_csv('../data/projections_2025.csv')
    weekly_totals = get_weekly_totals(league, team)
    weekly_longs = get_weekly_longs(weekly_totals)
    
    #weeklyApp = WeeklyTotalsApp(weekly_longs)
    
    team_stats = get_team_yearly_stats(league, team)
    wrs = get_position_stats(team_stats, 'WR')
    wr_weekly = get_weekly_totals(league, wrs)
    wr_longs = get_weekly_longs(wr_weekly)
    
    #wrsApp = WeeklyTotalsApp(wr_longs)
    
    #weeklyApp.run() 
    #wrsApp.run()

    app = WeeklyTotalsApp(get_weekly_longs_by_position, league, team, projections)
    app.run()

if __name__ == "__main__":

    main()

#    ScatterApp().run()
#    BarChartApp().run()
