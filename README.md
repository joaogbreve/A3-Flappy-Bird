# FlappyBird - Jogo feito em Python com Pygame

FlappyBird é uma recriação do clássico jogo Flappy Bird feito utilizando a biblioteca Pygame. O jogo consiste em um pássaro que deve desviar de obstáculos e passar por tubos. O projeto também inclui um menu interativo com botões para "Começar", "Tutorial/Manual" e "Sair".

## Funcionalidades

- **Menu Inicial**: Com botões para começar o jogo, ver o tutorial/manual e sair.
- **Jogo**: Jogo de Flappy Bird com física realista de pulo e colisão.
- **Tutorial/Manual**: Explicações sobre como jogar.
- **Botões interativos**: Os botões no menu mudam de cor quando o mouse passa por cima e respondem ao clique.

## Estrutura de Pastas

/FlappyBird
├── assets
│ ├── fonts
│ ├── images
│ └── sounds
├── scr # Código-fonte do jogo
├── .gitignore # Arquivo para ignorar arquivos temporários e pastas
├── README.md # Documento explicativo do projeto
├── requirements.txt # Dependências do projeto

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/FlappyBird.git
    ```
2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1  # No Windows
    source venv/bin/activate     # No Linux/Mac
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute o jogo:
    ```bash
    python main.py
    ```

## Contribuindo

1. Faça um fork do repositório
2. Crie uma nova branch (`git checkout -b feature/nova-feature`)
3. Faça suas modificações e commit (`git commit -am 'Adicionando nova feature'`)
4. Envie para o repositório remoto (`git push origin feature/nova-feature`)
5. Abra um pull request

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## Créditos

Asset: https://github.com/samuelcust/flappy-bird-assets