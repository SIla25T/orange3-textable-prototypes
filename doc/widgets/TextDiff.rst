.. meta::
   :description: Orange3 Textable Prototypes documentation, TextDiff widget
   :keywords: Orange3, Textable, Prototypes, documentation, TextDiff, widget

.. _TextDiff:

TextDiff
=============

.. image:: Text_Diff.png

The TextDiff widget compares two versions of the same text — such as different translations of a single work — and highlights the differences.

Authors
-------
Ilana Senape, Valentin Armbruster, Nada Waly, Théo Esseiva, Alyssa Gheza.


Signals
-------

Inputs:

- TextField: 

  TextField widget enables manual text entry. It supplies the TextDiff widget with the text data to bbe compared. TextDiff requires two inputs (TextField or TextFile) to perform a comparison.

- TextFile: 
  TextFile widget imports and normalizes data from raw text files. It supplies the TextDiff widget with the text data to be compared. 
  TextDiff needs two TextFile to do a comparison.

  TextDiff can accept two TextFields, two TextFiles or one of each as input to perform a comparison.

Outputs: 

- DataTable:
  The DataTable widget presents attribute-value data in a spreadsheet format, allowing users to visualize the differences identified by TextDiff.




Description
-----------

This widget aims to compare two text inputs from the same source (e.g., two versions of a document) and visualize the differences between them in a data table. 
Text_Diff supports any language, provided both inputs share the same language. It is compatible with any text genre (e.g., news articles, scientific papers, etc.) as long as the compared documents are of the same nature. 
It takes two text files or two text fields (or a combination of both) as input and outputs a datatable visualization of the divergences. 

Inputs
~~~~~~~~~~~~~~~~~~~~~~~~
.. _text_diff_fig1: 
.. figure:: figures/TextDiff_Basic.png
    :align: center
    :alt: inputs of the Text Diff widget
    Figure 1: **Text Diff** widget (inputs).

The **inputs** section allows the user to connect two text sources (Text Files or Text Fields) to compare. The widget will only activate if both inputs are connected. 

Interface 
~~~~~~~~~~~~~~~~~~~~~~~~
The **Text Diff** widget allows the user to compare two text inputs and visualize the differences between them in a data table.

.. _text_diff_fig2: 
.. figure:: figures/TextDiff_Basic.png
    :align: center
    :alt: Basic interface of the Text Diff widget

    Figure 2: **Text Diff** widget.


The **segmentation** section allows the user to choose the level of segmentation for the comparison (e.g., word or sentence). The default segmentation is at the word level.

The **status bar** displays a summary of the emitted output, showing the number of segments emitted and the number of differences identified between the two texts. It also indicates if the widget is ready to emit an output (e.g., if both inputs are connected and contain valid data).

The **options** section allows the user to customize the comparison and visualization of differences. For example, the user can set a similarity threshold for the segments.

The **info** section details the reasons why no output is emitted (e.g., no inputs connected, empty file, etc.).

Output
~~~~~~~~~~~~~~~~~~~~~~~~
.. _text_diff_fig3: 
.. figure:: figures/TextDiff_output.png
    :align: center
    :alt: Output of the Text Diff widget
    Figure 3: **Text Diff** widget (output).

The **data table** displays the differences between the two sources, including columns for the type of difference, the source segment and the target segment. The comparison relies on the difflib library, which segments the texts and identifies discrepancies. The possible types of differences are:

- Equal : the text segments are identical in both inputs.
- Replace: the text segments differ in both inputs (e.g., a word is replaced by another).The source segment is marked as "replace". 
- Insert: the text segment is present in the target input but not in the source input. The source segment is marked as "insert".
- Delete: the text segment is present in the source input but not in the target input. The source segment is marked as "delete".

The first row of the table shows the degree of similarity between the two texts (where 0% indicates no similarities and 100% indicates the two texts are identical). 

Messages
--------

Information
~~~~~~~~~~~
* **<N> diff lines sent to output**
  Indicates that the text comparison was successful and the results have been successfully emitted to the next widget.

Warnings
~~~~~~~~
**Texts are radically different**:
Occurs when the two connected texts have little to no overlap (e.g., comparing two completely unrelated books). The widget will still process the data, but the output will mostly consist of large "delete" and "insert" blocks rather than nuanced "replace" or "equal" segments.

*Fix:* Ensure that the texts you are comparing are indeed different versions of the same source (e.g., two translations of the same work, or two editions of a book). If you are trying to compare two completely different texts, consider using a different widget designed for that purpose.

Errors
~~~~~~

* **Not enough inputs**
  Occurs when fewer than the required number of text sources are connected. 
  *Fix:* Ensure you have connected valid text sources. The widget strictly requires two text inputs to perform a comparison.

* **Too many inputs**
  Occurs if more than two text sources are connected to the widget. 
  *Fix:* The Text Diff widget can only compare two texts side-by-side. Disconnect any extra inputs.

* **Invalid input type**
  Occurs when a connected widget sends data that is not recognized as text. 
  *Fix:* Ensure you are strictly connecting widgets that output valid text data (such as **Text File** or **Text Field**).
