============================
Specification and test cases
============================

The test-set is based on the requirements document developed in the Beter
Benutten MMRI project. The document contains an informal set of requirements,
which this project aims to formalize and test.


Specification
=============

The test specification is the formalization of the requirements. The document
is written in LaTeX_ and can be found under :file:`specs/testset.tex`. Every
requirement is tested as one or more test cases. A test case is defined by a
transit graph, a list of planning requests and the expected results.

.. _LaTeX: http://www.latex-project.org/


Building the specification document
-----------------------------------

You will need a copy of LaTeX on your system. Most Linux distributions carry
LaTeX packages in their repository. For Windows and Mac OS X, please see the
`download page`_.

You will also need the following packages from CTAN_. (Again, most Linux
distributions will carry these packages in either their base or an optional
LaTeX package.)

* colortbl_
* enumitem_
* pgf_
* `easy-todo`_

Build a PDF document from the LaTeX source by executing this command in the
:file:`specs` directory:

.. code-block:: console

    pdflatex testset.tex

You may have to run this command multiple times to correctly generate
references.

.. _`download page`: http://latex-project.org/ftp.html
.. _CTAN: http://ctan.org/
.. _colortbl: http://ctan.org/pkg/colortbl
.. _enumitem: http://ctan.org/pkg/enumitem
.. _pgf: http://ctan.org/pkg/pgf
.. _`easy-todo`: http://ctan.org/pkg/easy-todo


Test cases
==========

Test cases are implemented using :term:`GTFS` and :term:`GTFS-RT` datasets. 
