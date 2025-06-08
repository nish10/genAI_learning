# genAI_learning
Hands-on GenAI Essentials tutorial workspace

# GenAI Learning Workspace

## Prerequisites

* Homebrew installed
* `pyenv` available in your shell

## Python Version Management with pyenv

### 1. Install pyenv

```bash
brew install pyenv
```

### 2. Configure your shell for pyenv

Add the following to your `~/.zprofile` (or `~/.bash_profile` if you use bash):

```bash
export PYENV_ROOT="$HOME/.pyenv"
eval "$(pyenv init --path)"
```

Then add to your `~/.zshrc` (or `~/.bashrc`):

```bash
eval "$(pyenv init -)"
```

Reload your shell:

```bash
source ~/.zprofile
source ~/.zshrc
```

### 3. Create a new Python environment

1. Install a specific Python version (e.g., 3.12.0):

   ```bash
   pyenv install 3.12.0
   ```
2. Create a virtual environment named `genai-py312`:

   ```bash
   pyenv virtualenv 3.12.0 genai-py312
   ```

### 4. Activate the environment for your project

In your project root (e.g., `genAI_learning`), run:

```bash
cd ~/Projects/genAI_learning
pyenv local genai-py312
```

This writes a `.python-version` file locking this directory to use the `genai-py312` environment. To verify:

```bash
python --version  # Should output Python 3.12.0
which python      # Should point to ~/.pyenv/versions/genai-py312/bin/python
```

---

Continue with project-specific setup in each lab folder as described in this workspace.
