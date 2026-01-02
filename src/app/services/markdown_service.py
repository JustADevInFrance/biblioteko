import markdown
from markupsafe import Markup


def clean_markdown(md_text):
    lines = (md_text or "").splitlines()
    return "\n".join(
        line for line in lines
        if not line.startswith("J’ai apporté les corrections")
    )


def markdown_to_html(md_text):
    return Markup(markdown.markdown(
        md_text,
        extensions=[
            "extra",
            "fenced_code",
            "toc",
            "sane_lists",
            "smarty"
        ]
    ))
