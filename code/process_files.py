"""
process_files.py — Part 3: many files, one after another, with a running total.

The same job as process_file.py, but the app now remembers what it has already
done: how many files have been processed, how many packages that came to, and a
one-line summary of each file — and it keeps remembering across uploads.

That is the hard part, and it is hard for a specific reason: every interaction
reruns this whole script from the top, so an ordinary variable like
`files_processed = 0` is reset to zero on every rerun. Anything that has to
survive a rerun lives in `st.session_state` instead, and is initialised only
once — the first time the script runs.

The other trap is the uploader itself. Once a file has been chosen it stays
chosen on every rerun, so an app that processes "whenever there is a file" would
count the same file again on every interaction. Processing happens on a button
click instead: `st.button` is True only on the one rerun the click caused.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_files
"""

import json
import os

import streamlit as st

from packaging_parser import parse_packaging

if "files_processed" not in st.session_state:
    st.session_state.files_processed = 0
if "packages_processed" not in st.session_state:
    st.session_state.packages_processed = 0
if "file_summaries" not in st.session_state:
    st.session_state.file_summaries = []

st.title("Process Package Files")

uploaded_file = st.file_uploader(
    "Upload a package file",
    type=["txt"],
    key="package_file",
)

process_button = st.button("Process file", key="process")

if process_button and uploaded_file is not None:
    byte_data = uploaded_file.read()
    text_data = byte_data.decode("utf-8")
    lines = text_data.splitlines()

    parsed_packages = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "":
            continue
        parsed_packages.append(parse_packaging(stripped_line))

    st.session_state.files_processed += 1
    st.session_state.packages_processed += len(parsed_packages)

    original_name = uploaded_file.name
    new_name = original_name.replace(".txt", ".json")
    save_path = os.path.join("data", new_name)
    with open(save_path, "w", encoding="utf-8") as json_file:
        json.dump(parsed_packages, json_file, indent=2)

    summary = f"{len(parsed_packages)} packages written to {save_path}"
    st.session_state.file_summaries.append(summary)

files_col, packages_col = st.columns(2)
files_col.metric("Files processed", st.session_state.files_processed)
packages_col.metric("Packages processed", st.session_state.packages_processed)

for summary in st.session_state.file_summaries:
    st.info(summary)
