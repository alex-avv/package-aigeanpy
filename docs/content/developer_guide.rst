Developer Guide
===============

This page is a guide for those developers who want to contribute to the Aigeanpy library.

1.  Create a personal fork of the project from the `Github repository <https://github.com/UCL-COMP0233-22-23/aigeanpy-Working-Group-15>`_.

2.  Clone the fork onto your local machine.

    *   If your fork is out-dated pull the up-to-date version to your local repository:

        .. code-block:: Python

            git pull

3.  Create a new branch and begin implementing your code following the `PEP 8 style guide <https://peps.python.org/pep-0008/>`_.

    .. code-block:: Python

        git checkout -b <new-branch-name>
    
4.  Fully document your code using docstrings following the `numpy format <https://numpydoc.readthedocs.io/en/latest/format.html>`_.

5.  Move into the aigeanpy directory and run pytest in the terminal.

    .. code-block:: Python

        pytest

6.  Push your branch to your fork on Github. When creating commit messages please follow the `style guide <https://medium.com/swlh/writing-better-commit-messages-9b0b6ff60c67>`_.

7.  Create a new pull request targeting the master branch of the aigeanpy library.

    *   Please link issues, use relevant tags and use an appropriate title that summarises your changes concisely.