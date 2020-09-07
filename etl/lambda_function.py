import json
import sys

def get_pipeline_code():
    code = ''
    import requests
    url = 'https://raw.githubusercontent.com/mikevostrikov/2020-ontario-covid19-severe/master/etl/pipeline.ipynb'
    r = requests.get(url, allow_redirects=True)
    j = r.json()
    code += 'def run():\n\n'
    if j['nbformat'] >= 4:
        for i,cell in enumerate(j['cells']):
            if cell['cell_type'] == 'code':
                code += '    #cell ' + str(i) + '\n'
                for line in cell['source']:
                    if not '#noprod' in line:
                        code += f'    {line}'
                code += '    \n\n'
    return code

def load_module_from_code(name, code):
    from types import ModuleType
    module = ModuleType(name)
    exec(code, module.__dict__, module.__dict__)
    return module

def lambda_handler(event, context):
    try:
        load_module_from_code('pipeline', get_pipeline_code()).run()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps(None)
        }

# Estimate memory requirements:
# import tracemalloc
# tracemalloc.start()
# lambda_handler(None, None)
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
# tracemalloc.stop()
