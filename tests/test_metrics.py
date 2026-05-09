from asr_benchmark.metrics import (
    char_error_rate,
    locality_exact_match,
    locality_token_recall,
    word_error_rate,
)


def test_word_error_rate_zero_for_exact_match():
    assert word_error_rate("Main Koramangala mein rehta hoon", "Main Koramangala mein rehta hoon") == 0.0


def test_char_error_rate_non_zero_for_spelling_error():
    assert char_error_rate("Koramangala", "Koramanggala") > 0.0


def test_locality_exact_match_detects_locality():
    assert locality_exact_match("HSR Layout", "Mera address HSR Layout mein hai") == 1.0


def test_locality_token_recall_handles_partial_match():
    assert locality_token_recall("Electronic City", "Main Electronic mein kaam karta hoon") == 0.5
