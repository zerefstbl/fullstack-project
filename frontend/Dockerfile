# Escolha uma imagem base com Node.js
FROM node:14

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo 'package.json' e 'package-lock.json' (se disponível)
COPY package*.json ./

# Instale as dependências do projeto
RUN npm install

# Copie os arquivos do projeto para o diretório de trabalho
COPY . .

# Construa o aplicativo para produção
RUN npm run build

# Exponha a porta que seu app Node.js vai rodar
EXPOSE 3000
