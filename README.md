# MGitPython

CLI tool to work with multiple git repositories.

## 1. Install

Run:

```
pip3 install MGitPython
```

Create symbolic link to `main.py` file:

```
cd ~/bin
ls -la /opt/homebrew/lib/python3.11/site-packages
ln -s /opt/homebrew/lib/python3.11/site-packages/mgitpy/main.py mgit
chmod u+x mgit
```

## 2. Quickstart

Create a temporary folder:

```
mkdir work-with-mgit
cd work-with-mgit
```

Clone two arbitrary repos, for example:

```
git clone git@github.com:gajdaw/MGitPython.git
git clone git@github.com:github/gitignore.git
```

Verify the repos:

```
mgit info
```

Checkout a new branch named `lorem` in both repos:

```
mgit git "checkout -b lorem"
```

Verify the repos:

```
mgit info
```

Switch to `main` branch in both repos:

```
mgit checkout main
```

Get some help:

```
mgit
```

## 3. Test & Build & Install & Upload

```
# test
pytest mgitpy-test/test*.py

# build
rm -rf *
git reset --hard
python3 -m build

# install
pip3 install dist/MGitPython-0.8.3.tar.gz

# upload
twine upload dist/MGitPython-0.8.3.tar.gz dist/MGitPython-0.8.3-py3-none-any.whl
```
