from flask import Flask, request, Response
from PyPDF2 import PdfWriter, PdfReader
import os

app = Flask(__name__)


class AngleError(BaseException):
    pass


class PageNumberError(BaseException):
    pass


@app.route("/convert", methods=['POST'])
def convert_pdf():
    """
    Rotates a page of a pdf file my some degree(multiple of 90)
    :return: Response object
    """
    data = request.get_json()

    # check for valid data type and multiple of 90 angle of rotation
    try:
        angle_of_rotation = int(data["angle_of_rotation"]) % 360
        target_page_num = int(data["page_number"])

        if angle_of_rotation % 90 != 0:
            raise AngleError

    except ValueError:
        return Response('{"error": "page_number/angle_of_rotation is/are invalid"}',
                        status=400,
                        mimetype='application/json')
    except AngleError:
        return Response('{"error": "angle of rotation must be a multiple of 90"}',
                        status=400,
                        mimetype='application/json')

    file_path = data["file_path"]
    file_name, file_ext = os.path.splitext(file_path)

    # check allowing only pdf files to move forward
    if file_ext != '.pdf':
        return Response('{"error": "only pdf files are allowed"}',
                        status=400,
                        mimetype='application/json')

    # check if the file path is valid
    # check if the page number is greater than file pages
    try:
        in_file = open(file_path, "r+b")
        reader = PdfReader(in_file)
        writer = PdfWriter()

        if target_page_num > reader.numPages or target_page_num < 1:
            raise PageNumberError

        # page number passed is 1-indexed but PyPdf2 uses 0-indexing
        target_page_num -= 1

        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            if page_num == target_page_num:
                page.rotateClockwise(angle_of_rotation)
            writer.addPage(page)
        writer.write(in_file)
        in_file.close()
    except FileNotFoundError:
        return Response('{"error": "file not found"}',
                        status=400,
                        mimetype='application/json')
    except PageNumberError:
        return Response('{"error": "page number must be within file pages"}',
                        status=400,
                        mimetype='application/json')

    return Response(f'{{"success": "file was successfully transformed", "file_path": "{file_path}"}}',
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
