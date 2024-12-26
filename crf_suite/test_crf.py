import translation_line_crf_most_frequent_labels
import process_morpheme_line

filepath = "lez-test-track2-uncovered-copy"
print(process_morpheme_line.process_morpheme_line(filepath=filepath,replaceStems=False))
