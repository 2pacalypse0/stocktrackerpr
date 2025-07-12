# stocktrackerpr
A Python project that collects stock market data from Yahoo Finance, processes it, and stores structured data in a MySQL database for further analysis.

Keep in mind this is just something i do for fun and i wouldnt actually recommend using it for actual stock tracking seeing how its blatantly unfinished, not rigorously tested and debugged, lacks any sort of UI and is clearly just a poor attempt at replicating some more succesful already existing apps.

Features:
1. Fetches historical stock data using the yfinance lib
2. Cleans and compiles relevant data (closing prices, highs/lows, volume, averages)
3. Stores data into a MySQL database
4. Modular Python code for ease of maintance and revision

stuff used:
1. Python 3
2. yfinance
3. MySQL (mysqlconnector)
4. pandas


How to run the project:
1. Clone the repository
2. Install the libraries
3. Update the database connection settings with your data
4. Run the each script individually (I plan to change this soon with possible automation and centralization)

Possible future additions include automations, incorporation of LLMs for possible predictions, visualisation and perhaps even transformation into an actual app (if time allows). More realistic additions include centralization for the config file and better code and readability.


Possible issues that you could run into:
1. You could fail to start your server (not a script issue i ran into this too this is a MySQL issue where for some reason you have to start your server from services due to some unknown error)
2. It has a pre save hook that caused me some issues so look out for that (It fixed itself somehow?)
*Thats all the major issues i ran into for now*
