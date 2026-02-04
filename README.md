# Gold & Silver Market Analysis

A data analytics project focused on analyzing gold and silver prices using historical data, statistical analysis, and visualization.

## Project Goals
- Analyze historical gold and silver price trends
- Compare volatility and returns
- Build a clean, professional analytics pipeline
- Create a portfolio-ready project for data analyst roles

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- yFinance
- Streamlit (later)

## Project Structure

## Bollinger Band Strategy – Backtesting Results

A historical backtest was conducted to evaluate whether Bollinger Band signals add value beyond visual analysis for Gold and Silver prices.

### Strategy Logic
- Buy when price crosses below the lower Bollinger Band  
- Sell when price crosses above the upper Bollinger Band  
- 20-day moving average with ±2 standard deviations  
- Long-only, one position at a time  
- 0.1% transaction cost per trade  

### Key Results
- The strategy generated a low number of trades on daily data  
- Buy-and-hold outperformed the Bollinger strategy in total return  
- Gold exhibited smoother equity curves with lower drawdowns  
- Silver showed higher volatility, more frequent signals, and larger drawdowns  

### Interpretation
Bollinger Band signals captured short-term mean-reversion moves but failed to outperform a passive buy-and-hold approach for long-term trending assets like Gold and Silver. The strategy reduced exposure during extreme price movements but sacrificed participation in sustained trends.

### Conclusion
This backtest highlights the importance of validating intuitive technical indicators using historical data. In this context, Bollinger Bands are more effective as a risk-awareness and market-condition tool rather than a return-maximizing trading strategy.

*Results are for analytical and educational purposes only.*
