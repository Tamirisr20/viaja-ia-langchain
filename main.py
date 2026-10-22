import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.globals import set_debug

set_debug(os.getenv("DEBUG", "false").lower() == "true")

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

class Destino(BaseModel):
    cidade: str = Field(description="A cidade recomendada para visitar")
    motivo: str = Field(description="Motivo pelo qual é interessante visitar essa cidade")


class Restaurante(BaseModel):
    cidade: str = Field(description="A cidade recomendada para visitar")
    restaurantes: str = Field(description="Os restaurantes recomendados na cidade")


parseador_destino = JsonOutputParser(pydantic_object=Destino)
parseador_restaurante = JsonOutputParser(pydantic_object=Restaurante)

prompt_cidade = PromptTemplate(
    template="Sugira uma cidade para quem gosta de {interesse}.\n{formato_de_saida}",
    input_variables=["interesse"],
    partial_variables={"formato_de_saida": parseador_destino.get_format_instructions()},
)

prompt_restaurante = PromptTemplate(
    template="Sugira restaurantes populares entre locais em {cidade}.\n{formato_de_saida}",
    input_variables=["cidade"],
    partial_variables={"formato_de_saida": parseador_restaurante.get_format_instructions()},
)

prompt_cultural = PromptTemplate(
    template="Sugira atividades e locais culturais em {cidade}.",
    input_variables=["cidade"],
)

modelo = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.5,
    api_key=api_key,
)

cadeia_1 = prompt_cidade | modelo | parseador_destino
cadeia_2 = prompt_restaurante | modelo | parseador_restaurante
cadeia_3 = prompt_cultural | modelo | StrOutputParser()

# cadeia_1 devolve {"cidade", "motivo"} -> cadeia_2 usa "cidade"
# cadeia_2 devolve {"cidade", "restaurantes"} -> cadeia_3 usa "cidade"
cadeia = cadeia_1 | cadeia_2 | cadeia_3

if __name__ == "__main__":
    resposta = cadeia.invoke({"interesse": "praias"})
    print(resposta)