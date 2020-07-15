Django PDF Processor

This backend repo takes user PDFs and highlights interesting regions (text or chart). 
It does this by first converting the PDF to JPEG, then using CV2 to separate the image to foreground and background. 
Then, all foreground pixels are dilated by a set kernel size, and bounding boxes drawn for all overlapping regions. 

For reference, I included some processed open-access PDFs. 

Things to improve on:
1. Kernel size adjustment. 
2. Currently only returns the processed JPG with bounding boxes. Should return bounding boxes in CSV file or some such. 
3. Frontend. There's a placeholder front-end project there. 
4. Credentials?

