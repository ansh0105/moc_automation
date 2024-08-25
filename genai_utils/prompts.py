from langchain_core.prompts.prompt import PromptTemplate

PDF_STRUCTURE_PROMPT_V3 = """
#heading: Overall export trends

#graph: Overall export trends

#graph: Top five export commodities

#table: Export growth rates

#graph: Sector-wise analysis

#graph: Commodities comparison
"""

OVERALL_EXPORT_PROMPT = """{} Above data corresponds to India Export values for month of December 2022 and December 2023 and from april 2022 - december 2022 and  from april 2023-december 2023
I want to create a document that will be release on the press from ministry of commerce, therefore use poper terminology and answer should be precises
Using the above data please write a short note on overall trade of India.
While the overall export in million dollars for {} is {}.and overall export for {} is {}. which is shown in bar graph
So, write a short note for this total export value for December 2023 compared to December 2022 also.
Note: Answer should not include any headings, Just give summary in text explaining overall export trade of India.
"""


TOP_EXPORT_COM_PROMPT = """{} Above data corresponds to India's export value for month of {} and {} for top 5 commodities.
I want to create a document that will be release on the press from ministry of commerce, therefore use proper terminology and answer should be precises.
so using above data generate a summary or short note on top 5 commodities export in respective months .
Note: Answer should not include any headings, Just give summary in text explaining trends commodities wise that explain the whole data"""


EXPORT_GROWTH_RATE_PROMPT = """
{} Above data corresponds to Indias minimum growth rate of top 5 commodities from {} to {} and
{} Above data corresponds to Indias maximum growth rate of top 5 commodities from {} to {}.
I want to create a document that will be release on the press from ministry of commerce, therefore use proper terminology and answer should be precises.
so using above data of highest and lowest growth rate of commodities generate a summary or short note.
Note: Answer should not include any headings, Just give summary in text explaining trends commodities wise that explain the whole data 
"""


SECTOR_ANALYSIS_PROMPT ="""
{} Above data corresponds to India's top 10 commodities distribution export value during the time period of {}.
I want to create a document that will be release on the press from ministry of commerce, therefore use proper terminology and answer should be precises.
so using above data of commodities distribution of export generate a summary or short note.
Note: Answer should not include any headings, Just give summary in text explaining trends commodities wise that explain the whole data 
"""


COM_COMPARISION_PROMPT ="""
{} Above data corresponds to India's comparison of export of top 5  commodities between {} and {}
I want to create a document that will be release on the press from ministry of commerce, therefore use proper terminology and answer should be precises.
so using above data and generate a summary or short note or meaningful insights.
Note: Answer should not include any headings, Just give summary in text explaining trends commodities wise that explain the whole data 
"""

_template= """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {query}
Standalone question:"""

REPHRASE_QUES_PROMPT = PromptTemplate(input_variables=["chat_history","query"], template= _template)


CHATBOT_PROMPT ="""
You are a helpful technology agent who can answer queries realted to technology. You have the capability to answer question related to the information provided and also add reference from which answer is taken using metadata.
Here is the query of the user along with provided information and metadata (i.e reference of pageno from which information is retrieved)
Query - {}
Information - {}
Metadata - {}

Please refer the above information and metadata to answer query and generate response.
If no information is provided or information provided is not relevant to the query asked then respond "No information present in the knowledge source related to such query please ask different question related to technology" 
"""

