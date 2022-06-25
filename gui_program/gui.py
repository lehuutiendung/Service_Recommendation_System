import tkinter
from tkinter import *
from tkinter import ttk


def main(cf_rs, list_post_title, list_post_category):
    def get_id_user():
        """
        Lấy id người dùng và trả về danh sách bài viết
        """
        tv.delete(*tv.get_children())
        x1 = entry1.get()
        list_posts = cf_rs.recommend_top(int(x1),10)
        for i in range(10):
            tv.insert(parent='', index=i, iid=i, text='',
                      values=('{0:.{1}f}'.format(list_posts[i]['similar'], 2),
                              list_post_title[list_posts[i]['id']],
                              list_post_category[list_posts[i]['id']]))

    root = Tk()
    root.title('Recommendation System')
    root.resizable(False, False)

    window_height = 450
    window_width = 500

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    root.deiconify()

    canvas1 = tkinter.Canvas(root, width=window_width, height=window_height)
    canvas1.pack()

    label1 = tkinter.Label(root, text='Recommendation System')
    label1.config(font=('Segoe UI Semibold', 14))
    canvas1.create_window(250, 40, window=label1)

    label2 = tkinter.Label(root, text='Type UserID:')
    label2.config(font=('Segoe UI Symbol', 10))
    canvas1.create_window(175, 95, window=label2)

    entry1 = tkinter.Entry(root)
    canvas1.create_window(300, 95, window=entry1)

    button1 = tkinter.Button(text='Suggest me', command=get_id_user, bg='brown', fg='white',
                             font=('helvetica', 9, 'bold'))
    canvas1.create_window(250, 135, window=button1)

    tv = ttk.Treeview(root)
    tv['columns'] = ("SIMILAR RATE", "POST TITLE", "POST CATEGORY")
    tv.column('#0', width=0, stretch=NO)
    tv.column('SIMILAR RATE', anchor=CENTER, width=90)
    tv.column('POST TITLE', anchor=W, width=230)
    tv.column('POST CATEGORY', anchor=CENTER, width=90)

    tv.heading('#0', text='', anchor=CENTER)
    tv.heading('SIMILAR RATE', text='SIMILAR RATE', anchor=CENTER)
    tv.heading('POST TITLE', text='POST TITLE', anchor=CENTER)
    tv.heading('POST CATEGORY', text='POST CATEGORY', anchor=CENTER)

    canvas1.create_window(250, 290, window=tv)

    root.mainloop()
