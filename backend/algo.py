import collections
from ortools.sat.python import cp_model


class Event:
    def __str__(self):
        return f"P: {self.patient} {self.machine} - {self.start} - {self.end}"

    def __repr__(self):
        return f"P: {self.patient} {self.machine} - {self.start} - {self.end}"

    def __init__(self, machine, start, end, patient):
        self.machine = machine
        self.start = start
        self.end = end
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
        print("Solution %i, time = %f s, objective = %i" % (
            self.__solution_count, self.WallTime(), self.ObjectiveValue()))

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
                        events.append(Event(machine_name, start_value, start_value + treatment.duration, patient_id))
                        treatment_session_index += 1
            

        for patient_id, patient in enumerate(self.__patients):
            print("Patient %i:" % patient_id)
            treatment_session_index = 0  # Index for treatment sessions across all treatments
            for treatment_idx, treatment in enumerate(patient.treatments):
                for session_id in range(treatment.num_sessions):
                    key = (patient_id, treatment_session_index, session_id)
                    start_value = self.Value(self.__starts[key])
                    machine_idx = -1
                    for alt_id, machine_id in enumerate(self.__machines_for_treatments[patient_id][treatment_session_index]):
                        if self.Value(self.__presences[key + (alt_id,)]):
                            machine_idx = machine_id
                            break  # We found the assigned machine
                    machine_name = machines[machine_idx].name if machine_idx != -1 else "N/A"
                    print("  Treatment %i session %i starts at %i on machine %s with duration %i" % (
                        treatment_idx, session_id, start_value, machine_name, treatment.duration))
                    treatment_session_index += 1  # Increment after each session
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

patients = [
    Patient([Treatment("Breast", 10, 15)]),  # 3 sessions, each with duration 1
    Patient([Treatment("Lung", 12, 5)]),    # 4 sessions, each with duration 1
    Patient([Treatment("Crane", 14, 8)]),   # 2 sessions, each with duration 1
    Patient([Treatment("Breast", 12, 20)]),   # 2 sessions, each with duration 1
    Patient([Treatment("Lung_special", 12, 20)]),   # 2 sessions, each with duration 1
    Patient([Treatment("Head_and_neck", 12, 20)]),   # 2 sessions, each with duration 1
    Patient([Treatment("Pelvis", 12, 20)]),   # 2 sessions, each with duration 1
]

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


# Print final solution (if a solution was found).
# if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
#     print("Solve status: %s" % solver.StatusName(status))
#     print("Optimal objective value: %i" % solver.ObjectiveValue())
#     for patient_id, patient in enumerate(patients):
#         print("Patient %i:" % patient_id)
#         machine_assignment_idx = 0  # Reset index for each patient
#         for treatment_idx, treatment in enumerate(patient.treatments):
#             for session_id in range(treatment.num_sessions):
#                 key = (patient_id, machine_assignment_idx, session_id)
#                 if key in starts:
#                     start_value = solver.Value(starts[key])
#                     machine_idx = -1
#                     available_machines = machines_for_treatments[patient_id][machine_assignment_idx]
#                     for alt_id, machine_id in enumerate(available_machines):
#                         if solver.Value(presences[key + (alt_id,)]):
#                             machine_idx = machine_id
#                             break  # Assigned machine found
#
#                     machine_name = machines[machine_idx].name if machine_idx != -1 else "N/A"
#                     print(f"  Treatment {treatment_idx} session {session_id} starts at {start_value} on machine {machine_name} with duration {treatment.duration}")
#                 else:
#                     print(f"  Treatment {treatment_idx} session {session_id} could not be assigned a machine")
#             machine_assignment_idx += 1  # Increment the index after processing all sessions of a treatment
# else:
#     print("No solution found.")
#
# Display search statistics.
# print("\nStatistics")
# print("  - conflicts : %i" % solver.NumConflicts())
# print("  - branches  : %i" % solver.NumBranches())
# print("  - wall time : %f s" % solver.WallTime())
def compute(patients):


