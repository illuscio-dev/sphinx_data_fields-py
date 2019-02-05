.. islelib documentation master file, created by
   sphinx-quickstart on Mon Oct  1 00:18:03 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

islelib-py
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

``islelib`` is Illuscio's python library template. To build your own documentation,
simply start using it. Below we will show some example documentation with the basic
functions of this library template.

Table of Contents
=================

* :ref:`basic-usage`
* :ref:`setting-up`
* :ref:`writing`
* :ref:`deploying`
* :ref:`qol`

.. _basic-usage:

Basic Usage
===========

   >>> import islelib
   [basic useage example goes here]

Islelib comes with a number of pre-built quality-of-life macros for developers so they
can code more and manage less, most of which are accessed through ``make`` commands.

In addition to your lib's package folder, islelib has two other main directories:

   * ``./zdocs`` - where docs are built to and stored
   * ``./zdevelop`` - where tests, maintenance scripts, and other information is stored

In addition, the following files are used:

   * ``./README.md`` - brief description and pointer to doc link for `Github`_
   * ``./setup.cfg`` - when possible, settings for all tools are stored here
   * ``./Makefile`` - contains make commands for the development features detailed in this doc
   * ``./azure_pipelines.yml`` - build process definition for `Azure Pipelines`_
   * ``./readthedocs.yml`` - config file for `readthedocs`_ documentation builds

.. _setting-up:

Setting up your Library
=======================

Getting started is easy, just follow the below steps. Many of these steps include
``Make`` scripts that help you get up and running quickly. To run the ``Make`` commands,
ensure that the active directory of your terminal session is ``"islelib-py"``

1. Clone islelib-py from Github
--------------------------------

navigate to where you wish to keep your project in terminal: ::

   >>> cd /path/to/local_repository
   >>> git clone git@github.com:bpeake-illuscio/islelib-py.git

once the library is cloned, move into it as your active directory: ::

    >>> cd islelib-py

2. Pick a Name
--------------

