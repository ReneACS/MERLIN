import wikipedia
import os
from gensim.summarization.bm25 import BM25
import torch
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
#uses stanford question answering database to shorthen wiki andswers and give more precice answers
class TextExtractor:

    __pageTitle: str
    __pageId: str

    def __init__(self, pageTitle, pageId):
        self.__pageTitle = pageTitle
        self.__pageId = pageId

    def extract(self):
        fileName = "./text/" + self.__pageTitle + ".txt"
        if not os.path.isfile(fileName):
            page = wikipedia.page(title=self.__pageTitle, pageid=self.__pageId)
            f = open(fileName, "w")
            f.write(page.content)
            f.close()

    def getText(self):
        f = open("./text/" + self.__pageTitle + ".txt", "r")
        return f.read()


class TextExtractorPipe:

    __textExtractors: [TextExtractor]

    def __init__(self):
        self.__textExtractors = []

    def addTextExtractor(self, textExtractor: TextExtractor):
        self.__textExtractors.append(textExtractor)

    def extract(self) -> str:
        result = ''
        for textExtractor in self.__textExtractors:
            result = result + textExtractor.getText()
        return result

class QuestionProcessor:


    def __init__(self, nlp):
        self.pos = ["NOUN", "PROPN", "ADJ"]
        self.nlp = nlp


    def process(self, text):
        tokens = self.nlp(text)
        return ' '.join(token.text for token in tokens if token.pos_ in self.pos)

class ContextRetriever:

    def __init__(self, nlp, numberOfResults):
        self.nlp = nlp
        self.numberOfResults = numberOfResults

    def tokenize(self, sentence):
        return [token.lemma_ for token in self.nlp(sentence)]


    def getContext(self, sentences, question):
        documents = []
        for sent in sentences:
            documents.append(self.tokenize(sent))

        bm25 = BM25(documents)

        scores = bm25.get_scores(self.tokenize(question))
        results = {}
        for index, score in enumerate(scores):
            results[index] = score

        sorted_results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}
        results_list = list(sorted_results.keys())
        final_results = results_list if len(results_list) < self.numberOfResults else results_list[:self.numberOfResults]
        questionContext = ""
        for final_result in final_results:
            questionContext = questionContext + " ".join(documents[final_result])
        return questionContext

class AnswerRetriever:

    def getAnswer(self, question, questionContext):
        distilBertTokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased', return_token_type_ids=True)
        distilBertForQuestionAnswering = DistilBertForQuestionAnswering.from_pretrained(
            'distilbert-base-uncased-distilled-squad')

        encodings = distilBertTokenizer.encode_plus(question, questionContext)

        inputIds, attentionMask = encodings["input_ids"], encodings["attention_mask"]

        scoresStart, scoresEnd = distilBertForQuestionAnswering(torch.tensor([inputIds]),
                                                                attention_mask=torch.tensor([attentionMask]))

        tokens = inputIds[torch.argmax(scoresStart): torch.argmax(scoresEnd) + 1]
        answerTokens = distilBertTokenizer.convert_ids_to_tokens(tokens, skip_special_tokens=True)
        return distilBertTokenizer.convert_tokens_to_string(answerTokens)