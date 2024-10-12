# create and activate virtual venv

1. Create the virtual environment: Use the python3 -m venv command to create a virtual environment in a folder named venv (you can change the folder name if you prefer)
```bash
python -m venv venv
```
This will create a directory called venv containing the Python interpreter and libraries for your project.

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

3. Verify the environment: Once activated, you should see the virtual environment name (e.g., (venv)) in your terminal prompt. You can also check the Python version and location:

```bash
python --version
which python
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Deactivate the virtual environment: When you're done working in the virtual environment, you can deactivate it with:

```bash
deactivate
```