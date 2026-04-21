"""
Ce widget compare deux segmentations de texte (par exemple, des mots ou des phrases) et génère une table de différences entre les deux textes. Il utilise la bibliothèque difflib pour calculer les différences et crée une table Orange avec les segments comparés et leur type de changement (égal, remplacé, supprimé, inséré). L'utilisateur peut choisir le type de segmentation à comparer (mots ou phrases) et le widget gère automatiquement l'envoi des données de sortie lorsque les entrées changent.

Source de la fonction detectInputLanguage : widget transletto
"""

__version__ = "0.0.2"

import re
import difflib
import numpy as np

import LTTL.Segmenter as Segmenter
from LTTL.Segmentation import Segmentation
from LTTL.Input import Input

from Orange.data import Table, Domain, StringVariable, DiscreteVariable
from Orange.widgets import gui, settings
from Orange.widgets.utils.widgetpreview import WidgetPreview
from langdetect import detect
import json
import os
import inspect

from _textable.widgets.TextableUtils import (
    OWTextableBaseWidget,
    VersionedSettingsHandler,
    ProgressBar,
    InfoBox,
    SendButton,
    pluralize,
)


class TextDiff(OWTextableBaseWidget):
    """Orange3-Textable widget for comparing two texts. Name : Text Diff"""

    name = "Text Diff"
    description = "Compare two segmentations and output their differences."
    icon = "icons/Text_Diff.png"
    priority = 38

    inputs = [ #déclare la structure officielle du widget : inputs, ouputs, son interface, et les paramètres sauvegardés.
        ("Segmentation A", Segmentation, "inputDataA"),
        ("Segmentation B", Segmentation, "inputDataB"),
    ]
    outputs = [
        ("Diff data", Table),   #output de type Table, qui sera affiché dans un Data Table.
    ]

    want_main_area = False

    settingsHandler = VersionedSettingsHandler(
        version=__version__.rsplit(".", 1)[0]
    )

    # Widget settings that will be saved and restored
    selectedSegmentationType = settings.Setting("words")
    autoSend = settings.Setting(False)

    def __init__(self, *args, **kwargs): #création de l'intérface grahique du widget.
        super().__init__(*args, **kwargs)

        # Initialize attributes
        self.inputSegmentationA = None
        self.inputSegmentationB = None
        self.outputTable = None
        self.createdInputs = []

        # Path to the JSON file containing available languages and translators
        path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        # Load the available languages and translators from the JSON file
        try:
            with open(os.path.join(path, "translate_data.json"), "r") as file:
                self.available_languages_dict = json.load(file)
        # Else show error message
        except IOError:
            print("Failed to open json file.")
        # GUI elements for input language selection        
        optionsBoxInput = gui.widgetBox(
            widget=self.controlArea,
            box=u'Input language',
            orientation='vertical',
            addSpace=True,
        )
        self.testBox1 = gui.widgetBox(
            widget=optionsBoxInput,
            orientation='horizontal',
        )
        #Générer les listes des Traducteurs et Languages à être affichés au départ
        self.GenerateTranslatorLanguageList()
        gui.button(
            widget=self.testBox1,
            master=self,
            label=u'Detect the language',
            callback=self.detectInputLanguage,
            tooltip=("Auto-detect language"),
        )

        # UI Components
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute="infoBox",
        )

        # Options section for segmentation type
        optionsBox = gui.widgetBox(
            widget=self.controlArea,
            box="Segmentation type",
            orientation="vertical",
            addSpace=True,
        )
        gui.comboBox(
            widget=optionsBox,
            master=self,
            value="selectedSegmentationType",
            label="Select a segmentation type:",
            items=["words", "sentences"],
            sendSelectedValue=True,
            callback=self.sendButton.settingsChanged,
            tooltip="words: words\nsentences: sentences",
        )

        # Build the UI
        gui.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()

        # Attempt to send data immediately if autoSend is enabled
        self.sendButton.sendIf()

    def inputDataA(self, newInput): #méthodes d'entrée des données A, appelées automatiquement par Orange quand une nouvelle donnée arrive sur les inputs du widget.
        self.inputSegmentationA = newInput
        self.infoBox.inputChanged()
        self.sendButton.sendIf()
        self.detectInputLanguage()
        print("input data A ok")

    def inputDataB(self, newInput): #méthodes d'entrée des données, appelées automatiquement par Orange quand une nouvelle donnée arrive sur les inputs du widget.
        self.inputSegmentationB = newInput
        self.infoBox.inputChanged()
        self.sendButton.sendIf()
        self.detectInputLanguage()
        print("input data B ok")

    def clearCreatedInputs(self):#méthode pour nettoyer les inputs créés, en les supprimant de la segmentation.
        for i in self.createdInputs:
            Segmentation.set_data(i[0].str_index, None)
        del self.createdInputs[:]
    
    #---------------------------------------------
    fonction detectInputLanguage tests
    #---------------------------------------------

    # pour détecter la langue de l'input
    # faudrait trouver un moyen d'appliquer cette fonction à A et B
    # soit séparément (=faire une fonction générale et une classe Inputsegmentation générale) et faire une 2ème fonction pour check si les inputs sont dans la même langue
    # soit aux deux en même temps et comparer dans la fonction si c'est bien la même langue ou pas (-> message error : pas la même langue)
    def detectInputLanguage(self, newInput):
        """Auto-detect input language"""
        text = newInput[0].get_content()
        # fonction detect est importer depuis la libraire detectlang
        lang_detect_language = detect(text)

        for key, value in self.available_languages_dict["GoogleTranslator"]["lang"].items():
            if lang_detect_language == value:
                self.detectedInputLanguage = key
                print(f"lang_detect: {lang_detect_language}")
                self.inputLanguageKey = self.detectedInputLanguage
                return
        self.infoBox.setText(
                "Language not recognized",
                "warning"
            )
        return

    #---------------------------------------------

    def onDeleteWidget(self):#méthode appelée automatiquement par Orange quand le widget est supprimé, pour nettoyer les inputs créés.
        self.clearCreatedInputs()

    def setCaption(self, title):#méthode pour changer le titre du widget, en vérifiant si le titre a changé pour éviter de déclencher des recalculs inutiles.
        if "captionTitle" in dir(self):
            changed = title != self.captionTitle
            super().setCaption(title)
            if changed:
                self.sendButton.settingsChanged()
        else:
            super().setCaption(title)

    def extract_text(self, segmentation):#méthode pour extraire le texte d'une segmentation, en concaténant les contenus de tous les segments, et en gérant les exceptions au cas où un segment ne contiendrait pas de texte.
        if not segmentation:
            return ""

        contents = []
        for segment in segmentation:
            try:
                contents.append(segment.get_content())
            except Exception:
                pass

        return " ".join(contents).strip()

    def segment_text(self, text):#méthode pour segmenter un texte en fonction du type de segmentation sélectionné (mots ou phrases), en utilisant des expressions régulières pour extraire les segments, et en gérant les cas où le texte serait vide ou None.
        if text is None:
            return []

        text = str(text).strip()
        if not text:
            return []
        
        # Tokenize by words (including accented characters and hyphens)
        if self.selectedSegmentationType == "words":
            return re.findall(r"\b[\wÀ-ÿ'-]+\b", text, flags=re.UNICODE)
        
        # Tokenize by sentences (splitting on punctuation followed by space)
        if self.selectedSegmentationType == "sentences":
            parts = re.split(r"(?<=[.!?])\s+", text)
            return [part.strip() for part in parts if part.strip()]

        return []

    def expand_opcode(self, tag, a_chunk, b_chunk):#méthode pour transformer les opcodes de difflib en lignes de diff détaillées, en gérant les différents types d'opérations (equal, delete, insert, replace) et en créant des lignes de diff pour chaque segment concerné.
        rows = []

        if tag == "equal":#pour les segments égaux, on crée une ligne de diff pour chaque segment correspondant dans les deux textes.
            for a_seg, b_seg in zip(a_chunk, b_chunk):
                rows.append((a_seg, b_seg, "equal"))
            return rows

        if tag == "delete":#pareil pour delete.
            for a_seg in a_chunk:
                rows.append((a_seg, "", "delete"))
            return rows

        if tag == "insert":#pareil pour insert.
            for b_seg in b_chunk:
                rows.append(("", b_seg, "insert"))
            return rows

        if tag == "replace":#pour les segments remplacés, on utilise un SequenceMatcher secondaire pour comparer les segments concernés et créer des lignes de diff plus détaillées, en gérant les cas où les segments n'ont pas la même longueur.
            submatcher = difflib.SequenceMatcher(None, a_chunk, b_chunk)
            for subtag, si1, si2, sj1, sj2 in submatcher.get_opcodes():#
                sub_a = a_chunk[si1:si2]
                sub_b = b_chunk[sj1:sj2]

                if subtag == "equal":#pour les segments égaux, on crée une ligne de diff pour chaque segment correspondant dans les deux textes.
                    for a_seg, b_seg in zip(sub_a, sub_b):
                        rows.append((a_seg, b_seg, "equal"))

                elif subtag == "delete":#pareil pour delete.
                    for a_seg in sub_a:
                        rows.append((a_seg, "", "delete"))

                elif subtag == "insert":#pareil pour insert.
                    for b_seg in sub_b:
                        rows.append(("", b_seg, "insert"))

                elif subtag == "replace":
                    max_len = max(len(sub_a), len(sub_b))
                    for i in range(max_len):
                        a_seg = sub_a[i] if i < len(sub_a) else ""
                        b_seg = sub_b[i] if i < len(sub_b) else ""
                        rows.append((a_seg, b_seg, "replace"))

            return rows

        return rows

    def build_diff_rows(self, seg_a, seg_b):#construction des lignes de diff à partir des segments des deux textes.
        matcher = difflib.SequenceMatcher(None, seg_a, seg_b)
        rows = []

        # Iterate through the sequence of changes identified by difflib
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            a_chunk = seg_a[i1:i2]
            b_chunk = seg_b[j1:j2]
            rows.extend(self.expand_opcode(tag, a_chunk, b_chunk))

        return rows

    def build_output_table(self, rows):#construction de la table de sortie à partir des lignes de diff.
        change_var = DiscreteVariable(
            "change_type",
            values=["equal", "replace", "delete", "insert"]
        )

        # Define the meta attributes (strings)
        metas = [
            StringVariable("segment_A"),
            StringVariable("segment_B"),
            StringVariable("diff_line"),
        ]

        # Construct the Orange Domain
        domain = Domain(
            attributes=[],
            class_vars=[change_var],
            metas=metas,
        )

        y = [] # List for class variable values
        m = []# List for meta string values

        for a, b, tag in rows:#pour chaque ligne de diff, on ajoute une valeur à la variable de changement (y) et une ligne de métadonnées (m) avec les segments comparés et le type de changement.
            y.append([change_var.values.index(tag)])
            m.append([
                str(a),
                str(b),
                f"[{tag}] A: {a} | B: {b}",
            ])

        # Convert to numpy arrays (Orange requires 2D numpy arrays for tables)
        X = np.empty((len(rows), 0))
        Y = np.array(y, dtype=float) if y else np.empty((0, 1))
        M = np.array(m, dtype=object) if m else np.empty((0, 3), dtype=object)

        table = Table.from_numpy(domain, X=X, Y=Y, metas=M)
        table.name = self.captionTitle if hasattr(self, "captionTitle") else "Text Diff"
        return table

    def sendData(self):#méthode pour envoyer les données de diff, en vérifiant que les deux segmentations d'entrée sont présentes, en extrayant et segmentant les textes, en construisant les lignes de diff, en créant la table de sortie, et en gérant les exceptions éventuelles.
        if not self.inputSegmentationA or not self.inputSegmentationB:
            self.infoBox.setText("Widget needs 2 inputs.", "warning")
            self.send("Diff data", None)
            return
        
        # Disable UI during processing
        self.controlArea.setDisabled(True)

        # Extract and segment text from both inputs
        text_a = self.extract_text(self.inputSegmentationA)
        text_b = self.extract_text(self.inputSegmentationB)

        seg_a = self.segment_text(text_a)
        seg_b = self.segment_text(text_b)

        # Compute differences
        rows = self.build_diff_rows(seg_a, seg_b)

        # Initialize progress bar
        progressBar = ProgressBar(self, iterations=max(len(rows), 1))

        try:
            for _ in rows:
                progressBar.advance()

            # Build output Orange Table
            self.outputTable = self.build_output_table(rows)

            # Compute statistics for the UI InfoBox
            nb_equal = sum(1 for _, _, tag in rows if tag == "equal")
            nb_replace = sum(1 for _, _, tag in rows if tag == "replace")
            nb_delete = sum(1 for _, _, tag in rows if tag == "delete")
            nb_insert = sum(1 for _, _, tag in rows if tag == "insert")

            message = (
                "%i diff line@p sent to output "
                "(equal: %i, replace: %i, delete: %i, insert: %i)."
                % (len(rows), nb_equal, nb_replace, nb_delete, nb_insert)
            )
            message = pluralize(message, len(rows))
            self.infoBox.setText(message)

            # Finish processing
            progressBar.finish()
            self.controlArea.setDisabled(False)

            # Emit the data
            self.send("Diff data", self.outputTable)
            self.sendButton.resetSettingsChangedFlag()

        except Exception as exc:
            # Handle and display any errors that occur during processing
            self.infoBox.setText(f"Diff failed: {exc}", "error")
            self.controlArea.setDisabled(False)
            self.send("Diff data", None)


if __name__ == "__main__":#code de test pour prévisualiser le widget avec des données d'exemple, en créant deux segmentations à partir de textes différents et en les envoyant au widget.
    input1 = Input("Bonjour tout le monde.")
    input2 = Input("Bonjour tout le joli monde.")

    seg1 = Segmenter.concatenate([input1], label="A")
    seg2 = Segmenter.concatenate([input2], label="B")

    WidgetPreview(TextDiff).run(inputDataA=seg1, inputDataB=seg2)