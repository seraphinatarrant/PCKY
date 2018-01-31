We worked in a team of two: Ayushi & Seraphina.
We pair programmed implementing PCFG from the original CKY algorithm - we started with the example CKY baseline
in order to learn from the gold standard version. This was pretty easy - except that we didn't initially notice the root
symbol was hard-coded :). So we updated this to be a global based on the grammar we read in. We also added probabilities
to the rule object.
We designed the PCKY to maintain and update probabilities as the algorithm progressed through the table via storing the
cumulative probability in the backpointers as CKY progresses. This way, when we complete the CKY table, we can instantly
select the most probable parse with an argmax over all the start symbols in the upper right cell and only traverse back
the winning parse, which is much faster than maintaining all of them. We also recursively select the most probable parse
as we traverse back through the table in out get_best_tree function.
If no valid parses are found (ie no root symbol in upper right), we return an empty list.


Then Ayushi wrote the script to induce the PCFG.
We brainstormed all of the possible improvements we could do, and decided to do parent annotation, because it is grammar
agnostic and made intuitive sense. We considered doing lexicalisation and OOV but decided against it in order to
maintain grammar agnosticism as our experiments with both didn't successfully develop anything that was grammar
independent.
Then Ayushi added parent annotation and Seraphina changed the PCKY algorithm to print out without the parents and so that it
could be compared against gold like the baseline. We co-debugged.

The parent annotation was interesting in that it significantly reduced the number of sentences that received a valid
parse - likely due to the sparsity it introduced. However, the sentences that were recognised were much more accurate,
with +7% precision, recall, and F measure in bracketing and +18% complete matches to the gold standard. It additionally
significantly reduced crossing dependencies. It did not however improve total tagging accuracy.
