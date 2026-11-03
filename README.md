# Statistics Notes

This contains notes on mathematical statistics, providing an overview of a few topics and examples of how to apply the topics.
The notes are written in LaTeX, provided here as source, and can be built into a readable PDF.
In order to build the notes, ensure you have LaTeX installed, then run `./build.sh`.

## Organization

The top level contains an outline with table of contents and the build script.
The notes are organized into 6 parts, including the appendices, and each part is a subdirectory.

*NOTE:* This is currently a work in progress, and there may be things missing.
I'm transcribing this from a hand written document and it may take me a while, it's just something I'm doing in my free time to keep these more easily available.
I thought it would be good to post them somewhere public, hopefully this can help someone else!
The current state is that part I is finished, and more parts will be coming soon.

## Building

The only requirement for this project is LaTeX.
In order to build hte entire project, you can run `./build.sh`.
If you are interested in a single chapter, you can instead run teh script with the chapter specified, i.e. `./build.sh theory_of_probability/fundamentals_of_probability.tex`.
The PDF created will live in the base directory of hte project.

## Examples

THere are a few python examples included in this project.
Running them is not required, but may aid inunderstanding concepts.
The only requirement to run these is python.
