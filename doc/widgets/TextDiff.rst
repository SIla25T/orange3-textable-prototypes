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

This widget aims to compare two text inputs from the same source (e.g., two versions of a document) and visualize the differences between them in a data table. Text_Diff supports any language as long as the inputs are in the same language and can be used for any type of text forasmuch as they share the same type (e.g., news articles, scientific papers, etc.). It takes a text file or a text field as input and outputs a visualization of the differences. 


Basic Interface 
~~~~~~~~~~~~~~~~~~~~~~~~
in it's basic version (see :ref:`figure 1 <text_diff_fig1>`), the **Text Diff** widget allows the user to compare two text inputs and visualize the differences between them in a data table.

.. _text_diff_fig1: 
.. figure:: figures/TextDiff_Basic.png
    :align: center
    :alt: Basic interface of the Text Diff widget

    Figure 1: **Text Diff** widget (basic interface).


The **inputs** section allows the user to connect two text sources (Text Files or Text Fields) to compare. The widget will only activate if both inputs are connected. 


 The **data table** displays the the differences between the two texts, with columns for the type of difference, the source segment, the target segment, and their respective locations in the text. The comparison is based on the difflib library, which segments the texts and identifies the differences. The possible types of differences are:

- Equal : the text segments are identical in both inputs.
- Replace: the text segments are different in both inputs (e.g., a word is replaced by another).The source segment is marked as "replace" and the target segment is marked as "replace" as well.
- Insert: the text segment is present in the target input but not in the source input. The source segment is marked as "insert" and the target segment is marked as "equal" (if it is identical to a segment in the source input) or "replace" (if it is different from all segments in the source input).
- Delete: the text segment is present in the source input but not in the target input. The source segment is marked as "delete" and the target segment is marked as "equal" (if it is identical to a segment in the source input) or "replace" (if it is different from all segments in the source input).

The **Send** button triggers the emission of a segmentation to the output connection(s). When it is selected, the **Send automatically** checkbox disables the button and the widget attempts to automatically emit a segmentation at every modification of its interface.

Advanced Interface
~~~~~~~~~~~~~~~~~~~~~~~~

The **options** section allows the user to customize the comparison and visualization of differences. For example, the user can set a threshold for similarity between segments.

The **info** section indicates the reasons why no output is emitted (e.g., no inputs connected, empty file, etc.).

The  **Send** button and **Send automatically**, operate in the same way as in the basic interface.



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

# si les inputs sont incorectes : 
  #1 il n'y en a pas assez / trop (0/1 TextField ou 3/+) 
   # inputs accepter = 1 textFile / 1 TextFile + 1 TextField / 2 TextField
  #2 si ils sont du mauvais type (pas un textFile ou un TextField)
# si les deux textes sont radicalement differents ? 
