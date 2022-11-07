PDF Transform by rotating page number by a multiple of 90 degrees

API Endpoints:

POST /convert: rotates the page of a pdf file

payload: 
    
    file_path: path to file that must be transformed
    page_number: page number (between 1 to n, n is the pages of the file)
    angle_of_rotation: angle of rotation (multiple of 90 degrees)