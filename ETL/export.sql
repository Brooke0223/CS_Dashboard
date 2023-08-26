-- Create supplementary views and/or tables (that will represent dimensions)

-- Create 'Drugs' View
CREATE OR REPLACE VIEW `Drugs` AS
SELECT 
    DENSE_RANK() OVER (ORDER BY Drug_Name_Strength) AS drug_id,
    Drug_Name_Strength,
    AHFS_Description as Drug_Category,
    DEA_Drug_Schedule
FROM Prescription_Data
GROUP BY Drug_Name_Strength, Drug_Category, DEA_Drug_Schedule;


-- Create 'Locations' View
CREATE OR REPLACE VIEW `Locations` AS 
SELECT 
    ROW_NUMBER() OVER (ORDER BY County ASC) AS location_id,
    County,
    State
FROM (
    SELECT 
        Patient_County AS County, 
        Patient_State AS State 
    FROM Prescription_Data 

    UNION

    SELECT
        Prescriber_County AS County,
        Prescriber_State AS State
    FROM Prescription_Data 
) AS Subquery
ORDER BY County ASC;


-- Create 'Age_Brackets' Table
CREATE TABLE IF NOT EXISTS Age_Brackets (
    age_category_id VARCHAR(255) PRIMARY KEY,
    minimum_age INT NOT NULL,
    maximum_age INT
);

INSERT INTO Age_Brackets (age_category_id, minimum_age, maximum_age) VALUES ('Ages 4 and younger', 0, 4);
INSERT INTO Age_Brackets (age_category_id, minimum_age, maximum_age) VALUES ('Ages 5 To 17', 5, 17);
INSERT INTO Age_Brackets (age_category_id, minimum_age, maximum_age) VALUES ('Ages 18 To 24', 18, 24);
INSERT INTO Age_Brackets (age_category_id, minimum_age, maximum_age) VALUES ('Ages 25 To 34', 25, 34);
INSERT INTO Age_Brackets (age_category_id, minimum_age, maximum_age) VALUES ('Ages 35 To 44', 35, 44);
INSERT INTO Age_Brackets (age_category_id, minimum_age, maximum_age) VALUES ('Ages 45 To 54', 45, 54);
INSERT INTO Age_Brackets (age_category_id, minimum_age, maximum_age) VALUES ('Ages 55 To 64', 55, 64);
INSERT INTO Age_Brackets (age_category_id, minimum_age, maximum_age) VALUES ('Ages 65 and older', 65, NULL);


-- Create 'Dates' Table
CREATE TABLE IF NOT EXISTS Dates (
    year_id YEAR NOT NULL
);

INSERT INTO Dates (year_id) VALUES (2013);
INSERT INTO Dates (year_id) VALUES (2014);
INSERT INTO Dates (year_id) VALUES (2015);
INSERT INTO Dates (year_id) VALUES (2016);
INSERT INTO Dates (year_id) VALUES (2017);
INSERT INTO Dates (year_id) VALUES (2018);
INSERT INTO Dates (year_id) VALUES (2019);
INSERT INTO Dates (year_id) VALUES (2020);
INSERT INTO Dates (year_id) VALUES (2021);
INSERT INTO Dates (year_id) VALUES (2022);



-- ------------------------------------------------------------------------------------------------------------------------
-- Update the Main “Prescription_Data” Table to include a column for foreign keys,
-- then join the newly-created dimension tables based on the FK that connects them

-- Update Prescription_Data table to include FK column for drug_id
ALTER TABLE Prescription_Data
ADD COLUMN drug_id INT;
-- Populate the drug_id column using a JOIN with the Drug_dimensions table
UPDATE Prescription_Data AS p
JOIN Drugs AS d ON p.drug_name_strength = d.drug_name_strength
SET p.drug_id = d.drug_id;


-- Update Prescription_Data table to include FK column for patient_age_category
ALTER TABLE Prescription_Data
ADD COLUMN patient_age_category_id VARCHAR(255);
-- Populate the patient_age_category column using a JOIN with the Age_Brackets table
UPDATE Prescription_Data AS p
JOIN Age_Brackets AS a ON p.patient_age_bracket = a.age_category_id
SET p.patient_age_category_id = a.age_category_id;


