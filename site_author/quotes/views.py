from django.shortcuts import render, redirect
from django.core.paginator import Paginator

# Create your views here.
from .utils import get_mongodb
from .models import Author, Tag, Quote
from .forms import AuthorForm, QuoteForm, TagForm


def main(request, page=1):
    # db = get_mongodb()
    # quotes = db.quotes.find()
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def description_auth(request, id_):
    authors = Author.objects.filter(pk=id_).all()

    return render(request, template_name='quotes/descript_author.html', context={'authors': authors})


def tag_add(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_tag.html', {'form': form})

    return render(request, 'quotes/add_tag.html', {'form': TagForm()})


def author_add(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_author.html', {'form': form})

    return render(request, 'quotes/add_author.html', {'form': AuthorForm()})


def quote_add(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                quote.tags.add(tag)

            return redirect(to='quotes:root')

        else:
            return render(request, 'quotes/add_quote.html', {"tags": tags, 'form': form})

    return render(request, 'quotes/add_quote.html', {"tags": tags, 'form': QuoteForm()})

