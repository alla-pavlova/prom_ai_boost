"""
HTML formatter for Prom.ua product descriptions.
"""


def build_html_description(name: str, description: str, sku: str = "") -> str:
    return f"""
<h2><strong>{name}</strong></h2>

<p><strong>{description}</strong></p>

<h3>Основна інформація</h3>
<ul>
  <li><strong>Назва:</strong> {name}</li>
  <li><strong>Артикул:</strong> {sku if sku else "не вказано"}</li>
</ul>
"""