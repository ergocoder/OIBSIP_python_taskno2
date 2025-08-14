import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os

def bmi_calculator(event=None):
    try:
        feet = int(entry_feet.get())
        inches = int(entry_inches.get())
        weight_kg = float(entry_weight.get())

        total_inches = feet * 12 + inches
        height_m = total_inches * 0.0254

        bmi = weight_kg / (height_m ** 2)
        bmi = round(bmi, 2)

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        label_result.config(text=f"BMI: {bmi}\nCategory: {category}")
        save_bmi_data(feet, inches, weight_kg, bmi, category)

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for all fields.")

def save_bmi_data(feet, inches, weight_kg, bmi, category):
    file_exists = os.path.isfile('bmi_history.csv')
    with open('bmi_history.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Height (ft'in\")", "Weight (kg)", "BMI", "Category"])
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        height_str = f"{feet}'{inches}\""
        writer.writerow([date_str, height_str, weight_kg, bmi, category])

def show_bmi_graph():
    if not os.path.isfile("bmi_history.csv"):
        messagebox.showinfo("No Data", "No BMI data available to plot.")
        return

    dates = []
    bmis = []
    with open('bmi_history.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["Date"])
            bmis.append(float(row["BMI"]))

    if not dates:
        messagebox.showinfo("No Data", "BMI history is empty.")
        return

    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmis, marker='o', linestyle='-', color='blue')
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title("Historical BMI Data")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def reset_fields():
    entry_feet.delete(0, tk.END)
    entry_inches.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    label_result.config(text="")
    entry_feet.focus()

def focus_inches(event):
    entry_inches.focus()

def focus_weight(event):
    entry_weight.focus()

#GUI
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("330x370")
root.resizable(False, False)

#height input
tk.Label(root, text="Height:", font=('Arial', 12)).pack(pady=5)

frame_height = tk.Frame(root)
frame_height.pack()

entry_feet = tk.Entry(frame_height, width=5, font=('Arial', 12))
entry_feet.pack(side=tk.LEFT, padx=5)
tk.Label(frame_height, text="ft", font=('Arial', 12)).pack(side=tk.LEFT)

entry_inches = tk.Entry(frame_height, width=5, font=('Arial', 12))
entry_inches.pack(side=tk.LEFT, padx=5)
tk.Label(frame_height, text="in", font=('Arial', 12)).pack(side=tk.LEFT)

#weight input
tk.Label(root, text="Weight (kg):", font=('Arial', 12)).pack(pady=5)
entry_weight = tk.Entry(root, font=('Arial', 12))
entry_weight.pack()

#field navigation
entry_feet.focus()
entry_feet.bind("<Return>", focus_inches)
entry_inches.bind("<Return>", focus_weight)
entry_weight.bind("<Return>", bmi_calculator)

#buttons
tk.Button(root, text="Calculate BMI", command=bmi_calculator, font=('Arial', 12), bg="lightblue").pack(pady=10)
tk.Button(root, text="Reset", command=reset_fields, font=('Arial', 12), bg="lightcoral").pack(pady=5)
tk.Button(root, text="Show BMI Graph", command=show_bmi_graph, font=('Arial', 12), bg="lightgreen").pack(pady=5)

#result
label_result = tk.Label(root, text="", font=('Arial', 12), fg="green")
label_result.pack(pady=10)

root.mainloop()