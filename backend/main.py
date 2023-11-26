# Generate 20 patients
# Each patient has seleted id, random region and corresponding fraction number,
import random
import pydantic
import numpy as np
import enum

import collections
from ortools.sat.python import cp_model

class Machine2(enum.Enum):
    TB1 = "TB1"
    TB2 = "TB2"
    VB1 = "VB1"
    VB2 = "VB2"
    U = "U"

class Region2(enum.Enum):
    Craniospinal = "Craniospinal"
    Breast = "Breast"
    Breast_special = "Breast_special"
    Head_and_neck = "Head_and_neck"
    Abdomen = "Abdomen"
    Pelvis = "Pelvis"
    Crane = "Crane"
    Lung = "Lung"
    Lung_special = "Lung_special"
    Whole_Brain = "Whole_Brain"

class Patient2(pydantic.BaseModel):
    id: int
    region: Region2
    fraction_option: int
    
    def __str__(self):
        return f"{self.id} {self.region} {self.fraction_option} fractions"

    def __repr__(self):
        return str(self)

class Reservation2(pydantic.BaseModel):
    patient: Patient2
    machine: Machine2
    start_time: int
    end_time: int
    urgency: float

    def __str__(self):
        return f"{self.patient.id} {self.machine} start = {self.start_time}, end = {self.end_time}"

    def __repr__(self):
        return str(self)

class Event2(pydantic.BaseModel):
    title: str
    machine: Machine2
    start: int
    end: int
    region: Region2


# regions with probabilities (in dict)
# REGIONS_INFO = {Region.Craniospinal: {"probability": 0.01, "fraction_options": [13, 17, 20, 30]},
#            Region.Breast: {"probability": 0.25, "fraction_options": [15, 19, 25, 30]},
#            Region.Breast_special: {"probability": 0.05, "fraction_options": [15, 19, 25, 30]},
#            Region.Head_and_neck: {"probability": 0.1, "fraction_options": [5, 10, 15, 25, 30, 33, 35]},
#            Region.Abdomen: {"probability": 0.1, "fraction_options": [1, 3, 5, 8, 10, 12, 15, 18, 20, 30]},
#            Region.Pelvis: {"probability": 0.18, "fraction_options": [1, 3, 5, 10, 15, 22, 23, 25, 28, 35]},
#            Region.Crane: {"probability": 0.04, "fraction_options": [1, 5, 10, 13, 25, 30]},
#            Region.Lung: {"probability": 0.12, "fraction_options": [1, 5, 10, 15, 20, 25, 30, 33]},
#            Region.Lung_special: {"probability": 0.05, "fraction_options": [3, 5, 8]},
#            Region.Whole_Brain: {"probability": 0.1, "fraction_options": [5, 10, 12]}}
REGIONS_INFO = {Region2.Craniospinal: {"probability": 0.04, "fraction_options": [13, 17, 20, 30]},
           Region2.Breast: {"probability": 1.0, "fraction_options": [15, 19, 25, 30]},
           Region2.Breast_special: {"probability": 0.20, "fraction_options": [15, 19, 25, 30]},
           Region2.Head_and_neck: {"probability": 0.4, "fraction_options": [5, 10, 15, 25, 30, 33, 35]},
           Region2.Abdomen: {"probability": 0.4, "fraction_options": [1, 3, 5, 8, 10, 12, 15, 18, 20, 30]},
           Region2.Pelvis: {"probability": 0.72, "fraction_options": [1, 3, 5, 10, 15, 22, 23, 25, 28, 35]},
           Region2.Crane: {"probability": 0.12, "fraction_options": [1, 5, 10, 13, 25, 30]},
           Region2.Lung: {"probability": 0.48, "fraction_options": [1, 5, 10, 15, 20, 25, 30, 33]},
           Region2.Lung_special: {"probability": 0.20, "fraction_options": [3, 5, 8]},
           Region2.Whole_Brain: {"probability": 0.4, "fraction_options": [5, 10, 12]}}

