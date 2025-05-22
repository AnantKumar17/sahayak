import requests
import codecs
import re
import json
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
from fastapi import HTTPException
from services.rag_storage import retrieve_similar_reviews, store_review
# from services.rag_storage import retrieve_similar_reviews, store_review


client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential("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"),
)

def query_gpt(code_snippet):
    try:
        

        # **Step 2: Retrieve Similar Reviews**
        past_reviews = retrieve_similar_reviews(code_snippet)
        review_context = "\n\n".join(past_reviews) if past_reviews else "No past reviews available."

        # **Step 3: Full DeepSeek Call with Context**
        prompt_final = f"""
        You are a senior software architect reviewing the following code snippet.
        Consider past reviews of similar code snippets, if applicable and relatable, for additional context:

        **Past Reviews:**
        {review_context}

        **Code Snippet:**
        {code_snippet}

        Analyze the given code and return a JSON response with meaningful insights in the following format:

        {{
            "readability": "<Review on readability with examples>",
            "security": "<Identify security issues, suggest improvements>",
            "performance": "<Analyze bottlenecks and provide optimizations>",
            "best practices": "<Suggest adherence to coding standards>",
            "bugs": "<Detect potential bugs with explanations>",
            "overall analysis": "<Provide a brief summary of what the analysed code snippet does and tries to achieve, along with the overall assessment of the code using key findings from the above sections>",
            "suggested refactored code": "<Provide a refactored version of the code snippet, applying the key findings from the above sections. Ensure the suggested refactored code follows the correct syntax and conventions of the detected language.>"
        }}

        Respond **ONLY in JSON format**  
        Ensure all sections contain meaningful one-line insights wherever applicable.
        """

        response_final = client.complete(
            messages=[
                SystemMessage(""""""),
                UserMessage(prompt_final),
            ],
            model="gpt-4o",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )

        ai_response_final = response_final.choices[0].message.content.strip()

        # 🔹 Extract JSON from AI response
        json_match = re.search(r"\{.*\}", ai_response_final, re.DOTALL)
        if json_match:
            json_string = json_match.group(0).strip()
        else:
            raise HTTPException(status_code=500, detail="Final AI response did not contain valid JSON.")

        # 🔹 Parse extracted JSON
        parsed_response = json.loads(json_string)

        # 🔹 Process suggested refactored code
        if "suggested refactored code" in parsed_response:
            try:
                parsed_response["suggested refactored code"] = codecs.decode(parsed_response["suggested refactored code"], 'unicode_escape')
            except Exception:
                parsed_response["suggested refactored code"] = parsed_response["suggested refactored code"].replace('\\n', '\n').replace('\\"', '"')

        print(parsed_response["suggested refactored code"])

        # 🔹 Store final parsed_response (now complete)
        store_review(parsed_response)

        print("Review stored")
        return parsed_response

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in AI response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def followup_query(ai_review, followup_question):
        """Handles follow-up questions by generating a contextual AI response."""

        prompt = f"""
            You are an AI Code Review Assistant. Below is an AI-generated review and a follow-up question from a developer.

            AI Review:
            {ai_review}

            Developer's Follow-Up Question:
            {followup_question}

            Provide a **concise and insightful JSON response** addressing the user's question. Be **technical, practical, and context-aware**.

            The response should follow this JSON structure:

            {{
                "response": "<Provide a concise and insightful response addressing the user's question.>"
            {{
                ,
                "suggested refactored code": "<Only include this section if the developer's question explicitly asks for or hints at code improvements or implementations. Otherwise, exclude this field from the response.>"
            }} if applicable
            }}

            Ensure the response is **strictly in JSON format** without any additional text.
            """

        response = client.complete(
            messages=[
                SystemMessage("You are a code review assistant helping developers understand and improve their code."),
                UserMessage(prompt),
            ],
            # model="DeepSeek-V3",
            # temperature=0.8,
            # max_tokens=1024,
            # top_p=0.1
            model="gpt-4o",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )

        # Extract AI response
        ai_response = response.choices[0].message.content.strip()

        # 🔹 Use regex to extract JSON part safely
        json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)

        if json_match:
            json_string = json_match.group(0).strip()  # Extract JSON block
        else:
            raise HTTPException(status_code=500, detail="AI response did not contain a valid JSON block.")

        # 🔹 Parse extracted JSON
        parsed_response = json.loads(json_string)
        #print("calling store_review")
        return parsed_response
