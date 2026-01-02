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

def apercu_prop_content(prop, html_content):
    return f"""
    <div class="container mt-4">
      <h2>{prop.titre}</h2>
      <p><strong>Auteur:</strong> {prop.auteur}</p>
      <p><strong>Format:</strong> {prop.format_oeuvre}</p>
      <hr/>
      <div class="markdown-preview">
        {html_content}  <!-- HTML sûr -->
      </div>
      <div class="mt-3">
        <form method="post">
          <button class="btn btn-secondary" name="action" value="annuler">Annuler</button>
          <button class="btn btn-success" name="action" value="envoyer">Envoyer aux bibliothécaires</button>
        </form>
      </div>
    </div>
    """
