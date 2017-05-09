from nltk.translate.bleu_score import sentence_bleu
from nltk import word_tokenize
import json


def compute_bleu_scores(data):
    total_score = 0
    entry = 1
    for generation in data:
        print("ENTRY #" + str(entry))
        entry += 1
        print("\t" + generation['reference'])
        print("\t" + generation['hypothesis'])
        reference = word_tokenize(generation['reference'].lower())
        hypothesis = word_tokenize(generation['hypothesis'].lower())
        if min(len(hypothesis), len(reference)) < 4:
            weighting = 1.0 / min(len(hypothesis), len(reference))
            weights = tuple([weighting] * min(len(hypothesis), len(reference)))
        else:
            weights = (0.25, 0.25, 0.25, 0.25)
        generation['bleu_score'] = sentence_bleu([reference], hypothesis, weights=weights)
        print("\t" + str(generation['bleu_score']))
        total_score += generation['bleu_score']
    total_score /= len(data)
    with open('../static/bleu_scores.csv', 'w') as f:
        for generation in data:
            f.write(str(generation['bleu_score']) + "\n")
    print("Minimum: " + str(min((generation['bleu_score'] for generation in data))))
    print("Maximum: " + str(max((generation['bleu_score'] for generation in data))))
    print("Average: " + str(total_score))
    return data


def compute_bleu_score_for_users(data):
    # Get all of the sentences with more than one generation
    sentences = {}
    for generation in data:



if __name__ == "__main__":
    with open("../static/data.json", "r") as f:
        data = json.load(f)
    data = compute_bleu_scores(data)
