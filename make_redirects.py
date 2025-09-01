#!/usr/bin/env -S uv run -q

# /// script
# dependencies = ["pyyaml"]
# ///

import argparse
import yaml
from pathlib import Path


# Helper to create one redirect file
def make_redirect(path: Path, target_url: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"---\nredirect_to: {target_url}\n---\n"
    path.write_text(content, encoding="utf-8")
    print(f"Created redirect: {path} → {target_url}")


# Helper to process a single "file" entry
def handle_file(new_base_url: Path, file_entry: str):
    no_ext = Path(file_entry).with_suffix("")
    redirect_path = Path.cwd() / f"{no_ext}.md"
    target_url = f"{new_base_url.rstrip('/')}/{no_ext}"
    make_redirect(redirect_path, target_url)


def generate_redirects(toc_file: Path, new_base_url: str):
    # Load YAML
    toc = yaml.safe_load(toc_file.read_text())

    # Handle root page if present
    if "root" in toc:
        handle_file(new_base_url, toc["root"])

    # Handle all parts and chapters
    for part in toc.get("parts", []):
        for chapter in part.get("chapters", []):
            if "file" in chapter:
                handle_file(new_base_url, chapter["file"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Jekyll redirect .md files from a Jupyter Book _toc.yaml."
    )
    parser.add_argument("toc_file", type=Path, help="_toc.yaml file path")
    parser.add_argument("new_base_url", help="Base URL of the new site")

    args = parser.parse_args()
    generate_redirects(args.toc_file, args.new_base_url)
