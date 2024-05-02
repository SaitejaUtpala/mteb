from __future__ import annotations

from mteb.abstasks.TaskMetadata import TaskMetadata

from ....abstasks import AbsTaskClassification

_LANGUAGES = {
    "pan": ["pan-Guru"],
    "bgc": ["bgc-Deva"],
    "mag": ["mag-Deva"],
    "bns": ["bns-Deva"],
    "kfq": ["kfg-Deva"],
    "noe": ["noe-Deva"],
    "bhb": ["bhb-Deva"],
    "bho": ["bho-Deva"],
    "gbm": ["gbm-Deva"],
    "mup": ["mup-Deva"],
    "anp": ["anp-Deva"],
    "hne": ["hne-Deva"],
    "bra": ["bra-Deva"],
    "raj": ["raj-Deva"],
    "awa": ["awa-Deva"],  
    "guj": ["guj-Gujr"], 
    "ben": ["ben-Beng"], 
    "bhd" : ["bhd-Deva"],
    "kfy": ["kfy-Deva"], 
    "mar": ["mar-Deva"],
    "bjj" : ["bjj-Deva"]

}


class HinDialectClassification(AbsTaskClassification):
    metadata = TaskMetadata(
        name="HinDialectClassification",
        dataset={
            "path": "mlexplorer008/hin_dialect_classification",
            "revision": "8b3995ac4ef13e5b444d29003698a58d6338343f",
        },
        description="HinDialect: 26 Hindi-related languages and dialects of the Indic Continuum in North India",
        reference="https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-4839",
        category="s2s",
        type="Classification",
        eval_splits=["test"],
        eval_langs=_LANGUAGES,
        main_score="accuracy",
        date=("2010-01-01", "2023-01-01"),
        form=["written"],
        domains=["Web", "Non-fiction"],
        task_subtypes=["Language identification"],
        license="MIT",
        socioeconomic_status="mixed",
        annotations_creators="expert-annotated",
        dialect=[],
        text_creation="found",
        bibtex_citation= """
        @misc{11234/1-4839,
        title = {{HinDialect} 1.1: 26 Hindi-related languages and dialects of the Indic Continuum in North India},
        author = {Bafna, Niyati and {\v Z}abokrtsk{\'y}, Zden{\v e}k and Espa{\~n}a-Bonet, Cristina and van Genabith, Josef and Kumar, Lalit "Samyak Lalit" and Suman, Sharda and Shivay, Rahul},
        url = {http://hdl.handle.net/11234/1-4839},
        note = {{LINDAT}/{CLARIAH}-{CZ} digital library at the Institute of Formal and Applied Linguistics ({{\'U}FAL}), Faculty of Mathematics and Physics, Charles University},
        copyright = {Creative Commons - Attribution-{NonCommercial}-{ShareAlike} 4.0 International ({CC} {BY}-{NC}-{SA} 4.0)},
        year = {2022} }
        """,
        n_samples={"test": 2048},
        avg_character_length={"test": 247.49},
    )

    def dataset_transform(self) -> None:
        self.dataset = self.dataset.rename_columns(
            {" text": "text", "lang_id": "label"}
        )
        self.dataset = self.stratified_subsampling(self.dataset, seed=self.seed)
