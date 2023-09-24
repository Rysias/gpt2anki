import asyncio
import datetime as dt

import pytz
from bs4 import BeautifulSoup
from gpt2anki.data_access.highlight_sources.hypothesis import HypothesisHighlightGetter
from gpt2anki.data_access.hydrator.main import HighlightHydrator
from gpt2anki.data_access.persist_questions.markdown import write_qa_prompt_to_md
from gpt2anki.domain.highlights_to_questions import (
    highlights_to_questions,
    initialize_model,
)

if __name__ == "__main__":

    print("Getting highlights")
    highlights = HypothesisHighlightGetter(username="ryqiem").get_highlights_since_date(
        dt.datetime.now(tz=pytz.UTC) - dt.timedelta(days=200),
    )
    print("Hydrating highlights")
    hydrated_highlights = HighlightHydrator(
        soup_downloader=BeautifulSoup,
    ).hydrate_highlights(highlights=highlights)

    hydrated_highlights = list(filter(lambda x: x.context!="", hydrated_highlights))

    print("Generating QAs")
    model = initialize_model(model_name="gpt-4")
    questions = asyncio.run(
        highlights_to_questions(model=model, highlights=hydrated_highlights[0:2]),
    )

    print("Saving to disk")
    list(map(write_qa_prompt_to_md, questions))