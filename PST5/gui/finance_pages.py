
import streamlit as st
import pandas as pd


def show_finance_page(manager):
    """Renders the UI for all financial operations."""
    st.header("Finance & Payments")

    # Build a mapping from student names to IDs.
    student_list = {
        f"{s.name} (ID: {s.id})": s.id
        for s in manager.students
    }

    if not student_list:
        st.warning("No students available. Please register a student first.")
        return

    # Section 1: Record a Payment
    st.subheader("Record New Payment")

    with st.form("payment_form"):
        selected_student_name = st.selectbox(
            "Select Student",
            list(student_list.keys())
        )
        amount = st.number_input(
            "Payment Amount",
            min_value=0.01,
            step=1.00,
            format="%.2f"
        )
        method = st.text_input(
            "Payment Method (e.g., Credit Card, Cash)"
        )

        submitted = st.form_submit_button("Record Payment")

        if submitted:
            if not method.strip():
                st.error("Please enter a payment method.")
            else:
                student_id = student_list[selected_student_name]
                success = manager.record_payment(
                    student_id, amount, method.strip()
                )

                if success:
                    st.success(
                        f"Payment of {amount:.2f} for "
                        f"{selected_student_name} recorded."
                    )
                else:
                    st.error("Failed to record payment.")

    # Section 2: View Payment History
    st.subheader("View Student Payment History")

    history_student_name = st.selectbox(
        "Select Student to View History",
        list(student_list.keys()),
        key="history_student"
    )

    history_student_id = student_list[history_student_name]
    history = manager.get_payment_history(history_student_id)

    if history:
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True)

        # Export the selected student's payment history.
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Payment History (CSV)",
            data=csv_data,
            file_name=f"payment_history_{history_student_id}.csv",
            mime="text/csv"
        )
    else:
        st.info("This student has no payment history.")