Illuscio uses the ''isle'' prefix convention (phonetically sounds like I-L/"Aye-EL" as
opposed to "ill". Examples include ``isle_type``, ``isle_collections``, etc.

When you have chosen a name for your new lib, simply type: ::

   >>> make name n=libname
   library renamed! to switch your current directory, use the following	command:
   cd '/path/to/libname-py'

... where ``libname`` is the name of your new library. This will:

   * change the name of any packages with an __init__ to ``libname`` (uses a find and replace from the old name when applicable).
   * change all of the relevant setup.cfg options to ``libname``
   * change the top level folder to ``libname-py``
   * remove old ``islelib.egg`` folder

3. Pick a Description
---------------------

In the ``./setup.cfg`` file, under the ``[metadata]`` header, change the ``description``
field to a brief description of your project. This is the description that will appear
on builds in Illuscio's `Python Azure Artifacts Feed`_ (pypi package repository).
This description can be changed at any time.

4. Create a Virtual Environment
--------------------------------

To set up a virtual enviroment through virtualenv, type: ::

   >>> make venv

This will install a new virtual enviroment at ``~/venvs/[libname]-py-[## python version]``.

Example name: ``libname-py-37``

By default, this command uses your current "python3" alias, but a different version
can be supplied with a `py=` option: ::

   >>> make venv py="/Library/Frameworks/Python.framework/Versions/3.7/bin/python3"
   venv created! To enter virtual env, run :
   . ~/.bash_profile
   then run:
   env_libname-37

``make venv`` also registers the enviroment and library directory to your ~/.bash_profile.
This allows you to easily enter a development enviroment in terminal by typing: ::

   >>> env_libname-37

... where `libname` is the name of your lib and `37` is the python version of the venv.
This command is equivalent to: ::

   >>> cd /path/to/libname-py
   >>> source ~/venvs/libname-py-37/bin/activate

In order to use the new alias, you will need to refresh your current terminal session by
typing: ::

   >>> . ~/.bash_profile

5. Install the Dev Environment
------------------------------

islelib already comes pre-built with all the options and tools needed to write a generic
library. To install these tools into a python environment, type: ::

   >>> make install-dev

These tools include automation for building, versioning, testing and docing your new
library.

You will need to have Make installed on your machine. For OSX, you will be prompted
to install make through XCode when you attempt to run this command if it is not
already installed.

6. Initialize a new git repo
----------------------------

You should delete the existing ``.git`` folder for the repository, then initialize a
clean repo by typing: ::

   >>> git init

In the future, you may wish to cherry-pick commits / updates to this template into
your own libraries. A guide for how to do that can be found here:

[Guide needs to be written]

7. Register your library
------------------------

Please reference the relevant documentation for registering your library in Github,
Readthedocs, Azure Pipelines, etc. Links to relevant guides can be found below:

[Guides need to be written]

.. _writing:

Writing Your Library
====================

1. Style
--------

Illuscio's style guide is simple and straightforward:

   1. `Black`_ and `type hints`_ first
   2. `pep8`_ second
   3. When 1 & 2 contradict: see 1

While the writers of this guide may not agree with all opinions of these tools, there is
undeniable benefits to having a consistent, opinionated code style with automated tools.
From `Black's`_ documentation: ::

   By using Black, you agree to cede control over minutiae of hand-formatting. In
   return, Black gives you speed, determinism, and freedom from pycodestyle nagging
   about formatting. You will save time and mental energy for more important matters.

   Black makes code review faster by producing the smallest diffs possible. Blackened
   code looks the same regardless of the project you’re reading. Formatting becomes
   transparent after a while and you can focus on the content instead.

Black sits at the top of the hierarchy. For instance, black suggests line lengths do not
exceed 88 characters, where the default pep8 recommendation is 79. Illuscio code should
conform to the Black preference of 88 characters.

2. Lint
-------

To check the formatting of your library, type: ::

   >>> make lint

This will run the following tools to tell you where adjustments need to be made:

   * `flake8`_
   * `Black`_ (checking mode)
   * `MyPy`_

`flake8`_ and `Black`_ will both check your formatting and report any instances where
code does not conform to their respective standards. `Mypy`_ is a type checker and
reports instances where typing has been omitted or where type errors are detected,
which can help reduce bugs (ex: passing a known str to a function that only handles
ints).

These lint checks are also performed during deployment, and will cause failed code to
be kept from deploying to production.

3. Re-format
------------

Strict pep8 and Black adherence, while useful in many ways to the organization, can be
annoying and distracting to individual engineers. To help with this, the islelib
template comes with tools to re-format your code for you.

To re-format your code, type: ::

   >>> make format

This will run the following tools:

   * `autopep8`_
   * `Black`_

With these tools, keeping your code properly formatted is minimally invasive, and as an
organization will lead to a more consistent, maintainable codebase.

4. Test
-------

Tests are placed in ``zdevelop/tests``, and use the `pytest`_ library. To run your tests
type: ::

   >>> make test

... and watch the magic happen. This macro also creates coverage and error reports.
Coverage reports show what percentage of each file's code is tested. These reports can
be found in the following locations, and will be automatically opened in your default
browser once the tests complete:

   * results: ``zdevelop/tests/_reports/test_results.html``
   * coverage: ``zdevelop/tests/_reports/coverage/index.html``

Illuscio requires >= 85% code coverage in all files to publish a library. Libraries
with less than 85% coverage in any given file will be kicked back or will need to have
an exception granted.

Likewise, code will be tested upon deployment and kicked back in the case of failures.
The brief example tests in this library includes a failed test.

5. Document
-----------

islelib uses `Sphinx`_ to create it's documentation. To build docs for your new library,
type: ::

   >>> make doc

Docs will be generated at ``./zdocs/_build/index.html``. This command will also open
the newly created documentation in your default browser. islelib takes advantage of a
few specific sphinx plugins to:

   * automatically annotate types - types DO NOT need to be written in docstring to generate type annotations.
   * style docs with `readthedocs`_ theme

`Sphinx`_ offers a number of convenience features for auto-documenting code from
docstrings. Here is a brief example from a function in one of the make scripts:

.. autofunction:: zdevelop.make_scripts.make_name.edit_cfg

.. _deploying:

Deploying Your Library
======================

1. Make Commits:
----------------
Make your commits as you work

2. Version:
-----------

To version up your library, there are a few options depending on what part of the
``#.#.#`` version number you wish to increment. Islelib uses `bumpversion`_ to handle
its versioning, and as such, requires a clean commit before versioning up. Bumpverison
will also add and push gitlab tags upon versioning. Your library must be versioned up
in order to build. Builds without new versions will be rejected.

* 0.1.0 -> 0.1.1 ::

   >>> make version

* 0.1.1 -> 0.2.0 ::

   >>> make version-minor

* 0.2.0 -> 1.0.0 ::

   >>> make version-major

* 1.0.0 -> 0.0.0 ::

   >>> make version-reset

3. Push:
--------

When you are ready, push your code to github. This will set off a chain of events that
will:

   * automatically run formatting and unit tests
   * if tests are passed, build and push your library to be available to other developers
   * build new docs on Illuscio's readthedocs page

4. Build:
---------

islelib uses `Azure Pipelines`_ to automatically run builds, `Azure Artifacts`_ for
private pypi package hosting, and `readthedocs`_ to host documentation through github
webhooks.

Link: Illuscio `Python Package Pipeline`_ dashboard
Link: Illuscio `Python Azure Artifacts Feed`_
Link: Illuscio `readthedocs page`_

Azure Builds
############

Azure builds will only run on commits to the ``master`` branch or branches made with
Pull Requests.

When pushing to any applicable branch, Azure Pipelines will:

   * Lint the library in python 3.6 and 3.7. If `black`_, `mypy`_ or `flake8`_ throw an error, the build will fail.
   * Test the library in the above python versions on linux, mac, and windows using `pytest`_. Any failed tests will halt the build.
   * Check that test coverage exceeds 85%. If not, the build will fail.

When pushing to the ``master`` branch, azure will do the above, then also:

   * Build sdist and bdist_whl's through setuptools
   * Check that the version of library does not already exist in the `Python Azure Artifacts Feed`_. If it does, the build will fail.
   * Push these builds to illuscio's `Python Azure Artifacts Feed`_ using `twine`_.

All builds on azure also tag the github repository with their build number, so builds
can be easily pulled.

Readthedocs Builds
##################

Whenever a new commit is made to the ``master`` branch, `readthedocs`_ will execute a
new build of the documentation. This generation happens regardless of whether builds
pass in Azure, something which should eventually be fixed.

.. _qol:

Other Quality of Life Development Functions
===========================================

1. Clean Caches
---------------

``make clean`` will clear the following files from your library:

   * pytest cache
   * mypy cache
   * .coverage cache
   * ./build directory
   * ./dist directory
   * all .pyc files in the active directory tree
   * the ``build`` folder in ``./zdevelop/docs``
   * the ``.idea`` folder generated by pycharm to reset pycharm's cache


2. Scratch Folder
-----------------

The folder ``zdevelop/scratch`` is included in .gitignore, so you can store scratch work
to do quick tests in this directory without accidentally causing a commit conflict


.. web links:
.. _Github: https://github.com/
.. _Black: https://black.readthedocs.io/en/stable/
.. _Type Hints: https://mypy.readthedocs.io/en/latest/
.. _Pep8: https://www.python.org/dev/peps/pep-0008/?
.. _Black's: https://black.readthedocs.io/en/stable/
.. _flake8: https://pypi.org/project/flake8/
.. _Mypy: https://mypy.readthedocs.io/en/latest/
.. _autopep8: https://pypi.org/project/autopep8/
.. _pytest: https://docs.pytest.org/en/latest/
.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _readthedocs: https://readthedocs.com/
.. _bumpversion: https://github.com/peritus/bumpversion
.. _Azure Pipelines: https://azure.microsoft.com/en-us/services/devops/pipelines/
.. _PyPri: https://www.python-private-package-index.com/
.. _Azure Artifacts: https://azure.microsoft.com/en-us/services/devops/artifacts/
.. _Python Azure Artifacts Feed: https://dev.azure.com/illuscio/Python%20Packages/_packaging?_a=feed&feed=isle_pypi_libs
.. _Python Package Pipeline: https://dev.azure.com/illuscio/Python%20Packages/_build?definitionId=1
.. _readthedocs page: https://readthedocs.com/dashboard/
.. _twine: https://twine.readthedocs.io/en/latest/
