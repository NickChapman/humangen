from nltk.translate.bleu_score import sentence_bleu
from nltk import word_tokenize
import json

def compute_scores():
    with open("../static/data.json", "r") as f:
        data = json.load(f)
    total_score = 0
    entry = 1
    for generation in data:
        print("ENTRY #" + str(entry))
        entry += 1
        print("\t" + generation['reference'])
        print("\t" + generation['hypothesis'])
        reference = word_tokenize(generation['reference'])
        hypothesis = word_tokenize(generation['hypothesis'])
        if min(len(hypothesis), len(reference)) < 4:
            weighting = 1.0 / min(len(hypothesis), len(reference))
            weights = tuple([weighting] * min(len(hypothesis), len(reference)))
        else:
            weights = (0.25, 0.25, 0.25, 0.25)
        generation['score'] = sentence_bleu([reference], hypothesis, weights=weights)
        print("\t" + str(generation['score']))
        total_score += generation['score']
    total_score /= len(data)
    with open('../static/scores.csv', 'w') as f:
        for generation in data:
            f.write(str(generation['score']) + "\n")
    print("Minimum: " + str(min((generation['score'] for generation in data))))
    print("Maximum: " + str(max((generation['score'] for generation in data))))
    print("Average: " + str(total_score))

if __name__ == "__main__":
    compute_scores()