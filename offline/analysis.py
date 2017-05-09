from nltk.translate.bleu_score import sentence_bleu
from nltk import word_tokenize
import json
from math import ceil
from collections import Counter
from amr.amr_reader.amr import AMR


def compute_bleu_scores(data):
    print("****** BLEU SCORES ******")
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
    print("****** BLEU FOR MULTI-USER ******")
    # Get all of the sentences with more than one generation
    amr_id_to_generation = {}
    for generation in data:
        if generation['amr_id'] not in amr_id_to_generation:
            amr_id_to_generation[generation['amr_id']] = [generation]
        else:
            amr_id_to_generation[generation['amr_id']].append(generation)
    # Now get rid of all of them without multiple entries
    to_delete = []
    for id in amr_id_to_generation:
        if len(amr_id_to_generation[id]) < 2:
            to_delete.append(id)
    for id in to_delete:
        del amr_id_to_generation[id]
    # Now determine how much user scores differ by
    total_average_delta = 0
    deltas = []
    for amr in amr_id_to_generation:
        # Get the average score for the AMR then the average difference from that
        average_score = sum(generation['bleu_score'] for generation in amr_id_to_generation[amr]) / len(
            amr_id_to_generation[amr])
        average_delta = sum(
            abs(average_score - generation['bleu_score']) for generation in amr_id_to_generation[amr]) / len(
            amr_id_to_generation[amr])
        total_average_delta += average_delta
        deltas.append(average_delta)
        print("AMR ID #" + str(amr))
        print("\tScores: " + str(len(amr_id_to_generation[amr])))
        print("\tAvg. score: " + str(average_score))
        print("\tAvg. delta: " + str(average_delta))

    total_average_delta /= len(amr_id_to_generation)
    print("Total average delta: " + str(total_average_delta))
    with open('../static/multi_user_bleu_deltas.csv', 'w') as f:
        for delta in deltas:
            f.write(str(delta) + "\n")


def compute_jaccard_similarity(data):
    print("****** JACCARD SIMILARITY ******")
    total_average = 0
    entry = 1
    for generation in data:
        print("ENTRY #" + str(entry))
        entry += 1
        print("\t" + generation['reference'])
        print("\t" + generation['hypothesis'])
        reference_tokens = set(word_tokenize(generation['reference'].lower()))
        hypothesis_tokens = set(word_tokenize(generation['hypothesis'].lower()))
        intersection = reference_tokens.intersection(hypothesis_tokens)
        union = reference_tokens.union(hypothesis_tokens)
        generation['jaccard'] = len(intersection) / len(union)
        total_average += generation['jaccard']
        print("\tJaccard: " + str(generation['jaccard']))
    total_average /= len(data)
    print("Minimum: " + str(min((generation['jaccard'] for generation in data))))
    print("Maximum: " + str(max((generation['jaccard'] for generation in data))))
    print("Average: " + str(total_average))
    with open("../static/jaccard.csv", "w") as f:
        for generation in data:
            f.write(str(generation['jaccard']) + "\n")
    score_matrix = [[0 for x in range(10)] for y in range(10)]
    for generation in data:
        jaccard_index = int(ceil(generation['jaccard'] * 10) - 1)
        bleu_index = int(ceil(generation['bleu_score'] * 10) - 1)
        score_matrix[jaccard_index][bleu_index] += 1
    with open("../static/jaccard_vs_bleu.csv", "w") as f:
        for i in range(10):
            for j in range(10):
                if j != 9:
                    f.write(str(score_matrix[i][j]) + ", ")
                else:
                    f.write(str(score_matrix[i][j]) + "\n")
    return data


def compute_cosine_sim(data):
    print("****** COSINE SIMILARITY ******")
    total_average = 0
    entry = 1
    for generation in data:
        print("ENTRY #" + str(entry))
        entry += 1
        print("\t" + generation['reference'])
        print("\t" + generation['hypothesis'])
        reference_tokens = set(word_tokenize(generation['reference'].lower()))
        hypothesis_tokens = set(word_tokenize(generation['hypothesis'].lower()))
        ref_count = Counter(reference_tokens)
        hyp_count = Counter(hypothesis_tokens)
        words = list(set(ref_count.keys()).union(set(hyp_count.keys())))
        ref_vector = [ref_count.get(word, 0) for word in words]
        hyp_vector = [hyp_count.get(word, 0) for word in words]
        ref_len = sum(elem * elem for elem in ref_vector) ** 0.5
        hyp_len = sum(elem * elem for elem in hyp_vector) ** 0.5
        dot_product = sum(ref * hyp for ref, hyp in zip(ref_vector, hyp_vector))
        cosine = dot_product / (ref_len * hyp_len)
        generation['cosine'] = cosine
        total_average += cosine
        print("\t" + str(generation['cosine']))
    total_average /= len(data)
    print("Minimum: " + str(min((generation['cosine'] for generation in data))))
    print("Maximum: " + str(max((generation['cosine'] for generation in data))))
    print("Average: " + str(total_average))
    with open("../static/cosine.csv", "w") as f:
        for generation in data:
            f.write(str(generation['cosine']) + "\n")
    return data


def cosine_vs_length(data):
    with open("../static/cosine_vs_reference_token_length.csv", "w") as f:
        f.write("Cosine, Token Length\n")
        for generation in data:
            token_length = len(word_tokenize(generation['reference']))
            f.write(str(generation['cosine']) + ", " + str(token_length) + "\n")


def bleu_vs_amr_triples(data):
    with open("../static/bleu_vs_amr_triples.csv", "w") as f:
        f.write("bleu, triples\n")
        for generation in data:
            amr = AMR(generation['amr'])
            generation['triples'] = len(amr.triples())
            f.write(str(generation['bleu_score']) + ", " + str(len(amr.triples())) + "\n")
    return data


def triples_per_word(data):
    print("****** TRIPLES PER WORD ******")
    total_ref_average = 0
    total_hyp_average = 0
    entry = 1
    for generation in data:
        print("ENTRY #" + str(entry))
        entry += 1
        print("\t" + generation['reference'])
        print("\t" + generation['hypothesis'])
        tpw_ref = generation['triples'] / len(word_tokenize(generation['reference']))
        tpw_hyp = generation['triples'] / len(word_tokenize(generation['hypothesis']))
        generation['tpw_ref'] = tpw_ref
        generation['tpw_hyp'] = tpw_hyp
        print("\tTPW Reference: " + str(tpw_ref))
        print("\tTPW Hypothesis: " + str(tpw_hyp))
        total_ref_average += tpw_ref
        total_hyp_average += tpw_hyp
    total_ref_average /= len(data)
    total_hyp_average /= len(data)
    print("Average TPW Reference: " + str(total_ref_average))
    print("Average TPW Hypothesis: " + str(total_hyp_average))
    with open("../static/triples_per_word.csv", "w") as f:
        f.write("Reference, Hypothesis\n")
        for generation in data:
            f.write(str(generation['tpw_ref']) + ", " + str(generation['tpw_hyp']) + "\n")
    return data


if __name__ == "__main__":
    with open("../static/data.json", "r") as f:
        data = json.load(f)
    data = compute_bleu_scores(data)
    compute_bleu_score_for_users(data)
    data = compute_jaccard_similarity(data)
    data = compute_cosine_sim(data)
    cosine_vs_length(data)
    data = bleu_vs_amr_triples(data)
    data = triples_per_word(data)
