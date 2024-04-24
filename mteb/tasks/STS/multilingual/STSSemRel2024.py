from __future__ import annotations

import datasets

from mteb.abstasks.TaskMetadata import TaskMetadata

from ....abstasks import AbsTaskSTS, MultilingualTask

_LANGUAGES = {
    "afr": ["afr-Latn"],
    "arq": ["arq-Arab"],
    "amh": ["amh-Ethi"],
    "eng": ["eng-Latn"],
    "hau": ["hau-Latn"],
    "ind": ["ind-Latn"],
    "hin": ["hin-Deva"],
    "kin": ["kin-Latn"],
    "mar": ["mar-Deva"],
    "arb": ["arb-Arab"],
    "ary": ["ary-Arab"],
    "pan": ["pan-Guru"],
    "esp": ["esp"],
    "tel": ["tel"],
}


_SPLITS = ["dev", "test"]


class STSSemRel2024(AbsTaskSTS, MultilingualTask):
    metadata = TaskMetadata(
        name="STSSemRel2024",
        dataset={
            "path": "SemRel/SemRel2024",
            "revision": "ef5c383d1b87eb8feccde3dfb7f95e42b1b050dd",
        },
        description=(
            "Semantic Textual Similarity Benchmark (STSbenchmark) dataset,"
            "but translated using DeepL API."
        ),
        reference="https://github.com/PhilipMay/stsb-multi-mt/",
        type="STS",
        category="s2s",
        eval_splits=_SPLITS,
        eval_langs=_LANGUAGES,
        main_score="cosine_spearman",
        date=None,
        form=None,
        domains=None,
        task_subtypes=None,
        license=None,
        socioeconomic_status=None,
        annotations_creators=None,
        dialect=None,
        text_creation=None,
        bibtex_citation=None,
        n_samples=None,
        avg_character_length=None,
    )

    @property
    def metadata_dict(self) -> dict[str, str]:
        metadata_dict = super().metadata_dict
        metadata_dict["min_score"] = 0
        metadata_dict["max_score"] = 5
        return metadata_dict

    def load_data(self, **kwargs):
        if self.data_loaded:
            return

        def get_dataset_subset(lang: str):
            """For a specified subset (=language)
            only get the splits listed in _SPLIT
            and rename column "score"

            Args:
                lang (str): _description_

            Returns:
                datasets.DatasetDict: the dataset of the specified language
            """
            subset = datasets.DatasetDict(
                **dict(
                    zip(
                        _SPLITS,
                        datasets.load_dataset(
                            name=lang,
                            split=_SPLITS,
                            **self.metadata_dict["dataset"],
                        ),
                    )
                )
            )
            return subset.rename_column("similarity_score", "score")

        self.dataset = datasets.DatasetDict(
            **dict(zip(self.langs, [get_dataset_subset(lang) for lang in self.langs]))
        )

        self.data_loaded = True
