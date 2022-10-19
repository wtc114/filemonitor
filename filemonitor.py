import os
import fnmatch
import hashlib
import sys
import pickle


CHUNK_SIZE = 8192


def is_file_match(filename,patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(filename,pattern):
            return True
    return False


def find_specific_files(root,patterns=['*'],excluede_dirs=[]):
    for root,dirnames,filenames in os.walk(root):
        for filename in filenames:
            if is_file_match(filename,patterns):
                yield os.path.join(root,filename)
        for d in excluede_dirs:
            if d in dirnames:
                dirnames.remove(d)
        for dir in dirnames:
            if dir.startswith("."):
                dirnames.remove(dir)


def get_chunk(filename):
    with open(filename,'rb') as f:
        chunk = f.read(CHUNK_SIZE)
        while len(chunk)>0:
            yield chunk
            chunk = f.read(CHUNK_SIZE)


def get_file_checksum(filename):
    h = hashlib.md5()
    for chunk in get_chunk(filename):
        h.update(chunk)
    return h.hexdigest()


def main():
    sys.argv.append("")
    directory = sys.argv[1]
    temp=sys.argv[2]
    if temp=="True":
        is_init = True
    else:
        is_init = False
    print(type(is_init))
    print(is_init)
    if not os.path.isdir(directory):
        raise SystemExit("{0} is not a directory".format(directory))

    try:

        record = {}

        if is_init:
            for item in find_specific_files(directory, excluede_dirs=['Library']):
                checksum = get_file_checksum(item)
                record[checksum] = item
            print("in init...")
            print(record)
    #            os.path.isfile("gdoufile.pickle")
    #            os.remove("gdoufile.pickle")
            with open("gdoufile.pickle","wb") as f:
                pickle.dump(record,f)
        else:
            with open("gdoufile.pickle","rb") as f:
                record = pickle.load(f)

            for item in find_specific_files(directory,excluede_dirs=['Library','Applications','falskweb']):
                checksum = get_file_checksum(item)
                if checksum not in record:
                    with open("dd.log",'w') as f:
                        print(checksum,item)

    except Exception as ee:
        print("未知异常:{1}".format(str(ee)))




if __name__ == "__main__":
    main()