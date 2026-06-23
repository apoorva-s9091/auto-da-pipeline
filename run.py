import argparse
from utils.logger import logger
from pipeline.validator import validate
from pipeline.etl import load_data
from pipeline.profiler import profile
from pipeline.cleaner import clean
from pipeline.eda import run_eda
from pipeline.reporter import generate_report

def main():
    parser=argparse.ArgumentParser(description="Automated Data Analysis Pipeline")
    parser.add_argument("--input", required=True, help= "Path to input files (CSV/Excel/JSON)")
    parser.add_argument("--output", default="reports/", help="output folder for reports")
    args= parser.parse_args()

    logger.info("Pipeline Started")
    df= load_data(args.input)
    validate(df)
    profile_result= profile(df)
    df_clean= clean(df)
    eda_result = run_eda(df_clean)
    generate_report(profile_result, eda_result, args.output)


    logger.info("pipeline complete. Report saved to:"+ args.output)

    if __name__== "__main__":
        main()