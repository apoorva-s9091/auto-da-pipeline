import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from utils.logger import logger

CHARTS_DIR = "reports/charts"
os.makedirs(CHARTS_DIR, exist_ok=True)


def run_eda(df: pd.DataFrame) -> dict:
    logger.info("Starting EDA")
    eda_result = {}

    eda_result["correlation"] = plot_correlation(df)
    eda_result["distributions"] = plot_distributions(df)
    eda_result["boxplots"] = plot_boxplots(df)
    eda_result["countplots"] = plot_countplots(df)
    eda_result["missing_heatmap"] = plot_missing_heatmap(df)
    eda_result["pairplot"] = plot_pairplot(df)
    eda_result["outlier_summary"] = plot_outlier_summary(df)
    eda_result["violin"] = plot_violin(df)
    eda_result["cdf"] = plot_cumulative_distribution(df)
    eda_result["time_series"] = plot_time_series(df)
    eda_result["statistics"] = compute_statistics(df)

    target = input("\nDo you have a target column? Enter name or press Enter to skip: ").strip()
    if target and target in df.columns:
        eda_result["target_analysis"] = plot_target_analysis(df, target)
        eda_result["feature_importance"] = plot_feature_importance(df, target)
    else:
        logger.info("No target column specified")

    choice = input("\nWant custom AI analysis? (y/n): ").strip().lower()
    if choice == "y":
        from pipeline.ai_analyst import ai_analysis
        eda_result["ai_analysis"] = ai_analysis(df)

    logger.info("EDA complete")
    return eda_result


def plot_correlation(df: pd.DataFrame) -> str:
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        logger.warning("No numeric columns for correlation heatmap")
        return None
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "correlation_heatmap.png")
    plt.savefig(path)
    plt.close()
    logger.info("Saved correlation heatmap")
    return path

def plot_distributions(df: pd.DataFrame) -> list:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    paths = []
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col], kde=True, color="steelblue")
        plt.title(f"Distribution of {col}")
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, f"dist_{col}.png")
        plt.savefig(path)
        plt.close()
        paths.append(path)
        logger.info(f"Saved distribution plot for '{col}'")
    return paths

def plot_boxplots(df: pd.DataFrame) -> list:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    paths = []
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=df[col], color="lightcoral")
        plt.title(f"Boxplot of {col}")
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, f"box_{col}.png")
        plt.savefig(path)
        plt.close()
        paths.append(path)
        logger.info(f"Saved boxplot for '{col}'")
    return paths

def plot_countplots(df: pd.DataFrame) -> list:
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    paths = []
    for col in cat_cols:
        plt.figure(figsize=(6, 4))
        sns.countplot(x=df[col], palette="Set2")
        plt.title(f"Countplot of {col}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, f"count_{col}.png")
        plt.savefig(path)
        plt.close()
        paths.append(path)
        logger.info(f"Saved countplot for '{col}'")
    return paths

def plot_missing_heatmap(df: pd.DataFrame) -> str:
    if df.isnull().sum().sum() == 0:
        logger.info("No missing values — skipping missing heatmap")
        return None
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap="viridis", yticklabels=False)
    plt.title("Missing Value Heatmap")
    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "missing_heatmap.png")
    plt.savefig(path)
    plt.close()
    logger.info("Saved missing value heatmap")
    return path

def plot_pairplot(df: pd.DataFrame) -> str:
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        logger.warning("Not enough numeric columns for pairplot")
        return None
    if numeric_df.shape[1] > 6:
        numeric_df = numeric_df.iloc[:, :6]
        logger.warning("Too many columns — pairplot limited to first 6")
    pair = sns.pairplot(numeric_df)
    path = os.path.join(CHARTS_DIR, "pairplot.png")
    pair.savefig(path)
    plt.close()
    logger.info("Saved pairplot")
    return path

def plot_outlier_summary(df: pd.DataFrame) -> str:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    outlier_counts = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        count = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
        outlier_counts[col] = count
    plt.figure(figsize=(10, 5))
    plt.bar(outlier_counts.keys(), outlier_counts.values(), color="tomato")
    plt.title("Outlier Count per Column")
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "outlier_summary.png")
    plt.savefig(path)
    plt.close()
    logger.info("Saved outlier summary chart")
    return path

def plot_target_analysis(df: pd.DataFrame, target: str) -> list:
    paths = []
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if target in numeric_cols:
        numeric_cols.remove(target)
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(x=df[col], y=df[target], alpha=0.5)
        plt.title(f"{col} vs {target}")
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, f"scatter_{col}_vs_{target}.png")
        plt.savefig(path)
        plt.close()
        paths.append(path)
        logger.info(f"Saved scatter plot: {col} vs {target}")
    return paths

def plot_feature_importance(df: pd.DataFrame, target: str) -> str:
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    X = df.drop(columns=[target])
    y = df[target]
    X = X.select_dtypes(include="number")
    if y.dtype == "object":
        le = LabelEncoder()
        y = le.fit_transform(y)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importance.values, y=importance.index, palette="viridis")
    plt.title(f"Feature Importance vs '{target}'")
    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "feature_importance.png")
    plt.savefig(path)
    plt.close()
    logger.info("Saved feature importance chart")
    return path

def plot_violin(df: pd.DataFrame) -> list:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    paths = []
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.violinplot(x=df[col], color="mediumpurple")
        plt.title(f"Violin Plot of {col}")
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, f"violin_{col}.png")
        plt.savefig(path)
        plt.close()
        paths.append(path)
        logger.info(f"Saved violin plot for '{col}'")
    return paths

def plot_cumulative_distribution(df: pd.DataFrame) -> list:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    paths = []
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.ecdfplot(df[col], color="steelblue")
        plt.title(f"Cumulative Distribution of {col}")
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, f"cdf_{col}.png")
        plt.savefig(path)
        plt.close()
        paths.append(path)
        logger.info(f"Saved CDF plot for '{col}'")
    return paths

def plot_time_series(df: pd.DataFrame) -> list:
    date_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()
    if not date_cols:
        logger.info("No datetime columns found — skipping time series")
        return []
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    paths = []
    for date_col in date_cols:
        for num_col in numeric_cols:
            plt.figure(figsize=(10, 4))
            plt.plot(df[date_col], df[num_col], color="teal")
            plt.title(f"{num_col} over {date_col}")
            plt.tight_layout()
            path = os.path.join(CHARTS_DIR, f"timeseries_{num_col}.png")
            plt.savefig(path)
            plt.close()
            paths.append(path)
            logger.info(f"Saved time series: {num_col} over {date_col}")
    return paths

def compute_statistics(df: pd.DataFrame) -> dict:
    numeric_df = df.select_dtypes(include="number")
    stats = {
        "mean": numeric_df.mean().to_dict(),
        "median": numeric_df.median().to_dict(),
        "std": numeric_df.std().to_dict(),
        "variance": numeric_df.var().to_dict(),
        "skewness": numeric_df.skew().to_dict(),
        "kurtosis": numeric_df.kurtosis().to_dict(),
        "min": numeric_df.min().to_dict(),
        "max": numeric_df.max().to_dict(),
    }
    logger.info("Computed descriptive statistics")
    return stats