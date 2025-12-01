import pandas as pd
import numpy as np
import pickle
from datetime import datetime
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error
import lightgbm as lgb


class ModelConfig:
    EXCELLENT_DEAL_THRESHOLD = -15.0
    GOOD_DEAL_THRESHOLD = -8.0
    FAIR_DEAL_THRESHOLD = -3.0
    SLIGHTLY_HIGH_THRESHOLD = 5.0
    OVERPRICED_THRESHOLD = 10.0
    VERY_OVERPRICED_THRESHOLD = 15.0
    CONFIDENCE_INTERVAL = 0.95
    LOOKBACK_DAYS = 7


class FlightDataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.fitted = False

    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['SearchDate'] = pd.to_datetime(df['SearchDate'])
        df['DepartureDate'] = pd.to_datetime(df['DepartureDate'])
        df['departure_time'] = pd.to_datetime(df['departure_time'])
        
        df['days_until_departure'] = (df['DepartureDate'] - df['SearchDate']).dt.days
        df['search_dow'] = df['SearchDate'].dt.dayofweek
        df['departure_dow'] = df['DepartureDate'].dt.dayofweek
        df['departure_hour'] = df['departure_time'].dt.hour
        df['search_month'] = df['SearchDate'].dt.month
        df['departure_month'] = df['DepartureDate'].dt.month
        df['search_day'] = df['SearchDate'].dt.day
        df['departure_day'] = df['DepartureDate'].dt.day
        
        df['is_weekend'] = df['departure_dow'].isin([5, 6]).astype(int)
        df['is_friday'] = (df['departure_dow'] == 4).astype(int)
        df['is_monday'] = (df['departure_dow'] == 0).astype(int)
        df['is_last_minute'] = (df['days_until_departure'] < 7).astype(int)
        df['is_early_bird'] = (df['days_until_departure'] > 30).astype(int)
        df['is_morning'] = ((df['departure_hour'] >= 6) & (df['departure_hour'] < 12)).astype(int)
        df['is_afternoon'] = ((df['departure_hour'] >= 12) & (df['departure_hour'] < 18)).astype(int)
        df['is_evening'] = ((df['departure_hour'] >= 18) & (df['departure_hour'] < 24)).astype(int)
        df['airline_hash'] = df['airline'].apply(lambda x: hash(x) % 100)
        
        return df

    def create_lag_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.sort_values(['DepartureDate', 'departure_hour', 'SearchDate'])
        
        for flight_group in df.groupby(['DepartureDate', 'departure_hour']):
            mask = (df['DepartureDate'] == flight_group[0][0]) & (df['departure_hour'] == flight_group[0][1])
            flight_df = df[mask].sort_values('SearchDate')
            
            if len(flight_df) > 1:
                df.loc[mask, 'price_lag_1'] = flight_df['price'].shift(1)
                df.loc[mask, 'price_lag_3'] = flight_df['price'].shift(3)
                df.loc[mask, 'price_lag_7'] = flight_df['price'].shift(7)
                df.loc[mask, 'price_rolling_mean_3'] = flight_df['price'].rolling(window=3, min_periods=1).mean()
                df.loc[mask, 'price_rolling_std_3'] = flight_df['price'].rolling(window=3, min_periods=1).std()
                df.loc[mask, 'price_rolling_min_7'] = flight_df['price'].rolling(window=7, min_periods=1).min()
                df.loc[mask, 'price_rolling_max_7'] = flight_df['price'].rolling(window=7, min_periods=1).max()
        
        lag_cols = ['price_lag_1', 'price_lag_3', 'price_lag_7', 
                    'price_rolling_mean_3', 'price_rolling_std_3',
                    'price_rolling_min_7', 'price_rolling_max_7']
        for col in lag_cols:
            if col in df.columns:
                df[col].fillna(df['price'].median(), inplace=True)
            else:
                df[col] = df['price'].median()
        
        return df

    def get_feature_columns(self) -> List[str]:
        return [
            'days_until_departure','search_dow','departure_dow','departure_hour',
            'search_month','departure_month','is_weekend','is_friday','is_monday',
            'is_last_minute','is_early_bird','is_morning','is_afternoon','is_evening',
            'airline_hash','price_lag_1','price_lag_3','price_lag_7','price_rolling_mean_3',
            'price_rolling_std_3','price_rolling_min_7','price_rolling_max_7'
        ]


class FlightPriceForecaster:
    def __init__(self, model_type='lightgbm'):
        self.model_type = model_type
        self.model = None
        self.processor = FlightDataProcessor()
        self.feature_cols = self.processor.get_feature_columns()
        self.historical_stats = {}

    def build_model(self):
        if self.model_type == 'lightgbm':
            self.model = lgb.LGBMRegressor(
                n_estimators=200, learning_rate=0.05, max_depth=7,
                num_leaves=31, min_child_samples=20, subsample=0.8,
                colsample_bytree=0.8, random_state=42, n_jobs=-1
            )
        elif self.model_type == 'xgboost':
            self.model = xgb.XGBRegressor(
                n_estimators=200, learning_rate=0.05, max_depth=7,
                min_child_weight=3, subsample=0.8, colsample_bytree=0.8,
                random_state=42, n_jobs=-1
            )
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=200, learning_rate=0.05, max_depth=7,
                min_samples_split=20, subsample=0.8, random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")


class DealDetector:
    @staticmethod
    def calculate_deal_score(actual_price: float, predicted_price: float) -> Dict:
        price_diff = actual_price - predicted_price
        price_diff_pct = (price_diff / predicted_price) * 100
        
        if price_diff_pct <= ModelConfig.EXCELLENT_DEAL_THRESHOLD:
            category, recommendation, emoji = "EXCELLENT_DEAL", "BUY NOW", "🔥"
        elif price_diff_pct <= ModelConfig.GOOD_DEAL_THRESHOLD:
            category, recommendation, emoji = "GOOD_DEAL", "STRONG BUY", "✅"
        elif price_diff_pct <= ModelConfig.FAIR_DEAL_THRESHOLD:
            category, recommendation, emoji = "FAIR_DEAL", "CONSIDER BUYING", "👍"
        elif price_diff_pct < ModelConfig.SLIGHTLY_HIGH_THRESHOLD:
            category, recommendation, emoji = "FAIR_PRICE", "NEUTRAL", "➖"
        elif price_diff_pct < ModelConfig.OVERPRICED_THRESHOLD:
            category, recommendation, emoji = "SLIGHTLY_HIGH", "WAIT", "⚠️"
        elif price_diff_pct < ModelConfig.VERY_OVERPRICED_THRESHOLD:
            category, recommendation, emoji = "OVERPRICED", "AVOID", "❌"
        else:
            category, recommendation, emoji = "VERY_OVERPRICED", "DEFINITELY AVOID", "🚫"

        return {
            'actual_price': round(actual_price, 2),
            'predicted_price': round(predicted_price, 2),
            'price_difference': round(price_diff, 2),
            'price_difference_pct': round(price_diff_pct, 2),
            'category': category,
            'recommendation': recommendation,
            'emoji': emoji
        }


class RealTimePricingEngine:
    def __init__(self, model_path: str = None):
        if model_path:
            self.forecaster = FlightPriceForecaster.load_model(model_path)
        else:
            self.forecaster = None
        self.detector = DealDetector()