-- Update Prescription_Data table to include FK column for patient_location_category_id 
-- (*BUT ONLY FOR PRESCRIPTION_DATA ROWS ERTAINING TO PATIENT (NOT PRESCRIBER) DATA*)
ALTER TABLE Prescription_Data
ADD COLUMN patient_location_category_id INT;

-- Update the "patient_location_category_id" column using a JOIN with the Dates table
UPDATE Prescription_Data AS p
JOIN Locations AS l ON p.patient_county = l.county AND p.patient_state = l.state
SET p.patient_location_category_id = l.location_id
WHERE p.Patient_County IS NOT NULL;

-- Update the "patient_location_category_id" column to NULL for rows where there is no patient location data
UPDATE Prescription_Data
SET Prescription_Data.patient_location_category_id = NULL
WHERE Prescription_Data.Patient_County IS NULL;



-- ------------------------------------------------------------------------------------------------------------------------
-- Update Prescription_Data table to include FK column for prescriber_location_category_id 
-- (*BUT ONLY FOR PRESCRIPTION_DATA ROWS PERTAINING TO PRESCRIBER (NOT PATIENT) DATA*)
ALTER TABLE Prescription_Data
ADD COLUMN prescriber_location_category_id INT;

-- Update the "prescriber_location_category_id" column using a JOIN with the Dates table
UPDATE Prescription_Data AS p
JOIN Locations AS l ON p.prescriber_county = l.county AND p.prescriber_state = l.state
SET p.prescriber_location_category_id = l.location_id
WHERE p.Prescriber_County IS NOT NULL;

-- Update the "patient_location_category_id" column to NULL for rows where there is no patient location data
UPDATE Prescription_Data
SET Prescription_Data.prescriber_location_category_id = NULL
WHERE Prescription_Data.Prescriber_County IS NULL;


-- Update the Population table to include FK column for location_id foreign key
ALTER TABLE Population
ADD COLUMN location_id INT;
-- Update the "location_id" column using a JOIN with the Dates table
UPDATE Population AS p
JOIN Locations AS l ON l.county = p.county AND l.state = 'Michigan'
SET p.location_id = l.location_id;



-- Create views for both fact tables (by pulling data from the main “Prescription_Data” table)
-- (Note: Prescriptions_By_PATIENT_Category should only take rows pertaining to PATIENT data)
CREATE OR REPLACE VIEW `Prescriptions_By_Patient_Category` AS
SELECT 
    Prescription_Data.prescription_category_id AS prescriptions_by_patient_category_id,
    Prescription_Data.drug_id as drug_id,
    Prescription_Data.Patient_Location_Category_id as patient_location_id,
    Prescription_Data.Patient_Age_Bracket as patient_age_category_id,
    Prescription_Data.Prescription_Year as prescription_year,
    Prescription_Data.Total_Prescriptions as total_prescriptions,
    Prescription_Data.Total_Patients as total_patients,
    Prescription_Data.Total_Units as total_units,
    Prescription_Data.Total_Days_Supply as total_days_supply,
    Prescription_Data.average_daily_mme as average_daily_mme,
    Prescription_Data.total_above_90MME as total_above_90MME
FROM
    Prescription_Data
WHERE
    Patient_County is not null


-- (Note: Prescriptions_By_PRESCRIBER_Category should only take rows pertaining to PRESCRIBER data)
CREATE OR REPLACE VIEW `Prescriptions_By_Prescriber_Category` AS
SELECT 
    Prescription_Data.prescription_category_id AS prescriptions_by_prescriber_category_id,
    Prescription_Data.drug_id as drug_id,
    Prescription_Data.Prescriber_Location_Category_id as prescriber_location_id,
    Prescription_Data.Patient_Age_Bracket as patient_age_category_id,
    Prescription_Data.Prescription_Year as prescription_year,
    Prescription_Data.Total_Prescriptions as total_prescriptions,
    Prescription_Data.Total_Patients as total_patients,
    Prescription_Data.Total_Units as total_units,
    Prescription_Data.Total_Days_Supply as total_days_supply,
    Prescription_Data.average_daily_mme as average_daily_mme,
    Prescription_Data.total_above_90MME as total_above_90MME
FROM
    Prescription_Data
WHERE
    Prescriber_County is not null