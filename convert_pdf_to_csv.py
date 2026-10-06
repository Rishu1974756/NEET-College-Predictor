import re
import pdfplumber
import pandas as pd

PDF_FILE = "data/2026_round1.pdf"
CSV_FILE = "data/neet_2026_phase1.csv"


def clean_text(value):
    if value is None:
        return ""

    return re.sub(r"\s+", " ", str(value)).strip()


def is_number(value):
    value = clean_text(value)
    return value.isdigit()


def extract_row(row):
    if not row:
        return None

    row = [clean_text(cell) for cell in row]

    # The MCC table has:
    # SNo, Rank, Quota, Institute, Course,
    # Allotted Category, Candidate Category, Remarks
    if len(row) < 7:
        return None

    # Skip header rows
    header_text = " ".join(row).lower()

    if "rank" in header_text and "candidate category" in header_text:
        return None

    # Find SNo and Rank
    if not is_number(row[0]) or not is_number(row[1]):
        return None

    sno = int(row[0])
    rank = int(row[1])

    quota = row[2]
    institute = row[3]
    course = row[4]
    allotted_category = row[5]
    candidate_category = row[6]

    if not rank or not institute or not course:
        return None

    return {
        "sno": sno,
        "rank": rank,
        "quota": quota,
        "institute": institute,
        "course": course,
        "allottedCategory": allotted_category,
        "candidateCategory": candidate_category,
        "phase": 1
    }


def extract_pdf():
    records = []

    with pdfplumber.open(PDF_FILE) as pdf:

        total_pages = len(pdf.pages)

        print(f"Pages found: {total_pages}")
        print("Starting PDF extraction...\n")

        for page_number, page in enumerate(pdf.pages, start=1):

            tables = page.extract_tables()

            for table in tables:

                for row in table:

                    record = extract_row(row)

                    if record:
                        records.append(record)

            if page_number % 25 == 0:
                print(
                    f"Processed {page_number}/{total_pages} "
                    f"| Records: {len(records)}"
                )

    return records


def save_csv(records):

    if not records:
        print("\nNo records were extracted.")
        return

    df = pd.DataFrame(records)

    # Remove duplicate allotment rows.
    df = df.drop_duplicates()

    # Keep records ordered by NEET rank.
    df = df.sort_values("rank")

    columns = [
        "sno",
        "rank",
        "quota",
        "institute",
        "course",
        "allottedCategory",
        "candidateCategory",
        "phase"
    ]

    df = df[columns]

    df.to_csv(
        CSV_FILE,
        index=False,
        encoding="utf-8"
    )

    print("\nExtraction completed.")
    print(f"Records extracted: {len(df)}")
    print(f"CSV created: {CSV_FILE}")


def main():
    records = extract_pdf()
    save_csv(records)


if __name__ == "__main__":
    main()