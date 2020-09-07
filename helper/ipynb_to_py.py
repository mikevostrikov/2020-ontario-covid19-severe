import sys,json

with open(sys.argv[1], 'r') as f: #input.ipynb
    with open(sys.argv[2], 'w') as of: #output.py
        j = json.load(f)
        if j["nbformat"] >= 4:
            for i,cell in enumerate(j["cells"]):
                if cell["cell_type"] == "code":
                    of.write("#cell "+str(i)+"\n")
                    for line in cell["source"]:
                        if not "#noprod" in line:
                            of.write(line)
                    of.write('\n\n')
        else:
            for i,cell in enumerate(j["worksheets"][0]["cells"]):
                of.write("#cell "+str(i)+"\n")
                for line in cell["input"]:
                    if not "#noprod" in line:
                        of.write(line)
                of.write('\n\n')
