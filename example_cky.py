#!/usr/bin/env python3
"""
Basic Python PCKY parser implementation - takes a CNF (Chomsky Normal Form) Probabilistic Grammar and an input, and
uses the grammar to parse the input sentences, returning the maximum probability parse.

Uses NLTK to tokenize the input and to validate that the grammar is CNF.

Command to run: example_cky.py pcfg_file.cfg test_sentence_file output_parse_file

"""
import sys, string, nltk
import collections
import argparse
import re

# -------------------------------------------
# Root Symbol Definition
# -------------------------------------------
ROOT_SYMBOL = None


def pprint(tree):
    """
    Prints a cleanly indented version of the parse tree.
    :param tree:
    :return:
    """
    out_str = ''
    indent_depth = 0
    indent_span = '  '
    open_brackets = tree.split('(')
    open_count = 0
    for open_bracket in open_brackets:
        if open_count > 0:
            ct = 0
            while ct < indent_depth:
                out_str += indent_span
                ct += 1
            out_str += '('
        if open_bracket.find(')') >= 0:
            closes = open_bracket.split(')')
            close_count = 0
            while close_count < len(closes)-1:
                out_str += closes[close_count] + ')'
                indent_depth -= 1
                close_count += 1
            out_str += '\n'
        else:
            out_str += open_bracket+'\n'
        if open_count > 0:
            indent_depth += 1

        open_count += 1

    print(out_str+'\n')


class Rule(object):
    """
    Representation of a rule A -> B ... C
    """
    def __init__(self, head, symbols, prob=1.0):
        self.head = head
        self.symbols = symbols
        self._key = head, symbols
        self.prob = prob

    def __eq__(self, other):
        return self._key == other._key

    def __hash__(self):
        return hash(self._key)

def get_grammar(nltk_grammar):
    """
    Build a grammar from strings like "X -> Y Z "
    :type grammar_data: str
    :rtype: set[Rule]
    """
    #check if grammar is cnf, if not abort
    if not nltk_grammar.is_chomsky_normal_form():
        sys.exit('Grammar needs to be converted to CNF before using CKY')
    global ROOT_SYMBOL
    ROOT_SYMBOL = nltk_grammar.start()
    grammar = set()
    for prod in nltk_grammar.productions():
        head = prod.lhs() # Nonterminal object S
        symbols = prod.rhs() # tuple of nonterminal objects (NP, VP)
        prob = prod.prob() #float
        grammar.add(Rule(head, symbols, prob))
    return grammar


def get_best_prob(all_backpointers_list):
    return max(all_backpointers_list, key=lambda x: x[3])

def cky_table(grammar: set, words):
    """
    Given a grammar and the input words, build both the
    nonterminal table and backpointer table.
    :type grammar: set[rule]
    """
    nonterminal_table = collections.defaultdict(set)
    backpointer_table = collections.defaultdict(lambda: {})
    for j, word in enumerate(words):
        j += 1
        # find all rules for the current word
        for rule in grammar:
            if rule.symbols == (word,):
                nonterminal_table[j - 1, j].add(rule.head)
                backpointer_table[j - 1, j][rule.head] = []
                back = None, None, None, rule.prob
                backpointer_table[j - 1, j][rule.head].append(back)

        # for each span of words ending at the current word,
        # find all splits that could have formed that span
        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                # if the two constituents identified by this
                # split can be combined, add the combination
                # to the table
                for rule in grammar:
                    if len(rule.symbols) == 2:
                        l_sym, r_sym = rule.symbols
                        if l_sym in nonterminal_table[i, k]:
                            if r_sym in nonterminal_table[k, j]:
                                # store prob of rule expansion * prob of both children
                                nonterminal_table[i, j].add(rule.head)
                                #pick most max of backpointer
                                new_prob = rule.prob * get_best_prob(backpointer_table[i, k][l_sym])[3]\
                                           * get_best_prob(backpointer_table[k, j][r_sym])[3]
                                back = k, l_sym, r_sym, new_prob
                                if rule.head not in backpointer_table[i, j]:
                                    backpointer_table[i, j][rule.head] = []
                                if back not in backpointer_table[i, j][rule.head]:
                                    backpointer_table[i, j][rule.head].append(back)
    #check if valid parse found
    if ROOT_SYMBOL in nonterminal_table[0, len(words)]:
        # return tree
        return get_best_tree(0, len(words), ROOT_SYMBOL, backpointer_table, words)
    else:
        return []


def get_best_tree(row, col, symbol, backpointer_table, words):
    """
    iterates through all backpointers of start symbol in top right cell of nonterminal table and finds the most
    probable parse (which was determined by the CKY algorithm)
    :param ROOT_SYMBOL:
    :param backpointer_table:
    :return:
    """

    all_backpointers_list = backpointer_table[row, col][symbol]
    # returns bp with highest prob
    winner = max(all_backpointers_list, key=lambda x: x[3])

    mid, head1, head2, prob = winner
    if mid is head1 is head2 is None:
        return ['(%s %s)' % (symbol, words[row])]
    trees = []
    trees_left = get_best_tree(row, mid, head1, backpointer_table, words)
    trees_right = get_best_tree(mid, col, head2, backpointer_table, words)
    for tree_l in trees_left:
        for tree_r in trees_right:
            trees.append('(%s %s %s)' % (symbol, tree_l, tree_r))

    return(trees)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('grammarfile', help='Path to the CFG file to load.')
    p.add_argument('sentfile', help='Path to the sentences to parse.')
    p.add_argument('outputfile', help='filename to store output parses.')

    args = p.parse_args()

    grammar_cnf = get_grammar(nltk.data.load('file:{}'.format(args.grammarfile)))
    output_file = open(args.outputfile, 'w')
    # TODO : if it ever doesn't come up with a parse it stops parsing the whole file. Need to make sure it instead prints
    # a blank line
    with open(args.sentfile, 'r') as sent_f:

        for sent in sent_f.readlines():
            sent = sent[:-1]
            words = nltk.word_tokenize(sent)
            if len(words) > 0:
                trees = cky_table(grammar_cnf, words)

                # Print the sentence and number of parses.
                #print(sent + ' ['+str(len(trees))+' parse(s)]\n')

                # Prettyprint the resulting parses.
                for tree in trees:
                    output_file.write('{}\n'.format(tree))
                    # we are not using the pretty print since we want our tree on one line
                    #pprint(tree)
            else:
                output_file.write('\n')

main()
