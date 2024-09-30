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
docker-compose up
```

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

## Development

### Database

We use [PostgreSQL](https://www.postgresql.org) as the database for the recipe search service. Since it is managed in Docker, you don't need to install it on your machine.

We use [Alembic](https://alembic.sqlalchemy.org) for database migrations.

When there is a change in the database schema, you need to generate a new migration script:
```bash
alembic revision -m "Your migration message"
```

Then you should be able to see the generated migration script in the `alembic/versions` directory. Take a look at the [Operation Reference](https://alembic.sqlalchemy.org/en/latest/ops.html#ops) for the available operations.

### API Protocol

We use [gRPC](https://grpc.io) and [Protocol Buffers](https://protobuf.dev) for the communication between the services.

When you make changes to the `.proto` files in the `protos` directory, you need to regenerate the Python files in the `grpcs` directory:
```bash
python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. --pyi_out=. ./protos/*.proto
```

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

### Pushing Changes

Set your branch's upstream branch to be the same branch on the remote repository on GitHub.
```bash
git push -u origin <branch>
```

After the first time you set the upstream branch, you can simply push without specifying the branch.
```bash
git push
```
