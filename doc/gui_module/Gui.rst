Gui module
^^^^^^^^^^
This is the entry point for our application, it is mainly:

1. Create a wx application object.
2. Instantiate the controller.
    * The controller internally will instantiate the necessary model(s) and the main view.
3. Start the event loop.

.. code-block:: ../../gui/gui.py
