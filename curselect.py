import sqlite3, curses

conn = sqlite3.connect("/home/paulo/Documentos/src/automailer/contacts.db")
cursor = conn.cursor()

def print_menu(stdscr, selected_row_idx, menu):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx

        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,row)
    stdscr.refresh()

def main(stdscr):
    stdscr.clear()

    cursor.execute('SELECT name FROM contact ORDER BY ID DESC')
    rows = cursor.fetchall()
    rows = [i[0] for i in rows]
    rows.append("Quit")

    opt_row = ['Yes', 'No']

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    current_row = 0

    print_menu(stdscr, current_row, rows)

    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == ord('k') and current_row > 0:
            current_row -= 1
        elif key == ord('j') and current_row < len(rows) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            if current_row == len(rows) - 1:
                break
            cursor.execute('SELECT email FROM contact WHERE name = ?', (rows[current_row],))            
            mail_list = cursor.fetchall()[0][0]
            ncurr_row = 0
            print_menu(stdscr, ncurr_row, opt_row)
            while True:
                h, w = stdscr.getmaxyx()
                stdscr.addstr(h//3,w//4,f"You selected '{rows[current_row]}'. Their email is '{mail_list}'. Confirm?")

                nkey = stdscr.getch()
                stdscr.clear()
                if nkey == ord('k') and ncurr_row > 0:
                    ncurr_row -= 1
                elif nkey == ord('j') and ncurr_row < len(opt_row) - 1: 
                    ncurr_row += 1
                elif nkey == curses.KEY_ENTER or nkey in [10,13]:
                    if ncurr_row == len(opt_row) - 1:
                        break
                    else: 
                        result = mail_list 
                        f = open("/home/paulo/.cache/curselect.log", "w")
                        f.write(result+"\n")
                        f.close()
                        return(result)
                stdscr.refresh()
                print_menu(stdscr, ncurr_row, opt_row) 

            stdscr.refresh()
        print_menu(stdscr, current_row, rows)

curses.wrapper(main)
conn.close()

