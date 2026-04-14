.. meta::
   :description: Orange3 Textable Prototypes documentation, TextDiff widget
   :keywords: Orange3, Textable, Prototypes, documentation, TextDiff, widget

.. _TextDiff:

TextDiff
=============

.. image:: figures/TextDiff.png

The goal of the TextDiff widget is to compare two texts of similar 
nature and to highlight de differences between the two.

Authors
-------
Ilana Senape, Valentin Armbruster, Nada Waly, Théo Esseiva, Alyssa Gheza.

Signals
-------
Inputs:
- ``TextField``
  TextField is a text type of widget, that perrmit us to import text data from keyboard input.
  TextField provide to the widget TextDiff the text data that it has to compare.
  TextDiff will need two TextField input to do a comparison.
- ``TextFile``
  TextFile is a text type of widget, that permit us to import data from raw text files and to normalise them.
  TextFile provide to the widget TextDiff the text data that it has to compare.
  TextDiff will need one or two TextFile to do a comparison.

  TextDiff can also accept one input TextField and one input TextFile to do a comparison.
Outputs: 
- ``DataTable``
  The DataTable widget displays attribute-value data in a spreadsheet, what permit the user to 
  visualy read the comparison done by TextDiff in the shape of a data table.

Description
-----------
Explain what the widget does and describe the interface section by section.

Section 1 (e.g., Source)
~~~~~~~~~~~~~~~~~~~~~~~~
- Control A: ...
- Control B: ...

Section 2 (e.g., Options)
~~~~~~~~~~~~~~~~~~~~~~~~~
- ...

Send / Auto-send
~~~~~~~~~~~~~~~~
Explain briefly how **Send** and **Send automatically** work in this widget.

Messages
--------
Information
~~~~~~~~~~~
*<main success message>*
Explain what it means.

Warnings
~~~~~~~~
*<warning 1>*
Explain cause and fix.

Errors
~~~~~~
*<error 1>*
Explain cause and fix.