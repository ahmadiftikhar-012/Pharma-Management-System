-- Pharma Management System - Database Schema

CREATE DATABASE IF NOT EXISTS pharma_db;
USE pharma_db;

-- TABLE: users (login system)

CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(80)  NOT NULL UNIQUE,
    email       VARCHAR(120) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('admin', 'cashier') NOT NULL DEFAULT 'cashier',
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TABLE: suppliers

CREATE TABLE IF NOT EXISTS suppliers (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(120) NOT NULL,
    contact_person  VARCHAR(100),
    phone           VARCHAR(20),
    email           VARCHAR(120),
    address         TEXT
);

-- TABLE: medicines

CREATE TABLE IF NOT EXISTS medicines (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(120) NOT NULL,
    generic_name    VARCHAR(120),
    category        VARCHAR(80),
    dosage_form     VARCHAR(80),
    strength        VARCHAR(50),
    supplier_id     INT,
    expiry_date     DATE,
    price           DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    reorder_level   INT NOT NULL DEFAULT 10,
    CONSTRAINT fk_medicine_supplier
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        ON DELETE SET NULL
);

-- TABLE: stock

CREATE TABLE IF NOT EXISTS stock (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id     INT NOT NULL,
    quantity        INT NOT NULL DEFAULT 0,
    batch_number    VARCHAR(80),
    last_updated    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_stock_medicine
        FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        ON DELETE CASCADE
);

-- TABLE: sales

CREATE TABLE IF NOT EXISTS sales (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    sale_date       DATETIME DEFAULT CURRENT_TIMESTAMP,
    customer_name   VARCHAR(120),
    total_amount    DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    payment_method  ENUM('cash', 'card', 'online') DEFAULT 'cash'
);

-- TABLE: sale_items (junction table: sale <-> medicine)

CREATE TABLE IF NOT EXISTS sale_items (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    sale_id         INT NOT NULL,
    medicine_id     INT NOT NULL,
    quantity        INT NOT NULL,
    unit_price      DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_saleitem_sale
        FOREIGN KEY (sale_id) REFERENCES sales(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_saleitem_medicine
        FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        ON DELETE RESTRICT
);

-- INDEXES (for performance)

CREATE INDEX idx_medicine_expiry     ON medicines(expiry_date);
CREATE INDEX idx_medicine_supplier   ON medicines(supplier_id);
CREATE INDEX idx_stock_medicine      ON stock(medicine_id);
CREATE INDEX idx_stock_quantity      ON stock(quantity);
CREATE INDEX idx_saleitem_sale       ON sale_items(sale_id);
CREATE INDEX idx_saleitem_medicine   ON sale_items(medicine_id);
CREATE INDEX idx_sale_date           ON sales(sale_date);

-- VIEW: low_stock_view

CREATE OR REPLACE VIEW low_stock_view AS
    SELECT
        m.id,
        m.name,
        m.category,
        s.quantity,
        m.reorder_level,
        (m.reorder_level - s.quantity) AS shortage
    FROM medicines m
    JOIN stock s ON m.id = s.medicine_id
    WHERE s.quantity < m.reorder_level;

-- VIEW: expiry_warning_view (medicines expiring within 30 days)

CREATE OR REPLACE VIEW expiry_warning_view AS
    SELECT
        m.id,
        m.name,
        m.category,
        m.expiry_date,
        DATEDIFF(m.expiry_date, CURDATE()) AS days_left,
        s.quantity
    FROM medicines m
    JOIN stock s ON m.id = s.medicine_id
    WHERE m.expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY);

-- VIEW: sales_summary_view

CREATE OR REPLACE VIEW sales_summary_view AS
    SELECT
        DATE(sale_date)     AS sale_day,
        COUNT(id)           AS total_transactions,
        SUM(total_amount)   AS daily_revenue
    FROM sales
    GROUP BY DATE(sale_date)
    ORDER BY sale_day DESC;

-- STORED PROCEDURE: process_sale
-- Inserts a sale, sale_items, and deducts stock atomically

DELIMITER $$

CREATE PROCEDURE process_sale(
    IN  p_customer_name   VARCHAR(120),
    IN  p_payment_method  VARCHAR(20),
    IN  p_medicine_id     INT,
    IN  p_quantity        INT,
    IN  p_unit_price      DECIMAL(10,2),
    OUT p_sale_id         INT,
    OUT p_success         BOOLEAN,
    OUT p_message         VARCHAR(255)
)
BEGIN
    DECLARE v_stock_qty INT DEFAULT 0;
    DECLARE v_total     DECIMAL(10,2);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'Transaction failed, rolled back.';
    END;

    START TRANSACTION;

    -- Check available stock
    SELECT quantity INTO v_stock_qty
    FROM stock
    WHERE medicine_id = p_medicine_id
    LIMIT 1;

    IF v_stock_qty < p_quantity THEN
        SET p_success = FALSE;
        SET p_message = 'Insufficient stock.';
        ROLLBACK;
    ELSE
        SET v_total = p_quantity * p_unit_price;

        -- Insert sale
        INSERT INTO sales (customer_name, total_amount, payment_method)
        VALUES (p_customer_name, v_total, p_payment_method);

        SET p_sale_id = LAST_INSERT_ID();

        -- Insert sale item
        INSERT INTO sale_items (sale_id, medicine_id, quantity, unit_price)
        VALUES (p_sale_id, p_medicine_id, p_quantity, p_unit_price);

        -- Deduct stock
        UPDATE stock
        SET quantity = quantity - p_quantity
        WHERE medicine_id = p_medicine_id;

        COMMIT;
        SET p_success = TRUE;
        SET p_message = 'Sale processed successfully.';
    END IF;
END$$

DELIMITER ;

-- TRIGGER: auto-flag low stock after update

DELIMITER $$

CREATE TRIGGER after_stock_update
AFTER UPDATE ON stock
FOR EACH ROW
BEGIN
    -- Log can be added here or alerts table inserted
    IF NEW.quantity < (SELECT reorder_level FROM medicines WHERE id = NEW.medicine_id) THEN
        -- Insert into an alerts log table if needed
        -- For now, the low_stock_view handles this
        SET @low_stock_flag = TRUE;
    END IF;
END$$

DELIMITER ;


-- SEED: default admin user (password: admin123)
-- Run: python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('admin123'))"
-- Replace the hash below with the generated one

INSERT INTO users (username, email, password, role)
VALUES ('admin', 'admin@pharma.com', 'pbkdf2:sha256:placeholder_run_seed_script', 'admin');
