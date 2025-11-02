class Event:
    def __init__(self, name, date, venue):
        self.name = name
        self.date = date
        self.venue = venue
        self.participants = []

    def add_participant(self, student):
        self.participants.append(student)
        print(f"Participant {student.name} added to event {self.name}")

    def show_participants(self):
        if not self.participants:
            print("No participants registered yet.")
        else:
            print(f"Participants for event {self.name}:")
            for s in self.participants:
                print(f"- {s.name} (Roll No: {s.roll_no}, Department: {s.department})")


class Student:
    def __init__(self, name, department, roll_no):
        self.name = name
        self.department = department
        self.roll_no = roll_no

    def register_for_event(self, event):
        event.add_participant(self)


class Admin:
    def __init__(self, name, department=None):
        self.name = name
        self.department = department
        self.events = []

    def create_event(self, name, date, venue):
        new_event = Event(name, date, venue)
        self.events.append(new_event)
        print(f"Event '{name}' created by admin {self.name}")
        return new_event

    def show_all_events(self):
        if not self.events:
            print("No events available.")
        else:
            print("Available Events:")
            for e in self.events:
                print(f"- {e.name} ({e.date} at {e.venue})")


admin = Admin("Ashith")
code_manthan = admin.create_event("Code Manthan", "12-06-2024", "Auditorium")
anveshan = admin.create_event("Anveshan", "15-06-2024", "Conference Hall")
admin.show_all_events()
s1 = Student("Ashith Rai", "AIML", "21VC101")
s2 = Student("Diya", "CSE", "21VC102")
s1.register_for_event(code_manthan)
s2.register_for_event(anveshan)
s2.register_for_event(code_manthan)
code_manthan.show_participants()
anveshan.show_participants()
