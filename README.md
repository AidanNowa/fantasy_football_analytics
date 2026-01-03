# Fantasy Football Analytics TUI
A simple terminal-based fantasy football analytics dashboard for exploring weekly player performance and projections.

This project was used as my "First Personal Project" for the Boot.dev coursework

## Overview
This project allows a user with a Yahoo fantasy football team review thier players total points scored and their difference over/under projection on a weekly scale. It generates a TUI that allows the user to swap between position groups to make insightful decisions about who to start each week. Users who want to quickly generate weekly graphs beyond what is provided by the base Yahoo fantasy football website can use this as a base to build out thier own decision trees. Data exploration can also be carried out within notebooks or other files using some of the functions created during the data exploration phase of this project.

## Features
* Interactive terminal-based charts
* Position-based player filtering
* Weekly points and weekly margin visualizations
* Dynamic updates when player selections change
* Long and wide formats for pandas-based data transformations

## Example

<img width="1916" height="1011" alt="Screenshot_20260103_132705" src="https://github.com/user-attachments/assets/5e9b39c7-cff9-4cba-ada4-d5700879aa6d" />

## Tech Stack
* Python
* Textual - Terminal UI framework
* plotext - Terminal plotting
* pandas - Data transformation and analytics

## Project Structure
src/
|-- tui.py              # Textual application and plotting
|-- data_collection.py  # Data fetching and transformations functions
noteboks/
|-- exploration.ipynb   # Jupyter notebooks showing testing, exploration, and function use

## How to Run
```console
pip install -r requirements.txt
python src/tui.py
```

## Inspiration

For years I have participated in a dynasty fantasy football leauge where each team keeps all their players from year to year.
This type of leauge poses many challenges beyond a standard leauge due to the need to account not only for the current season but future seasons as well.
I believe a stronger understanding of the underlying data for each player and team can provide siginificant upside in player acquistion, trades, and team management.
This project attempts to highligh key insights from the data in a streamlined manner.

## Disclaimer

This project is provided for educational and personal use only. It is not affiliated with, endorsed by, or sponsored by the NFL, Yahoo, or any fantasy sports platform. All trademarks and data sources belong to their respective owners.

## License

This project is licensed under the MIT Liscense.

You are free to use, modify, and distribute this software for any purpose, including personal and commercial use, at no cost. This project is provided "as is", without warranty of any kind.
