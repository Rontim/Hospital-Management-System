import tkinter as tk
from tkinter import messagebox, simpledialog, OptionMenu

from hospitalPriorityQueue import HospitalPriorityQueue, Patient


class HospitalGUI:
    def __init__(self, master):
        self.patient_position = None
        self.master = master
        self.master.title("Hospital Management System")

        self.patient_image = tk.PhotoImage(file="man-stand.png")
        self.stick_man_objects = []

        self.hospital = HospitalPriorityQueue()

        self.hospital_frame = tk.Frame(
            master, width=850, height=450, padx=10, pady=10)
        self.hospital_frame.pack()

        self.waiting_room_canvas = tk.Canvas(
            self.hospital_frame, width=830, height=200, bg="yellow")
        self.waiting_room_canvas.place(x=10, y=10)

        self.waiting_room_label = tk.Label(
            self.hospital_frame, text="Waiting Room", padx=10, pady=5, font=("Arial", 12))
        self.waiting_room_label.place(x=10, y=5)

        self.reception()

        button_width = 15
        button_height = 2
        button_margin = 10

        self.admit_button = tk.Button(
            self.hospital_frame, text="Admit Patient", command=self.admit_patient, width=button_width,
            background='blue')
        self.admit_button.place(x=10, y=250)

        self.treat_button = tk.Button(
            self.hospital_frame, text="Treat Patient", command=self.treat_patient, width=button_width,
            background='blue')
        self.treat_button.place(x=420, y=250)

        self.check_button = tk.Button(
            self.hospital_frame, text="Check Patients", command=self.check_patients, width=button_width,
            background='blue')
        self.check_button.place(x=10, y=285)

        self.next_button = tk.Button(
            self.hospital_frame, text="Check Next Patient", command=self.check_next_patient, width=button_width,
            background='blue')
        self.next_button.place(x=420, y=285)

        self.priority_button = tk.Button(
            self.hospital_frame, text="Change Priority", command=self.change_priority, width=button_width,
            background='blue')
        self.priority_button.place(x=210, y=320)

        self.exit_button = tk.Button(
            self.hospital_frame, text="Exit", command=self.exit, width=10, background="red")

        self.exit_button.place(x=230, y=360)

    def reception(self):
        self._reception = self.waiting_room_canvas.create_rectangle(
            60, 150, 100, 200, outline="black", fill="blue")
        self._reception_label = self.waiting_room_canvas.create_text(
            90, 140, text="Reception", font=("Arial", 12))
        self._receptionist = self.waiting_room_canvas.create_image(
            5, 120, image=self.patient_image, anchor=tk.NW)

    def exit(self):
        confirmation = messagebox.askokcancel(
            "Exit", "Exiting Hospital Management System...       \nAre you sure?", icon="warning")
        if confirmation:
            self.master.destroy()

    def admit_patient(self):
        name = simpledialog.askstring(
            "Admit Patient", "Enter patient name:")

        if name is None:
            return messagebox.showinfo("Admit Patient", "Patient admission cancelled", icon="warning")

        if len(name) == 0:
            messagebox.showinfo(
                "Admit Patient", "Patient name cannot be empty", icon="warning")
            return self.admit_patient()

        condition = simpledialog.askstring(
            "Admit Patient", "Enter patient condition (Critical/Serious/Stable):")

        if condition is None:
            return messagebox.showinfo("Admit Patient", "Patient admission cancelled", icon="warning")
        if len(condition) == 0:
            messagebox.showinfo(
                "Admit Patient", "Patient condition cannot be empty", icon="warning")
            return self.admit_patient()

        if condition and name:
            name = name.capitalize()
            condition = condition.capitalize()

        patient = Patient(name, condition)
        result = self.hospital.admit_patient(patient)
        self.patient_position = self.hospital.find_patient_position(name)
        messagebox.showinfo("Admitted Patient", result)
        self.draw_patient(patient.name, self.patient_position)

    def treat_patient(self):
        result = self.hospital.treat_patient()
        messagebox.showinfo("Treat Patient", result)

        self.remove_patient()

    def check_patients(self):
        result = self.hospital.check_patients()
        message = ''
        if type(result) is str:
            message = "No patients in the hospital."
        else:
            for item in result:
                message += item + '\n'

            message += f'\nTotal patients: {len(result)}'

        messagebox.showinfo("Check Patients", message)

    def check_next_patient(self):
        result = self.hospital.check_next_patient()
        if type(result) is str:
            messagebox.showinfo("Check Next Patient", result)
        else:
            messagebox.showinfo(
                "Check Next Patient", f'Patient: {result[0].name} | Condition: {result[0].condition}')

    def change_priority(self):
        patient_name = simpledialog.askstring(
            "Change Priority", "Enter patient name:")

        if patient_name is None:
            return messagebox.showinfo("Change Priority", "Change priority cancelled", icon="warning")

        if len(patient_name) == 0:
            messagebox.showinfo(
                "Change Priority", "Patient name cannot be empty", icon="warning")
            return self.change_priority()

        new_condition = simpledialog.askstring(
            "Change Priority", "Enter patient condition (Critical/Serious/Stable):")

        if new_condition is None:
            return messagebox.showinfo("Change Priority", "Change priority cancelled", icon="warning")
        if len(new_condition) == 0:
            messagebox.showinfo(
                "Change Priority", "Patient condition cannot be empty", icon="warning")
            return self.change_priority()

        print(patient_name, new_condition)

        old_position = self.hospital.find_patient_position(patient_name)

        result = self.hospital.change_priority(
            patient_name, new_condition)

        new_position = self.hospital.find_patient_position(patient_name)

        if old_position is not None:
            self.re_draw_patients(
                patient=patient_name, position=new_position, old_position=old_position)

        messagebox.showinfo("Change Priority", result)

    def re_draw_patients(self, patient, position, old_position):
        oldPosition = self.stick_man_objects.pop(old_position - 1)
        self.waiting_room_canvas.delete(oldPosition['name'])
        self.waiting_room_canvas.delete(oldPosition['stickman'])

        print(f'Old position: {old_position}')
        print(f'New position: {position}')

        if position == old_position:
            return

        if position < old_position:
            self.draw_patient(patient, position)

        if position > old_position:
            for i in range(old_position - 1, position - 1):
                self.waiting_room_canvas.move(
                    self.stick_man_objects[i]['name'], -100, 0)
                self.waiting_room_canvas.move(
                    self.stick_man_objects[i]['stickman'], -100, 0)

            self.draw_patient(patient, position)

    def draw_patient(self, patient, position):
        x = 20 + (position * 105)
        y = 100

        position = position - 1

        for i in range(position, len(self.stick_man_objects)):
            _object = self.stick_man_objects[i]
            self.waiting_room_canvas.move(_object['name'], 105, 0)
            self.waiting_room_canvas.move(_object['stickman'], 100, 0)

        new_stickman_image = self.waiting_room_canvas.create_image(
            x - 10, y + 20, image=self.patient_image, anchor=tk.NW)
        patient_name = self.waiting_room_canvas.create_text(
            x + 5, y, text=f'(Name: {patient})', anchor=tk.CENTER, font=("Arial", 10))

        new_object = {
            'name': patient_name,
            'stickman': new_stickman_image,
        }

        self.stick_man_objects.insert(position, new_object)

    def remove_patient(self):
        if len(self.stick_man_objects) > 0:
            top_patient = self.stick_man_objects.pop(0)
            self.waiting_room_canvas.delete(top_patient['name'])
            self.waiting_room_canvas.delete(top_patient['stickman'])

            for i in self.stick_man_objects:
                self.waiting_room_canvas.move(i['name'], -100, 0)
                self.waiting_room_canvas.move(i['stickman'], -100, 0)


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()
