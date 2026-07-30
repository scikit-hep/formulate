Contributing to Formulate
=======================================

Thank you for your interest in contributing to Formulate! This guide will help you get started with contributing to the project.

Setting Up Your Development Environment
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

1. **Fork the Repository**

   Start by forking the `Formulate repository <https://github.com/scikit-hep/formulate>`_ on GitHub.

2. **Clone Your Fork**

   .. code-block:: bash

       git clone https://github.com/YOUR-USERNAME/formulate.git
       cd formulate

3. **Set Up a Virtual Environment**

   It's recommended to use a virtual environment for development (e.g.
   ``venv``, ``conda``, ``uv``, etc.):

   .. code-block:: bash

       python -m venv .venv
       source .venv/bin/activate   # .venv\Scripts\activate on Windows

4. **Install Development Dependencies**

   .. code-block:: bash

       pip install -e ".[dev]"

   The ``dev`` extra pulls in the test and docs requirements plus ``prek``.
   ``.[test]`` on its own is enough to run the whole suite; ``.[docs]`` on its
   own is enough to build the documentation.

5. **Set Up Pre-commit Hooks**

   Formulate uses pre-commit hooks to ensure code quality. They are run with
   `prek <https://github.com/j178/prek>`_, a faster drop-in replacement for
   ``pre-commit`` that reads the same ``.pre-commit-config.yaml``. It is
   installed by the ``dev`` extra above, so you only need to install the hooks:

   .. code-block:: bash

       prek install

   To run all the hooks against every file without making a commit:

   .. code-block:: bash

       prek run --all-files

Development Workflow
----------------------------------------------

1. **Create a Branch**

   Create a new branch for your feature or bugfix:

   .. code-block:: bash

       git checkout -b feature-or-bugfix-name

2. **Make Your Changes**

   Implement your feature or fix the bug. Be sure to:

   - Follow the coding style of the project
   - Add tests for your changes
   - Update documentation if necessary

3. **Run Tests**

   Make sure all tests pass:

   .. code-block:: bash

       pytest

   A few useful variations:

   .. code-block:: bash

       pytest tests/test_root.py            # one file
       pytest -k tmath_min                  # one test, by name
       pytest --cov=formulate --cov-branch  # with coverage

   Note that ``tests/test_constants.py`` evaluates expressions with the real
   engines and skips the ROOT half unless ROOT is importable, which CI only
   arranges on one job. Everything else runs everywhere.

4. **Commit Your Changes**

   Commit your changes with a descriptive commit message:

   .. code-block:: bash

       git add .
       git commit -m "Add feature X" or "Fix bug Y"

5. **Push Your Changes**

   Push your changes to your fork:

   .. code-block:: bash

       git push origin feature-or-bugfix-name

6. **Create a Pull Request**

   Go to the `Formulate repository <https://github.com/scikit-hep/formulate>`_ and create a pull request from your branch.

Using nox
----------------------------------------------

`nox <https://nox.thea.codes/>`_ runs each task in its own isolated
environment, which is what CI does and is the quickest way to reproduce a CI
failure locally. It needs no setup beyond ``pipx install nox``:

.. code-block:: bash

    nox                       # the default: lint, pylint and tests
    nox -s tests              # just the tests
    nox -s coverage           # tests, with coverage measured
    nox -s lint               # all the pre-commit hooks
    nox -s docs               # build the documentation
    nox -s docs -- --serve    # build it and serve it at localhost:8000

Coding Guidelines
-----------------------------

1. **Code Style**

   Formulate follows the PEP 8 style guide, enforced by ``ruff``. The hooks
   installed above take care of the formatting for you; ``mypy`` also runs over
   ``src`` in strict mode, so new code needs to be fully typed.

2. **Documentation**

   - Document all public functions, classes, and methods using docstrings.
     They are what the :doc:`../api/api` pages are built from.
   - Update the narrative documentation when you add or change a feature. In
     particular, ``docs/guide/expressions.rst`` lists every supported function
     and constant, and ``docs/guide/issues.rst`` is the reference for the
     places where the languages disagree — both should stay in step with the
     code.
   - Examples in the docs are executed when the docs are built, so an example
     that has gone stale will show up as a failed build rather than as wrong
     output on the website.

3. **Testing**

   - Write tests for all new features and bug fixes
   - Coverage is enforced at 100% for both the project and the diff, so a new
     branch needs a test that reaches it. Genuinely unreachable code is marked
     ``# pragma: no cover``; if a branch cannot be reached, consider whether it
     should exist at all.
   - Warnings are errors in the test suite, so anything that starts warning
     will fail

4. **Commit Messages**

   - Write clear, concise commit messages
   - Start with a short summary line (50 chars or less)
   - Optionally, follow with a blank line and a more detailed explanation

Adding a function or a constant
------------------------------------------------

This is the most common kind of contribution, and it is mostly table editing.
In ``src/formulate/identifiers.py``:

1. Add the canonical name to ``FUNCTIONS`` or ``CONSTANTS``. This name is
   internal — it is what appears in the AST — so it should not be any one
   language's spelling. The NumPy-style name is the usual choice.
2. Add an entry to each backend's map (``ROOT_FUNCTIONS``,
   ``NUMEXPR_FUNCTIONS``, ``PYTHON_FUNCTIONS``, and the ``*_CONSTANTS``
   equivalents) for the languages that support it. Leaving it out of a map is
   how "not supported here" is expressed; the conversion will then raise a
   clear ``ValueError`` rather than emitting something wrong.
3. Add any other spellings people might write to ``FUNCTION_ALIASES``,
   ``CONSTANTS_ALIASES`` or ``CONSTANTS_FUNCTION_ALIASES``.

``tests/test_identifiers.py`` drives every entry in these tables through the
parser and cross-checks the tables against each other, so a name that is
declared but not mapped — or mapped but not declared — fails loudly.

Finally, add the new name to the tables in ``docs/guide/expressions.rst``,
which is where users look for what is supported.

Types of Contributions
------------------------------------------------

There are many ways to contribute to Formulate:

1. **Bug Reports**

   If you find a bug, please report it by creating an issue on GitHub. Include:

   - A clear description of the bug
   - Steps to reproduce the bug
   - Expected behavior
   - Actual behavior
   - Any relevant logs or error messages

2. **Feature Requests**

   If you have an idea for a new feature, create an issue on GitHub describing:

   - What the feature would do
   - Why it would be useful
   - How it might be implemented

3. **Documentation Improvements**

   Help improve the documentation by:

   - Fixing typos or errors
   - Clarifying explanations
   - Adding examples
   - Translating documentation

4. **Code Contributions**

   Contribute code by:

   - Fixing bugs
   - Implementing new features
   - Improving performance
   - Refactoring code

5. **Reviewing Pull Requests**

   Help review pull requests by:

   - Testing the changes
   - Reviewing the code
   - Providing constructive feedback
