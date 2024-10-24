 Project Documentation: Django-based Financial Data System

 Project Overview

This project is a Django-based backend system that fetches financial data from a public API, stores it in a relational database, performs backtesting with historical data, and generates performance reports. Additionally, it integrates a pre-trained machine learning model to predict future stock prices and provides these predictions for comparison with actual stock data.

 Features

1. Fetch Financial Data: The system fetches daily stock price data from the Alpha Vantage API for a given stock symbol (e.g., IBM). The data includes fields such as Open, Close, High, Low, and Volume. This data is then stored in a relational PostgreSQL database.
  
2. Backtesting Module: Users can input parameters such as an initial investment amount, and the system implements a simple backtesting strategy (buy when the stock price dips below a 50-day moving average and sell when it goes above a 200-day moving average). It calculates performance metrics such as total return, maximum drawdown, and the number of trades.

3. Machine Learning Integration: A pre-trained model (e.g., a linear regression model) is used to predict future stock prices based on the fetched historical data. The predictions are stored alongside the actual stock prices for comparison.

4. Report Generation: After backtesting or generating predictions, the system creates performance reports that include financial metrics and visualizations. These reports are available as JSON responses and downloadable PDFs.

5. Deployment: The project is containerized using Docker and deployed on the cloud with PostgreSQL hosted via Neon (a cloud provider similar to AWS RDS, used due to rebilling issues with AWS).



 Step-by-Step Breakdown

 1. Fetch Financial Data

- API Used: Alpha Vantage
  - Daily stock price data is fetched using Alpha Vantage's API. The fields fetched include `Open`, `Close`, `High`, `Low`, and `Volume`.
  
- Database Storage: The data is stored in a PostgreSQL database with the following key fields:
  - Stock Symbol
  - Date of Data
  - Open, Close, High, Low Prices
  - Volume of the stock

- Challenges:
  - The API imposes rate limits. This was handled by including error handling and retry mechanisms in the Django view.
  - Data storage was optimized by ensuring appropriate data types and indexing in PostgreSQL for quick querying.

 2. Backtesting Module

- Strategy: A simple strategy was implemented:
  - Buy: When the stock price dips below a 50-day moving average.
  - Sell: When the stock price rises above a 200-day moving average.
  
- User Input:
  - Initial Investment Amount
  - Stock Symbol
  
- Output:
  - The total return from the investment
  - Maximum drawdown
  - Number of trades executed
  
- Challenges:
  - Handling large amounts of historical data efficiently was crucial to ensure that backtesting runs quickly without overwhelming the system.
  - Implementing accurate calculations, including edge cases where prices do not fluctuate enough to trigger buy or sell conditions, was also a challenge.

 3. Machine Learning Integration

- Pre-Trained Model: A pre-trained machine learning model (such as linear regression) was used to predict stock prices for the next 30 days based on historical data. This model was loaded from a file (`.pkl`), and the predictions were stored in the database.
  
- Predictions:
  - Predicted stock prices are stored for comparison with actual stock data, allowing for post-hoc analysis.
  
- Challenges:
  - Loading the pre-trained model into Django and integrating it with the views required careful separation of concerns to ensure that the model logic did not interfere with the Django views.

 4. Report Generation

- Performance Metrics: After backtesting or using machine learning predictions, the following metrics were generated:
  - Total return on investment
  - Maximum drawdown
  - Number of trades executed (for backtesting)
  - Mean Absolute Error (MAE) and Root Mean Square Error (RMSE) (for predictions)

- Visualization: Visual graphs were generated using Matplotlib or Plotly, comparing predicted vs. actual stock prices. These graphs were included in the final reports.

- Report Formats:
  - JSON response via an API.
  - Downloadable PDF format with metrics and visualizations.
  
- Challenges:
  - Generating graphs that could be used in both PDF and JSON responses required handling both Matplotlib and Plotly.
  - Ensuring that the report generation process was efficient, especially for larger datasets.

 5. Deployment

- Cloud Provider: Due to rebilling issues with AWS RDS, Neon was used as the alternative cloud provider to host the PostgreSQL database. Neon is a serverless platform that provides database services similar to AWS RDS.
  
- Deployment Tools:
  - Docker was used to containerize the Django application.
  - GitHub Actions (or another CI/CD tool) was used to automate deployment to the cloud.
  
- Challenges:
  - AWS RDS Rebilling Issues: Initially, AWS RDS was the planned database solution. However, due to rebilling and cost-related issues, it was not feasible to continue with it. Switching to Neon as a PostgreSQL provider solved this issue.
  - psycopg2 Installation: Installing `psycopg2` (the PostgreSQL adapter for Python) on different platforms can be challenging due to dependencies on system-level libraries (e.g., `libpq-dev` on Linux). This was resolved by ensuring the right dependencies were installed on the local machine and within the Docker environment.



 Random Test Cases for Backtesting

1. Test Case 1: Buy Condition Trigger
   - Input: 
     - Stock symbol: IBM
     - Initial investment: $10,000
   - Condition: Price dips below the 50-day moving average.
   - Expected Outcome: The backtesting module should trigger a buy order when the price dips below the 50-day moving average.

2. Test Case 2: No Trades Executed
   - Input: 
     - Stock symbol: TSLA
     - Initial investment: $5,000
   - Condition: The stock price fluctuates, but never dips below the 50-day moving average or rises above the 200-day moving average.
   - Expected Outcome: No trades should be executed, and the system should return the initial investment as the total return.

3. Test Case 3: Multiple Buy and Sell Conditions
   - Input: 
     - Stock symbol: IBM
     - Initial investment: $20,000
   - Condition: The stock price fluctuates over the period, meeting both buy and sell conditions multiple times.
   - Expected Outcome: Multiple trades should be executed, and the total return should reflect the profit/loss from these trades.

4. Test Case 4: Edge Case with No Historical Data
   - Input: 
     - Stock symbol: XYZ (a symbol with no available data)
     - Initial investment: $10,000
   - Condition: The stock symbol does not have historical data.
   - Expected Outcome: The system should return an error or a clear message indicating that no data is available for the given stock symbol.



 Challenges Faced

1. Integrating AWS RDS PostgreSQL:
   - Initially, AWS RDS was planned to host the PostgreSQL database. However, due to rebilling issues, it became unsustainable to continue using AWS. The solution was to switch to Neon, a cloud-based serverless PostgreSQL provider. While Neon worked well as an alternative, it required reconfiguring some parts of the deployment process, especially with database connections and environment variable management.

2. Installing `psycopg2`:
   - Installing `psycopg2` was another challenge due to platform-specific dependencies. On local development environments, especially on macOS and Linux, additional libraries like `libpq-dev` were required. The solution involved ensuring these dependencies were included both locally and in the Docker container.

3. Handling Large Data Volumes:
   - Fetching large volumes of historical financial data from the API and storing it in the database posed performance challenges. To overcome this, proper database indexing and optimization techniques were applied.

4. Model Integration:
   - Integrating the pre-trained machine learning model within the Django architecture required careful separation of logic. Ensuring that the model could be loaded, applied, and results stored without affecting the performance of the Django views was a key challenge.

