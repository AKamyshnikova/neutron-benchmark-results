import collections
import os

import jinja2

import parsing


def main():
    j2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tmpl = j2_env.get_template('index.tmpl.html')

    context = {
        'shaker': [{
            'filename': fname,
            'filepath': 'shaker/' + fname,
            'scenario': res['scenarios'].keys()[0],
            'statuses': collections.Counter(
                r.get('status') for r in res['records'].itervalues()),
        } for fname, res in parsing.all_shaker_results()],
        'rally': [{
            'filename': fname,
            'filepath': 'shaker/' + fname,
            'sources': [{
                'name': name,
                'concurrency': task[0]['runner']['concurrency'],
                'times': task[0]['runner']['times'],
            } for name, task in res['source'].iteritems()],
            'errors': [len(s['errors']) for s in res['scenarios']],
        } for fname, res in parsing.all_rally_results()],
    }
    rendered = tmpl.render(context)
    with open('.index.new.html', 'w') as f:
        f.write(rendered)
    os.rename('.index.new.html', 'index.html')

if __name__ == '__main__':
    main()
