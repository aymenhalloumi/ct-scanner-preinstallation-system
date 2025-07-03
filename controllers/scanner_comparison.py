import logging
from config import SCANNER_SPECS

logger = logging.getLogger(__name__)

class ScannerComparison:
    """Provide side-by-side comparison of CT scanner models."""

    def __init__(self):
        self.scanner_specs = SCANNER_SPECS

    def compare_scanners(self, models):
        """Return specifications for the given scanner models."""
        comparisons = {}
        for model in models:
            specs = self.scanner_specs.get(model)
            if specs:
                comparisons[model] = specs
            else:
                logger.warning("Scanner model '%s' not found", model)
        return comparisons
