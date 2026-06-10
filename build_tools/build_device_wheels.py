import tempfile
from pathlib import Path
import shutil
import tomllib
import tomli_w
import subprocess

TARGETS = [
    "generic",
    "avx2",
]

SCRIPT_DIR = Path(__file__).resolve().parent
PARENT_DIR = SCRIPT_DIR.parent

def _banner(msg: str):
    header = "=" * 20
    print(f'{header} {msg} {header}')


def _build(path: Path, target: str):
    dst = Path(f'{PARENT_DIR}/dist')
    print(f'Building at {path}')
    subprocess.run(
        ["uv", "build", "--wheel", "-o", dst],
        cwd=path,
        check=True
    )


def _rewrite_project_name(path: Path, target: str):
    file_path = Path(f"{path}/pyproject.toml")
    print(file_path)
    data = tomllib.loads(file_path.read_text())

    data['project']['name'] = f'simddot-core-{target}'

    cmake = (
        data
        .setdefault('tool', {})
        .setdefault('scikit-build', {})
        .setdefault('cmake', {})
        .setdefault('define', {})
    )
    cmake['SIMDDOT_ISA'] = target

    file_path.write_text(tomli_w.dumps(data))


def _main():
    for target in TARGETS:
        _banner(f'Building {target} target')
        with tempfile.TemporaryDirectory() as tmp:
            tmp = f"{tmp}-{target}"
            tmpdir = Path(tmp)
            shutil.copytree(PARENT_DIR, tmpdir)

            _rewrite_project_name(tmpdir, target)
            _build(tmpdir, target)


if __name__ == '__main__':
    _main()
