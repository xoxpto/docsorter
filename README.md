docsorter

CLI para organizar ficheiros por ano/mês: pega nos ficheiros de uma pasta origem e move (ou copia) para DEST/AAAA/MM/ com base na data.

Prioridade de deteção de data:

padrões no nome do ficheiro → 2) EXIF (imagens) → 3) data de modificação do ficheiro.

✨ Exemplos rápidos

Organizar a sério (move):

docsorter "C:\Users\André\Downloads" "C:\Arquivo" --verbose


Simular sem tocar em nada:

docsorter "C:\Users\André\Downloads" "C:\Arquivo" --dry-run --verbose


Copiar (em vez de mover), útil para testar:

docsorter "C:\Users\André\Downloads" "C:\Arquivo_TESTE" --copy --verbose


Usar um ficheiro de configuração:

docsorter "C:\Users\André\Downloads" "C:\Arquivo" --config .\my.config.yaml --verbose

🧩 Instalação
Opção recomendada (isolada) — pipx

Mantém a CLI num ambiente próprio e adiciona o comando docsorter ao PATH.

python -m pip install --user pipx
python -m pipx ensurepath
# abre uma nova consola PowerShell
pipx install "git+https://github.com/xoxpto/docsorter@main"


Atualizar:

pipx reinstall "git+https://github.com/xoxpto/docsorter@main"


Desinstalar:

pipx uninstall docsorter

Alternativa — pip (global/venv)
pip install "git+https://github.com/xoxpto/docsorter@main"


Requisitos: Python ≥ 3.10.

🖥️ Uso
docsorter [OPTIONS] SOURCE DEST

Organiza ficheiros de SOURCE para DEST/AAAA/MM/.

Opções:
  --config, -c PATH    Ficheiro YAML com regras
  --copy               Copiar em vez de mover
  --dry-run            Mostrar o plano sem alterar nada
  --verbose/--no-verbose
  --help

⚙️ Configuração (YAML)

Exemplo de my.config.yaml:

# Pastas (dentro de SOURCE) a ignorar
exclude_dirs:
  - "B668MHNGIS"
  - "content"
  - "Pure 1.40 Highres"

# Extensões permitidas (sem ponto, minúsculas)
extensions: ["pdf","docx","xlsx","jpg","jpeg","png","txt"]

# Prioridade de deteção de data
prefer_order: ["filename","exif","mtime"]

Como a data é detetada

filename: procura padrões comuns no nome, p.ex.
YYYY-MM-DD, YYYY_MM_DD, YYYYMMDD, YYYY-MM, YYYY_MM, YYYYMM.
(Se não encontrar, passa ao próximo método.)

exif: data de captura para imagens com EXIF (normalmente JPEG).
PNG raramente tem EXIF — nesses casos avança para mtime.

mtime: data de modificação do ficheiro no sistema.

🔒 Segurança

Sem chamadas de rede; atua apenas sobre SOURCE/DEST que passas.

Recomenda-se --dry-run antes de mover; e --copy para ensaios.

Não precisa de privilégios de administrador.

Instalar com pipx isola a ferramenta do resto do Python do sistema.

🧪 Exemplos de fluxos

Teste seguro:
docsorter "C:\Downloads" "C:\Arquivo_TESTE" --copy --verbose

Simular antes de mover:
docsorter "C:\Downloads" "C:\Arquivo" --dry-run --verbose

Ignorar certas pastas e limitar extensões:
docsorter "C:\Downloads" "C:\Arquivo" --config .\my.config.yaml --verbose

🛠️ Desenvolvimento

Clonar e instalar em modo editável:

git clone https://github.com/xoxpto/docsorter
cd docsorter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .


Correr testes:

pytest -q

🚧 Limitações conhecidas

Não lê EXIF em PNG; nesses casos cai para mtime.

Não extrai ficheiros de zip/rar/7z; apenas trabalha com ficheiros “normais”.

Padrões de datas muito “exóticos” podem não ser reconhecidos no nome.

📄 Licença

MIT — ver LICENSE