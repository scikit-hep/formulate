Ask a Question
====================

If you have questions about using Formulate, this page provides guidance on where and how to ask for help.

Where to Ask Questions
------------------------------------------------

Depending on the nature of your question, there are several channels available:

GitHub Discussions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For general questions about using Formulate, feature requests, or to share your experience:

* Visit the `Formulate GitHub Discussions <https://github.com/scikit-hep/formulate/discussions>`_
* Create a new discussion in the appropriate category (Q&A, Ideas, Show and Tell, etc.)
* Be sure to check existing discussions first to see if your question has already been answered

GitHub Issues
~~~~~~~~~~~~~~~~~~~~~~

For bug reports or specific technical issues:

* Check the `existing issues <https://github.com/scikit-hep/formulate/issues>`_ to see if your problem has already been reported
* If not, create a `new issue <https://github.com/scikit-hep/formulate/issues/new>`_ with details about your problem
* Include information about your environment, steps to reproduce, and any error messages

Elsewhere in Scikit-HEP
~~~~~~~~~~~~~~~~~~~~~~~

If your question is really about the tool at the other end of the conversion —
how ``TTreeFormula`` evaluates something, or what numexpr does with a
particular dtype — that project's own issue tracker will get you a better
answer. The `Scikit-HEP <https://scikit-hep.org/>`_ website lists the packages
in the ecosystem and where each is discussed.

How to Ask Effective Questions
------------------------------------------------------------------------------------------------------------------------------------------

To get the best help possible, consider these tips when asking questions:

1. **Be Specific**

   Clearly state what you're trying to accomplish and where you're stuck. Instead of "Formulate isn't working," try "I'm trying to convert this ROOT expression to numexpr and getting this specific error."

2. **Include Context**

   Provide relevant information about your environment:

   * Formulate version
   * Python version
   * Operating system
   * Any other relevant packages and their versions

3. **Show Minimal Examples**

   Include the smallest possible code example that demonstrates your issue —
   the expression that fails, and what you expected instead:

   .. jupyter-execute::

       import formulate

       # This converts fine
       print(formulate.from_root("x + y").to_numexpr())

       # This does not, and here is what it says
       try:
           formulate.from_root("arr[0]").to_numexpr()
       except ValueError as error:
           print(error)

   Reducing a long expression to the part that misbehaves is usually the step
   that answers the question by itself.

4. **Include Full Error Messages**

   If you're encountering an error, include the complete error message with
   traceback. Formulate's parse errors carry a location and often a
   suggestion, and both are useful:

   .. jupyter-execute::

       try:
           formulate.from_root("a & b")
       except formulate.ParseError as error:
           print(error)

5. **Describe What You've Tried**

   Mention approaches you've already attempted to solve the problem.

6. **Be Patient and Respectful**

   Remember that most help comes from volunteers. Be patient waiting for responses and respectful of people's time.

Common Questions
----------------------------

Before asking, check if your question is answered in one of these resources:

* :doc:`../quickstart/introduction` - For basic information about Formulate
* :doc:`../guide/expressions` - For details on supported expressions
* :doc:`../guide/issues` - For common issues and their solutions
* :doc:`../api/api` - For API documentation

Getting Involved
----------------------------

If you find yourself frequently answering questions about Formulate, consider getting more involved with the project:

* Help improve the documentation
* Contribute code fixes
* Join the development team

See the :doc:`../contributing/contributing` page for more information on how to contribute.
