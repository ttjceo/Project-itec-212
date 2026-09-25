from flask import Flask , request ,jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
import os 


load_dotenv()

app = Flask (__name__)
client=OpenAI(
   api_key=os.getenv("OPENAI_API_KEY")
   )

#Home page 
@app.route("/")
def home () :
  return send_from_directory(".", "Trivahub.html")


#Triva page 

@app.route("/triva" )
def triva():
     return send_from_directory(".", "Triva.html")

#Chat Endpoint 
@app.route ("/chat", methods=["Post"])
def chat():
  
    message = request.form.get("message","").strip()
    link =request.form.get("link","").strip()
    uploaded_file = request.files.get("file")

    #Triva requires a file or a web link
    if not uploaded_file and not link:
        return jsonify  ({
        "error":" File or web link is not present. please  provide a web link before asking triva a question."
    }), 400 
    
    if not message:
       return jsonify({
          "error": "Please enter a question for triva"

       }),400
    source_information=""
    
    #handle web link
    if link:
       source_information += f"""
       The user provided this web link:
       
       {link}

       Use the information from this source when answering the users question.
       """
       #Handle uploaded file 
       if uploaded_file:
          file_name = uploaded_file.filename
          file_contents= uploaded_file.read()
            
          try:
             file_text= file_contents.decode("utf-8")
             
             source_information += f"""
             The user uploaded this file:
             File name: {file_name}

             File contents:

             {file_text}
             """
          except UnicodeDecodeError:
             
             source_information += f"""
             The user uploaded a file named {file_name}.
             The file could not be read as plain text by this basci version.
             """

             # Ask Troy
    
    response = client.responses.create(
                model="gpt-5.6-luna",
                instructions="""
                You are Triva, The Ai assistant 

                You are an evidence-based AI assistant.
                 
                Important:
                Only answer questions using information provided 
                by the user's uploaded file or web link.

                If the provided source does not contain enough information 
                to answer the question, clearly say the  source doesn't provide
                enough infornmtion 

                Do not pretend that information came from the source 
                when it did not 

                Be clear and helpful.
                """,
                      input=f"""
                      source information:
                      {source_information}
                 
User Question:
 {message}
"""
  )
    return jsonify({
             "response": response.output_text
             
             })



    
         

    
if__name__ == "__main__"

app .run(debug=True)