-- ============================================================
-- PharmaMS - Sample Data
-- Run: cmd /c "mysql -u root -p pharma_db < sample_data.sql"
-- ============================================================

USE pharma_db;

-- ============================================================
-- SUPPLIERS (5 Pakistani pharma suppliers)
-- ============================================================
INSERT INTO suppliers (name, contact_person, phone, email, address) VALUES
('Getz Pharma',        'Ahmed Raza',    '021-35241000', 'ahmed@getzpharma.com',    'Korangi Industrial Area, Karachi'),
('GSK Pakistan',       'Sara Malik',    '021-35685001', 'sara@gsk.com.pk',         'F-8 Markaz, Islamabad'),
('Highnoon Labs',      'Bilal Sheikh',  '042-35761000', 'bilal@highnoon.com.pk',   'Lahore Industrial Estate, Lahore'),
('Sami Pharmaceuticals','Zara Khan',   '021-34380001', 'zara@samipharma.com.pk',  'SITE Area, Karachi'),
('Abbott Pakistan',    'Omar Farooq',   '051-28110000', 'omar@abbott.com.pk',      'Blue Area, Islamabad');

-- ============================================================
-- MEDICINES (20 common Pakistani medicines)
-- ============================================================
INSERT INTO medicines (name, generic_name, category, dosage_form, strength, supplier_id, expiry_date, price, reorder_level) VALUES
('Panadol',         'Paracetamol',       'Analgesic',      'Tablet',  '500mg',  1, '2027-06-30',  12.00, 50),
('Amoxil',          'Amoxicillin',       'Antibiotic',     'Capsule', '500mg',  2, '2027-03-31',  28.00, 30),
('Omez',            'Omeprazole',        'Antacid',        'Capsule', '20mg',   3, '2026-12-31',  35.00, 20),
('Glucophage',      'Metformin',         'Antidiabetic',   'Tablet',  '500mg',  4, '2027-09-30',  18.00, 40),
('Zyrtec',          'Cetirizine',        'Antihistamine',  'Tablet',  '10mg',   5, '2027-08-31',  22.00, 25),
('Brufen',          'Ibuprofen',         'Analgesic',      'Tablet',  '400mg',  1, '2027-05-31',  20.00, 30),
('Flagyl',          'Metronidazole',     'Antibiotic',     'Tablet',  '400mg',  2, '2026-11-30',  15.00, 20),
('Lipitor',         'Atorvastatin',      'Statin',         'Tablet',  '10mg',   3, '2027-07-31',  85.00, 15),
('Norvasc',         'Amlodipine',        'Antihypertensive','Tablet', '5mg',    4, '2027-04-30',  45.00, 20),
('Augmentin',       'Amoxicillin+Clav',  'Antibiotic',     'Tablet',  '625mg',  5, '2026-10-31',  95.00, 15),
('Calpol Syrup',    'Paracetamol',       'Analgesic',      'Syrup',   '120mg',  1, '2026-08-31',  55.00, 20),
('Ventolin',        'Salbutamol',        'Bronchodilator', 'Inhaler', '100mcg', 2, '2027-02-28',  280.00,10),
('Nexium',          'Esomeprazole',      'Antacid',        'Tablet',  '40mg',   3, '2027-01-31',  120.00,10),
('Diamicron',       'Gliclazide',        'Antidiabetic',   'Tablet',  '80mg',   4, '2027-10-31',  65.00, 15),
('Clarinase',       'Loratadine',        'Antihistamine',  'Tablet',  '10mg',   5, '2027-11-30',  48.00, 20),
('Disprin',         'Aspirin',           'Analgesic',      'Tablet',  '75mg',   1, '2026-07-31',  8.00,  40),
('Zithromax',       'Azithromycin',      'Antibiotic',     'Tablet',  '500mg',  2, '2027-06-30',  145.00,10),
('Losartan',        'Losartan Potassium','Antihypertensive','Tablet', '50mg',   3, '2026-09-30',  38.00, 20),
('Vitamin C',       'Ascorbic Acid',     'Vitamin',        'Tablet',  '500mg',  4, '2027-12-31',  25.00, 30),
('Risek',           'Omeprazole',        'Antacid',        'Capsule', '40mg',   5, '2027-03-31',  42.00, 15);

-- ============================================================
-- STOCK (one entry per medicine)
-- ============================================================
INSERT INTO stock (medicine_id, quantity, batch_number) VALUES
(1,  150, 'BT-2026-001'),
(2,   80, 'BT-2026-002'),
(3,   60, 'BT-2026-003'),
(4,  120, 'BT-2026-004'),
(5,   90, 'BT-2026-005'),
(6,   75, 'BT-2026-006'),
(7,    8, 'BT-2026-007'),  -- low stock
(8,   45, 'BT-2026-008'),
(9,   55, 'BT-2026-009'),
(10,   5, 'BT-2026-010'), -- low stock
(11,  30, 'BT-2026-011'),
(12,  12, 'BT-2026-012'),
(13,  25, 'BT-2026-013'),
(14,  40, 'BT-2026-014'),
(15,  35, 'BT-2026-015'),
(16, 200, 'BT-2026-016'),
(17,   7, 'BT-2026-017'), -- low stock
(18,  50, 'BT-2026-018'),
(19, 110, 'BT-2026-019'),
(20,  65, 'BT-2026-020');

-- ============================================================
-- SALES (5 sample sales)
-- ============================================================
INSERT INTO sales (sale_date, customer_name, total_amount, payment_method) VALUES
('2026-05-25 09:15:00', 'Ahmed Raza',    ' 500.00', 'cash'),
('2026-05-25 10:30:00', 'Sara Khan',     '1250.00', 'card'),
('2026-05-25 11:45:00', 'Walk-in',        '244.00', 'cash'),
('2026-05-25 13:00:00', 'Bilal Mahmood', '3280.00', 'online'),
('2026-05-25 14:20:00', 'Zara Ahmed',     '890.00', 'cash');

-- ============================================================
-- SALE ITEMS
-- ============================================================
-- Sale 1: Ahmed Raza
INSERT INTO sale_items (sale_id, medicine_id, quantity, unit_price) VALUES
(1, 1, 10, 12.00),
(1, 6,  5, 20.00),
(1, 19, 8, 25.00);

-- Sale 2: Sara Khan
INSERT INTO sale_items (sale_id, medicine_id, quantity, unit_price) VALUES
(2, 8,  5, 85.00),
(2, 9,  5, 45.00),
(2, 5, 10, 22.00),
(2, 15, 5, 48.00);

-- Sale 3: Walk-in
INSERT INTO sale_items (sale_id, medicine_id, quantity, unit_price) VALUES
(3, 1,  5, 12.00),
(3, 5,  4, 22.00),
(3, 16, 8,  8.00);

-- Sale 4: Bilal Mahmood
INSERT INTO sale_items (sale_id, medicine_id, quantity, unit_price) VALUES
(4, 12, 2, 280.00),
(4, 13, 5, 120.00),
(4, 17, 5, 145.00),
(4, 8,  5,  85.00);

-- Sale 5: Zara Ahmed
INSERT INTO sale_items (sale_id, medicine_id, quantity, unit_price) VALUES
(5, 3,  5, 35.00),
(5, 20, 8, 42.00),
(5, 19, 5, 25.00),
(5, 6,  5, 20.00);

-- ============================================================
SELECT 'Sample data loaded successfully!' AS Status;
SELECT COUNT(*) AS Total_Suppliers FROM suppliers;
SELECT COUNT(*) AS Total_Medicines FROM medicines;
SELECT COUNT(*) AS Total_Sales     FROM sales;
-- ============================================================
