from .dtrees import classifier
def handle_uploaded_file(f):
    print("received",f.name)
    with open("blank/static/tmp/"+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
