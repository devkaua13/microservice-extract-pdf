from fastapi import FastAPI, UploadFile, File
import pdfplumber
import io

app = FastAPI()

@app.post("/extrair-estrutura")
async def extrair_estrutura(file: UploadFile = File(...)):
    conteudo = await file.read()
    estrutura = []

    # PDF
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(conteudo)) as pdf:
            for pagina in pdf.pages:
                words = pagina.extract_words(extra_attrs=["size"])
                for word in words:
                    tamanho = round(word.get("size", 12))
                    if tamanho >= 16:
                        tipo = "Heading 1"
                    elif tamanho >= 14:
                        tipo = "Heading 2"
                    else:
                        tipo = "Normal"
                    estrutura.append({
                        "tipo": tipo,
                        "texto": word.get("text", "")
                    })

    return {"estrutura": estrutura}