# normalized probabilities from 0 to 1, where 0 is the minumum and 1 is the maximum (0.25 corresponds to 1)
# normalized_probabilities = [0.04, 1.0, 0.20, 0.4, 0.4, 0.72, 0.12, 0.48, 0.20, 0.4]


MACHINE_REGION_MAP = {
    Machine2.TB1: [Region2.Craniospinal, Region2.Breast, Region2.Breast_special, Region2.Head_and_neck, Region2.Abdomen, Region2.Pelvis, Region2.Crane, Region2.Lung, Region2.Lung_special],
    Machine2.TB2: [Region2.Craniospinal, Region2.Breast, Region2.Breast_special, Region2.Head_and_neck, Region2.Abdomen, Region2.Pelvis, Region2.Crane, Region2.Lung, Region2.Lung_special],

    Machine2.VB1: [Region2.Breast, Region2.Head_and_neck, Region2.Abdomen, Region2.Pelvis, Region2.Crane, Region2.Lung, Region2.Lung_special, Region2.Whole_Brain],
    Machine2.VB2: [Region2.Breast, Region2.Head_and_neck, Region2.Abdomen, Region2.Pelvis, Region2.Crane, Region2.Lung, Region2.Lung_special, Region2.Whole_Brain],

    Machine2.U: [Region2.Breast, Region2.Whole_Brain],
}

MACHINES = [Machine2.TB1, Machine2.TB2, Machine2.VB1, Machine2.VB2, Machine2.U]

# map to track when machines are next free (in minutes from the beginning)
MACHINE_RESERVATION_MAP = {
    Machine2.TB1: 0,
    Machine2.TB2: 0,
    Machine2.VB1: 0,
    Machine2.VB2: 0,
    Machine2.U: 0,
}

min_loss = 1e9

def generate_patients(n):
    patients = []
    for i in range(n):
        region = np.random.choice(list(REGIONS_INFO.keys()))
        fraction = np.random.choice(REGIONS_INFO[region]["fraction_options"])
        patients.append(Patient2(id=i, region=region, fraction_option=fraction))
    return patients


def compute_loss_for_reservations(reservations):
    loss = 0
    for r in reservations:
        loss += r.urgency * r.end_time
    return loss

    
def generate_random_fraction_duration():
    return np.random.randint(0, 24) + AVERAGE_MINUTES_PER_FRACTION
    # return AVERAGE_MINUTES_PER_FRACTION


def make_reservation(patient, machines, reservations):
    m: Machine2 = None
    closest_time_minutes = int(1e9)

    # find closes free time for correct region
    for machine in machines:
        if patient.region in MACHINE_REGION_MAP[machine]:
            if MACHINE_RESERVATION_MAP[machine] < closest_time_minutes:
                m = machine
                closest_time_minutes = MACHINE_RESERVATION_MAP[machine]
            
    duration = generate_random_fraction_duration()
    MACHINE_RESERVATION_MAP[m] += duration
    # reservations.append(Reservation(patient=patient, machine=m, start_time=closest_time_minutes, end_time=closest_time_minutes + AVERAGE_MINUTES_PER_FRACTION, urgency=REGIONS_INFO[patient.region]["probability"]))
    reservations.append(Reservation2(patient=patient, machine=m, start_time=closest_time_minutes, end_time=closest_time_minutes + duration, urgency=REGIONS_INFO[patient.region]["probability"]))
    assert(m is not None)
    

def create_all_reservations(patients, reservations):
    for patient in patients:
        make_reservation(patient, MACHINES, reservations)




AVERAGE_MINUTES_PER_FRACTION = 12 # 12 minutes

PATIENTS_NUM = 40

def create_events(reservations):
    events = []
    for r in reservations:
        events.append(Event2(title=str(f"{r.urgency} {r.patient.id}"), machine=r.machine, start=r.start_time, end=r.end_time, region=r.patient.region))

    # create dict of events but also parse Machine and Region as strings
    events_json = []
    for e in events:
        e.machine = e.machine.value
        e.region = e.region.value
        events_json.append(e.dict())

    import json
    with open("../front/web/public/events.json", "w") as f:
        json.dump(events_json, f)
        
    return events

