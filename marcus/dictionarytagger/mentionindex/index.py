from docria import Document, MsgpackCodec
from typing import List
import os.path
from py4j.java_gateway import GatewayParameters, JavaGateway


class MentionIndex:
    def get_java_file(self, path: str):
        # Here we do the py4j equivalent for new java.io.File(path)
        return self.jvm.java.io.File(os.path.abspath(path))

    def connect_jvm(self, port: int):
        gateway_parameters = GatewayParameters(port=port, auto_convert=True, auto_field=True)
        gateway = JavaGateway(gateway_parameters=gateway_parameters)
        app = gateway.entry_point
        self.jvm = gateway.jvm
        self.app = app
        self.gateway = gateway
        return True

    def build_index(self, dictionary: str, output: str):
        self.app.buildIndex(self.get_java_file(dictionary), self.get_java_file(output))

    def build_keyed_index(self, dictionary: str, output: str):
        self.app.buildKeyedIndex(self.get_java_file(dictionary), self.get_java_file(output))

    def load_index(self, dictionary: str):
        return self.app.loadIndex(self.get_java_file(dictionary))

    def load_keyed_index(self, dictionary: str):
        return self.app.loadKeyedIndex(self.get_java_file(dictionary))

    def process(self, indx, doc: Document):
        binary_doc = MsgpackCodec.encode(doc)  # Encode the document into binary representation
        search_binary_doc = self.app.search(indx, binary_doc)  # Process it in java
        return MsgpackCodec.decode(search_binary_doc)  # Decode it back into python

    def process_tokenized(self, indx, sentences: List[List[str]]):
        """
        :param indx: the index to use
        :param sentences: list of sentences with tokens
        :return: Document
        """
        search_binary_doc = self.app.searchPreTokenized(indx, doc)  # Process it in java
        return MsgpackCodec.decode(search_binary_doc)  # Decode it back into python
