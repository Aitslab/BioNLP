import spacy
import neuralcoref
import datetime
from scrape_abstracts import get_abstracts


def find_prep(doc, root, depth=0):
    children = root.children
    prep_children = doc[root.i: root.i + 1]
    for child in children:
        print("\t", child.i, child.text, child.dep_)
        if child.dep_ == 'compound' or child.dep_ == 'nmod' or child.dep_ == 'amod':
            start = min (child.i,  prep_children[0].i)
            end = max(child.i, prep_children[-1].i)
            prep_children = doc[start: end]  # Ofärdig - här läggs nouns dubbelt
        if child.dep_ == 'prep':
            #prep_children = doc[prep_children[0].i: child.i + 1]
            child_preps = find_prep(doc, child, depth + 1)
            start = min(child_preps[0].i, prep_children[0].i)
            end = max(child_preps[-1].i, prep_children[-1].i)
            prep_children = doc[start: end]  # Ofärdig - här läggs nouns dubbelt
    return prep_children


if __name__ == '__main__':
    print("Loading spacy...")
    # spacy.prefer_gpu()
    nlp = spacy.load("en_core_web_sm")
    neuralcoref.add_to_pipe(nlp)
    filename = 'corpus/pubmed19n0651.xml'
    print("Scraping abstracts from " + filename + "...")
    unfiltered_abstracts = get_abstracts(filename)
    keywords = {'activates', 'activate', 'activating', 'induces', 'induce', 'inducing', 'impairs', 'impair', 'impairing',
                'inhibits', 'inhibit', 'inhibitors', 'inhibitor', 'inhibiting', 'promotes', 'promote', 'promoting',
                'localizes', 'localize', 'localizing', 'leading', 'lead', 'leads', 'enhances', 'enhance', 'enhancing',
                'activator', 'stabilizes', 'stabilize', 'stabilizing', 'agonist', 'increase', 'increases', 'increasing',
                'mediates', 'mediate', 'mediator', 'executes', 'execute', 'causes', 'causing', 'cause', 'inactivate',
                'inactivates', 'block', 'blocks', 'repress', 'represses', 'antagonist', 'reduces', 'reduce', 'reducing',
                'disrupts', 'disrupt', 'disrupting', 'prevents', 'prevent', 'preventing', 'participates', 'contributes',
                'participate', 'contribute', 'participating', 'contributing'}  # should contain all keywords?

    print("Filtering abstracts...")
    abstracts = dict()
    for pmid in unfiltered_abstracts:
        text = unfiltered_abstracts[pmid]
        for word in text.split():
            if word in keywords:
                abstracts[pmid] = text
                break
    # could use lemma instead to skip all other forms of words

    # large file holds 3960 mentions of keywords?, small file only 21
    cnt = 0
    print("Analyzing abstracts...")
    #print(str(datetime.datetime.now()).split('.')[0])
    start_time = datetime.datetime.now()
    for abstract in abstracts:
        nsubjstring = None
        keyword = None
        dobjstring = None
        norigin = None
        dorigin = None
        text = abstracts[abstract] #  meningen under är för att testa så att det fungerar
        text = 'Interleukin 1 (IL-1) is a 17 kDa protein highly conserved through evolution and is a key mediator of inflammation, fever and the acute-phase response. IL-1 has important functions in the innate immune defense against microbes, trauma and stress, and is also an effector molecule involved in tissue destruction and fibrosis. The inhibition of IL-1 action has clinical efficacy in many inflammatory diseases, such as hereditary autoinflammatory disorders, familial hereditary fever, gout, rheumatoid arthritis and type 2 diabetes mellitus (T2DM). The latter is a common metabolic condition caused by insulin resistance and pancreatic beta-cell failure, the causes of both of which have inflammatory components. IL-1 signaling has roles in beta-cell dysfunction and destruction via the NFkappaB and mitogen-activated-protein-kinase pathways, leading to endoplasmic reticulum and mitochondrial stress and eventually activating the apoptotic machinery. In addition, IL-1 acts on T-lymphocyte regulation. The modulating effect of IL-1 on the interaction between the innate and adaptive immune systems and the effects of IL-1 on the beta-cell point to this molecule being a potential interventional target in autoimmune diabetes mellitus. Genetic or pharmacological abrogation of IL-1 action reduces disease incidence in animal models of type 1 diabetes mellitus (T1DM) and clinical trials have been started to study the feasibility, safety and efficacy of IL-1 therapy in patients with T1DM. Here, we review the rationale for blocking IL-1 in patients with T1DM.'
        doc = nlp(text)  # break down an abstract to sentences
        print(text + "\n")
        for i in range(len(doc)):
            token = doc[i]
            #tc_i_e = len(doc[0:i + 1].text)
            #tc_i_s = tc_i_e - len(token.text)
            print(token.i, token.text, token.dep_, token.head.text, token.head.pos_,
                  [child for child in token.children])
            text += token.text + " "

        for chunk in doc.noun_chunks:
            if (chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'nsubjpass') and chunk.root.head.text in keywords:
                nsubjstring = chunk
                norigin = chunk
                nsubjstring = find_prep(doc, chunk.root)
                for cluster in doc._.coref_clusters:
                    a = []
                    a.append(cluster.mentions)
                    for mention in a:
                        mention_is = list(set(t.i for t in span) for span in mention)
                        chunk_is = set(t.i for t in chunk)
                        if any(chunk_is.issuperset(m) or chunk_is.issubset(m) for m in mention_is):
                            print("replaced nsubjstring (chunk) '" + nsubjstring + "' with '" + cluster.mentions[1].text + "'")
                            nsubjstring = cluster.mentions[1]

                keyword = chunk.root.head
                for chunk2 in doc.noun_chunks:
                    if chunk2.root.dep_ == 'dobj' and chunk2.root.head == keyword:
                        dobjstring = chunk2
                        dorigin = chunk2
                        dobjstring = find_prep(doc, chunk2.root)
                        for cluster in doc._.coref_clusters:
                            b = []
                            b.append(cluster.mentions)
                            for mention in b:
                                mention_is = list(set(t.i for t in span) for span in mention)
                                chunk2_is = set(t.i for t in chunk2)
                                if any(chunk2_is.issuperset(m) or chunk2_is.issubset(m) for m in mention_is):
                                    print("replaced dobjstring (chunk2) '" + dobjstring + "' with '" + cluster.mentions[1].text + "'")
                                    dobjstring = cluster.mentions[1]

                        if nsubjstring is not None or dobjstring is not None:
                            print("With coreferencing:")
                            print(nsubjstring.text, keyword.text, dobjstring.text)
                            print("Without coreferencing: ")
                            print(norigin.text, keyword.text, dorigin.text, '\n')
                cnt += 1
        break #  bara för att testa en enda mening

        """
        # chunking strategy - take one sentence at a time, chunk, and match nsubj and dobj with the keyword
        for s in doc.sents:
            sent = nlp(s.text)  # break down a sentence into deprels, POS, NEr etc
            nsubjstring = ""
            keyword = ""
            dobjstring = ""
            for chunk in sent.noun_chunks:
                if chunk.root.dep_ == 'nsubj' and chunk.root.head.text in keywords:
                    nsubjstring = chunk.text
                    keyword = chunk.root.head.text
                    cnt += 1
                if chunk.root.dep_ == 'dobj' and chunk.root.head.text in keywords:
                    dobjstring = chunk.text
                    keyword = chunk.root.head.text

            if nsubjstring != "" and dobjstring != "":
                print(nsubjstring, keyword, dobjstring)
        """
    nlp_time = datetime.datetime.now() - start_time
    #print(str(datetime.datetime.now()).split('.')[0])
    print(cnt, "keywords found in", nlp_time.seconds, "seconds.")