def main():
    reservations = []
    processed_hashes = set()
    patients = generate_patients(PATIENTS_NUM)
    n = 0
    r_with_min_loss = None
    r_with_max_loss = None
    min_loss = 1e9
    max_loss = 0

    while n < 10000:
        random_picked = random.sample(patients, PATIENTS_NUM)
        processed_ids = [patient.id for patient in random_picked]
        hash_processed = hash(tuple(processed_ids))
        # if hash_processed not in processed_hashes:
        create_all_reservations(random_picked, reservations)
        loss = compute_loss_for_reservations(reservations)
        if loss > max_loss:
            max_loss = loss
            r_with_max_loss = reservations.copy()

        if loss < min_loss:
            min_loss = loss
            r_with_min_loss = reservations.copy()
        # else:
        #     print("loss", loss)
        #     print(reservations)
        processed_hashes.add(hash_processed)
        reservations.clear()
        MACHINE_RESERVATION_MAP[Machine2.TB1] = 0
        MACHINE_RESERVATION_MAP[Machine2.TB2] = 0
        MACHINE_RESERVATION_MAP[Machine2.VB1] = 0
        MACHINE_RESERVATION_MAP[Machine2.VB2] = 0
        MACHINE_RESERVATION_MAP[Machine2.U] = 0

        # else:
            # print("already processed")
        n += 1
        # break

    # print(MACHINE_RESERVATION_MAP)
    # print(reservations)
    print(r_with_min_loss)
    print(r_with_max_loss)
    print(min_loss)
    print(max_loss)

    create_events(r_with_min_loss)

    

class Event:
    def __str__(self):
        return f"P: {self.patient} {self.machine} - {self.start} - {self.end}"

    def __repr__(self):
        return f"P: {self.patient} {self.machine} - {self.start} - {self.end}"

    def __init__(self, machine, start, end, patient, region):
        self.machine = machine
        self.start = start
        self.end = end
        self.region = region
        self.patient =  patient

events = []

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, starts, presences, machines_for_treatments, patients):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__starts = starts
        self.__presences = presences
        self.__machines_for_treatments = machines_for_treatments
        self.__patients = patients
        self.__solution_count = 0
        self.__min_objective = float("inf")

    def on_solution_callback(self):
        # print("Solution %i, time = %f s, objective = %i" % (
        #     self.__solution_count, self.WallTime(), self.ObjectiveValue()))

        if self.ObjectiveValue() < self.__min_objective:
            self.__min_objective = self.ObjectiveValue()
            events.clear()
            for patient_id, patient in enumerate(self.__patients):
                treatment_session_index = 0

                for treatment_idx, treatment in enumerate(patient.treatments):
                    for session_id in range(treatment.num_sessions):
                        key = (patient_id, treatment_session_index, session_id)
                        start_value = self.Value(self.__starts[key])
                        machine_idx = -1
                        for alt_id, machine_id in enumerate(self.__machines_for_treatments[patient_id][treatment_session_index]):
                            if self.Value(self.__presences[key + (alt_id,)]):
                                machine_idx = machine_id
                                break

                        machine_name = machines[machine_idx].name if machine_idx != -1 else "N/A"
                        print(treatment.region)
                        events.append(Event(machine_name, start_value, start_value + treatment.duration, patient_id, treatment.region))
                        treatment_session_index += 1
            

        # for patient_id, patient in enumerate(self.__patients):
        #     print("Patient %i:" % patient_id)
        #     treatment_session_index = 0  # Index for treatment sessions across all treatments
        #     for treatment_idx, treatment in enumerate(patient.treatments):
        #         for session_id in range(treatment.num_sessions):
        #             key = (patient_id, treatment_session_index, session_id)
        #             start_value = self.Value(self.__starts[key])
        #             machine_idx = -1
        #             for alt_id, machine_id in enumerate(self.__machines_for_treatments[patient_id][treatment_session_index]):
        #                 if self.Value(self.__presences[key + (alt_id,)]):
        #                     machine_idx = machine_id
        #                     break  # We found the assigned machine
        #             machine_name = machines[machine_idx].name if machine_idx != -1 else "N/A"
        #             print("  Treatment %i session %i starts at %i on machine %s with duration %i" % (
        #                 treatment_idx, session_id, start_value, machine_name, treatment.duration))
        #             treatment_session_index += 1  # Increment after each session
            self.__solution_count += 1

