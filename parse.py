import os
import csv
import re
import dotenv

dotenv.load_dotenv()

log_directory = os.getenv("log_directory")

for root, dirs, files in os.walk(log_directory):
    for file in files:
        if file.endswith('_LIN_LOG.txt'):
            file_path = os.path.join(root, file)
            output_csv_file = file_path.replace('.txt', '_output.csv')  
            data = []  

            with open(file_path, 'r') as log_file:
                line_number = 0  
                for line in log_file:
                    line_number += 1 
                    if line.startswith('/synergy_wa'):
                        parts = line.split()
                        # print(parts)
                        if len(parts) >= 4:
                            file_path = parts[0]
                            error_no = parts[3].rstrip(":")
                         
                            error_message = ' '.join(parts[4:])
                            # print(error_message)
                            error_message_part = error_message.split('[MM')[0].strip() 
                            if ' ' in error_message_part:
                                error_message_part = f'"{error_message_part}"' 
                            # print(error_message_part)
                           
                            misra_level_match = re.search(r'\bMM-PWT (\d+)', error_message)
                            misra_level = misra_level_match.group(0) if misra_level_match else ''
                            # print(misra_level)

                         
                            misra_rule_match = re.search(r'MISRA\s(.*?)(\d+\.\d+)', error_message)
                            misra_rule_no = f"MISRA {misra_rule_match.group(1)} {misra_rule_match.group(2)}" if misra_rule_match else ''

                            if not misra_level:
                                misra_level = 'N/A' 
                            if not misra_rule_no:
                                misra_rule_no = 'N/A' 

                            data.append((line_number, file_path, error_no, error_message_part, misra_level, misra_rule_no))

            with open(output_csv_file, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Line No", "File Path", "Error No", "Error Message", "Misra Level", "MISRA Rule No"])
                csv_writer.writerows(data)

# for entry in data:
#     print("Line No:", entry[0])
#     print("File Path:", entry[1])
#     print("Error No:", entry[2])
#     print("Error Message:", entry[3])
#     print("Misra Level:", entry[4])
#     print("MISRA Rule No:", entry[5])
#     print()
