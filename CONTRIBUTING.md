# Strictly follow the guidelines !!

# Git
-------------

## 1. Commit messages

Use **imperative, present tense** for commit messages.
For example:  

> Add memory efficient data structure

Instead of:

> Added memory efficient data structure


## 2. No redundant commits

Please! do not push redundant commits whenever you change your code.  

For example (redundant commit):

> Edit README.md
> 
> Fix typo in README.md


# Python
-------------

Strictly follow [pep-8](https://www.python.org/dev/peps/pep-0008/)
Following are some of the imposed conventions that every pythonista must follow:

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
