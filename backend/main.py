# Generate 20 patients
# Each patient has seleted id, random region and corresponding fraction number,
import random
import pydantic
import numpy as np
import enum

class Machine(enum.Enum):
    TB1 = "TB1"
    TB2 = "TB2"
    VB1 = "VB1"
    VB2 = "VB2"
    U = "U"

class Region(enum.Enum):
    Craniospinal = "Craniospinal"
    Breast = "Breast"
    Breast_special = "Breast special"
    Head_and_neck = "Head and neck"
    Abdomen = "Abdomen"
    Pelvis = "Pelvis"
    Crane = "Crane"
    Lung = "Lung"
    Lung_special = "Lung special"
    Whole_Brain = "Whole Brain"

class Patient(pydantic.BaseModel):
    id: int
    region: Region
    fraction_option: int
    
    def __str__(self):
        return f"{self.id} {self.region} {self.fraction_option} fractions"

    def __repr__(self):
        return str(self)

class Reservation(pydantic.BaseModel):
    patient: Patient
    machine: Machine
    start_time: int
    end_time: int
    urgency: float

    def __str__(self):
        return f"{self.patient.id} {self.machine} start = {self.start_time}, end = {self.end_time}"

    def __repr__(self):
        return str(self)



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
REGIONS_INFO = {Region.Craniospinal: {"probability": 0.04, "fraction_options": [13, 17, 20, 30]},
           Region.Breast: {"probability": 1.0, "fraction_options": [15, 19, 25, 30]},
           Region.Breast_special: {"probability": 0.20, "fraction_options": [15, 19, 25, 30]},
           Region.Head_and_neck: {"probability": 0.4, "fraction_options": [5, 10, 15, 25, 30, 33, 35]},
           Region.Abdomen: {"probability": 0.4, "fraction_options": [1, 3, 5, 8, 10, 12, 15, 18, 20, 30]},
           Region.Pelvis: {"probability": 0.72, "fraction_options": [1, 3, 5, 10, 15, 22, 23, 25, 28, 35]},
           Region.Crane: {"probability": 0.12, "fraction_options": [1, 5, 10, 13, 25, 30]},
           Region.Lung: {"probability": 0.48, "fraction_options": [1, 5, 10, 15, 20, 25, 30, 33]},
           Region.Lung_special: {"probability": 0.20, "fraction_options": [3, 5, 8]},
           Region.Whole_Brain: {"probability": 0.4, "fraction_options": [5, 10, 12]}}

# normalized probabilities from 0 to 1, where 0 is the minumum and 1 is the maximum (0.25 corresponds to 1)
# normalized_probabilities = [0.04, 1.0, 0.20, 0.4, 0.4, 0.72, 0.12, 0.48, 0.20, 0.4]


MACHINE_REGION_MAP = {
    Machine.TB1: [Region.Craniospinal, Region.Breast, Region.Breast_special, Region.Head_and_neck, Region.Abdomen, Region.Pelvis, Region.Crane, Region.Lung, Region.Lung_special],
    Machine.TB2: [Region.Craniospinal, Region.Breast, Region.Breast_special, Region.Head_and_neck, Region.Abdomen, Region.Pelvis, Region.Crane, Region.Lung, Region.Lung_special],

    Machine.VB1: [Region.Breast, Region.Head_and_neck, Region.Abdomen, Region.Pelvis, Region.Crane, Region.Lung, Region.Lung_special, Region.Whole_Brain],
    Machine.VB2: [Region.Breast, Region.Head_and_neck, Region.Abdomen, Region.Pelvis, Region.Crane, Region.Lung, Region.Lung_special, Region.Whole_Brain],

    Machine.U: [Region.Breast, Region.Whole_Brain],
}

MACHINES = [Machine.TB1, Machine.TB2, Machine.VB1, Machine.VB2, Machine.U]

# map to track when machines are next free (in minutes from the beginning)
MACHINE_RESERVATION_MAP = {
    Machine.TB1: 0,
    Machine.TB2: 0,
    Machine.VB1: 0,
    Machine.VB2: 0,
    Machine.U: 0,
}

min_loss = 1e9

def generate_patients(n):
    patients = []
    for i in range(n):
        region = np.random.choice(list(REGIONS_INFO.keys()))
        fraction = np.random.choice(REGIONS_INFO[region]["fraction_options"])
        patients.append(Patient(id=i, region=region, fraction_option=fraction))
    return patients


def compute_loss_for_reservations(reservations):
    loss = 0
    for r in reservations:
        loss += r.urgency * r.end_time
    return loss

    

def make_reservation(patient, machines, reservations):
    m: Machine = None
    closest_time_minutes = int(1e9)

    # find closes free time for correct region
    for machine in machines:
        if patient.region in MACHINE_REGION_MAP[machine]:
            if MACHINE_RESERVATION_MAP[machine] < closest_time_minutes:
                m = machine
                closest_time_minutes = MACHINE_RESERVATION_MAP[machine]
            
    MACHINE_RESERVATION_MAP[m] += AVERAGE_MINUTES_PER_FRACTION
    reservations.append(Reservation(patient=patient, machine=m, start_time=closest_time_minutes, end_time=closest_time_minutes + AVERAGE_MINUTES_PER_FRACTION, urgency=REGIONS_INFO[patient.region]["probability"]))
    assert(m is not None)
    

def create_all_reservations(patients, reservations):
    for patient in patients:
        make_reservation(patient, MACHINES, reservations)




AVERAGE_MINUTES_PER_FRACTION = 12 # 12 minutes

PATIENTS_NUM = 10

def main():
    reservations = []
    processed_hashes = set()
    patients = generate_patients(PATIENTS_NUM)
    n = 0
    r_with_min_loss = None
    r_with_max_loss = None
    min_loss = 1e9
    max_loss = 0

    while n < 1000:
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
        MACHINE_RESERVATION_MAP[Machine.TB1] = 0
        MACHINE_RESERVATION_MAP[Machine.TB2] = 0
        MACHINE_RESERVATION_MAP[Machine.VB1] = 0
        MACHINE_RESERVATION_MAP[Machine.VB2] = 0
        MACHINE_RESERVATION_MAP[Machine.U] = 0

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


if __name__ == "__main__":
    main()
