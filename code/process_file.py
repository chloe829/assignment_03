"""
process_file.py — Part 2: one file of package descriptions, uploaded.

A Streamlit app that accepts an uploaded text file with one package description
per line, shows the total for every line, and writes the parsed packages to a
JSON file in the `data/` folder — `data/packaging1.txt` in, `data/packaging1.json`
out.

New here: an uploaded file arrives as **bytes**, not text, so it has to be
decoded before it can be split into lines. And a text file usually ends with a
newline, so the last "line" is empty and must be skipped rather than parsed.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_file
"""

import json
import os

import streamlit as st

from packaging_parser import calc_total_units, get_unit, parse_packaging

st.title("Process File of Packages")

uploaded_file = st.file_uploader(
    "Upload a package file",
    type=["txt"],
    key="package_file",
)

if uploaded_file is not None:
    byte_data = uploaded_file.read()
    text_data = byte_data.decode("utf-8")
    lines = text_data.splitlines()

    all_parsed_packages = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "":
            continue

        package = parse_packaging(stripped_line)
        all_parsed_packages.append(package)

        total = calc_total_units(package)
        unit = get_unit(package)
        st.write(f"{stripped_line} ➡️ Total 📦 Size: {total} {unit}")

    original_name = uploaded_file.name
    new_name = original_name.replace(".txt", ".json")
    save_path = os.path.join("data", new_name)
    with open(save_path, "w", encoding="utf-8") as json_file:
        json.dump(all_parsed_packages, json_file, indent=2)

    st.success(f"{len(all_parsed_packages)} packages written to {save_path}")