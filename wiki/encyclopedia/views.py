import markdown2
import random
from django.shortcuts import render, redirect

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


def search(request):
    query = (
        request.GET.get("q", "").strip().lower()
    )  # Get the query from the GET request
    entries = util.list_entries()  # Get the list of entries

    # Check if the query matches any entry exactly
    for entry in entries:  # Check if the query matches any entry
        if entry.lower() == query:  # If it does
            return redirect("entry", title=entry)  # redirect to the entry page

    # Serach for entries that contain the query as a substring
    search_result = [entry for entry in entries if query in entry.lower()]

    return render(
        request,
        "encyclopedia/search.html",
        {"query": query, "search_result": search_result},
    )


def new_page(request):
    if request.method == "POST":  # If the form is submitted
        title = request.POST.get(
            "title", ""
        ).strip()  # Get the title from the POST request
        content = request.POST.get(
            "content", ""
        ).strip()  # Get the content from the POST request

        # Check if the title is empty
        if not title or not content:  # If the title is empty
            return render(
                request,
                "encyclopedia/error.html",
                {"message": "The title cannot be empty."},
            )  # Return an error message

        # Check if the title is already taken
        if util.get_entry(title):
            return render(
                request,
                "encyclopedia/error.html",
                {"message": f"The page '{title}' already exists."},
            )  # Return an error message

        formatted_content = f"# {title}\n\n{content}"  # Format the content

        util.save_entry(title, formatted_content)  # Save the entry

        return redirect("entry", title=title)  # Redirect to the entry page

    return render(request, "encyclopedia/new_page.html")  # Render the new page form


def edit(request, title):
    if request.method == "POST":  # If the form is submitted
        content = request.POST.get(
            "content", ""
        ).strip()  # Get the content from the POST request

        util.save_entry(title, content)  # Save the entry

        return redirect("entry", title=title)  # Redirect to the entry page

    content = util.get_entry(title)  # Get the content of the entry

    return render(
        request, "encyclopedia/edit.html", {"title": title, "content": content}
    )  # Render the edit page form


def random_page(request):
    entries = util.list_entries()  # Get the list of entries
    random_entry = random.choice(entries)  # Pick a random entry

    return redirect("entry", title=random_entry)  # Redirect to the random entry page
