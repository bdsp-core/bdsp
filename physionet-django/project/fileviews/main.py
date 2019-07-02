import os

from django.http import Http404
from django.shortcuts import redirect

from project.fileviews.base import RawFileView
from project.fileviews.csv import CSVFileView, GzippedCSVFileView
from project.fileviews.image import ImageFileView
from project.fileviews.text import TextFileView

_suffixes = {
    '.bmp': ImageFileView,
    '.csv': CSVFileView,
    '.gif': ImageFileView,
    '.htm': RawFileView,
    '.html': RawFileView,
    '.jpeg': ImageFileView,
    '.jpg': ImageFileView,
    '.png': ImageFileView,
    '.svg': ImageFileView,
}


def display_project_file(request, project, file_path):
    """
    Display a file from either a published or unpublished project.

    The user is assumed to be authorized to view the project.
    file_path is the name of the file relative to project.file_root().
    """

    try:
        abs_path = os.path.join(project.file_root(), file_path)
        with open(abs_path, 'rb') as infile:
            if file_path.endswith('.csv.gz'):
                cls = GzippedCSVFileView
            else:
                (_, suffix) = os.path.splitext(file_path)
                cls = _suffixes.get(suffix, TextFileView)
            view = cls(project, file_path, infile)
            return view.render(request)
    except IsADirectoryError:
        return redirect(request.path + '/')
    except FileNotFoundError:
        raise Http404()