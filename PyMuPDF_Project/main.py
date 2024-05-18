import pdfplumber

input_pdf = "Personal Information.pdf"

with pdfplumber.open(input_pdf) as pdf:
    # page, word, bbox
    document_info: dict[int, dict[str, [list[[int, float]], list]]] = dict()
    for i, page in enumerate(pdf.pages):
        word_bboxes: list = []  # will be a list of str,list dicts that contain word (str) and bbox info (list)
        words: list = page.extract_words()  # returns a list of dictionaries, one dictionary for each word-looking thing
        # which contains the text and info about the bounding box
        for word in words:
            text: str = word["text"]
            bbox: list = [word["x0"], word["top"], word["x1"],
                          word["bottom"]]  # Bounding box: (left, top, right, bottom)
            word_bboxes.append({"text": text, "bbox": bbox})
            document_info[i] = {"document": word_bboxes, "dimension": [page.width, page.height]}
    print(document_info)


# get list of bboxes: document_info[0]['document']


def group_bboxes_by_lines(bboxes, threshold=10):  # threshold determines if 2 bboxes are on the same line
    grouped_lines = []  # list of lists (lines) containing text/bbox dict for each word
    current_line: list = [bboxes[0]]
    is_parsed = [bboxes[0]]
    # print(current_line[-1])

    for i_bbox in bboxes[1:]:
        # compares y distance between current and previous bounding box, to see if they are on the same line
        if abs(i_bbox["bbox"][1] - current_line[-1]["bbox"][1]) < threshold:
            current_line.append(i_bbox)
        else:
            grouped_lines.append(current_line)
            current_line = [i_bbox]

    grouped_lines.append(current_line)
    return grouped_lines


# get nearest words in the given lines into same bbox
def group_nearest_words(line_bboxes, h_threshold=15):
    formatted_line_bboxes = []
    for line in line_bboxes:  # boxes in the lines are horizontally sorted
        formatted_line = []
        current_words = [line[0]]

        for i, word in enumerate(line[1:]):
            if abs(word["bbox"][0] - current_words[-1]["bbox"][2]) < h_threshold:
                current_words.append(word)
            else:  # may not reach end words
                formatted_line.append(current_words)
                current_words = [word]

        if i == len(line[1:]) - 1 and current_words not in formatted_line:  # if it reaches end words
            formatted_line.append(current_words)
    formatted_line_bboxes.append(formatted_line)
    print(formatted_line)

    return formatted_line_bboxes
