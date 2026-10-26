import os 
from io import BytesIO
from django.conf import settings
from django.shortcuts import render, redirect 
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST




from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from docx import Document 

from .forms import SignUpForm 


load_dotenv(settings.BASE_DIR.parent /".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


#Homepage
def home (request):
    return render(request,"Trivahub.html")

#User registration
def signup(request):
 if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid ():
         user= form.save()
         login(request,user)
         return redirect("Triva")

 else:
  form = SignUpForm()
 return render(request, "signup.html", {"form": form})

    #Triva chatbot page 
@login_required
def triva_page(request):
 return render (request, "Triva.html")

#Extract text from uploaded documents
def extract_text(uploaded_file):
    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    if filename.endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif filename.endswith(".docx"):
        document = Document(BytesIO(file_bytes))

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    elif filename.endswith(".txt"):
     return file_bytes.decode("utf-8")

    else:
     raise ValueError("Unsupported file type: {filename}") 



 #Ai chat endpoint 
@login_required
@require_POST
def chat(request):
    message = request.POST.get("message", "").strip()
    uploaded_files = request.FILES.getlist("files")

   

    if not message:
        return JsonResponse({
        "error": "Please enter a question for Triva"
        }, status=400)

    if not uploaded_files:
     return JsonResponse(
        {"error": "Please upload a file. " }, 
           status=400
           )

    documents = []
    try:
        for uploaded_file in uploaded_files:
            if uploaded_file.size > 10 * 1024 * 1024:
                return JsonResponse(
                    {"error": "Each file must be under 10 MB."},
                    status=400,
                )

            text = extract_text(uploaded_file)
            documents.append(text)
    except Exception:
        return JsonResponse(
            {"error": "Could not read one of the uploaded files."},
            status=400,
        )
         

           