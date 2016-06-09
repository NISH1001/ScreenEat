# Strictly follow the guidelines !!

# Git
-------------

## 1. Write quality commit messages

Use **imperative, present tense** for title part of your commit messages.
For example:  

> Add memory efficient data structure

Instead of:

> Added memory efficient data structure

Make sure these are less than or equal to 50 characters long and do not
end with a full stop.

You may optionally add a body part, which is a paragraph with not more than
72-characters each line and ends with a full-stop, to explain the commit
in detail.


## 2. Make commits as logical change sets

Do not too many redundant commits. Do not make commits that only has un-meaningful,
unusable or unstable changes.

Yet, make sure that your commits as separate change sets are digestible. Do not
code for number of days and commit large independent logical changes as one commit.

# Python
-------------

Strictly follow [pep-8](https://www.python.org/dev/peps/pep-0008/)
Following are some of the imposed conventions that every pythonista are recommended to follow:

## 1. Function definitions
- Use lower case for function names
- In case the function has multiple words, separate them by **underscore**
- `do_this()`

## 2. Packages
- Follow same convention as in function definitions
- Be sure to create a package in a folder that contains `__init__.py`
- `package`

## 3. Classes
- Use **UpperCaseCamelCase** convention like this one
- `Exception` classes should end in **Error**
- `ScrapError`
- **Public** variables should be in lower case seperated by underscore
- `self.my_list`
- **Private** variables should begin with a **single** underscore

## 4. Constants
- Use **FULLY_CAPITALIZED** name for constants
- In case of multiple words, separate them by underscore
