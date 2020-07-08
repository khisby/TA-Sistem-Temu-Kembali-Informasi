import esky.bdist_esky
from esky.bdist_esky import Executable as Executable_Esky
from cx_Freeze import setup, Executable

include_files = ['data_default.csv','data.csv', 'main.py','post-preprocessing.csv','post-preprocessing_defaut.csv','Preprocessing.py','Scraping.py']

setup(
    name = 'Khisoft Hadits',
    version = '1.0.0',
    options = {
        'build_exe': {
            'packages': ['backcall','bleach','bs4','certifi','cffi','chardet','click','cloudpickle','colorama','cycler','dask','decorator','defusedxml','entrypoints','idna','ipykernel','ipython','jedi','Jinja2','joblib','jsonschema','kiwisolver','llvmlite','Markdown','MarkupSafe','matplotlib','mistune','nbconvert','nbformat','networkx','nltk','notebook','numba','numpy','packaging','pandas','pandocfilters','parso','pickleshare','pycparser','Pygments','pyparsing','pyrsistent','pytz','QtPy','regex','requests','resampy','Sastrawi','scipy','Send2Trash','six','sklearn','SoundFile','soupsieve','tensorboard','terminado','testpath','toolz','tornado','tqdm','traitlets','urllib3','wcwidth','webencodings','Werkzeug','widgetsnbextension','wincertstore','xmltodict','zipp'],
            'include_files': include_files,
            'include_msvcr': True,
        },
        'bdist_esky': {
            'freezer_module': 'cx_freeze',
        }
    },
    data_files = include_files,
    scripts = [
        Executable_Esky(
            "main.py",
            gui_only = True,
            #icon = XPTO #Coloque um icone aqui se quiser ,
            ),
    ],
    executables = [Executable('main.py',base='Win32GUI')]
    )