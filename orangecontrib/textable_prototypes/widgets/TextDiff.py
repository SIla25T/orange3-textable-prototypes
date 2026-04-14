"""
Class OWTextableTextDiff
"""

__version__ = "0.0.1"

import re
import difflib
import numpy as np

import LTTL.Segmenter as Segmenter
from LTTL.Segmentation import Segmentation
from LTTL.Input import Input

from Orange.data import Table, Domain, StringVariable, DiscreteVariable
from Orange.widgets import gui, settings
from Orange.widgets.utils.widgetpreview import WidgetPreview

from _textable.widgets.TextableUtils import (
    OWTextableBaseWidget,
    VersionedSettingsHandler,
    ProgressBar,
    InfoBox,
    SendButton,
    pluralize,
)


class TextDiff(OWTextableBaseWidget):
    """Orange3-Textable widget for comparing two texts."""

    name = "Text Diff"
    description = "Compare two segmentations and output their differences."
    icon = "icons/Text_Diff.png"
    priority = 38

    inputs = [
        ("Segmentation A", Segmentation, "inputDataA"),
        ("Segmentation B", Segmentation, "inputDataB"),
    ]
    outputs = [
        ("Diff data", Table),   # <- IMPORTANT
    ]

    want_main_area = False

    settingsHandler = VersionedSettingsHandler(
        version=__version__.rsplit(".", 1)[0]
    )

    selectedSegmentationType = settings.Setting("words")
    autoSend = settings.Setting(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inputSegmentationA = None
        self.inputSegmentationB = None
        self.outputTable = None
        self.createdInputs = []

        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute="infoBox",
        )

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

        gui.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()

        self.sendButton.sendIf()

    def inputDataA(self, newInput):
        self.inputSegmentationA = newInput
        self.infoBox.inputChanged()
        self.sendButton.sendIf()

    def inputDataB(self, newInput):
        self.inputSegmentationB = newInput
        self.infoBox.inputChanged()
        self.sendButton.sendIf()

    def clearCreatedInputs(self):
        for i in self.createdInputs:
            Segmentation.set_data(i[0].str_index, None)
        del self.createdInputs[:]

    def onDeleteWidget(self):
        self.clearCreatedInputs()

    def setCaption(self, title):
        if "captionTitle" in dir(self):
            changed = title != self.captionTitle
            super().setCaption(title)
            if changed:
                self.sendButton.settingsChanged()
        else:
            super().setCaption(title)

    def extract_text(self, segmentation):
        if not segmentation:
            return ""

        contents = []
        for segment in segmentation:
            try:
                contents.append(segment.get_content())
            except Exception:
                pass

        return " ".join(contents).strip()

    def segment_text(self, text):
        if text is None:
            return []

        text = str(text).strip()
        if not text:
            return []

        if self.selectedSegmentationType == "words":
            return re.findall(r"\b[\wÀ-ÿ'-]+\b", text, flags=re.UNICODE)

        if self.selectedSegmentationType == "sentences":
            parts = re.split(r"(?<=[.!?])\s+", text)
            return [part.strip() for part in parts if part.strip()]

        return []

    def expand_opcode(self, tag, a_chunk, b_chunk):
        rows = []

        if tag == "equal":
            for a_seg, b_seg in zip(a_chunk, b_chunk):
                rows.append((a_seg, b_seg, "equal"))
            return rows

        if tag == "delete":
            for a_seg in a_chunk:
                rows.append((a_seg, "", "delete"))
            return rows

        if tag == "insert":
            for b_seg in b_chunk:
                rows.append(("", b_seg, "insert"))
            return rows

        if tag == "replace":
            submatcher = difflib.SequenceMatcher(None, a_chunk, b_chunk)
            for subtag, si1, si2, sj1, sj2 in submatcher.get_opcodes():
                sub_a = a_chunk[si1:si2]
                sub_b = b_chunk[sj1:sj2]

                if subtag == "equal":
                    for a_seg, b_seg in zip(sub_a, sub_b):
                        rows.append((a_seg, b_seg, "equal"))

                elif subtag == "delete":
                    for a_seg in sub_a:
                        rows.append((a_seg, "", "delete"))

                elif subtag == "insert":
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

    def build_diff_rows(self, seg_a, seg_b):
        matcher = difflib.SequenceMatcher(None, seg_a, seg_b)
        rows = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            a_chunk = seg_a[i1:i2]
            b_chunk = seg_b[j1:j2]
            rows.extend(self.expand_opcode(tag, a_chunk, b_chunk))

        return rows

    def build_output_table(self, rows):
        """Create an Orange Table readable by Data Table."""
        change_var = DiscreteVariable(
            "change_type",
            values=["equal", "replace", "delete", "insert"]
        )

        metas = [
            StringVariable("segment_A"),
            StringVariable("segment_B"),
            StringVariable("diff_line"),
        ]

        domain = Domain(
            attributes=[],
            class_vars=[change_var],
            metas=metas,
        )

        y = []
        m = []

        for a, b, tag in rows:
            y.append([change_var.values.index(tag)])
            m.append([
                str(a),
                str(b),
                f"[{tag}] A: {a} | B: {b}",
            ])

        X = np.empty((len(rows), 0))
        Y = np.array(y, dtype=float) if y else np.empty((0, 1))
        M = np.array(m, dtype=object) if m else np.empty((0, 3), dtype=object)

        table = Table.from_numpy(domain, X=X, Y=Y, metas=M)
        table.name = self.captionTitle if hasattr(self, "captionTitle") else "Text Diff"
        return table

    def sendData(self):
        if not self.inputSegmentationA or not self.inputSegmentationB:
            self.infoBox.setText("Widget needs 2 inputs.", "warning")
            self.send("Diff data", None)
            return

        self.controlArea.setDisabled(True)

        text_a = self.extract_text(self.inputSegmentationA)
        text_b = self.extract_text(self.inputSegmentationB)

        seg_a = self.segment_text(text_a)
        seg_b = self.segment_text(text_b)

        rows = self.build_diff_rows(seg_a, seg_b)

        progressBar = ProgressBar(self, iterations=max(len(rows), 1))

        try:
            for _ in rows:
                progressBar.advance()

            self.outputTable = self.build_output_table(rows)

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

            progressBar.finish()
            self.controlArea.setDisabled(False)

            self.send("Diff data", self.outputTable)
            self.sendButton.resetSettingsChangedFlag()

        except Exception as exc:
            self.infoBox.setText(f"Diff failed: {exc}", "error")
            self.controlArea.setDisabled(False)
            self.send("Diff data", None)


if __name__ == "__main__":
    input1 = Input("Bonjour tout le monde.")
    input2 = Input("Bonjour tout le joli monde.")

    seg1 = Segmenter.concatenate([input1], label="A")
    seg2 = Segmenter.concatenate([input2], label="B")

    WidgetPreview(TextDiff).run(inputDataA=seg1, inputDataB=seg2)