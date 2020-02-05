import json
from kafka import KafkaConsumer, KafkaProducer


class Producer:
    producer = None

    def __init__(self, servers):
        """
        Class Producer para Kafka
        Args:
            servers: tuple com os servers
        """
        self.factory_connection(servers)

    def send_message(self, message, topic):
        """
        Metodo para enviar mensagens a consumers
        Args:
            message: mensagem a ser enviada
            topic: tópico que receberá a mensagem

        Returns: void
        """
        self.producer.send(topic, value=message)
        self.producer.flush()

    def factory_connection(self, servers):
        """
        Metodo de factory de conexão para o producer
        Args:
            servers: list com os servers que serão conectados
        Returns: void
        """
        self.producer = KafkaProducer(
            bootstrap_servers=servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )


class Consumer:

    consumer = None

    def __init__(self, servers, topics):
        """
        Class Consumer para Kafka
        Args:
            servers: list com servidores
            topics: tuple com os topicos a serem conectados
        """
        if self.consumer is None:
            self.factory_connection(servers, topics)

    def factory_connection(self, servers, topics):
        """
        Metodo de factory de conexão para o consumer
        Args:
            servers: list com os servers que serão conectados
            topics: tuple com os tópicos do kafka requeridos
        Returns: void
        """
        self.consumer = KafkaConsumer(
            bootstrap_servers=servers,
            group_id='my-group',
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        self.consumer.subscribe(topics)
