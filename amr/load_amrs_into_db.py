import sys
import re


from amr.models import AmrEntry


def main():
    if len(sys.argv) < 2:
        print("You must enter a filename", file=sys.stderr)
        exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Remove blank lines and comment lines
        lines = [line.strip() for line in lines if line.strip() != '' and not line.startswith('#')]
        # Now gather all of the entries
        iLine = 0
        sentence_number_pattern = re.compile(r'^[0-9]+\.\s+')
        end_of_sentence_number_pattern = re.compile(r'\(lpp_1943\.[0-9]+\)')
        while iLine < len(lines):
            while iLine < len(lines) and not len(sentence_number_pattern.findall(lines[iLine])):
                iLine += 1
            # When it halts we have found the sentence
            # Strip off the number at the beginning and end

            #    sed - r
            #    's/^[0-9]+\.//g' | sed - r
            #    's/\(lpp_1943\.[0-9]+\)//g'
            sentence = sentence_number_pattern.sub('', lines[iLine])
            sentence = end_of_sentence_number_pattern.sub('', sentence)
            iLine += 1
            # Now get the AMR that is under the sentence
            # Iterate while a sentence number is not present
            amr_lines = []
            while iLine < len(lines) and not len(sentence_number_pattern.findall(lines[iLine])):
                if lines[iLine].strip() != '':
                    amr_lines.append(lines[iLine])
                iLine += 1
            amr = '\n'.join(amr_lines)
            amr_entry = AmrEntry(sentence=sentence, amr=amr)
            amr_entry.save()

if __name__ == "__main__":
    main()
