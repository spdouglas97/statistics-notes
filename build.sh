#!/bin/bash

# Build the LaTeX document
pdflatex statistics_notes_outline.tex

# Run twice to resolve references
pdflatex statistics_notes_outline.tex

# Clean up auxiliary files
rm -f statistics_notes_outline.aux statistics_notes_outline.log statistics_notes_outline.toc statistics_notes_outline.out

echo "Build complete: statistics_notes_outline.pdf"
