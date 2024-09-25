def load_training_data(vn):
    vn.train(
        documentation="This dataset contains repair ticket information for a company's maintenance operations. It includes details such as request type, urgency, completion status, contractor details, costs, and feedback from tenants."
    )

    vn.train(
        ddl="""
        CREATE TABLE public.repairs (
            request_id character varying,
            request_date character varying,
            completion_date character varying,
            amount character varying,
            urgency character varying,
            repair_type character varying,
            description character varying,
            address character varying,
            city character varying,
            state character varying,
            zip_code character varying,
            assigned_contractor character varying,
            contractor_contact character varying,
            comments character varying,
            status character varying,
            priority_score character varying,
            request_method character varying,
            repair_start_date character varying,
            completion_status character varying,
            tenant_feedback character varying,
            feedback_rating character varying
        );
        """
    )

    # Question 1
    vn.train(
        question="What is the total amount spent on all completed repair requests?",
        sql="""
            SELECT SUM(CAST(REPLACE(amount, '$', '') AS NUMERIC)) AS total_spent
            FROM repairs
            WHERE status = 'Completed';
        """,
    )

    # Question 2
    vn.train(
        question="Find the average feedback rating for each contractor, showing the contractor's name and the average rating.",
        sql="""
            SELECT assigned_contractor, AVG(CAST(feedback_rating AS NUMERIC)) AS average_rating
            FROM repairs
            WHERE feedback_rating IS NOT NULL
            GROUP BY assigned_contractor;
        """,
    )

    # Question 3
    vn.train(
        question="List all repair requests that were marked as 'High' urgency but are still pending, showing request ID, repair type, and start date.",
        sql="""
            SELECT request_id, repair_type, repair_start_date
            FROM repairs
            WHERE urgency = 'High'
              AND completion_status = 'Pending';
        """,
    )

    # Question 4
    vn.train(
        question="Find the top 3 cities with the highest number of 'Plumbing' repair requests, showing the city and the count.",
        sql="""
            SELECT city, COUNT(*) AS plumbing_requests
            FROM repairs
            WHERE repair_type = 'Plumbing'
            GROUP BY city
            ORDER BY plumbing_requests DESC
            LIMIT 3;
        """,
    )

    # Question 5
    vn.train(
        question="List all repair requests where the completion date exceeded the start date by more than 7 days, showing request ID, repair type, start date, and completion date.",
        sql="""
            SELECT request_id, repair_type, repair_start_date, completion_date
            FROM repairs
            WHERE (completion_date::DATE - repair_start_date::DATE) > 7;
        """,
    )

    # Question 6
    vn.train(
        question="Find the contractor with the most repair assignments, showing the contractor's name and the total number of assignments.",
        sql="""
            SELECT assigned_contractor, COUNT(*) AS total_assignments
            FROM repairs
            GROUP BY assigned_contractor
            ORDER BY total_assignments DESC
            LIMIT 1;
        """,
    )

    # Question 7
    vn.train(
        question="Calculate the average amount spent on 'Electrical' repairs for requests that have been marked as 'Done'.",
        sql="""
            SELECT AVG(CAST(REPLACE(amount, '$', '') AS NUMERIC)) AS average_spent
            FROM repairs
            WHERE repair_type = 'Electrical'
              AND completion_status = 'Done';
        """,
    )

    # Question 8
    vn.train(
        question="List all repair requests that were initiated via 'Phone Call' and have not yet been completed, showing request ID, repair type, and status.",
        sql="""
            SELECT request_id, repair_type, status
            FROM repairs
            WHERE request_method = 'Phone Call'
              AND status <> 'Completed';
        """,
    )

    # Question 9
    vn.train(
        question="Find the most common repair type that was marked as 'Low' priority, showing the repair type and the count.",
        sql="""
            SELECT repair_type, COUNT(*) AS repair_count
            FROM repairs
            WHERE urgency = 'Low'
            GROUP BY repair_type
            ORDER BY repair_count DESC
            LIMIT 1;
        """,
    )

    # Question 10
    vn.train(
        question="List all repairs where tenant feedback included the word 'satisfied', showing request ID, feedback, and feedback rating.",
        sql="""
            SELECT request_id, tenant_feedback, feedback_rating
            FROM repairs
            WHERE tenant_feedback ILIKE '%satisfied%';
        """,
    )