class Machine:
    def __init__(self, name, regions):
        self.name = name
        self.regions = regions

class Treatment:
    def __init__(self, region, duration, num_sessions):
        self.region = region
        self.duration = duration
        self.num_sessions = num_sessions

class Patient:
    def __init__(self, treatments):
        self.treatments = treatments

class Solution:
    patients: list[Patient]
    machines: list[Machine]
    num_machines: int
    num_patients: int
    horizon: int

    def __init__(self, patients, machines, num_machines, num_patients, horizon):
        self.patients = patients
        self.machines = machines
        self.num_machines = num_machines
        self.num_patients = num_patients
        self.horizon = horizon

# Example data
machines = [
    Machine("TB1", ["Craniospinal", "Breast", "Breast_special", "Head_and_neck", "Abdomen", "Pelvis", "Crane", "Lung", "Lung_special"]),
    Machine("TB2", ["Craniospinal", "Breast", "Breast_special", "Head_and_neck", "Abdomen", "Pelvis", "Crane", "Lung", "Lung_special"]),
    Machine("VB1", ["Breast", "Head_and_neck", "Abdomen", "Pelvis", "Crane", "Lung", "Lung_special", "Whole_Brain"]),
    Machine("VB2", ["Breast", "Head_and_neck", "Abdomen", "Pelvis", "Crane", "Lung", "Lung_special", "Whole_Brain"]),
    Machine("U", ["Breast", "Whole_Brain"])
]

# patients = [
#     Patient([Treatment("Breast", 10, 15)]),  # 3 sessions, each with duration 1
#     Patient([Treatment("Lung", 12, 5)]),    # 4 sessions, each with duration 1
#     Patient([Treatment("Crane", 14, 8)]),   # 2 sessions, each with duration 1
#     Patient([Treatment("Breast", 12, 20)]),   # 2 sessions, each with duration 1
#     Patient([Treatment("Lung_special", 12, 20)]),   # 2 sessions, each with duration 1
#     Patient([Treatment("Head_and_neck", 12, 20)]),   # 2 sessions, each with duration 1
#     Patient([Treatment("Pelvis", 12, 20)]),   # 2 sessions, each with duration 1
# ]

# print(patients)

def map_patient2_to_patient(patients2):
    patients = []
    for p2 in patients2:
        treatments = []
        for i in range(p2.fraction_option):
            treatments.append(Treatment(p2.region.value, 12, 1))
        patients.append(Patient(treatments))
    return patients

p = generate_patients(10)
patients = map_patient2_to_patient(p)

num_machines = len(machines)
all_machines = range(num_machines)

num_patients = len(patients)
all_patients = range(num_patients)

horizon = sum(treatment.duration * treatment.num_sessions for patient in patients for treatment in patient.treatments)

model = cp_model.CpModel()

# Initialize start variables, interval variables, presences, and other necessary structures
intervals = collections.defaultdict(list)
starts = {}
presences = {}
machines_for_treatments = [[] for _ in all_patients]
patient_ends = []

