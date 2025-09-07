from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
# --- Import the centralized settings object ---
from app.core.config import settings
from .models import IdeaExtractionList, PostFilter
from .prompts import extraction_prompt, filter_prompt, analysis_prompt, report_prompt


# LLM for simple filtering tasks
filtering_llm = ChatOpenAI(
    # --- Use the setting ---
    model=settings.AGENT_FILTER_MODEL,
    temperature=0,
    api_key=settings.OPENAI_API_KEY.get_secret_value()
)

# A more powerful LLM for complex extraction tasks
extraction_llm = ChatOpenAI(
    # --- Use the setting ---
    model=settings.AGENT_EXTRACTION_MODEL,
    temperature=0.2,
    api_key=settings.OPENAI_API_KEY.get_secret_value()
)


# --- The rest of this file is already correct and needs no changes ---

# Create the extraction chain using LCEL
extraction_chain = extraction_prompt | extraction_llm.with_structured_output(IdeaExtractionList)

# Create the filtering chain using LCEL
filter_chain = filter_prompt | filtering_llm.with_structured_output(PostFilter)

# Create the analysis chain using LCEL
analysis_chain = analysis_prompt | extraction_llm | StrOutputParser()

# Create the final report generation chain using LCEL
report_chain = report_prompt | extraction_llm | StrOutputParser()