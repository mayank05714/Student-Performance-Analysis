# Student Performance Analysis Project

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("=== Student Performance Analysis ===")
print("By: [Apna Naam Yahan Likho]")
print()

# ----------------------------------------
# STEP 1: Dataset Banana
# ----------------------------------------
data = {
    'Student_Name': [
        'Rahul', 'Priya', 'Amit', 'Sneha', 'Rohit',
        'Pooja', 'Vikram', 'Neha', 'Arjun', 'Kavya',
        'Suresh', 'Meera', 'Ravi', 'Anita', 'Karan',
        'Divya', 'Mohit', 'Shreya', 'Ajay', 'Nisha'
    ],
    'Math':    [85, 92, 45, 78, 55, 88, 72, 95, 60, 83,
                40, 76, 68, 91, 53, 87, 74, 96, 62, 79],
    'Science': [78, 88, 50, 82, 60, 91, 68, 93, 55, 80,
                45, 72, 65, 89, 58, 84, 70, 94, 58, 75],
    'English': [72, 85, 55, 75, 65, 87, 70, 90, 58, 78,
                50, 68, 62, 86, 60, 82, 67, 92, 55, 73],
    'History': [68, 80, 48, 70, 58, 83, 65, 88, 52, 75,
                42, 65, 60, 84, 55, 79, 64, 89, 50, 70],
    'Gender':  ['M','F','M','F','M','F','M','F','M','F',
                'M','F','M','F','M','F','M','F','M','F'],
    'Attendance': [90, 95, 60, 85, 70, 92, 80, 98, 65, 88,
                   55, 78, 72, 94, 68, 91, 82, 97, 63, 84]
}

df = pd.DataFrame(data)

# Total aur Average marks calculate karo
df['Total'] = df['Math'] + df['Science'] + df['English'] + df['History']
df['Average'] = (df['Total'] / 4).round(2)

# Grade assign karo
def assign_grade(avg):
    if avg >= 90:
        return 'A+'
    elif avg >= 80:
        return 'A'
    elif avg >= 70:
        return 'B'
    elif avg >= 60:
        return 'C'
    elif avg >= 50:
        return 'D'
    else:
        return 'F'

df['Grade'] = df['Average'].apply(assign_grade)

# Pass/Fail
df['Result'] = df['Average'].apply(lambda x: 'Pass' if x >= 50 else 'Fail')

# ----------------------------------------
# STEP 2: Data Cleaning
# ----------------------------------------
print("--- Data Overview ---")
print(f"Total Students: {len(df)}")
print(f"Total Columns:  {len(df.columns)}")
print()
print("Missing Values:")
print(df.isnull().sum())
print()
print("--- Basic Statistics ---")
print(df[['Math', 'Science', 'English', 'History', 'Average']].describe())
print()

# ----------------------------------------
# STEP 3: Analysis (Insights)
# ----------------------------------------
print("--- Key Insights ---")
print(f"Class Average Score:  {df['Average'].mean():.2f}")
print(f"Highest Average:      {df['Average'].max()} ({df.loc[df['Average'].idxmax(), 'Student_Name']})")
print(f"Lowest Average:       {df['Average'].min()} ({df.loc[df['Average'].idxmin(), 'Student_Name']})")
print(f"Total Pass Students:  {len(df[df['Result'] == 'Pass'])}")
print(f"Total Fail Students:  {len(df[df['Result'] == 'Fail'])}")
print()

print("--- Top 5 Students ---")
top5 = df.nlargest(5, 'Average')[['Student_Name', 'Average', 'Grade']]
print(top5.to_string(index=False))
print()

print("--- Subject Wise Average ---")
subjects = ['Math', 'Science', 'English', 'History']
for sub in subjects:
    print(f"{sub:10}: {df[sub].mean():.2f}")
print()

print("--- Grade Distribution ---")
print(df['Grade'].value_counts())
print()

print("--- Gender Wise Performance ---")
print(df.groupby('Gender')['Average'].mean().round(2))

# ----------------------------------------
# STEP 4: Visualizations
# ----------------------------------------
plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(2, 2, figsize=(18, 13))
fig.suptitle('Student Performance Analysis Dashboard',
             fontsize=18, fontweight='bold')

# ---- Chart 1: Top 10 Students (Horizontal Bar) ----
top10 = df.nlargest(10, 'Average')
colors = ['gold' if i == 0 else 'steelblue' for i in range(len(top10))]
bars = axes[0, 0].barh(top10['Student_Name'], top10['Average'],
                        color=colors)
axes[0, 0].set_title('Top 10 Students by Average Score',
                      fontsize=13, pad=12)
axes[0, 0].set_xlabel('Average Score', fontsize=10, labelpad=15)
axes[0, 0].set_ylabel('Student Name', fontsize=10)
axes[0, 0].set_xlim(0, 110)
for bar, val in zip(bars, top10['Average']):
    axes[0, 0].text(val + 1, bar.get_y() + bar.get_height()/2,
                    f'{val}', va='center', fontsize=9)
axes[0, 0].grid(True, alpha=0.3, axis='x')

# ---- Chart 2: Subject Wise Average (Bar) ----
subject_avg = df[subjects].mean()
bar_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
bars2 = axes[0, 1].bar(subject_avg.index, subject_avg.values,
                        color=bar_colors, width=0.5)
axes[0, 1].set_title('Subject Wise Average Score',
                      fontsize=13, pad=12)
axes[0, 1].set_xlabel('Subject', fontsize=10, labelpad=15)
axes[0, 1].set_ylabel('Average Score', fontsize=10)
axes[0, 1].set_ylim(0, 100)
for bar in bars2:
    height = bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=10)
axes[0, 1].grid(True, alpha=0.3, axis='y')

# ---- Chart 3: Grade Distribution (Pie) ----
grade_counts = df['Grade'].value_counts()
grade_colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#9b59b6']
axes[1, 0].pie(
    grade_counts.values,
    labels=grade_counts.index,
    autopct='%1.1f%%',
    colors=grade_colors[:len(grade_counts)],
    startangle=90,
    pctdistance=0.75,
    labeldistance=1.15,
    textprops={'fontsize': 10}
)
axes[1, 0].set_title('Grade Distribution', fontsize=13, pad=20)

# ---- Chart 4: Attendance vs Performance (Scatter) ----
gender_colors = {'M': 'steelblue', 'F': 'tomato'}
for gender, group in df.groupby('Gender'):
    axes[1, 1].scatter(
        group['Attendance'],
        group['Average'],
        c=gender_colors[gender],
        label=f"{'Male' if gender == 'M' else 'Female'}",
        s=80, alpha=0.8
    )
axes[1, 1].set_title('Attendance vs Academic Performance',
                      fontsize=13, pad=12)
axes[1, 1].set_xlabel('Attendance (%)', fontsize=10, labelpad=15)
axes[1, 1].set_ylabel('Average Score', fontsize=10)
axes[1, 1].legend(fontsize=9)
axes[1, 1].grid(True, alpha=0.3)

# ---- Save & Show ----
plt.tight_layout(pad=4.0, h_pad=5.0, w_pad=4.0)
plt.savefig('student_dashboard.png', dpi=150, bbox_inches='tight')
print("\nDashboard save ho gaya: student_dashboard.png")
plt.show()

print("\n=== Analysis Complete! ===")