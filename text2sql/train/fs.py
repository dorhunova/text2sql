def load_training_data(vn):
    vn.train(
        documentation="""
        The table contracts contains information about the contracts between the company and its customers.
        Contract name can be treated as the identier of the customer. Customer names can be provided not in full, but as a part of the contract name.
        """
    )

    vn.train(
        ddl="""
        CREATE TABLE billable_route_invoice_line_item (
            id NUMBER(38,0) autoincrement start 1 increment 1 noorder,
            task_date DATE,
            billable_route_id NUMBER(38,0),
            business_unit_id NUMBER(38,0),
            customer_id NUMBER(38,0),
            contract_id NUMBER(38,0),
            billable_id NUMBER(38,0),
            invoice_id NUMBER(38,0) COMMENT 'Reference to Invoice [Send to JDE Batch] table.',
            contract_service_type_id NUMBER(38,0),
            contract_service_title_id NUMBER(38,0),
            contract_service_id NUMBER(38,0),
            rate_id NUMBER(38,0),
            cancelation_reason_id NUMBER(38,0),
            contract_service_type VARCHAR(16777216),
            contract_service_title VARCHAR(16777216),
            billable_route_name VARCHAR(16777216),
            billable_route_description VARCHAR(16777216),
            performed BOOLEAN,
            cancelation_reason_code VARCHAR(16777216),
            cancelation_reason_name VARCHAR(16777216),
            currency VARCHAR(16777216),
            rate NUMBER(38,4),
            charge_multiplier NUMBER(38,2),
            total_amount NUMBER(38,2),
            status VARCHAR(16777216) COMMENT 'Placeholder column for tracking statuses, e.i. Reviewed, Approved, Ready for JDE, Sent to JDE etc',
            comment_c VARCHAR(16777216) COMMENT 'Placeholder column for providing additional explanation/reasoning by BillingApp User.',
            insert_ts TIMESTAMP_NTZ(9),
            update_ts TIMESTAMP_NTZ(9),
            inserted_by VARCHAR(16777216),
            updated_by VARCHAR(16777216),
            batch_id NUMBER(38,0)
        );"""
    )

    vn.train(
        ddl="""
        CREATE TABLE contract (
            contract_id NUMBER(38,0),
            customer_id VARCHAR(16777216),
            latest_contract_file_name VARCHAR(16777216) COMMENT 'Name of the latest contract file, can be treated as name of the customer.',
            start_date DATE,
            end_date DATE
        );"""
    )

    vn.train(
        question="Number of performed Billable Routes for 3 Contract for Spring months",
        sql="""
            SELECT
                br_ini.contract_id,
                c.latest_contract_file_name,
                EXTRACT(MONTH FROM br_ini.task_date) AS month,
                SUM(CASE WHEN br_ini.performed = TRUE THEN 1 ELSE 0 END) AS performed_route_number
                FROM billable_route_invoice_line_item br_ini
                LEFT JOIN contract c
                ON c.contract_id = br_ini.contract_id
                WHERE
                br_ini.task_date BETWEEN '2024-03-01' AND '2024-05-31'
                AND br_ini.business_unit_id IN (12645, 12525, 12675)
                GROUP BY
                br_ini.contract_id,
                c.latest_contract_file_name,
                EXTRACT(MONTH FROM br_ini.task_date);
        """,
    )

    vn.train(
        question="Invoice Amount for 3 Contract for Spring months",
        sql="""
        SELECT
            br_ini.contract_id,
            c.latest_contract_file_name,
            EXTRACT(MONTH FROM br_ini.task_date) AS month,
            SUM(br_ini.total_amount) AS invoice_amount
            FROM billable_route_invoice_line_item br_ini
            LEFT JOIN contract c
            ON c.contract_id = br_ini.contract_id
            WHERE
            br_ini.task_date BETWEEN '2024-03-01' AND '2024-05-31'
            AND br_ini.business_unit_id IN (12645, 12525, 12675)
            GROUP BY
            br_ini.contract_id,
            c.latest_contract_file_name,
            EXTRACT(MONTH FROM br_ini.task_date);
        """
    )

    vn.train(
        question="How month Invoice Amount deviates from average Invoice Amount within a Contract in Spring Quarter?", 
        sql="""
        WITH monthly_invoice_amount AS (
        SELECT
            br_ini.contract_id,
            c.latest_contract_file_name,
            EXTRACT(MONTH FROM br_ini.task_date) AS month,
            SUM(br_ini.total_amount) AS invoice_amount
        FROM billable_route_invoice_line_item br_ini
        LEFT JOIN contract c
            ON c.contract_id = br_ini.contract_id
        WHERE br_ini.task_date BETWEEN '2024-03-01' AND '2024-05-31'
            AND br_ini.business_unit_id IN (12645, 12525, 12675)
        GROUP BY
            br_ini.contract_id,
            c.latest_contract_file_name,
            EXTRACT(MONTH FROM br_ini.task_date)
        ),
        average_invoice_amount AS (
        SELECT
            contract_id,
            ROUND(AVG(invoice_amount), 0) AS average_monthly_invoice_amount
        FROM monthly_invoice_amount
        GROUP BY contract_id
        )
        SELECT 
        m.contract_id,
        m.month,
        m.invoice_amount,
        a.average_monthly_invoice_amount,
        ROUND((m.invoice_amount / a.average_monthly_invoice_amount) * 100.00 - 100.00, 2) AS diff_from_average
        FROM monthly_invoice_amount m
        LEFT JOIN average_invoice_amount a
        ON m.contract_id = a.contract_id
        WHERE LOWER(m.latest_contract_file_name) LIKE '%methacton%'
        """
    )

    vn.train(
        question="What are the specific days in March (the least 'Performed' month) where the number of performed routes deviated negatively from the usual median number of performed routes per day for that month?",
        sql="""
        WITH daily_route_number AS (
        SELECT
            br_ini.contract_id,
            c.latest_contract_file_name,
            br_ini.task_date,
            SUM(CASE WHEN br_ini.performed = TRUE THEN 1 ELSE 0 END) AS performed_route_num_per_day
        FROM billable_route_invoice_line_item br_ini
        LEFT JOIN contract c
            ON c.contract_id = br_ini.contract_id
        WHERE LOWER(c.latest_contract_file_name) LIKE '%methacton%'  -- specific Contract
            AND br_ini.task_date BETWEEN '2024-03-01' AND '2024-03-31'  -- specific Month
            AND br_ini.business_unit_id IN (12645, 12525, 12675)
        GROUP BY
            br_ini.contract_id,
            c.latest_contract_file_name,
            br_ini.task_date
        ),
        usual_daily_route_number AS (
        SELECT
            EXTRACT(MONTH FROM task_date) AS month,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY performed_route_num_per_day) AS usual_route_number_per_day
        FROM daily_route_number
        GROUP BY EXTRACT(MONTH FROM task_date)
        )
        SELECT *
        FROM daily_route_number d
        LEFT JOIN usual_daily_route_number u
        ON EXTRACT(MONTH FROM d.task_date) = u.month
        WHERE d.performed_route_num_per_day < (0.1 * u.usual_route_number_per_day);
        """
    )

    vn.train(
        question="tell me when the contract ends with xenia", 
        sql="""
        SELECT
            contract_id,
            latest_contract_file_name,
            end_date
        FROM contract
        WHERE LOWER(latest_contract_file_name) LIKE '%xenia%';
        """
    )

    vn.train(
        question="can you please show me total invoice amount for each month and and show me how many unique billable routes did i have",
        sql="""
        SELECT
            EXTRACT(YEAR FROM br_ini.task_date) AS year,
            EXTRACT(MONTH FROM br_ini.task_date) AS month,
            SUM(br_ini.total_amount) AS total_invoice_amount,
            COUNT(DISTINCT br_ini.billable_route_id) AS total_billable_route
        FROM
            billable_route_invoice_line_item br_ini
        GROUP BY
            EXTRACT(YEAR FROM br_ini.task_date),
            EXTRACT(MONTH FROM br_ini.task_date)
        ORDER BY
            year,
            month;
        """
    )