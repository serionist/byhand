---
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Skill]
tags: [decks]
---

This is meant to add one slide per row, with its title and body text, but every slide comes out with an empty body. What is wrong?

```python
from pptx import Presentation


def build(rows, path):
    prs = Presentation()
    layout = prs.slide_layouts[1]
    for row in rows:
        slide = prs.slides.add_slide(layout)
        slide.shapes.title.text = row["title"]
        body = slide.placeholders[1]
        body.text = row.get("body", "")
        body.text_frame.clear()
    prs.save(path)
```
