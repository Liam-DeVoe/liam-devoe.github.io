from pelican import signals


def hide_articles(generator):
    hidden = []
    visible = []
    for article in generator.articles:
        if getattr(article, "hidden", "").lower() == "true":
            hidden.append(article)
        else:
            visible.append(article)

    # Remove hidden articles from tag lists
    hidden_set = set(hidden)
    for tag, articles in generator.tags.items():
        generator.tags[tag] = [a for a in articles if a not in hidden_set]
    generator.tags = {t: a for t, a in generator.tags.items() if a}

    # Fix prev/next chains to only link visible articles
    for i, article in enumerate(visible):
        article.next_article = visible[i - 1] if i > 0 else None
        article.prev_article = visible[i + 1] if i < len(visible) - 1 else None

    generator.articles = visible
    generator._hidden_articles = hidden


def write_hidden_articles(generator, writer):
    for article in getattr(generator, "_hidden_articles", []):
        writer.write_file(
            article.save_as,
            generator.get_template("article"),
            generator.context,
            article=article,
            category=article.category,
            blog=True,
        )


def register():
    signals.article_generator_finalized.connect(hide_articles)
    signals.article_writer_finalized.connect(write_hidden_articles)
