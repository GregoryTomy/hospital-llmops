# Hospital Data Documentation

This README document describes the datasets available for analyzing and querying data in a large hospital system managed by our company. The datasets cover various aspects of hospital operations including details about hospitals, physicians, insurance payers, patient visits, and reviews.

## Datasets

### 1. hospitals.csv
This dataset contains information about each hospital within the system.

1. hospital_id: An integer uniquely identifying a hospital.
2. hospital_name: The name of the hospital.
3. hospital_state: The state where the hospital is located.
There are a total of 30 hospitals recorded in this file.
### 2. physicians.csv
This file records details about the physicians employed in our hospital system.

1. physician_id: An integer uniquely identifying a physician.
2. physician_name: The name of the physician.
3. physician_dob: Date of birth of the physician.
4. physician_grad_year: The year the physician graduated from medical school.
5. medical_school: The medical school attended by the physician.
6. salary: The annual salary of the physician.

### 3. payers.csv
This dataset contains information about the insurance companies that are billed for patient visits.

1. payer_id: An integer uniquely identifying each insurance payer.
2. payer_name: The name of the insurance company.

The dataset includes five payers: Medicaid, UnitedHealthcare, Aetna, Cigna, and Blue Cross.

### 4. reviews.csv
This dataset comprises patient reviews concerning their experiences at the hospitals.

1. review_id: An integer uniquely identifying a review.
2. visit_id: An integer that identifies the patient’s visit linked to the review.
3. review: Free form text review left by the patient.
4. physician_name: Name of the physician who treated the patient.
5. hospital_name: Name of the hospital where the stay occurred.
6. patient_name: The name of the patient.

### 5. visits.csv
This dataset acts as a fact table connecting hospitals, physicians, patients, and payers with each hospital visit.

1. visit_id: The unique identifier for a hospital visit.
2. patient_id: The ID of the patient associated with the visit.
3. date_of_admission: The admission date to the hospital.
4. room_number: Room number of the patient.
5. admission_type: The type of admission (Elective, Emergency, Urgent).
6. chief_complaint: Primary reason for the hospital visit.
7. primary_diagnosis: Primary diagnosis made during the visit.
8. treatment_description: Summary of the treatment provided.
9. test_results: Results of tests performed (Inconclusive, Normal, Abnormal).
10. discharge_date: Discharge date from the hospital.
11. physician_id: ID of the treating physician.
12. hospital_id: ID of the hospital.
13. payer_id: ID of the insurance payer.
14. billing_amount: Amount billed to the insurance payer.
15. visit_status: Status of the visit (OPEN, DISCHARGED).


## Additional Information

### API for Wait Times
While historical data for wait times are not available, current wait time information can be retrieved via an API. 