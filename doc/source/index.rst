PartsGenie's Documentation
==========================

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
############

.. _RetroRules: https://retrorules.org/
.. _RetroPath2.0: https://github.com/Galaxy-SynBioCAD/RetroPath2
.. _rp2paths: https://github.com/Galaxy-SynBioCAD/rp2paths
.. _rpSBML: https://github.com/Galaxy-SynBioCAD/rpBase
.. _rpBase: https://github.com/Galaxy-SynBioCAD/rpBase
.. _rpCache: https://github.com/Galaxy-SynBioCAD/rpCache
.. _rpVisualiser: https://github.com/brsynth/rpVisualiser
.. _rpSelenzyme: https://github.com/brsynth/rpSelenzyme
.. _SBOL: https://sbolstandard.org/
.. _doebase: https://github.com/pablocarb/doebase
.. _PartsGenie: https://github.com/neilswainston/PartsGenie-legacy

Welcome to PartsGenie's documentation. This tool provides a docker that calls a PartsGenie_ REST service.

.. code-block:: bash

   docker build -t brsynth/partsgenie-standalone .

You can run the docker using the following command:

.. code-block:: bash

   python run.py -input test/input.sbol -input_format sbol -taxonomy_input 8333 taxonomy_format string -output test/test_output.sbol

API
###

.. currentmodule:: run

.. autoclass:: main
    :show-inheritance:
    :members:
    :inherited-members:
