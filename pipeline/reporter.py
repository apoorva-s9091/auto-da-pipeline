import os
import json
from jinja2 import Environment, FileSystemLoader
from utils.logger import logger

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_report(profile_result: dict, eda_result: dict, output_dir: str) -> str:
    logger.info("Generating report")

    os.makedirs(output_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html.j2")

    html_content = template.render(
        profile=profile_result,
        eda=eda_result
    )

    report_path = os.path.join(output_dir, "report.html")
    with open(report_path, "w") as f:
        f.write(html_content)

    logger.info(f"Report saved to: {report_path}")
    return report_path