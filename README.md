# Format Feedback for Sakai

> Help format Jupyter notebook homeworks into bulk submission format

This simply takes in a directory full of Jupyter notebook homework assignments
and the `grades.csv` file.

The grades file can be downloaded from Sakai from where you upload the files.
This page should contain a link to download a template. Download this once so
that you have a list of student names and emails.

**Contents**

- [Usage](#usage)
- [Prerequisites](#prerequisites)
- [Example Directory Structure](#example-directory-structure)
- [Example Jupyter Notebook](#example-jupyter-notebook)
- [License](#license)

## Usage

```shell
python format_feedback_for_sakai.py example_before
```

where `example_before` is the name of the directory path to search for files.

## Prerequisites

Python 3.X and pandas

In Sakai, you'll need to download a `grades.csv` file. This can be found using
the "Download All" link when you are in a submission page about to grade the
assignments. This `grades.csv` file will be put with the flat directory as seen
below.

[Here](https://longsight.screenstepslive.com/s/sakai_help/m/59830/l/610136-how-do-i-upload-graded-assignment-submissions-and-feedback)
are some more visual instructions on how to do this.

## Example Directory Structure

Example directory structure for example directory `week_8`:

```txt
grades.csv
XXX_Assignment8_BCB_90.ipynb
XXX_Assignment8_61.ipynb
XXX_Assignment8_BCB_96.ipynb
XXX_Assignment8_94.ipynb
XXX_Assignment8_96.ipynb
XXX_Assignment8.ipynb
XXX_Assignment8_BCBa_100.ipynb
XXX_Assignment8_100.ipynb
XXX_Assignment8_100.ipynb
XXX_Assignment8_BCB_80.ipynb
XXX_Assignment_8_84.ipynb
XXX_Assignment8_92.ipynb
XXX_Assignment8_97.ipynb
XXX_Assignment8_96.ipynb
XXX_Assignment8_80.ipynb
XXX_Assignment8_BCB_96.ipynb
```

**Note: The Python script file should be outside this directory containing the
graded files. It should be arranged in a similar way as to how this directory
is arranged.**

## Example Jupyter Notebook

The Python script here opens up the Jupyter notebook with the extension `.ipynb`
and extracts the first Markdown text block. This text block should contain the
comments you wish to give back to a student.

See [here](./example_before/a_Assignment5_50.ipynb) for an example notebook.

## License

MIT