# Model setup for each patient and their treatments
for patient_id in all_patients:
    patient = patients[patient_id]
    machine_assignment_idx = 0  # Reset index for each patient
    previous_end = None

    # Precompute machines for treatments before creating variables
    for treatment in patient.treatments:
        treatment_list = []
        for machine_id, machine in enumerate(machines):
            if treatment.region in machine.regions:
                treatment_list.append(machine_id)
        # Extend lists for the total number of sessions for current treatment
        machines_for_treatments[patient_id].extend([treatment_list] * treatment.num_sessions)

    # Create variables and constraints for each treatment's sessions
    for treatment_idx, treatment in enumerate(patient.treatments):
        for session_id in range(treatment.num_sessions):
            # Create a unique identifier for each session variable and interval
            suffix_name = f"p{patient_id}_t{treatment_idx}_s{session_id}"
            start = model.NewIntVar(0, horizon, f"start_{suffix_name}")
            end = model.NewIntVar(0, horizon, f"end_{suffix_name}")
            interval = model.NewIntervalVar(start, treatment.duration, end, f"interval_{suffix_name}")

            # Key for the session in the starts and presences dictionaries
            key = (patient_id, machine_assignment_idx, session_id)
            starts[key] = start

            if previous_end is not None:
                model.Add(start >= previous_end)  # Ensure treatments are sequential
            previous_end = end

            # Determine the available machines for the current session
            available_machines = machines_for_treatments[patient_id][machine_assignment_idx]
            if len(available_machines) == 1:
                # There is only one machine that can handle this treatment, so allocate it directly
                machine_id = available_machines[0]
                intervals[machine_id].append(interval)
                presences[key + (0,)] = model.NewConstant(1)
            else:
                # More than one machine can handle this treatment, so we need to select one
                alternatives = []
                for alt_id, machine_id in enumerate(available_machines):
                    alt_suffix = f"p{patient_id}_t{treatment_idx}_s{session_id}_m{alt_id}"
                    presence = model.NewBoolVar(f"presence_{alt_suffix}")

                    interval_alt = model.NewOptionalIntervalVar(start, treatment.duration, end, presence, f"interval_{alt_suffix}")
                    alternatives.append(presence)
                    presences[key + (alt_id,)] = presence
                    intervals[machine_id].append(interval_alt)

                model.AddExactlyOne(alternatives)  # Enforce that exactly one machine is selected

            machine_assignment_idx += 1  # Move to the next session in machines_for_treatments

    patient_ends.append(previous_end)

# Constraints to ensure no overlap on each machine
for machine_id in all_machines:
    if intervals[machine_id]:
        model.AddNoOverlap(intervals[machine_id])

# Objective: minimize the makespan (latest treatment completion time)
treatment_completion = model.NewIntVar(0, horizon, "treatment_completion")
model.AddMaxEquality(treatment_completion, patient_ends)
model.Minimize(treatment_completion)

solver = cp_model.CpSolver()
solution_printer = SolutionPrinter(starts, presences, machines_for_treatments, patients)
status = solver.Solve(model, solution_printer)



def create_events_2():
    # first map events to Event2
    import json
    global events
    events_to_save = []
    # for e in events:
    #     e = Event2(title=str(f"{e.patient}"), machine=e.machine, start=e.start, end=e.end, region=e.patient)
    #     events_to_save.append(e)


    # for r in reservations:
    #     events_to_save.append(Event2(title=str(f"{r.urgency} {r.patient.id}"), machine=r.machine, start=r.start_time, end=r.end_time, region=r.patient.region))

    # create dict of events but also parse Machine and Region as strings
    events_json = []
    # for e in events_to_save:
    #     e.machine = e.machine.value
    #     e.region = e.region.value
    #     events_json.append(e.dict())

    for e in events:
        # e.region = e.region.name
        events_json.append({'title': e.machine, 'machine': e.machine, 'start': e.start, 'end': e.end, 'patient': e.patient, 'region': e.region})
    # with open("../front/web/public/events.json", "w") as f:
    with open("../front/web/public/events_test.json", "w") as f:
        json.dump(events_json, f)
        
    return events_to_save

create_events_2()
# if __name__ == "__main__":
#     main()
