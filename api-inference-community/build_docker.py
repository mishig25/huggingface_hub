#!/usr/bin/env python
import uuid
import sys
import subprocess
import argparse


def run(command):
    print(" ".join(command))
    p = subprocess.run(command)
    if p.returncode != 0:
        sys.exit(p.returncode)


def build(framework: str):
    DEFAULT_HOSTNAME = "854676674973.dkr.ecr.us-east-1.amazonaws.com"
    hostname = DEFAULT_HOSTNAME
    tag = str(uuid.uuid4())[:5]
    container_tag = f"{hostname}/api-inference-community:{framework}-{tag}"

    command = ["docker", "build", f"docker_images/{framework}", "-t", container_tag]
    run(command)

    command = ["aws", "ecr", "get-login"]
    output = subprocess.check_output(command)

    command_args = output.strip().decode("utf-8").split()
    # Ignore -e none
    command = command_args[:-3] + command_args[-1:]
    run(command)

    command = ["docker", "push", container_tag]
    run(command)


def main():
    frameworks = {
        "allennlp",
        "asteroid",
        "espnet",
        "flair",
        "speechbrain",
        "timm",
        "sentence_transformers",
        "spacy",
    }
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "framework",
        type=str,
        choices=frameworks,
        help="Which framework image to build.",
    )
    args = parser.parse_args()
    build(args.framework)


if __name__ == "__main__":
    main()
