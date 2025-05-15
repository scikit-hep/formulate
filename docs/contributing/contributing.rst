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

   It's recommended to use a virtual environment for development (e.g., `venv`, `conda`, `uv` etc.):

4. **Install Development Dependencies**

   .. code-block:: bash

       pip install -e ".[dev]"

5. **Set Up Pre-commit Hooks**

   Formulate uses pre-commit hooks to ensure code quality:

   .. code-block:: bash

       pip install pre-commit
       pre-commit install

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

Coding Guidelines
-----------------------------

1. **Code Style**

   Formulate follows the PEP 8 style guide. The pre-commit hooks will help ensure your code adheres to this style.

2. **Documentation**

   - Document all public functions, classes, and methods using docstrings
   - Use type hints where appropriate
   - Update the documentation if you add new features or change existing ones

3. **Testing**

   - Write tests for all new features and bug fixes
   - Ensure all tests pass before submitting a pull request
   - Aim for high test coverage

4. **Commit Messages**

   - Write clear, concise commit messages
   - Start with a short summary line (50 chars or less)
   - Optionally, follow with a blank line and a more detailed explanation

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
