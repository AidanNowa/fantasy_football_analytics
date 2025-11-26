from textual.app import App, ComposeResult
from textual_plotext import PlotextPlot

class ScatterApp(App[None]):
    def compose(self) -> ComposeResult:
        yield PlotextPlot()
    
    def on_mount(self) -> None:
        plt = self.query_one(PlotextPlot).plt
        y = plt.sin()
        plt.scatter(y)
        plt.title("Scatter Plot")

if __name__ == "__main__":
    ScatterApp().run()
