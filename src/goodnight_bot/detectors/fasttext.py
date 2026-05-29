import logging

import fasttext

from goodnight_bot.detectors.base import DetectorStrategy

logger = logging.getLogger(__name__)

_LABEL = "__label__goodnight"


class FasttextDetector(DetectorStrategy):
    def __init__(self, model_path: str, threshold: float = 0.5) -> None:
        self._threshold = threshold
        try:
            self._model = fasttext.load_model(model_path)
            logger.info("Loaded fasttext model from %s", model_path)
        except Exception:
            logger.exception("Failed to load fasttext model from %s", model_path)
            raise

    def is_goodnight(self, text: str) -> bool:
        if not text:
            return False
        labels, probs = self._model.predict(text.replace("\n", " ").strip())
        if not labels:
            return False
        return labels[0] == _LABEL and probs[0] >= self._threshold