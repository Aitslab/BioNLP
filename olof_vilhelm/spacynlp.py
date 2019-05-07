import spacy
import neuralcoref
import datetime
from scrape_abstracts import get_abstracts


def find_prep(root, string, depth):
    print(string, depth)
    children = root.children
    for child in children:
        print(child, child.dep_)
        if child.dep_ == 'compound' or child.dep_ == 'nmod' or child.dep_ == 'amod':
            string = child.text + " " + string #  Ofärdig - här läggs nouns dubbelt
        if child.dep_ == 'prep':
            string += " " + child.text
            string = find_prep(child, string, depth+1) ## den når hit men rekursionen går inte
    return string


if __name__ == '__main__':
    print("1")
    # spacy.prefer_gpu()
    nlp = spacy.load("en_core_web_sm")
    neuralcoref.add_to_pipe(nlp)
    print("2")
    abstracts = get_abstracts('pubmed19n0651.xml')
    """
    for article in root:
        pmid = ""
        abstract = ""
        for xid in article.iter("PMID"):
            pmid = xid.text
        for txt in article.iter("AbstractText"):
            abstract = txt.text
        if abstract != "" and pmid != "":
            abstracts[pmid] = abstract
    """
    keywords = {'activates', 'activate', 'activating', 'induces', 'induce', 'inducing', 'impairs', 'impair', 'impairing',
                'inhibits', 'inhibit', 'inhibitors', 'inhibitor', 'inhibiting', 'promotes', 'promote', 'promoting',
                'localizes', 'localize', 'localizing', 'leading', 'lead', 'leads', 'enhances', 'enhance', 'enhancing',
                'activator', 'stabilizes', 'stabilize', 'stabilizing', 'agonist', 'increase', 'increases', 'increasing',
                'mediates', 'mediate', 'mediator', 'executes', 'execute', 'causes', 'causing', 'cause', 'inactivate',
                'inactivates', 'block', 'blocks', 'repress', 'represses', 'antagonist', 'reduces', 'reduce', 'reducing',
                'disrupts', 'disrupt', 'disrupting', 'prevents', 'prevent', 'preventing', 'participates', 'contributes',
                'participate', 'contribute', 'participating', 'contributing'}  # should contain all keywords?
    # could use lemma instead to skip all other forms of words

    # large file holds 3960 mentions of keywords?, small file only 21
    cnt = 0
    print("3")
    print(str(datetime.datetime.now()).split('.')[0])
    for abstract in abstracts:
        nsubjstring = ""
        keyword = ""
        dobjstring = ""
        norigin = ""
        dorigin = ""
        text = abstracts[abstract] #  meningen under är för att testa så att det fungerar
        text = 'Interleukin 1 (IL-1) is a 17 kDa protein highly conserved through evolution and is a key mediator of inflammation, fever and the acute-phase response. IL-1 has important functions in the innate immune defense against microbes, trauma and stress, and is also an effector molecule involved in tissue destruction and fibrosis. The inhibition of IL-1 action has clinical efficacy in many inflammatory diseases, such as hereditary autoinflammatory disorders, familial hereditary fever, gout, rheumatoid arthritis and type 2 diabetes mellitus (T2DM). The latter is a common metabolic condition caused by insulin resistance and pancreatic beta-cell failure, the causes of both of which have inflammatory components. IL-1 signaling has roles in beta-cell dysfunction and destruction via the NFkappaB and mitogen-activated-protein-kinase pathways, leading to endoplasmic reticulum and mitochondrial stress and eventually activating the apoptotic machinery. In addition, IL-1 acts on T-lymphocyte regulation. The modulating effect of IL-1 on the interaction between the innate and adaptive immune systems and the effects of IL-1 on the beta-cell point to this molecule being a potential interventional target in autoimmune diabetes mellitus. Genetic or pharmacological abrogation of IL-1 action reduces disease incidence in animal models of type 1 diabetes mellitus (T1DM) and clinical trials have been started to study the feasibility, safety and efficacy of IL-1 therapy in patients with T1DM. Here, we review the rationale for blocking IL-1 in patients with T1DM.'
        doc = nlp(text)  # break down an abstract to sentences
        print(text)
        for token in doc:
            print(token.text, token.dep_, token.head.text, token.head.pos_,
                  [child for child in token.children])
        #print(doc._.coref_clusters)
        #for cluster in doc._.coref_clusters:
            #print(cluster.mentions)
        #print("Abstract ", abstract, ": ", abstracts[abstract], '\n')
        for chunk in doc.noun_chunks:
            # print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
            if (chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'nsubjpass') and chunk.root.head.text in keywords:
                nsubjstring = chunk.text
                norigin = chunk.text
                nsubjstring = find_prep(chunk.root,nsubjstring, 0)
                for cluster in doc._.coref_clusters:
                    a = []
                    a.append(cluster.mentions)
                    for mention in a:
                        if chunk.text == mention:
                            nsubjstring = cluster.mentions[1]

                keyword = chunk.root.head.text
                for chunk2 in doc.noun_chunks:
                    if chunk2.root.dep_ == 'dobj' and chunk2.root.head.text == keyword:
                        dobjstring = chunk2.text
                        dorigin = chunk2.text

                        dobjstring = find_prep(chunk2.root, dobjstring, 0)
                        for cluster in doc._.coref_clusters:
                            b = []
                            b.append(cluster.mentions)
                            for mention in b:
                                if chunk2.text == mention:
                                    dobjstring = cluster.mentions[1]


                        if nsubjstring != "" or dobjstring != "":
                            print("With coreferencing:")
                            print(nsubjstring, keyword, dobjstring)
                            print("Without coreferencing: ")
                            print(norigin, keyword, dorigin, '\n')
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
    print(str(datetime.datetime.now()).split('.')[0])
    print("keywords found: ", cnt)
