# Kolton Bittner - August 11 2023


import csv
import json
import tkinter as tk
from tkinter import filedialog

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

def extract_values(responses):
    try:
        response_dict = json.loads(responses)
        is_rejected = response_dict.get("is_rejected", "")

        support_level = ""
        sensitive_topics = ""
        information_not_supported = ""

        response_json = json.loads(response_dict.get("response", "{}"))
        if response_json:
            response_key = next(iter(response_json))
            response_payload = response_json[response_key]["payload"]
            if response_payload:
                values = response_payload[0]["values"]
                support_level = values.get("support_level", "")
                sensitive_topics = values.get("sensitive_topics", "")
                information_not_supported = values.get("information_not_supported", "")

        return is_rejected, support_level, sensitive_topics, information_not_supported
    except (json.JSONDecodeError, KeyError):
        pass
    return "", "", "", ""

def process_csv():
    input_file_path = input_entry.get()
    output_file_path = output_entry.get()

    with open(input_file_path, mode="r") as input_file, open(output_file_path, mode="w", newline="") as output_file:
        csv_reader = csv.DictReader(input_file)
        fieldnames = ["job_id", "is_rejected", "support_level", "sensitive_topics", "information_not_supported"]
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        csv_writer.writeheader()

        for row in csv_reader:
            job_id = row.get("job_id")
            responses = row.get("responses")

            is_rejected, support_level, sensitive_topics, information_not_supported = extract_values(responses)

            csv_writer.writerow({
                "job_id": job_id,
                "is_rejected": is_rejected,
                "support_level": support_level,
                "sensitive_topics": sensitive_topics,
                "information_not_supported": information_not_supported
            })

    result_label.config(text="Extraction and writing completed.")

root = tk.Tk()
root.title("CSV Extraction Tool")

input_label = tk.Label(root, text="Select Input CSV File:")
input_label.pack()
input_entry = tk.Entry(root, width=50)
input_entry.pack()
input_button = tk.Button(root, text="Browse", command=browse_file)
input_button.pack()

output_label = tk.Label(root, text="Select Output CSV File:")
output_label.pack()
output_entry = tk.Entry(root, width=50)
output_entry.pack()
output_button = tk.Button(root, text="Browse", command=browse_output_file)
output_button.pack()

process_button = tk.Button(root, text="Process", command=process_csv)
process_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
