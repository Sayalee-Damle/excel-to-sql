from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import excel_to_sql.create_table as ct
from excel_to_sql.config import cfg




def image_chain_factory() -> LLMChain:
    prompt = PromptTemplate(
        input_variables=["image_desc"],
        
        template="prompt which desribes {image_desc} in 20 words",
    )
    return LLMChain(llm=cfg.llm, prompt=prompt, verbose=cfg.verbose_llm)


def generate_image(chain: LLMChain, description: str) -> str:
    return DallEAPIWrapper().run(chain.run(description))


def generate_advice_image(chain: LLMChain) -> str:
    image_description = f"a person using a computer"
    return generate_image(chain, image_description)


if __name__ == "__main__":
    chain = image_chain_factory()
    
    def create_image_bot():
        image_prompt_res = chain.run({"image_desc": 
                                      """a person using a computer which has a excel file open on it
                                      """})
        #print(image_prompt_res)
        image_url = DallEAPIWrapper().run(image_prompt_res)
        return image_url
    
    print(create_image_bot())


