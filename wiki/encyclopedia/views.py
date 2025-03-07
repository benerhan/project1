import markdown2
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    entry_content = util.get_entry(title)

    if entry_content is None:
        return render(
            request,
            "encyclopedia/error.html",
            {"message": f"The requested '{title}' page was not found."},
        )

    html_content = markdown2.markdown(entry_content)

    return render(
        request, "encyclopedia/entry.html", {"title": title, "content": html_content}
    )
