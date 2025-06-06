def write_to_file(fname, val):
    file = open(fname, 'w')
    file.write(val)
    file.close()