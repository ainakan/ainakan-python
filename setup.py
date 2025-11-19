import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterator

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

SOURCE_ROOT = Path(__file__).resolve().parent
AINAKAN_EXTENSION = os.environ.get("AINAKAN_EXTENSION", None)


def main():
    setup(
        name="ainakan",
        version=detect_version(),
        description="Dynamic instrumentation toolkit for developers, reverse-engineers, and security researchers",
        long_description=compute_long_description(),
        long_description_content_type="text/markdown",
        author="Ainakan Developers",
        author_email="oleavr@ainakan.re",
        url="https://ainakan.re",
        install_requires=["typing_extensions; python_version<'3.11'"],
        python_requires=">=3.7",
        license="wxWindows Library Licence, Version 3.1",
        keywords="ainakan debugger dynamic instrumentation inject javascript windows macos linux ios iphone ipad android qnx",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Environment :: MacOS X",
            "Environment :: Win32 (MS Windows)",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved",
            "Natural Language :: English",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: JavaScript",
            "Topic :: Software Development :: Debuggers",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        packages=["ainakan", "ainakan._ainakan"],
        package_data={"ainakan": ["py.typed"], "ainakan._ainakan": ["py.typed", "__init__.pyi"]},
        ext_modules=[
            Extension(
                name="ainakan._ainakan",
                sources=["ainakan/_ainakan/extension.c"],
                py_limited_api=True,
            )
        ],
        cmdclass={"build_ext": AinakanPrebuiltExt if AINAKAN_EXTENSION is not None else AinakanDemandBuiltExt},
        zip_safe=False,
    )


def detect_version() -> str:
    pkg_info = SOURCE_ROOT / "PKG-INFO"
    in_source_package = pkg_info.exists()
    if in_source_package:
        version_line = [
            line for line in pkg_info.read_text(encoding="utf-8").split("\n") if line.startswith("Version: ")
        ][0].strip()
        return version_line[9:]

    version = os.environ.get("AINAKAN_VERSION")
    if version is not None:
        return version

    releng_location = next(enumerate_releng_locations(), None)
    if releng_location is not None:
        sys.path.insert(0, str(releng_location.parent))
        from releng.ainakan_version import detect

        return detect(SOURCE_ROOT).name.replace("-dev.", ".dev")

    return "0.0.0"


def compute_long_description() -> str:
    return (SOURCE_ROOT / "README.md").read_text(encoding="utf-8")


def enumerate_releng_locations() -> Iterator[Path]:
    val = os.environ.get("MESON_SOURCE_ROOT")
    if val is not None:
        parent_releng = Path(val) / "releng"
        if releng_location_exists(parent_releng):
            yield parent_releng

    local_releng = SOURCE_ROOT / "releng"
    if releng_location_exists(local_releng):
        yield local_releng


def releng_location_exists(location: Path) -> bool:
    return (location / "ainakan_version.py").exists()


class AinakanPrebuiltExt(build_ext):
    def build_extension(self, ext):
        target = self.get_ext_fullpath(ext.name)
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(AINAKAN_EXTENSION, target)


class AinakanDemandBuiltExt(build_ext):
    def build_extension(self, ext):
        make = SOURCE_ROOT / "make.bat" if platform.system() == "Windows" else "make"
        subprocess.run([make], check=True)

        outputs = [entry for entry in (SOURCE_ROOT / "build" / "ainakan" / "_ainakan").glob("_ainakan.*") if entry.is_file()]
        assert len(outputs) == 1
        target = self.get_ext_fullpath(ext.name)
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(outputs[0], target)


if __name__ == "__main__":
    main()
