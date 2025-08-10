import streamlit as st
import pandas as pd
import tempfile
from io import BytesIO
from comparator import InvoiceComparator

st.set_page_config(page_title="Invoice Discrepancy Checker", layout="centered")
st.title("📄 Invoice vs Master Data Discrepancy Checker")

# File uploads
pdf1 = st.file_uploader("Upload First Invoice PDF", type="pdf")
pdf2 = st.file_uploader("Upload Second Invoice PDF", type="pdf")
excel = st.file_uploader("Upload Master Data Excel", type=["xlsx", "xls"])

# When all files are uploaded and user clicks the button
if st.button("Compare & Generate Report"):
    if pdf1 and pdf2 and excel:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save the uploaded files temporarily
            pdf1_path = f"{tmpdir}/invoice1.pdf"
            pdf2_path = f"{tmpdir}/invoice2.pdf"
            excel_path = f"{tmpdir}/master.xlsx"
            output_path = f"{tmpdir}/Discrepancies_Report.xlsx"

            with open(pdf1_path, "wb") as f:
                f.write(pdf1.read())
            with open(pdf2_path, "wb") as f:
                f.write(pdf2.read())
            with open(excel_path, "wb") as f:
                f.write(excel.read())

            # Run the comparator
            comparator = InvoiceComparator()
            comparator.process_invoices([pdf1_path, pdf2_path], excel_path, output_path)

            # Read the output Excel to display in Streamlit
            df = pd.read_excel(output_path)
            st.success("Comparison completed. Here are the discrepancies:")
            st.dataframe(df)

            # Offer download
            with open(output_path, "rb") as f:
                st.download_button(
                    label="📥 Download Discrepancy Report",
                    data=f,
                    file_name="Discrepancies_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.warning("Please upload all three files before proceeding.")
