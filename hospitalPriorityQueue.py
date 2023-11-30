from priorityQueue import PriorityQueue


class Patient:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

    def __str__(self):
        return f"Patient: {self.name} | Condition: {self.condition}"


class HospitalPriorityQueue:
    def __init__(self):
        self._data = PriorityQueue()

    def admit_patient(self, patient):
        priority = self._calculate_priority(patient.condition)
        self._data.enqueue(patient, priority)

        return f"Admitted {patient.name} with priority {priority}"

    def treat_patient(self):
        if self._data.is_empty():
            print("No patients to treat.")

            return "No patients to treat."
        else:
            treated_patient = self._data.dequeue()
            return f"Treated {treated_patient[0].name} with condition {treated_patient[0].condition}"

    def check_patients(self):
        patients = []
        if self._data.is_empty():
            return "No patients in the hospital queue."
        else:

            i = 0
            for patient in self._data._data:
                i += 1
                patient = f'{i}) Patient: {patient[0].name} | Condition: {patient[0].condition}'
                patients.append(patient)

        return patients

    def check_next_patient(self):
        if self._data.is_empty():
            return "No patients in the hospital queue."
        else:
            print("Next patient in the hospital:")
            patient = self._data.peek()
            patient = f'Patient: {patient[0].name} | Condition: {patient[0].condition}'

        return patient

    def change_priority(self, patient_name, new_condition):
        patient = self.search_patient(patient_name)
        if patient is None:
            return f"Patient {patient_name} not found in the hospital."

        priority = self._calculate_priority(new_condition)
        self._data.change_priority(patient, priority)

        return f"Changed priority of {patient_name} to {priority}"

    def search_patient(self, patient_name):
        patient = None
        for _, (patient, priority) in enumerate(self._data.data):
            print(f'Before if: {patient}')
            if patient.name == patient_name:
                print(f'After if: {patient}')
                return patient

        return None

    @staticmethod
    def _calculate_priority(condition):
        if condition == "Critical":
            return 1
        elif condition == "Serious":
            return 2
        elif condition == "Stable":
            return 3
        else:
            return 4

    def find_patient_position(self, target_patient):
        if self._data.is_empty():

            return "No patients in the hospital queue."

        for i, (patient, priority) in enumerate(self._data.data):
            if patient.name == target_patient:
                return i+1
        return None


def main():
    hospital = HospitalPriorityQueue()

    while True:
        print("\nHospital Management System Menu:")
        print("1. Admit a patient")
        print("2. Treat a patient")
        print("3. Check patients")
        print("4. Check next patient")
        print("5. Check patient position")
        print("6. Change patient priority")
        print("7. Exit")
        print()

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter patient name: ")
            condition = input(
                "Enter patient condition (Critical/Serious/Stable): ")
            patient = Patient(name, condition)
            hospital.admit_patient(patient)
            print()
        elif choice == "2":
            hospital.treat_patient()
        elif choice == "3":
            hospital.check_patients()
        elif choice == "4":
            hospital.check_next_patient()
        elif choice == "5":
            patient = input("Enter patient name: ")
            hospital.find_patient_position(patient)
        elif choice == "6":
            patient = input("Enter patient name: ")
            condition = input(
                "Enter patient condition (Critical/Serious/Stable): ")
            hospital.change_priority(patient, condition)

        elif choice == "7":
            print("Exiting the Hospital Management System.")
            break
        else:
            print("Invalid choice. Please select a valid option (1-4).")


if __name__ == "__main__":
    main()
