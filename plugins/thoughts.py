import os
import re

from pelican import signals, contents


def inject_thought_title(content):
    """Inject a title for thought files so Pelican doesn't skip them."""
    if not isinstance(content, contents.Article):
        return
    source = content.source_path or ""
    if "/thoughts/" not in source and not source.startswith("thoughts/"):
        return
    if not hasattr(content, "title"):
        basename = os.path.splitext(os.path.basename(source))[0]
        content.title = basename
        content.slug = basename


def separate_thoughts(generator):
    thoughts = []
    articles = []
    for article in generator.articles:
        if article.category == "thoughts":
            basename = os.path.splitext(os.path.basename(article.source_path))[0]
            match = re.fullmatch(r"(\d+)", basename)
            if not match:
                raise ValueError(
                    f"Thought file must be named as a number (e.g. 1.md), "
                    f"got: {basename}.md"
                )
            thought_id = int(match.group(1))
            article.thought_id = thought_id
            article.override_url = f"thoughts/{thought_id}"
            article.override_save_as = f"thoughts/{thought_id}/index.html"
            thoughts.append(article)
        else:
            articles.append(article)

    thoughts.sort(key=lambda t: t.thought_id)

    for i, article in enumerate(articles):
        article.next_article = articles[i - 1] if i > 0 else None
        article.prev_article = articles[i + 1] if i < len(articles) - 1 else None

    for i, thought in enumerate(thoughts):
        thought.next_article = thoughts[i - 1] if i > 0 else None
        thought.prev_article = thoughts[i + 1] if i < len(thoughts) - 1 else None

    generator.articles = articles
    generator._thoughts = thoughts
    generator.context["thoughts"] = thoughts


def write_thoughts(generator, writer):
    for thought in getattr(generator, "_thoughts", []):
        writer.write_file(
            thought.override_save_as,
            generator.get_template("thought"),
            generator.context,
            article=thought,
            category=thought.category,
            override_output=thought.override_save_as,
            url=thought.override_url,
        )

    thoughts = getattr(generator, "_thoughts", [])
    if thoughts:
        writer.write_file(
            "thoughts/index.html",
            generator.get_template("thoughts"),
            generator.context,
            thoughts=thoughts,
        )


def register():
    signals.content_object_init.connect(inject_thought_title)
    signals.article_generator_finalized.connect(separate_thoughts)
    signals.article_writer_finalized.connect(write_thoughts)
