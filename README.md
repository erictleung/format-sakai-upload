# Format Feedback for Sakai

> Help format Python homeworks into bulk submission format

This simply takes in a directory full of homework assignments and the
grades.csv file. The grades file can be downloaded from Sakai from where you
upload the files. This page should contain a link to download a template.
Download this once so that you have a list of their names.

**Contents**

- [Usage](#usage)
- [Prerequisites](#prerequisites)

## Usage

```shell
python format_feedback_for_sakai.py example_before
```

where `example_before` is the name of the directory path to search for files.

## Prerequisites

Python 3.X

In Sakai, you'll need to download a `grades.csv` file. This can be found using
the "Download All" link when you are in a submission page about to grade the
assignments. This grades.csv file will be put with the flat directory as seen
below.

Example directory structure from `tree`:

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

The script file should be outside this file containing the graded files.
