import tkinter as tk
from tkinter import messagebox

# Store data
doctors = []
appointment_requests = []

class HealthApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Health Companion App")
        self.root.geometry("600x500")
        self.current_user = None
        self.show_login_page()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- LOGIN PAGE ----------------
    def show_login_page(self):
        self.clear_screen()

        tk.Label(self.root, text="Health Companion App", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Login As", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Patient", width=20, command=self.patient_basic_details).pack(pady=10)
        tk.Button(self.root, text="Doctor", width=20, command=self.doctor_basic_details).pack(pady=10)

    # ---------------- PATIENT FLOW ----------------
    def patient_basic_details(self):
        self.clear_screen()

        tk.Label(self.root, text="Patient Basic Details", font=("Arial", 14)).pack(pady=10)

        self.p_name = tk.Entry(self.root)
        self.p_email = tk.Entry(self.root)
        self.p_phone = tk.Entry(self.root)
        self.p_address = tk.Entry(self.root)

        for label, entry in [("Name", self.p_name),
                             ("Email", self.p_email),
                             ("Phone", self.p_phone),
                             ("Address", self.p_address)]:
            tk.Label(self.root, text=label).pack()
            entry.pack()

        tk.Button(self.root, text="Next", command=self.patient_health_details).pack(pady=10)

    def patient_health_details(self):
        self.clear_screen()

        tk.Label(self.root, text="Health Details (Optional)", font=("Arial", 14)).pack(pady=10)

        self.bp = tk.Entry(self.root)
        self.sugar = tk.Entry(self.root)
        self.chol = tk.Entry(self.root)
        self.allergy = tk.Entry(self.root)
        self.other = tk.Entry(self.root)

        for label, entry in [("Blood Pressure", self.bp),
                             ("Blood Sugar", self.sugar),
                             ("Cholesterol", self.chol),
                             ("Allergy", self.allergy),
                             ("Other Diseases", self.other)]:
            tk.Label(self.root, text=label).pack()
            entry.pack()

        tk.Button(self.root, text="Next", command=self.patient_symptoms_page).pack(pady=10)

    def patient_symptoms_page(self):
        self.clear_screen()

        tk.Label(self.root, text="Enter Symptoms", font=("Arial", 14)).pack(pady=10)

        self.symptoms = tk.Entry(self.root, width=50)
        self.symptoms.pack()

        tk.Button(self.root, text="Find Doctors", command=self.show_doctor_list).pack(pady=10)

    def show_doctor_list(self):
        self.clear_screen()

        tk.Label(self.root, text="Available Doctors", font=("Arial", 14)).pack(pady=10)

        if not doctors:
            tk.Label(self.root, text="No doctors available.").pack()
            tk.Button(self.root, text="Back", command=self.show_login_page).pack()
            return

        for doc in doctors:
            tk.Button(self.root,
                      text=f"{doc['name']} - {doc['specialization']} - {doc['location']}",
                      command=lambda d=doc: self.send_request(d)).pack(pady=5)

    def send_request(self, doctor):
        patient_data = {
            "name": self.p_name.get(),
            "email": self.p_email.get(),
            "phone": self.p_phone.get(),
            "address": self.p_address.get(),
            "symptoms": self.symptoms.get()
        }

        appointment_requests.append({"doctor": doctor, "patient": patient_data, "status": "Pending"})
        messagebox.showinfo("Success", "Appointment Request Sent!")
        self.show_login_page()

    # ---------------- DOCTOR FLOW ----------------
    def doctor_basic_details(self):
        self.clear_screen()

        tk.Label(self.root, text="Doctor Basic Details", font=("Arial", 14)).pack(pady=10)

        self.d_name = tk.Entry(self.root)
        self.d_reg = tk.Entry(self.root)
        self.d_spec = tk.Entry(self.root)
        self.d_time = tk.Entry(self.root)

        for label, entry in [("Name", self.d_name),
                             ("Registration Number", self.d_reg),
                             ("Specialization", self.d_spec),
                             ("Available Time", self.d_time)]:
            tk.Label(self.root, text=label).pack()
            entry.pack()

        tk.Button(self.root, text="Next", command=self.doctor_clinic_details).pack(pady=10)

    def doctor_clinic_details(self):
        self.clear_screen()

        tk.Label(self.root, text="Clinic Details", font=("Arial", 14)).pack(pady=10)

        self.d_location = tk.Entry(self.root)
        self.d_contact = tk.Entry(self.root)

        for label, entry in [("Clinic Location", self.d_location),
                             ("Clinic Contact", self.d_contact)]:
            tk.Label(self.root, text=label).pack()
            entry.pack()

        tk.Button(self.root, text="Register", command=self.register_doctor).pack(pady=10)

    def register_doctor(self):
        doctor = {
            "name": self.d_name.get(),
            "reg": self.d_reg.get(),
            "specialization": self.d_spec.get(),
            "time": self.d_time.get(),
            "location": self.d_location.get(),
            "contact": self.d_contact.get()
        }

        doctors.append(doctor)
        messagebox.showinfo("Success", "Doctor Registered Successfully!")
        self.doctor_notifications(doctor)

    def doctor_notifications(self, doctor):
        self.clear_screen()
        tk.Label(self.root, text="Appointment Requests", font=("Arial", 14)).pack(pady=10)

        found = False
        for req in appointment_requests:
            if req["doctor"] == doctor and req["status"] == "Pending":
                found = True
                patient = req["patient"]
                tk.Label(self.root,
                         text=f"Patient: {patient['name']} | Symptoms: {patient['symptoms']}").pack()
                tk.Button(self.root,
                          text="Accept",
                          command=lambda r=req: self.accept_request(r)).pack(pady=5)

        if not found:
            tk.Label(self.root, text="No appointment requests.").pack()

        tk.Button(self.root, text="Back to Login", command=self.show_login_page).pack(pady=10)

    def accept_request(self, request):
        request["status"] = "Accepted"
        messagebox.showinfo("Accepted", "Appointment Accepted!")

# Run App
root = tk.Tk()
app = HealthApp(root)
root.mainloop()