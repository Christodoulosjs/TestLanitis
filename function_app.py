import azure.functions as func
import logging
import pandas as pd
import tempfile
import os
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="XlsToXlsx", methods=["POST"])
def XlsToXlsx(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get('file')
        if not file:
            return func.HttpResponse("No file uploaded", status_code=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xls") as temp_xls:
            file.save(temp_xls.name)

        df = pd.read_excel(temp_xls.name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_xlsx:
            df.to_excel(temp_xlsx.name, index=False)

        with open(temp_xlsx.name, "rb") as f:
            xlsx_data = f.read()

        os.remove(temp_xls.name)
        os.remove(temp_xlsx.name)

        return func.HttpResponse(
            xlsx_data,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
