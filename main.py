import smtplib
from email.mime.text import MIMEText
from re import search

students = {}
file_path = input("Prosze wpisać ścieżkę do pliku ze studentami\n")
print("Prosze wpisać swój mail:")
email = input("Mail: ")
print("Prosze wpisać swoje hasło do aplikacji:")
password = input("Password: ")


def read_students():
    _students = {}
    with open(file_path) as file:
        for line in file:
            if line[-1] == "\n":
                line = line.split('\n')[0]
            line = line.split(',')
            mail = line[0]
            _student = [line[1], line[2], int(line[3])]
            if len(line) >= 5:
                _student.append(line[4])
                if len(line) == 6:
                    _student.append(line[5])
            _students.update({mail: _student})
    return _students


def show_students():
    for mail, student in students.items():
        print(f"{mail}: {student}")


def save():
    with open(file_path, "w") as file:
        for key, value in students.items():
            line = f"{key}"
            for i in value:
                line += ',' + str(i)
            line += "\n"
            file.write(line)
    file.close()


def send_email(subject, body, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(email, password)
    smtp_server.sendmail(email, recipients, msg.as_string())
    smtp_server.quit()
    save()


def calc_grad(points):
    if points < 51:
        return 2
    return (points / 20).__ceil__()


def send_email_to(recipient):
    if recipient not in students:
        return
    subject = "Ocena końcowa"
    body = "Twoja końcowa ocena jest" + str(students[recipient][3])
    send_email(subject, body, recipient)


def calc_grads():
    for mail, student in students.items():
        if len(student) == 3:
            grad = calc_grad(student[2])
            student.append(grad)
            student.append("GRADED")
            students.update({mail: student})
    save()


def send_mails():
    for mail, student in students.items():
        if len(student) == 5:
            if student[4] != "MAILED":
                send_email_to(mail)
                student[4] = "MAILED"
                students.update({mail: student})


def delete_student():
    mail = input("Prosze wpisać mail studeta, którego trzeba usunąć:\n")
    if mail not in students:
        print(f"Student z mailem \"{mail}\" nie istnieje")
        return
    students.pop(mail)
    save()
    print(f"Student z mailem \"{mail}\" został usunięty")


def add_student():
    mail = input("Prosze wpisać mail studeta, którego trzeba dodać:\n")
    if mail in students:
        print(f"Student z mailem \"{mail}\" już istnieje")
        return
    data = input("Prosze podać dane studenta w formacie:\n"
                 "\"<imie>,<nazwisko>,<punkty>[,<ocena>,<status>]\",\n"
                 "gdzie wszystko wpisane między [] jest opcjonalne, status może być GRADED albo MAILED\n")
    if not search("^[A-Z]?[a-z]+,[A-Z]?[a-z]+,\\d{1,3}(,[2-5](,(GRADED)|(MAILED))?)?$", data):
        print("Niepoprawne dane")
        return
    student = []
    data = data.split(",")
    student.append(data[0])
    student.append(data[1])
    student.append(int(data[2]))
    if len(data) > 3:
        student.append(data[3])
        if len(data) == 5:
            student.append(data[4])
    students.update({mail: student})
    save()
    print("Student został dodany")


students = read_students()

commands = ["rate all", "send mails", "add", "delete", "show", "exit"]

print(f'Prosze wpisywać komendy. Dostępne komendy to {commands}:')
command = input()
while command != "exit":
    if command not in commands:
        command = input("Podana komenda nie istnieje\n")
        continue
    if command == "rate all":
        calc_grads()
        command = input("Oceny studentów zostały przeliczone\n")
        continue
    if command == "send mails":
        send_mails()
        command = input("Maile zostały wysłane\n")
        continue
    if command == "add":
        add_student()
        command = input()
        continue
    if command == "show":
        show_students()
        command = input()
        continue
    if command == "delete":
        delete_student()
        command = input()
        continue
