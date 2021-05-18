from jinja2 import Environment, FileSystemLoader
import yaml
import os
from datetime import datetime

"""Script to auto-generate jobs.yaml file declaring prow-jobs
"""

# Load the config to be used with jinja templates.
config = yaml.safe_load(open('./jobs_config.yaml'))
env = Environment(loader=FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)


def load_templates(prow_job_type: str, template_dir: str) -> str:
    try:
        template_files = os.listdir(template_dir)
    except FileNotFoundError as fe:
        print(f'{template_dir}: No such directory to load templates. Ignoring.')
        return ""

    content = f'{prow_job_type}:\n'
    for file_name in template_files:
        template_content = env.get_template(f'{template_dir}/{file_name}')
        content += f'{template_content.render(config)}\n'

    return content


def main():
    jinja_path = './jinja'
    periodic_jobs_path = f'{jinja_path}/periodics'
    postsubmit_jobs_path = f'{jinja_path}/postsubmits'
    presubmit_jobs_path = f'{jinja_path}/presubmits'

    prowjobs_content = "# Autogenerated. Do NOT update Manually.\n"
    prowjobs_content += f'# Last generated on {datetime.now()}.\n'
    prowjobs_content += load_templates('periodics', periodic_jobs_path)
    prowjobs_content += load_templates('postsubmits', postsubmit_jobs_path)
    prowjobs_content += load_templates('presubmits', presubmit_jobs_path)

    with open('./jobs.yaml', 'w') as jobs_file:
        jobs_file.write(prowjobs_content)


if __name__ == "__main__":
    main()