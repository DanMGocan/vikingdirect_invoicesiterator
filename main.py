
import pdfplumber
import os

processed_table = { "purchased_items": {}, "quantity_purchased": {} }
directory = "vikingdirect"

def extract_data(table):
    for element in list(table[0].split("\n")):
        if "QD" in element:
            element_array = list(element.split(" "))
            if float(element_array[-3]) != 0:
                item = f"{element_array[2]} {element_array[3]} {element_array[4]} {element_array[5]}"
                value = float(element_array[-2])
                quantity = float(value / float(element_array[-3]))

            try: 
                processed_table["purchased_items"][item] += value
                processed_table["quantity_purchased"][item] += quantity

            except:
                processed_table["purchased_items"][item] = value
                processed_table["quantity_purchased"][item] = quantity


# Will iterate over the files in the directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        with pdfplumber.open(f) as pdf:
            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                table = page.extract_table()
                extract_data(table[1])

value = sorted(processed_table["purchased_items"].items(), key=lambda item: item[1], reverse=True)
quantities = sorted(processed_table["quantity_purchased"].items(), key=lambda item: item[1], reverse=True)

f1 = open("sortedfinal.txt", "w")
f2 = open("sortedquantities.txt", "w")

for element in value:
    f1.write(f"{element[0]}: €{round(element[1], 2)} \n")

for element in quantities:
    f2.write(f"{element[0]}: {round(element[1], 2)} pieces \n")


# Uncomment if need to write the dictionary object to a separate file
# f = open("demofile2.py", "w")
# f.write(f"{processed_table}")




