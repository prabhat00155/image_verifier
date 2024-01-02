from flask import Flask, render_template, request
from requests.exceptions import HTTPError
import json
import requests


app = Flask(__name__)

valid_indices = []
items = []
category = 'birds'
folder = f'/Users/prabhatroy/Documents/AllProjects/data/{category}'


@app.route('/', methods=['GET', 'POST'])
def index():
    global valid_indices
    image_index = request.form.get('image_index')
    list_index = request.form.get('list_index')
    if image_index is None:
        image_index = 0
    else:
        image_index = int(image_index)

    if list_index is None:
        list_index = 0
    else:
        list_index = int(list_index)

    fname = f'jsons/{category}.json'
    with open(fname, 'r') as json_file:
        elements = json.load(json_file)
    element = elements[list_index]
    label = element['name']
    image_urls = element['urls']

    if request.method == 'POST':
        button_value = request.form.get('button')
        if button_value == 'yes':
            valid_indices.append(image_index)
        elif button_value == 'no':
            pass

        image_index += 1

    # Make sure image_index doesn't go beyond the last image
    if image_index >= len(image_urls):
        images = []
        for i, index in enumerate(valid_indices):
            try:
                response = requests.get(image_urls[index])
                if response.status_code == 200:
                    ext = image_urls[index].split('.')[-1]
                    updated_name = element['name'].replace(' ', '')
                    output_file = f'{folder}/{updated_name}{i}.{ext}'
                    images.append(output_file)
                    with open(output_file, "wb") as f:
                        f.write(response.content)
            except HTTPError as http_error:
                print(f"HTTPError: {http_error}")
        element['urls'] = images
        items.append(element)
        image_index = 0
        list_index += 1
        valid_indices = []

    if list_index < len(elements):
        element = elements[list_index]
        label = element['name']
        image_urls = element['urls']
    else:
        return "<p><center>End of verification!<center></p>"

    return render_template(
        'index.html', image_url=image_urls[image_index],
        image_index=image_index, list_index=list_index, label=label)


def main():
    app.run(debug=True)
    if items:
        fname = f'jsons/output_{category}.json'
        with open(fname, "w") as f:
            f.write(json.dumps(items))


if __name__ == '__main__':
    main()
