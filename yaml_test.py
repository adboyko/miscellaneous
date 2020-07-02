import yaml


# Followed this.. Good basic:
# https://stackabuse.com/reading-and-writing-yaml-to-a-file-in-python/
data = {
    'cars': [
        'Civic',
        'Audi',
        'Ford',
        'Dodge'
        ],
    'towns': [
        'NYC',
        'Austin',
        'Ottawa'
        ]
    }
with open('d.yml', 'w') as y_file:
    y_file.write('---\n\n')
    yaml.dump(data, y_file)
with open('d.yml', 'r') as y_in:
    print(yaml.full_load(y_in))
