# IntelliCook Recipe Search

This is the recipe search service of IntelliCook.

## Environment Setup

### Docker

We use [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose) to manage the environment in both development and production.

Before starting anything, you have to define the environment variables in the `.env` file. You can copy the `.env.example` file and fill in the values.
```bash
cp .env.example .env
```

With Docker Compose, you can run the services in the `docker-compose.yml` file:
```bash
docker compose up
```

**Note**: Your configurations may convert the line endings of `entrypoint.sh` to CRLF. You need to convert it back to LF for docker to run the script.

### Python

We use Python 3.12.2, so make sure you have that installed.

You could use [pyenv](https://github.com/pyenv/pyenv) or [pyenv-win](https://github.com/pyenv-win/pyenv-win) (Windows is not recommended to install pyenv because it does not get native support) to manage your Python versions.

Install the Python version you want to use.
```bash
pyenv install 3.12.2
```

Specify the version for this directory.
```bash
pyenv local 3.12.2
```

To check your Python version, run `python --version` in your terminal.
```bash
python --version
```
Or you may need to specify the version explicitly if you didn't use pyenv or have multiple versions installed.
```bash
python3 --version
```

### Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

It is highly recommended to use the [venv](https://docs.python.org/3/library/venv.html) module that comes with Python.

To create a virtual environment in the `.venv` directory, run:
```bash
python -m venv .venv
```

Activate the environment.
```bash
# Linux, Bash, Mac OS X
source .venv/bin/activate
# Linux, Fish
source .venv/bin/activate.fish
# Linux, Csh
source .venv/bin/activate.csh
# Linux, PowerShell Core
.venv/bin/Activate.ps1
# Windows, cmd.exe
.venv\Scripts\activate.bat
# Windows, PowerShell
.venv\Scripts\Activate.ps1
```

Install the dependencies.
```bash
# Install the dependencies of PyTorch
pip install numpy==2.1.2 pillow==11.0.0 Jinja2==3.1.4

# Install the CPU version of PyTorch if you want to use it
pip install torch==2.5.1+cpu torchaudio==2.5.1+cpu torchvision==0.20.1+cpu \
    -i https://download.pytorch.org/whl/cpu

# Install the main requirements
pip install -r requirements.txt
```

When you want to deactivate the virtual environment.
```bash
deactivate
```

### Lint and Pre-commit

We use [Flake8](https://flake8.pycqa.org) and [ISort](https://pycqa.github.io/isort/) for the coding style and guidelines. The style is then enforced by [pre-commit](https://pre-commit.com).

Finish the environment setup above (especially installing the dependencies with pip) before using pre-commit.

Install and setup pre-commit.
```bash
pre-commit install
```

To run pre-commit manually (only scans staged files).
```bash
pre-commit run --all-files
```

Remember to stage files again if there are any changes made by the pre-commit hooks or by you.
```bash
git add .
```

### VS Code Settings

You can add a workspace setting to automatically format your code on save using the black formatter.

You need to have the [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) VS Code extension installed.

Bring up the command palette with Ctrl+Shift+P(Windows/Linux) / Cmd+Shift+P(Mac) and search for "Preferences: Open Workspace Settings (JSON)".

Then replace the content with the following:
```json
{
    "editor.formatOnSave": true,
    "python.envFile": "",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
    },
    "black-formatter.args": [
        "--line-length",
        "79",
        "--preview",
        "--enable-unstable-feature",
        "string_processing"
    ],
}
```

**Important**: The `python.envFile` option is quite important, because it will set the environment variables from the `.env` file automatically in the terminal, but when we run the tests, we want to use the `.env.test` file instead. So we need to set it to an empty string.

## Development

### Clone Repository

First clone the repository.
```bash
git clone git@github.com:<username>/<repository>.git
```

**Important**: You may need to setup SSH keys for your GitHub account. See [this guide](https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) for more information.

### Checkout Branch

Then checkout the branch you want to work on.
```bash
git checkout <branch>
```

### Committing Changes

Commit your changes to the branch you are working on.
```bash
git add .
git commit -m "Your commit message"
```

Make any changes and stage your files again according to the pre-commit hooks.

**Important**: Do not commit the index file! It is recommended to name the index file with extension `.faiss` because it is set in `.gitignore`.

### Pushing Changes

Set your branch's upstream branch to be the same branch on the remote repository on GitHub.
```bash
git push -u origin <branch>
```

After the first time you set the upstream branch, you can simply push without specifying the branch.
```bash
git push
```

### Database

We use [PostgreSQL](https://www.postgresql.org) as the database for the recipe search service. Since it is managed in Docker, you don't need to install it on your machine.

We use [Alembic](https://alembic.sqlalchemy.org) for database migrations.

When there is a change in the database schema, you need to generate a new migration script:
```bash
alembic revision -m "Your migration message"
```

Implement the `upgrade` and `downgrade` functions in the generated migration script, you may reference the output from:
```py
from sqlalchemy.schema import CreateTable
print(CreateTable(YourModel.__table__))
```

Alternatively, you can use the `--autogenerate` flag to automatically generate the script:
```bash
alembic revision --autogenerate -m "Your migration message"
```

**Important**: For some reason, autogenerate always tries to remove the `alembic_version` table, you should remove the line that drops the table in the `upgrade` function and the line that creates the table in the `downgrade` function. If you know how to fix that, please let me know.

**Important**: If you are calling these commands from the host machine, you may want to assign a value to the `DB_OVERRIDE_CONNECTION_STRING` environment variable to something like:
```bash
postgresql+psycopg://postgres:postgres@host.docker.internal:2605/recipe_search
```

Then you should be able to see the generated migration script in the `alembic/versions` directory. Take a look at the [Operation Reference](https://alembic.sqlalchemy.org/en/latest/ops.html#ops) for the available operations.

### API Protocol

We use [gRPC](https://grpc.io) and [Protocol Buffers](https://protobuf.dev) for the communication between the services.

When you make changes to the `.proto` files in the `protos` directory, you need to regenerate the Python files in the `grpcs` directory:
```bash
python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. --pyi_out=. ./protos/*.proto
```

### GPU Acceleration

Although we can use CPU for the service, we also allows [CUDA](https://developer.nvidia.com/cuda-toolkit) for GPU acceleration.

If you already have CUDA installed on your machine, you can check the version with:
```bash
nvcc --version
```

You may need to install different versions for specific packages, including [PyTorch](https://pytorch.org) and [Faiss](https://github.com/facebookresearch/faiss). Please refer to the official documentations for [PyTorch](https://pytorch.org/get-started/locally/) and [Faiss](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md).

Alternatively, if you don't want to or cannot use CUDA, you may install their CPU versions. The CPU versions are by default installed in the `requirements.txt` file.

### Testing

We use [Pytest](https://pytest.org) for testing.

The requirements for testing is different, it is in the `test-requirements.txt` file.

The test requirements is a subset of the main requirements without the AI related packages, the imports of them are mocked in `tests/conftest.py`.

If you want to change the test requirements, you should add entries in `test-excluded-requirements.txt` then geneerate the `test-requirements.txt` file:
```bash
.\generate-test-requirements.ps
```

To run the tests:
```bash
pytest
```
