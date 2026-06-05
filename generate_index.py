import sys
import html
import shutil
import os
import re
from collections import defaultdict
from pathlib import Path
import hashlib

OUTPUT_DIR = "site"
SIMPLE_PATH = f"{OUTPUT_DIR}/simple"
PACKAGES_PATH = f"{OUTPUT_DIR}/packages"

HTML = """
<!DOCTYPE html>
<html><body>
{content}
</body></html>
"""


def _get_projects(input_dir: str) -> dict[str, list[str]]:
    projects = defaultdict(list)
    try:
        wheels = list(os.walk(input_dir))[0][2]
    except IndexError:
        # the specified input dir doesn't exist
        # if it exists, we'll always get the triplet
        wheels = []

    for wheel in wheels:
        project = wheel.strip().split('-')[0]
        project_normalized = re.sub(r"[-_.]+", '-', project).lower()
        projects[project_normalized].append(f"{input_dir}/{wheel}")

    return projects


def _write_root_index_html(projects_wheels_map: dict[str, list[str]]):
    anchors = []
    project_anchors_map = defaultdict(list)

    Path(SIMPLE_PATH).mkdir(parents=True, exist_ok=True)
    Path(PACKAGES_PATH).mkdir(parents=True, exist_ok=True)

    for project, wheels in projects_wheels_map.items():
        anchors.append(f'<a href="{project}/">{project}</a>')
        project_anchors_map[project].extend(
            _get_project_anchors(project, wheels)
        )

    with open(f"{SIMPLE_PATH}/index.html", "w") as f:
        f.write(HTML.format(content="<br>".join(anchors)))

    for project, anchors in project_anchors_map.items():
        with open(f"{SIMPLE_PATH}/{project}/index.html", "w") as f:
            f.write(HTML.format(content="<br>".join(anchors)))


def _get_project_anchors(project_name: str, wheels: list) -> list[str]:
    anchors = []

    Path(f"{SIMPLE_PATH}/{project_name}").mkdir(parents=True, exist_ok=True)

    for wheel in wheels:
        wheel_filename = wheel.split('/')[-1]
        dst = f"{PACKAGES_PATH}/{wheel_filename}"
        print(wheel_filename)
        shutil.copyfile(wheel, f"{PACKAGES_PATH}/{wheel_filename}")
        wheel_handle = open(dst, 'rb')
        digest = hashlib.sha256(wheel_handle.read()).hexdigest()
        requires_python = html.escape(">=3.12")  # TODO read from pyproject
        anchors.append(
            f'<a href="../../packages/{wheel_filename}#sha256={digest}" '
            f'data-requires-python="{requires_python}">'
            f'{wheel_filename}</a>'
        )

    return anchors


def main(input_dirs: list[str]):
    projects_wheels_map = defaultdict(list)
    for input_dir in input_dirs:
        projects = _get_projects(input_dir)
        for project, wheels in projects.items():
            projects_wheels_map[project].extend(wheels)

    _write_root_index_html(projects_wheels_map)


if __name__ == '__main__':
    main(sys.argv[1:])
