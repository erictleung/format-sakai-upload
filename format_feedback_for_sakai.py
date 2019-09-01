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


def check_path():
    '''
    Function to check command line input to be legitimate directory name

    Args:
        None

    Returns:
        String name of where assignment files are
    '''
    try:
        assignment_path = sys.argv[1]
    except IndexError:
        path_error = """Append the directory with grades after the script name:
        $ python format_feedback_for_sakai.py directory_with_grades"""
        raise Exception(path_error)

    return assignment_path


def read_grades(assignment_path):
    '''
    Function to try reading in grades.csv file

    Args:
        assignment_path: String name of the path where grades.csv file is

    Returns:
        pandas DataFrame with student grade information
    '''
    try:
        grades = pd.read_csv(assignment_path + '/grades.csv')
    except FileNotFoundError:
        grade_error = 'Directory should contain a grades.csv file'
        raise Exception(grade_error)

    return grades


def extract_and_write_comment(student_file_path, full_student_dir):
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

        with open(full_student_dir + '/comments.txt', 'w') as com_fh:
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


def archive_for_upload(assignment_path):
    '''
    Archive files and directories ready for Sakai upload (WIP)

    Looks through the assignment path for directories and the grades.csv file.
    This function then takes these directories and file and zips it into a file
    `upload_to_sakai.zip` that you can use to upload to Sakai.

    Args:
        assignment_path

    Return:
        None
    '''
    output_filename = assignment_path + '/upload_to_sakai.zip'
    make_archive(assignment_path, 'zip', output_filename)



if __name__ == '__main__':
    assignment_path = check_path()
    grades = read_grades(assignment_path)

    # Create column that'll be used to name the folders so it'll be formatted
    # as 'Last, First(email@address.edu)'
    grades['folder_name'] = grades['Last Name'] + ', ' + \
        grades['First Name'] + '(' + grades['Display ID'] + ')'

    graded_files = os.listdir(assignment_path)

    check_ipynb = re.compile(r'ipynb$')
    for student_file in graded_files:

        if check_ipynb.search(student_file):

            student_name_search = re.search(r'^[A-Za-z]*', student_file)
            student_name = student_name_search.group().capitalize()

            # Set student grade in grade data frame
            student_grade = re.search(r'([0-9]{,3}).ipynb', student_file)
            student_idx = grades['Last Name'].str.contains(student_name)
            grades.loc[student_idx, 'grade'] = student_grade.group(1)

            # Create student submission directory for students
            student_dir = grades.loc[student_idx, 'folder_name'].values[0]
            full_student_dir = assignment_path + '/' + student_dir
            if not os.path.exists(full_student_dir):
                os.makedirs(full_student_dir)

            student_file_path = assignment_path + '/' + student_file
            extract_and_write_comment(student_file_path, full_student_dir)

            # Copy feedback file into 'Feedback Attachment(s)/'
            feedback_dir = full_student_dir + '/Feedback Attachment(s)'
            if not os.path.exists(feedback_dir):
                os.makedirs(feedback_dir)
            copy(student_file_path, feedback_dir)

    grades.to_csv(assignment_path + '/grades.csv', sep=',', index=False)
