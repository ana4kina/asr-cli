from typing import List
from setuptools import find_packages, setup


def get_requires() -> List[str]:
    return [
        "soundfile==0.12.1",
        "soxr==0.3.7",
        "torch==2.3.0",
        "torchaudio==2.3.0",
        "numpy==1.23.5",
        "transformers==4.40.2",
        "webrtcvad==2.0.10",
        "Cython==3.0.10",
        "nemo_toolkit @ git+https://github.com/NVIDIA/NeMo.git@r1.21.0#egg=nemo_toolkit",
        "hydra-core==1.3.2",
        "pytorch-lightning==2.2.4",
        "sentencepiece==0.2.0",
        "wheel==0.43.0",
        "youtokentome==1.0.6",
        "inflect==7.2.1",
        "webdataset==0.2.86",
        "pyannote.audio==3.2.0",
        "editdistance==0.8.1",
        "jiwer==3.0.4",
        "omegaconf",
        "IPython",
        "pyaudio",
        "matplotlib"
    ]


setup(
    name="asr_cli",
    entry_points = {
        'console_scripts': ['asr-cli=asr_cli.main:main'],
    },
    version="0.dev",
    description="Simple ASR CLI tool",
    package_dir={"": "src"},
    packages=find_packages("str", include=["asr_cli", "asr_cli.*"]),
    include_package_data=True,
    install_requires=get_requires(),
    dependency_links=[
        'git+https://github.com/NVIDIA/NeMo.git@r1.21.0#egg=nemo_toolkit[all]'
    ],
    python_requires=">=3.8",
    zip_safe=False
)
