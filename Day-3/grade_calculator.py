name = input("Enter student name: ")
sub1 = float(input("Enter marks for subject 1: "))
sub2 = float(input("Enter marks for subject 2: "))
sub3 = float(input("Enter marks for subject 3: "))

total = sub1 + sub2 + sub3
average = total / 3

if average >= 40:
    status = "Pass"
else:
    status = "Fail"

if average >= 90:
    grade = "A"
elif average >= 75:
    grade = "B"
elif average >= 50:
    grade = "C"
else:
    grade = "D"

print("Student Name:", name)
print("Total Marks:", total)
print("Average Marks:", average)
print("Status:", status)
print("Grade:", grade)
