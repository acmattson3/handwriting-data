COLLECTING=True

def collect(is_collecting):
    global COLLECTING
    COLLECTING=is_collecting

def writer_id():
    if not COLLECTING:
        return
    writer_id=input("Please enter your name: ")
    input_string="You entered: '" + writer_id + "'. Is this correct? (y/n) "
    is_correct = input(input_string)
    while is_correct != 'y':
        writer_id=input("Please enter your name: ")
        input_string="You entered: '" + writer_id + "'. Is this correct? (y/n) "
        is_correct = input(input_string)
    
    return writer_id