import logging
import pandas as pd
import io
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("XLS to XLSX conversion function triggered.")

    # Read uploaded file
    file = req.files.get("file")
    if not file:
        return func.HttpResponse(
            "No file uploaded. Please send a file with key 'file'.",
            status_code=400
        )

    try:
        # Read the XLS file into a DataFrame
        df = pd.read_excel(file, engine="xlrd")

        # Write to XLSX format in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        # Return XLSX file as response
        return func.HttpResponse(
            output.getvalue(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=converted.xlsx"
            }
        )

    except Exception as e:
        logging.exception("Error converting file")
        return func.HttpResponse(
            f"Error converting file: {str(e)}",
            status_code=500
        )
