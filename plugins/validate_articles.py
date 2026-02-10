from pelican import signals


def validate_articles(generator):
    for article in generator.articles:
        if article.status == "draft":
            continue
        if not hasattr(article, "date") or article.date is None:
            raise Exception(
                f"Article '{article.source_path}' has no date. "
                "Add a 'Date:' metadata field or set 'Status: draft'."
            )


def register():
    signals.article_generator_finalized.connect(validate_articles)
