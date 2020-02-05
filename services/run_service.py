import threading
from clients import kafka_client
from settings import settings
from utils import file_util, rules_util
from copy import deepcopy


class RunService:

    logger = None
    dictionary_rules = None

    def __init__(self):

        self.logger = settings.LOGGER

        self.logger.info('Inicializando Middleware')
        self.read_rules()
        self.logger.info('Middleware Iniciado com sucesso')

    def read_rules(self):
        self.logger.info("Iniciando leitura do arquivo de Regras")

        self.dictionary_rules = file_util.read_json(settings.RULES)

        if self.dictionary_rules == {}:
            raise Exception("Arquivo de regras vazio")

        self.logger.info("Leitura finalizada")

    def get_topics(self):
        self.logger.info("Buscando topicos")
        return tuple(x['topic'] for x in self.dictionary_rules.get('configs'))

    def get_rules(self, topic):
        self.logger.info("Buscando regras do topico {}".format(topic))
        return [x for x in self.dictionary_rules.get('configs') if x['topic'] == topic][0]

    def post_receipt(self, message, topic):
        try:
            topic_rules = self.get_rules(topic)

            self.logger.info("Iniciando filter do topico {}".format(topic))
            if rules_util.is_payload_accept(message, topic_rules.get('filter')):
                self.logger.info("Filter realizado com sucesso")

                self.logger.info("Iniciando Classification do topico {}".format(topic))

                new_topic = rules_util.classification_data(message, topic_rules.get('classification'))

                self.logger.info("Classification realizado com sucesso")

                self.logger.info("Iniciando Map do topico {}".format(topic))

                new_message = rules_util.model_map_util(deepcopy(topic_rules.get('map_model')), message)

                self.logger.info("Map realizado com sucesso")

                self.send_message(new_message, new_topic)
            else:
                self.logger.error('Payload nao aceito pelo metodo definido no filter')

        except Exception as ex:
            self.logger.exception(ex)

    def send_message(self, message, new_topic):
        self.logger.info("Abrindo conexao Producer com o topico {}".format(new_topic))

        producer = kafka_client.Producer(settings.KAFKA_SERVER)

        self.logger.info("Abrindo conexao Producer com o topico {}".format(new_topic))

        self.logger.info("Enviando mensagem para o  Producer com o topico {}".format(new_topic))

        producer.send_message(message, new_topic)

        self.logger.info("Mensagem enviada com sucesso")

    def run(self):
        try:
            self.logger.info("Inicializando conexao com o Servidor do Kafka")

            consumer = kafka_client.Consumer(settings.KAFKA_SERVER, self.get_topics())

            self.logger.info("Conectado aguardando Mensagens")

            for message in consumer.consumer:
                self.logger.info("Nova mensagem")
                self.post_receipt(message.value.get('payload'), message.topic)
        except Exception as exc:
            self.logger.exception(exc)
