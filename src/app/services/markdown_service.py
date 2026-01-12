import markdown
from markupsafe import Markup

import re

def clean_llm_markdown(md_text: str) -> str:
    """
    Enlève les blocs ```markdown ...``` renvoyés par le LLM.
    """
    if not md_text:
        return ""
    # Supprime ```markdown …```
    cleaned = re.sub(r"```markdown\s*\n(.*?)```", r"\1", md_text, flags=re.DOTALL)
    # Supprime ``` tout court si reste
    cleaned = re.sub(r"```(.*?)```", r"\1", cleaned, flags=re.DOTALL)
    return cleaned.strip()


def clean_markdown(md_text):
    lines = (md_text or "").splitlines()
    return "\n".join(
        line for line in lines
        if not line.startswith("J’ai apporté les corrections")
    )


def markdown_to_html(md_text):
    html = markdown.markdown(
        md_text or "",
        extensions=[
            "extra",
            "fenced_code",
            "toc",
            "sane_lists",
            "smarty"
        ]
    )
    return Markup(html)

def apercu_prop_content(prop, html_content):
    html_content = markdown_to_html(prop.contenu_markdown)

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
