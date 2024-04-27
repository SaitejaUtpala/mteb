from __future__ import annotations

from mteb.abstasks import AbsTaskClassification
from mteb.abstasks.TaskMetadata import TaskMetadata


class MarathiNewsClassification(AbsTaskClassification):
    metadata = TaskMetadata(
        name="MarathiNewsClassification",
        description="A Marathi dataset for 3-class classification of Marathi news articles",
        reference="https://github.com/goru001/nlp-for-punjabi/",
        dataset={
            "path": "mlexplorer008/marathi_news_classification",
            "revision": "7640cf8132cca1f99995ac71512a670e3c965cf1",
        },
        type="Classification",
        category="s2s",
        date=("2014-01-01", "2018-01-01"),
        eval_splits=["test"],
        eval_langs=["pan-Guru"],
        main_score="accuracy",
        form=["written"],
        domains=["News"],
        task_subtypes=["Topic classification"],
        license="MIT",
        socioeconomic_status="mixed",
        annotations_creators="derived",
        dialect=[],
        text_creation="found",
        bibtex_citation=None,
        n_samples={"train": 627, "test": 157},
        avg_character_length={"train": 4222.22, "test": 4115.14},
    )

    def dataset_transform(self):
        self.dataset = self.dataset.rename_column("article", "text")
        self.dataset = self.dataset.rename_column("is_about_politics", "label")
