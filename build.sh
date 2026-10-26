#!/bin/bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${repo_root}"

target_path="${1:-statistics_notes_outline.tex}"

if [[ "${target_path}" != *.tex ]]; then
    echo "Error: expected a .tex file path, got '${target_path}'." >&2
    exit 1
fi

if [[ ! -f "${target_path}" ]]; then
    echo "Error: TeX file not found: ${target_path}" >&2
    exit 1
fi

target_stem="$(basename "${target_path%.tex}")"

# Run twice to resolve references when the document contains cross-links.
pdflatex -output-directory="." "${target_path}"
pdflatex -output-directory="." "${target_path}"

rm -f \
    "./${target_stem}.aux" \
    "./${target_stem}.log" \
    "./${target_stem}.toc" \
    "./${target_stem}.out" \
    "./${target_stem}.lof" \
    "./${target_stem}.lot" \
    "./${target_stem}.fls" \
    "./${target_stem}.fdb_latexmk" \
    "./${target_stem}.bbl" \
    "./${target_stem}.blg"

echo "Build complete: ./${target_stem}.pdf"
