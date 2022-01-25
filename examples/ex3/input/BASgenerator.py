#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 11:40:19 2021

TEXT CORPUS TO BAS PROJECT GENERATOR
WITH RICH (DI,TRI)-PHONE TEXT SELECTION ALGORITHM

@author: ivan
"""

import os
import sys
from typing import List

import numpy as np
import random as rn
import pickle
import re
import shutil
from datetime import datetime
from itertools import groupby
import uuid

import matplotlib.pyplot as plt

project_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<ProjectConfiguration version="4.0.0">
  <name>$PROJECT$</name>
  <RecordingConfiguration>
    <url>RECS/</url>
    <captureScope>SESSION</captureScope>
  </RecordingConfiguration>
  <PromptConfiguration>
    <promptsUrl>$PROJECT$_script.xml</promptsUrl>
    <InstructionsFont>
      <family>SansSerif</family>
    </InstructionsFont>
    <PromptFont>
      <family>SansSerif</family>
    </PromptFont>
    <DescriptionFont>
      <family>SansSerif</family>
    </DescriptionFont>
    <automaticPromptPlay>false</automaticPromptPlay>
    <PromptBeep>
      <beepGainRatio>1.0</beepGainRatio>
    </PromptBeep>
  </PromptConfiguration>
  <Speakers>
    <speakersUrl>$PROJECT$_speakers.xml</speakersUrl>
  </Speakers>
</ProjectConfiguration>'''

script_front = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE script SYSTEM "SpeechRecPrompts_4.dtd">
<script id="$PROJECT$">
  <metadata>
    <key/>
    <value/>
  </metadata>
  <recordingscript>
    <section speakerdisplay="true">'''

script_back = '''
 	 </section>
  </recordingscript>
</script>'''

# selected_sentence_ids = ()
delimiter = '$'
digraphs = {'C_H': 'CH', 'D_Ź': 'DŹ'}

uasr_map = {
    'w': 'U v',
    'ts': 't s',
    'tS': 't S',
    'jn': 'j n',
    'dZ': 'd S',
    'dS': 'd S',
    'ng': 'n g',
    'Z': 'S',
    '1': 'Y'
}

exceptions = dict()
graphemes = list()
phoneme_maps = dict()
min_phm_len = 25

# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


''' Generate BAS speakers template for a given number of speakers'''

def speakers(num_speakers):
    output = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <speakers>'''

    spk_body = ''' 
        <speakers>
            <personId>$PERSON$</personId>
            <registered>$TIME$</registered>
            <uuid>$UUID$</uuid>
            <informedConsentInPaperFormSigned>false</informedConsentInPaperFormSigned>
        </speakers>
        '''
    spk_end = '''
    </speakers>
    '''
    for spk in range(num_speakers):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%dT%H:%M:%f%z")
        spk_body = spk_body.replace('$UUID$', str(uuid.uuid4()))
        spk_body = spk_body.replace('$TIME$', date_time)
        spk_body = spk_body.replace('$PERSON$', str(spk + 1))
        output = output + spk_body

    output = output + spk_end
    return output


''' Partition list of sentences in n sets '''


def partition(list_in, n):
    rn.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]


''' Check if file conforms to the UTF-8 format'''


def checkUTF8(filename):
    import codecs
    try:
        f = codecs.open(filename, encoding='utf-8', errors='strict')
        for line in f:
            pass
        return True
    except UnicodeDecodeError:
        print(f'SKIPPING: {filename} is invalid UTF-8')
        return False


'''Read G2P exceptions file'''


def read_exceptions(exp_file_name):
    try:
        with open(os.path.join(os.getcwd(), exp_file_name), 'r', encoding='utf8') as expfile:
            for line in expfile:
                p = line.strip().split('\t')
                exceptions[p[0]] = p[1]
    except FileNotFoundError:
        print('Error opening exceptions file.')


'''Check if there are exceptions for a given phoneme context'''


def check_exceptions(rules):
    excps = []
    for e in exceptions:
        for rule in rules:
            if e in rule:
                excps.extend([exceptions[e]])
        r = list(dict.fromkeys(excps))
    return r


'''G2P for a given word and phoneme map'''


def phonemize(word, phmap):
    phns = []

    if phmap is not None:
        canonical = []
        excpc = 0
        graphs = '_'.join(list('$' + word.strip() + '$'))
        for d in digraphs:
            graphs = graphs.replace(d, digraphs[d])
        graphs = graphs.split('_')

        for i in graphs:
            if i != "$":
                cp = phmap[i][0].split(' ')

                if mode == 'uasr':
                    map_temp = []
                    for n in cp:
                        uasr_phn = uasr_map.get(n, n).split()
                        for u in uasr_phn:
                            map_temp.append(u)
                    cp = map_temp

                canonical.extend(cp)

        for g in range(len(graphs) - 2):
            left = graphs[g]
            grapheme = graphs[g + 1]
            right = graphs[g + 2]
            rule1 = left + '_' + grapheme + '_' + right
            rule2 = ('#' + phmap[left][1] if left != '$' else '$') + '_' + grapheme + '_' + (
                '#' + phmap[right][1] if right != '$' else '$')
            excp = check_exceptions([rule1, rule2])
            excpc = excpc + len(excp)

            if len(excp) > 1:
                excp = [excp[0]]
            phn = []
            if len(excp) == 1:
                if excp[0] != '*':
                    phn = excp[0].split(' ')
            else:
                phn = phmap[grapheme][0].split(' ')

            if mode == 'uasr':
                map_temp = []
                for n in phn:
                    uasr_phn = uasr_map.get(n, n).split()
                    for u in uasr_phn:
                        map_temp.append(u)
                phn = map_temp

            phns.extend(phn)

        can = [key for key, _ in groupby(canonical)]
        p = [key for key, _ in groupby(phns)]

        if excpc != 0:
            return [p, can]
        else:
            return [can]
    else:
        return word.strip()


'''Load Phoneme Inventory'''


def read_inventory(f):
    try:
        with open(os.path.join(os.getcwd(), f), 'r', encoding='utf8') as invfile:
            for line in invfile:
                p = line.strip().split('\t')
                phoneme_maps[p[0]] = (p[1], p[2])
                graphemes.append(p[0])
    except FileNotFoundError:
        print('SKIPPING: Error opening file:', f['fn'])


'''Load text data in UTF-8 txt file(s)'''


def load_data(files):
    crpus = []
    for f in files:
        try:
            fn = os.path.join(os.getcwd(), f)
            if not checkUTF8(fn):
                continue
            with open(fn, 'r', encoding='utf8') as txtfile:
                for line in txtfile:
                    p = line.strip()
                    crpus.append(p)
        except FileNotFoundError:
            print('Error opening file:', f['fn'])
    return crpus


'Normalize text, remove sentences containing non-inventory characters or shorter than the minimal phoneme count'


def normalize_text(crpus, inventory, uv=None):
    txt = []
    rmv = []
    inv = set(inventory)
    if uv is not None:
        if case == 'uc':
            uv = list(map(lambda x: x.upper(), uv))
        if case == 'lc':
            uv = list(map(lambda x: x.lower(), uv))
        # Converting it into list
        uv = set(list(uv))

    for line in crpus:

        tline = re.sub(r'[^\w\s\d]', '', line)

        if case == "uc":
            tline = tline.upper().strip()
        elif case == "lc":
            tline = tline.lower().strip()
        else:
            tline = tline.strip()

        if uv is not None:
            lwrds = set(tline.split())
            if not lwrds.issubset(uv):
                continue

        grphs = '_'.join(tline.upper())
        for d in digraphs:
            grphs = grphs.replace(d, digraphs[d])

        grphs = grphs.strip().split('_')

        if inventory:
            linv = set(grphs)
            linv.discard(' ')
            if linv.issubset(inv) and len(linv) > min_phm_len:
                txt.append(tline)
            else:
                rmv.append((linv.difference(inv), tline))
        else:
            txt.append(tline)

    return txt, rmv


'''Extract vocabulary from the normalized corpus'''


def get_vocabulary(crpus):
    text = ' '.join(crpus)
    return sorted(list(set(text.split())))


'''Make lexicon from vocabulary'''


def make_lexicon(vocab):
    lex = dict()
    for v in vocab:
        pron = phonemize(v.upper(), phoneme_maps)
        lex[v] = pron
    return lex


''' Generate phoneme sequences from sentences'''


def map_prons(sent, lex, pmap):
    pronunciation = []
    sents = []
    lexset = set(lex.keys())
    for idx, s in enumerate(sent):
        prn = []
        words = s.strip().split(' ')
        words = list(filter(None, words))
        if not set(words).issubset(lexset) and bool(lex):
            continue

        prn.extend('.')

        for w in words:
            if not lex.get(w):
                phn = phonemize(w.upper(), pmap)[0]
            else:
                phn = lex[w][0]

            prn.extend(phn)
            prn.extend('.')

        pronunciation.append(prn)
        sents.append(s)
    return pronunciation, sents


''' Statisctics about the selected sentences '''


def get_stats(p, bar=False):
    stats = {}
    phones = {}
    diphones = {}
    triphones = {}

    counter = 0
    l = len(p)
    # Initial call to print 0% progress
    if bar:
        printProgressBar(0, l, prefix='Get  Statistics:', suffix='Complete', length=50)

    for ln in p:
        phonelist = ln
        for phon in phonelist:
            try:
                phones[phon] += 1
            except:
                phones[phon] = 1

        # extract diphones from phones
        for i in range(len(phonelist) - 1):
            dip = "{}_{}".format(phonelist[i], phonelist[i + 1])
            try:
                diphones[dip] += 1
            except:
                diphones[dip] = 1

        for i in range(len(phonelist) - 2):
            tri = "{}^{}+{}".format(phonelist[i], phonelist[i + 1], phonelist[i + 2])
            try:
                triphones[tri] += 1
            except:
                triphones[tri] = 1

        if bar:
            counter += 1
            printProgressBar(counter + 1, l, prefix='Get  Statistics:', suffix='Complete', length=50)

    stats['phones'] = phones
    stats['diphones'] = diphones
    stats['triphones'] = triphones

    return stats


''' Sentence scoring'''


def score_sentence(sentence, scorestats):
    if scoring_type == 1 or scoring_type == 2:
        score = (np.dot(sentence, scorestats))
    elif scoring_type == 3:
        # According to Berry & Fadiga "Data-driven Design of a Sentence List for an Articulatory Speech Corpus"
        T = np.sum(sentence)  # number of tokens (phonemes, di-tri phones)
        if T != 0:
            u = np.count_nonzero(np.array(sentence))  # unique tokens
            binsent = sentence
            binsent[np.nonzero(sentence)] = 1
            score = 1 / T * np.dot(binsent, scorestats) * (u / T)
        else:
            score = 0
    else:
        raise SystemExit('Wrong scoring type.')

    return score


''' Count the used tokens by type'''


def token_counts(corp, token_type, token_ids, score):
    scr = []
    i = 0
    l = len(corp)
    # Initial call to print 0% progress
    printProgressBar(0, l, prefix='Score Sentences:', suffix='Complete', length=50)

    for phonlist in corp:
        if token_type == "phones":
            tokens = phonlist
        elif token_type == "diphones":
            tokens = ["{}_{}".format(phonlist[i], phonlist[i + 1]) for i in range(len(phonlist) - 1)]
        elif token_type == "triphones":
            tokens = ["{}^{}+{}".format(phonlist[i], phonlist[i + 1], phonlist[i + 2]) for i in
                      range(len(phonlist) - 2)]
        else:
            raise SystemExit('Token type not defined')

        dataset = np.zeros(len(token_ids))
        for token in tokens:
            idx = np.where(np.array(token_ids) == np.array(token))
            try:
                dataset[idx] += 1
            except:
                dataset[idx] = 1
        scr.append(score_sentence(dataset, score))
        i += 1
        printProgressBar(i + 1, l, prefix='Score Sentences:', suffix='Complete', length=50)

    return scr


''' Make lists for different scoring methods'''


def scorelists(stat, name):
    tokens = list(stat[name].keys())
    # Score 1: each type should be present at least once
    score1 = np.full(np.array(list(stat[name].values())).shape[0], 1)

    # Score 2: each base type according the negative probability logs
    score2 = np.array(list(stat[name].values()))
    score2 = -np.log(score2 / np.sum(score2))

    return tokens, list(score1), list(score2), list(score2)


''' Sentence selection according the scoring methodology '''


def sent_selection(stats, score_type=1):
    if 1 > score_type > 3:
        raise SystemExit("Wrong scoring type")

    scores = scorelists(stats, basic_type)
    dataset = token_counts(utterances, basic_type, scores[0], scores[score_type])

    print('Scoring Done')

    return np.argsort(dataset)[-num_sentences:]


'''Main loop'''
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} config')
        raise SystemExit()

    ''' 
        *   config       - YAML config file;
    '''
    import yaml

    config_file = sys.argv[1]
    projectname = config_file.split('.')[0]

    input_txts = ['corpus.hsb']
    exceptions_file = 'exceptions.txt'
    phoneme_inventory = 'phonmap.txt'
    mode = 'sampa'  # "sampa" or "uasr" phoneme sets
    basic_type = 'diphones'
    split = 3
    case = "uc"
    offset = 0  # speaker id starting number
    num_sentences = 100
    no_speakers = 1
    min_duration = 3  # seconds of speech
    names = ["phones", "diphones", "triphones"]
    scoring_type = 3  # 1, 2 or 3; choose 2 for negative log-prob weights, 3 for sentence weights
    user_vocab = ["user.vocab"]

    try:
        with open(config_file, 'r') as stream:
            config = yaml.safe_load(stream)
        locals().update(config)
    except:
        raise Warning('No yaml config file. Using default configuration')

    if os.path.exists('sentences'):
        shutil.rmtree('sentences')
    os.mkdir('sentences')

    if os.path.exists('speechrecorder'):
        shutil.rmtree('speechrecorder')
    os.mkdir('speechrecorder')

    if os.path.exists('corpus'):
        shutil.rmtree('corpus')
    os.mkdir('corpus')

    filelist = input_txts

    min_phm_len = min_duration * 10

    ''' Corpus processing '''
    corpus = load_data(filelist)
    if exceptions_file is not None:
        read_exceptions(exceptions_file)
    if phoneme_inventory is not None:
        read_inventory(phoneme_inventory)
    if user_vocab is not None:
        user_vocab = load_data(user_vocab)

    corpus_n, removed = normalize_text(corpus, graphemes, user_vocab)
    corpus_n = list(dict.fromkeys(corpus_n))
    vocabulary = get_vocabulary(corpus_n)
    lexicon = make_lexicon(vocabulary)

    utterances, sentences = map_prons(corpus_n, lexicon, phoneme_maps)
    top = np.unique(' '.join(corpus_n).split(' '), return_counts=True)
    count_sort_ind = np.argsort(-top[1])

    freq = zip(top[0][count_sort_ind], top[1][count_sort_ind])

    freq_file = open(os.path.join(os.getcwd(), 'corpus', projectname.lower() + '.freq'), "w", encoding='utf-8')
    for word in freq:
        freq_file.write(word[0] + '\t' + str(word[1]) + '\n')
    freq_file.close()

    corp_file = open(os.path.join(os.getcwd(), 'corpus', projectname.lower() + '.corp'), "w", encoding='utf-8')
    corp_file.write("\n".join(sentences))
    corp_file.close()

    rmv_file = open(os.path.join(os.getcwd(), 'corpus', projectname.lower() + '.rmvd'), "w", encoding='utf-8')
    for r in removed:
        rmv_file.write(str(r[0]) + '\t' + r[1] + '\n')
    rmv_file.close()

    vocab_file = open(os.path.join(os.getcwd(), 'corpus', projectname.lower() + '.vocab'), "w", encoding='utf-8')
    vocab_file.write("\n".join(vocabulary))
    vocab_file.close()

    lex_file = open(os.path.join(os.getcwd(), 'corpus', projectname.lower() + '_' + mode + '.lex'), "w",
                    encoding='utf-8')
    phmodels = set()
    for key in lexicon.keys():
        for pvar in lexicon[key]:
            lex_file.write(key + '\t' + ' '.join(pvar) + '\n')
            phmodels.update(pvar)
    lex_file.close()

    ulex_file = open(os.path.join(os.getcwd(), 'corpus', projectname.lower() + '_' + mode + '.ulex'), "w",
                     encoding='utf-8')
    phmodels = set()
    for key in lexicon.keys():
        for pvar in lexicon[key]:
            ulex_file.write(key + '\t' + ''.join(pvar) + '\n')
            phmodels.update(pvar)
    ulex_file.close()

    phm_file = open(os.path.join(os.getcwd(), 'corpus', projectname.lower() + '.classes'), "w", encoding='utf-8')
    phm_file.write('\n'.join(sorted(list(phmodels))))
    phm_file.close()

    if basic_type is None:
        raise SystemExit('Skip sentence selection.')

    ''' Sentence selection  '''
    ideal_stats = get_stats(utterances, bar=True)
    selected_sentence_ids = sent_selection(ideal_stats, scoring_type)

    ''' Split the datasets '''
    split_ids = partition(list(selected_sentence_ids), split)

    for i, idx in enumerate(split_ids):
        out_file = 'sentsel_' + basic_type + '_' + str(scoring_type) + '_' + mode + '_' + str(
            i + 1) + '.txt'
        sentsel = open(os.path.join(os.getcwd(), 'sentences', out_file), "w", encoding='utf-8')
        part_folder = 'speechrecorder/' + projectname + '-' + str(i + 1)

        if os.path.exists(part_folder):
            shutil.rmtree(part_folder)
        os.mkdir(part_folder)
        basprojectfile = open(os.path.join(os.getcwd(), part_folder, projectname + '-' + str(i + 1) + '.prt'),
                              "w", encoding='utf-8')

        sxml_file = open(
            os.path.join(os.getcwd(), part_folder, projectname + '-' + str(i + 1) + '_speakers.xml'),
            "w", encoding='utf-8')
        sxml_file.write(speakers(no_speakers))
        sxml_file.close()

        pxml_file = open(os.path.join(os.getcwd(), part_folder, projectname + '-' + str(i + 1) + '_project.prj'),
                         "w", encoding='utf-8')
        pxml_file.write(project_xml.replace('$PROJECT$', projectname + '-' + str(i + 1)))
        pxml_file.close()

        scxml_file = open(os.path.join(os.getcwd(), part_folder, projectname + '-' + str(i + 1) + '_script.xml'),
                          "w", encoding='utf-8')

        scxml_file.write(script_front.replace('$PROJECT$', projectname + '-' + str(i + 1)))

        for k, sm_id in enumerate(idx):
            header = projectname + '_' + str(i + 1) + '_' + str(k).zfill(3) + '\t'
            sentsel.write(header + sentences[sm_id] + '\n')
            sentsel.write(header + ' '.join(utterances[sm_id]) + '\n')

            for spk in range(no_speakers):
                drname = os.path.join(os.getcwd(), 'transliterations', projectname + '-' + str(i + 1), 'RECS',
                                      str(spk + 1 + offset).zfill(4))
                os.makedirs(drname, exist_ok=True)
                trlfile = open(drname + '/' + str(spk + 1 + offset).zfill(4) + header[:-1] + '.trl', "w",
                               encoding='utf-8')

                words = list(filter(None, sentences[sm_id].split()))

                trlfile.write('\n'.join(words) + '\n')
                trlfile.close()

            basprojectfile.write(header + sentences[sm_id] + '\n')
            scxml_file.write('<recording itemcode="' + header[:-1] +
                             '" postrecdelay="500" prerecdelay="2" recduration="25000">' +
                             '<recprompt><mediaitem>"' + sentences[sm_id] +
                             '"</mediaitem></recprompt></recording>' + '\n')

        basprojectfile.close()
        scxml_file.write(script_back)
        scxml_file.close()
        sentsel.close()

        '''Phonemic unit analysis'''
        utt_sel = list(np.array(utterances, dtype='object')[idx])
        sent_sel = list(np.array(sentences, dtype='object')[idx])

        wrd_cnt = len((' '.join([''.join(s) for s in sent_sel])).split(' '))
        char_cnt = len((' '.join([' '.join(u) for u in utt_sel]).split(' ')))

        sel_stats = get_stats(utt_sel, bar=False)
        whtspc = sel_stats['phones']['.']

        if len(utterances) <= num_sentences:
            num_sentences = len(utterances)
        rnd_sent = rn.sample(utterances, int(num_sentences / split))
        rnd_stats = get_stats(rnd_sent)

        print(f'\n\nSet Nr.: {i + 1}')
        print(f'sentences: {int(num_sentences / split)}')
        print(f'sell word count: {wrd_cnt}')
        # Fonagy, I.; K. Magdics (1960). "Speed of utterance in phrases of different length".
        # Language and Speech. 3 (4): 179–192. doi:10.1177/002383096000300401.
        pps_min = 10  # 9.4  # reading poetry
        pps_max = 15  # 13.83  # commenting sport
        print(
            f'estimated duration by phoneme units (min): {((char_cnt - whtspc) / pps_max) / 60} - {((char_cnt - whtspc) / pps_min) / 60}')
        # http://prosodia.upf.edu/home/arxiu/publicacions/rodero/
        # rodero_a-comparative-analysis-of-speech-rate-and-perception-in-radio-bulletins.pdf
        wpm_min = 100  # 168  # Englisch BBC
        wpm_max = 160  # 210  # Spanish RNE
        print(f'estimated duration by number of words (min): {(wrd_cnt / wpm_max)} - {(wrd_cnt / wpm_min)}')

        for b_type in names:
            total_tokens = list(ideal_stats[b_type].keys())
            sel_tokens = list(sel_stats[b_type].keys())
            rnd_tokens = list(rnd_stats[b_type].keys())
            print(f'\ntype: {b_type}')
            print(f'total tokens: {len(total_tokens)}')
            print(f'random ratio: {len(rnd_tokens) / len(total_tokens)}')
            #print(f'rand diff: {set(total_tokens).difference(set(sel_tokens))}')
            print(f'selected ratio: {len(sel_tokens) / len(total_tokens)}')
            #print(f'sell diff: {set(total_tokens).difference(set(sel_tokens))}')

    print('Done')
exit()
