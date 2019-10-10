#!/usr/bin/env python3

'''
Title:
    Help format Python homeworks into bulk submission format

Description:
    This simply takes in a directory full of homework assignments and the
    grades.csv file. The grades file can be downloaded from Sakai from where
    you upload the files. This page should contain a link to download a
    template.  Download this once so that you have a list of their names.

Prerequisites:

In Sakai, you'll need to download a grades.csv file. This can be found using
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
XXX_Assignment8_BCB_LATE_80.ipynb
XXX_Assignment_8_84.ipynb
XXX_Assignment8_92.ipynb
XXX_Assignment8_97.ipynb
XXX_Assignment8_96.ipynb
XXX_Assignment8_LATE_80.ipynb
XXX_Assignment8_BCB_96.ipynb
```

Tasks:

- Extracts grade from files which are put in NAME_XX.ipynb where XX is the
  score to extract
- Takes extracted grades and puts them in the grade column of the grade.csv
  file
- Extract the first text of the files into the comments.txt file located in
  STUDENT > comments.txt file

Author: Eric Leung
Date: 2019-08-13
Last Updated: 2019-09-01
Python Version: 3.X
Usage:

    $ python format_feedback_for_sakai.py ./path-to-graded-assignments/
'''

import os
import sys
import json
import re
from shutil import copy, make_archive

import pandas as pd


def extract_and_write_comment(student_file_path, student_dir_path):
    '''
    Extract the first code block with comments and write out file

    Args:
        student_file_path: string path to graded assignment
        full_student_dir: string path to directory to upload to Sakai

    Return:
        None
    '''
    with open(student_file_path) as fh:

        assignment = json.load(fh)
        comment_raw = assignment['cells'][0]['source'][0]

        search_for_grade_comment = r'\([0-9]{,3}\/100\) (.*)<'
        comment = re.search(search_for_grade_comment, comment_raw)

        comment_file_path = os.path.join(student_dir_path, 'comments.txt')
        with open(comment_file_path, 'w') as com_fh:
            com_fh.write(comment.group(1))


def check_grades():
    '''
    Check that the grade in the file name is the same as the grade commented in
    the document itself (WIP)

    Args:
        TODO

    Return:
        TODO
    '''
    pass


if __name__ == '__main__':
    # Check command line argument exists to use as assignment and out path
    try:
        assignment_path = sys.argv[1]
    except IndexError:
        args_error = """Add grades and output folder after the script name:
        $ python format_feedback_for_sakai.py grades_dir"""
        raise Exception(args_error)

    try:
        complete_grade_path = os.path.join(assignment_path, 'grades.csv')
        grades = pd.read_csv(complete_grade_path)
    except FileNotFoundError:
        raise Exception('Directory should contain a grades.csv file')

    # Create column that'll be used to name the folders so it'll be formatted
    # as 'Last, First(email@address.edu)'
    grades['folder_name'] = grades['Last Name'] + ', ' + \
        grades['First Name'] + '(' + grades['Display ID'] + ')'

    student_files = os.listdir(assignment_path)
    for student_file in student_files:

        # Make sure we're only dealing with Jupyter notebook files
        if re.search(r'ipynb$', student_file):

            # Make the student name from the file consistent with what we would
            # expect from the downloaded Sakai grades file, i.e., capitalized
            student_name_search = re.search(r'^[A-Za-z]*', student_file)
            student_name = student_name_search.group().capitalize()

            # Set student grade in grade data frame from the file name
            # e.g., a_Assignment5_70.ipynb => 70
            student_grade = re.search(r'([0-9]{,3}).ipynb$', student_file)
            student_idx = grades['Last Name'].str.contains(student_name)
            grades.loc[student_idx, 'grade'] = student_grade.group(1)

            # Create student submission directory for students
            student_dir = grades.loc[student_idx, 'folder_name'].values[0]
            student_dir_path = os.path.join(assignment_path, student_dir)
            if not os.path.exists(student_dir_path):
                os.makedirs(student_dir_path)

            student_file_path = os.path.join(assignment_path, student_file)
            extract_and_write_comment(student_file_path, student_dir_path)

            # I'd rather not move the original assignments to the student
            # folders in case things don't work out; instead, we can copy them
            feedback_dir = os.path.join(student_dir_path,
                                        'Feedback Attachment(s)')
            if not os.path.exists(feedback_dir):
                os.makedirs(feedback_dir)
            copy(student_file_path, feedback_dir)

    grades_path = os.path.join(assignment_path, 'grades.csv')
    grades.to_csv(grades_path, sep=',', index=False)

    # Make archive to zip and upload and go to Sakai
    output_filename = os.path.join('upload_to_sakai')
    make_archive(output_filename, 'zip', assignment_path)
