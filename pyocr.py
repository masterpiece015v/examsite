from PIL import Image
import os
import MySQLdb
import pyocr

t_path = "C:\\Tesseract-OCR"

if t_path not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + t_path

tools = pyocr.get_available_tools()
tool = tools[0]

#print("Will use tool '%s'" % (tool.get_name()))
langs = tool.get_available_languages()
#print("Available languages: %s" % ", ".join(langs))
lang = langs[2]


def sql():
    conn = MySQLdb.connect(
        user='webmaster',
        passwd='P@ssword',
        host='kyouin-02',
        db='examsitedb',
        charset='utf8'
    )

    print( conn.is_connected())

    cur = conn.cursor(prepared=True)
    cur_dir = os.curdir()
    path_files = os.listdir("")

    for path_file in path_files:
        txt = tool.image_to_string(
            Image.open( path_file ),lang=lang,builder=pyocr.builders.TextBuilder()
        )
        name_file = path_file.split("\\")
        q_id = name_file[len(name_file) - 1].split(".")[0]
        q_content = txt.replace("\n","")
        q_content = q_content.replace(" ","")
        print( q_id )
        print( q_content )

        try:
            cur.execute("update exam_question set q_content=? where q_id=?",(q_content,q_id))
            conn.commit()
            print( "commit")
        except:
            conn.rollback()
            print( "rollback")
            raise

    cur.close()
    conn.close()
