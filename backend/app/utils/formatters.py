def fiscal_number(establishment: str, emission_point: str, document_type: str, correlative: int) -> str:
    return f"{establishment}-{emission_point}-{document_type}-{correlative:08d}"
