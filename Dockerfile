FROM mongo:4.4-bionic

# Definindo um nome de usuário e senha vazios para acesso livre
ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=root

# Definindo o volume para persistência de dados
VOLUME /data/db

# Expondo a porta 27017 para acesso externo
EXPOSE 27017

# Definindo o comando de entrada para iniciar o MongoDB
CMD ["mongod", "--auth", "--port", "27017"]
