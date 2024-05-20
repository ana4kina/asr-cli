#!/usr/bin/env python3

import warnings
from argparse import ArgumentParser, Namespace

from asr_cli.asr_config import ASRArch
from asr_cli.asr_getter import get_asr
from asr_cli.vad_config import VadArch
from asr_cli.vad_getter import get_vad
from asr_cli.infer import infer

warnings.filterwarnings("ignore")


def _get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--wav_path", type=str, help="wav_path to process", required=True)
    return parser.parse_args()


def cli_entrypoint(wav_path: str):
    asr_recognizer = get_asr(ASRArch.gigaam_ctc, remote=False)
    vad_cutter = get_vad(VadArch.webrtc)

    result = infer(wav_path, asr_recognizer, vad_cutter)
    print(result)


def main():
    args = _get_args()
    cli_entrypoint(args.wav_path)


if __name__ == "__main__":
    main()
