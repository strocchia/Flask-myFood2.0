import csv

test_list1 = [1,2,3]
test_list2 = [4,5,6]
test_list3 = [7,8,9]
rows = zip(test_list1, test_list2, test_list3)

print rows

with open('test.csv', 'wb') as f:
	writer = csv.writer(f, delimiter='\t')
	#for val in test_list1:
	#	writer.writerow([val])
	for row in rows:
		writer.writerow(row)
