# english2hindi

Hindi is a relatively free-word order language and generally tends to follow SOV (Subject-Object-Verb) order and English tends to follow SVO (Subject-Verb-Object) word order.
Research has shown that pre-ordering source language to conform to target language word order significantly improves translation quality.
We created a re-ordering module for transforming an English sentence to be in the Hindi order based on reordering rules provided by Anusaaraka. The reordering rules are based on parse output produced by the Stanford Parser.

The transformation module requires the text to contain only  surface form of words, however, we  extended it to support surface form along with its factors such as lemma and Part of Speech (POS).


{Input} : the girl in blue shirt is my sister

{Output} : in blue shirt the girl is my sister.

{Hindi} : neele shirt waali ladki meri bahen hai
        ( blue) ( shirt) (Mod)(girl)(my)(sister)(Vaux)

With this transformation, the English sentence is structurally closer to the Hindi sentence which  leads to better phrase alignments. The model trained with the transformed corpus produces a new baseline score of 21.84 BLEU score an improvement over the earlier baseline of 20.04 BLEU points.
