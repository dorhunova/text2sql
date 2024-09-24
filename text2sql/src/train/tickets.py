def load_training_data(vn):
    vn.train(
        documentation="This dataset contains ticket information for a company's internal operations. It includes details such as ticket type, description, priority, status, and resolution details."
    )

    vn.train(
        ddl="""
        CREATE TABLE public.tickets (
        ticket_id character varying,
        request_type character varying,
        request_title character varying,
        description character varying,
        priority character varying,
        status character varying,
        created_date character varying,
        updated_date character varying,
        requested_by character varying,
        department character varying,
        assigned_to character varying,
        category character varying,
        subcategory character varying,
        due_date character varying,
        completion_date character varying,
        location character varying,
        attachments character varying,
        cost_estimate character varying,
        actual_cost character varying,
        comments character varying,
        approval_status character varying,
        approved_by character varying,
        approval_date character varying,
        sla_breach character varying,
        sla_target_date character varying,
        resolution_summary character varying
        );
        """
    )
    vn.train(
        question="Find the number of tickets raised by each department.",
        sql="""
            SELECT department, COUNT(*) AS ticket_count
            FROM tickets
            WHERE department IS NOT NULL
            GROUP BY department;
        """,
    )

    vn.train(
        question="List all high-priority tickets that are still open, including the ticket ID, request title, requested by, and created date.",
        sql="""
            SELECT ticket_id, request_title, requested_by, created_date
            FROM tickets
            WHERE priority = 'High'
                AND status = 'Open';
        """,
    )

    vn.train(
        question="Find the average estimated cost and actual cost of tickets for the 'IT Support' request type.",
        sql="""
            SELECT AVG(CAST(REPLACE(cost_estimate, '$', '') AS NUMERIC)) AS average_estimated_cost, 
                   AVG(CAST(REPLACE(actual_cost, '$', '') AS NUMERIC)) AS average_actual_cost
            FROM tickets
            WHERE request_type = 'IT Support'
              AND cost_estimate IS NOT NULL
              AND actual_cost IS NOT NULL;
        """,
    )

    vn.train(
        question="List all tickets that have breached the SLA target date, showing the ticket ID, request title, requested by, and SLA target date.",
        sql="""
            SELECT ticket_id, request_title, requested_by, sla_target_date
            FROM tickets
            WHERE sla_breach = 'Yes';
        """,
    )

    vn.train(
        question="Find the number of tickets approved by each manager.",
        sql="""
            SELECT approved_by, COUNT(*) AS tickets_approved
            FROM tickets
            WHERE approval_status = 'Approved'
            AND approved_by IS NOT NULL
            GROUP BY approved_by;
        """,
    )

    vn.train(
        question="List all tickets related to 'Equipment Repair' that were resolved successfully, showing the ticket ID, title, actual cost, and resolution summary.",
        sql="""
            SELECT ticket_id, request_title, CAST(REPLACE(actual_cost, '$', '') AS NUMERIC) AS actual_cost, resolution_summary
            FROM tickets
            WHERE request_type = 'Equipment Repair'
                AND status = 'Closed';
        """,
    )

    vn.train(
        question="Find all tickets that were updated within the same month they were created, showing the ticket ID, created date, and updated date.",
        sql="""
            SELECT ticket_id, created_date, updated_date
            FROM tickets
            WHERE EXTRACT(MONTH FROM created_date::DATE) = EXTRACT(MONTH FROM updated_date::DATE)
                AND updated_date IS NOT NULL;
        """,
    )

    vn.train(
        question="Calculate the total actual cost of all tickets related to 'Software Installation' that have been closed.",
        sql="""
            SELECT SUM(CAST(REPLACE(actual_cost, '$', '') AS NUMERIC)) AS total_actual_cost
            FROM tickets
            WHERE request_type = 'Software Installation'
                AND status = 'Closed';
        """,
    )

    vn.train(
        question="Find the top 3 most common request types, showing the request type and the number of tickets.",
        sql="""
            SELECT request_type, COUNT(*) AS ticket_count
            FROM tickets
            WHERE request_type IS NOT NULL
            GROUP BY request_type
            ORDER BY ticket_count DESC
            LIMIT 3;
        """,
    )

    vn.train(
        question="List all tickets where the approval status is pending, along with the ticket ID, request title, requested by, and approval status.",
        sql="""
            SELECT ticket_id, request_title, requested_by, approval_status
            FROM tickets
            WHERE approval_status = 'Pending';
        """,
    )