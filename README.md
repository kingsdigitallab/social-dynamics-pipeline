# Social Dynamics Pipeline

Social Dynamics Pipeline is an experimental pipeline for extracting text from handwritten forms and ingesting the data
into a database for correction and research.

The pipeline has been developed in several parts to maximise flexibility since the project is exploratory:

* **tasks** - these are individual functions that can be used in a variety of ways and arranged in a pipeline
* **command-line interface** - this is a convenience wrapper around the tasks
* **web GUI**
    * `muster` app:
        * main app for viewing and editing the database
    * `dev` app:
        * exposes some pipeline tasks in a user-friendly UI
        * provides basic image and database browsing to support development

**Status**: Work in progress.

## Setup

### Dev Container

A Dev Container configuration is provided for convenient development. You can either run it in Codespaces in the usual
way or locally with your preferred IDE (e.g. VSCode). By default, it starts `muster` app, but you can also start the
`dev` app manually if you like.

### Local Installation

NB: The application runs on Python 3.10. Other versions of Python have not been tested.

First, clone this repository and enter the directory:

```aiignore
$ git clone git@github.com:kingsdigitallab/social-dynamics-pipeline.git
$ cd social-dynamics-pipeline
```

#### Using `uv`

You can use `uv` to handle the Python version, virtual environment and dependencies for you. You only need to run _any_
project command for the first time and `uv` will handle everything in one step. For example:

```aiignore
$ uv run python -m pipeline --help
```

However, if you really prefer, you can have more manual control over the virtual environment process:

```aiignore
$ uv python install 3.10
$ uv venv --python 3.10
$ source .venv/bin/activate
(venv) $ uv sync
```

#### Using `pip`

Alternatively, you can install dependencies using vanilla `pip` with the supplied `requirements.txt` file -- but you
will need to have Python 3.10 installed in some way:

```aiignore
$ python3.10 -m venv venv
$ source venv/bin/activate
(venv) $ python -m pip install -r requirements.txt
```

### Development Dependencies

If you want to develop on the codebase and not just use the project, install the development dependencies and pre-commit
hooks:

#### Using `uv`

```aiignore
$ uv pip install -e ".[dev]"
$ uv run pre-commit install
```

NB: The default handling of `uv` is to add `--dev` dependencies to `[dependency-groups]` in the `pyproject.toml` and
always sync it by default. However, we do not want this to happen in the production environment in which this repository
will be used because it takes a long
time to install development dependencies for no reason. So, we have gone with the standard PEP 621
`[project.optional-dependencies]`
solution instead, which enables us to have more granular control and more portability.

#### Using `pip`

```aiignore
(venv) $ python -m pip install -e ".[dev]"
(venv) $ pre-commit install
```

#### Run Tests

To check that the development dependencies have installed correctly, you can run the test suite:

```aiignore
$ uv run pytest
```

or

```aiignore
(venv) $ pytest
```

## Usage

### Command-line Interface

All commands are run via:

```aiignore
$ python -m pipeline <command> [OPTIONS]
```

To see all the options, use `--help`:

```aiignore
$ python -m pipeline --help
$ python -m pipeline extract-images --help
```

Extract embedded images from a single PDF file or all PDFs in a folder:

```aiignore
python -m pipeline extract-images -p path/to/file_or_folder.pdf -o output/
```

Create 150px-wide thumbnails from an image file or a folder of images:

```aiignore
python -m pipeline thumbnail-images -p path/to/image_or_folder -o output/thumbnails
```

Resizes image to a given width and/or height, preserving aspect ratio:

```aiignore
python -m pipeline resize-images -p path/to/image_or_folder -o output/ --width 200 --height 300
```

Import JSON-formatted B102r form data into the database:

```aiignore
python -m pipeline import-b102r -i path/to/json/files
```

NB: The JSON file format is that produced by running VLM inference
using [BVQA](https://github.com/kingsdigitallab/kdl-vqa).

**Options**
`--log-level` (optional): Control output verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL). Default is WARNING.

### Web Applications

#### Application `muster` - the main app for viewing and editing the database

##### Using `uv`:

```aiignore
$ PYTHONPATH=. uv run python pipeline/ui/muster/app.py
```

##### Direct invocation:

```aiignore
(venv) $ PYTHONPATH=. python pipeline/muster/app.py
```

The `muster` app will be available at http://localhost:8080.

#### Application `dev` - a collection of utilities used during development

The `dev` web app has 4 pages:

1. Browse images - browse the images in the configured `IMAGES_DIR`
2. Extract Images from PDF - wrapper around [
   `extract_images_from_pdf()`](https://github.com/kingsdigitallab/social-dynamics-pipeline/blob/main/pipeline/tasks/pdf_processing.py#L23)
3. Blank Detection (Demo) - non-functional demonstration of a workflow to distinguish between 2 different categories of
   images
4. Browse Database - browse the database configured in `DATABASE_NAME`

The `dev` app will be available at http://localhost:8090.

#### Changing ports

By default, the ports are set in their respective `app.py` scripts and will not conflict, so you can run them both at
the same time. If for some reason you want to change a port, you can pass a
different port number e.g.

`ui.run(port=8081)`

#### Configure Environmental Variables

The default web GUI settings can be found in `pipeline/ui/config.py`. When running an app using these defaults, it
presents demo data (images and database). When you want to use real data, you need to override the defaults in an `.env`
file in the **root of the project**. Typically, you will want to set a different image folder and database:

```
IMAGES_DIR=/path/to/your/images/folder
DATABASE_NAME=database_name.db
```
