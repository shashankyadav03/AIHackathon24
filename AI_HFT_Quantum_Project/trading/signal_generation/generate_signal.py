#File to connect all the dots
# Step 1: Get historical data and store it in a csv file
# Step 2: Get sentiment analysis data and store it in a csv file
# Step 3: Do feature engineering and store it in a csv file
# Step 4: Do inferencing with pre trained model and generate the signal
# Step 4.5: Compare quantum signal with classical ML signal
# Step 5: Do risk management and generate the position size
# Step 6: Execute the trade
# Step 7: Update the daily loss
# Step 8: Repeat the process

import pandas as pd
import time

from AI_HFT_Quantum_Project.data.real_time.real_time_data import get_historical_data
from AI_HFT_Quantum_Project.models.nlp.sentiment_analysis import get_sentiment_analysis_data
from AI_HFT_Quantum_Project.models.feature.feature_engineering import perform_feature_engineering
from AI_HFT_Quantum_Project.models.reinforcement_learning.classical_ml import generate_trading_signal
from AI_HFT_Quantum_Project.models.quantum.run import compare_signals
from AI_HFT_Quantum_Project.trading.risk_management.risk_management import calculate_risk, update_daily_loss
from AI_HFT_Quantum_Project.trading.execution.agent import convert_signal_to_trade_action

def run_pipeline():
    # Step 1: Get historical data and store it
    historical_data = get_historical_data()

    # Step 2: Get sentiment analysis data and store it
    sentiment_data = get_sentiment_analysis_data()

    # Step 3: Do feature engineering and store it
    features = perform_feature_engineering(historical_data, sentiment_data)

    # Step 4: Do inferencing with pre trained model and generate the signal
    signal = generate_trading_signal(features)

    # Step 4.5: Compare quantum signal with classical ML signal
    quantum_signal = compare_signals(signal)  # Assuming this returns an enhanced signal

    # Step 5: Do risk management and generate the position size
    calculate_risk(signal)

    # Step 6: Execute the trade
    convert_signal_to_trade_action(signal)

    # Step 7: Update the daily loss
    update_daily_loss()

def main():
    #run the pipeline every minute
    while True:
        run_pipeline()
        time.sleep(60)


if __name__ == "__main__":
    main()