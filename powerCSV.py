import sys
import subprocess
import time
import csv

duration = sys.argv[1]
file_name = sys.argv[2]
time_elapsed = 0

with open(file_name + '.csv', 'w') as file_out:
    write = csv.writer(file_out)
    first_row = ['Instantaneous_power_reading(W)', 'Minimum_during_sampling_period(W)', 'Maximum_during_sampling_period(W)', 'Average_power_reading_over_sample_period(W)', 'Day_of_Week', 'Month', 'Day',  'Time', 'Year', 'Sampling_period','Power_reading_state_is','Time_elapsed']
    write.writerow(first_row)
    end = time.time() + float(duration)
    while end > time.time():
        command = ['sudo', 'ipmitool', 'dcmi', 'power', 'reading']
        process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                universal_newlines=True)
        output = process.stdout
        output = output.replace(' ', '').split('\n')
        current_row = []
        # Instantaneous_power_reading
        current_row.append(output[1].split(':')[1].replace('Watts', ''))
        # Minimum_during_sampling_period
        current_row.append(output[2].split(':')[1].replace('Watts', ''))
        # Maximum_during_sampling_period
        current_row.append(output[3].split(':')[1].replace('Watts', ''))
        # Average_power_reading_over_sample_period
        current_row.append(output[4].split(':')[1].replace('Watts', ''))
        # IPMI_time_stamp
        #current_row += ',' + output[5].split(':')
        # Day_of_Week
        current_row.append(output[5].split(':')[1][:3])
        # Month
        current_row.append(output[5].split(':')[1][3:6])
        # Days values higher than 9
        if (len(output[5].split(':')[1]) == 10):
            # Day
            current_row.append(output[5].split(':')[1][6:8])
            # Time
            current_row.append(output[5][22:30])
            # Year
            current_row.append(output[5][30:])
        else:
            # Day
            current_row.append(output[5].split(':')[1][6])
            # Time
            current_row.append(output[5][21:29])
            # Year
            current_row.append(output[5][29:])
        # Sampling_period
        current_row.append(output[6].split(':')[1].replace('Seconds.', ''))
        # Power_reading_state_is
        current_row.append(output[7].split(':')[1])
        # Time_elapsed
        time_elapsed += int(output[6].split(':')[1].replace('Seconds.', ''))
        current_row.append(str(time_elapsed).zfill(8))
        write.writerow(current_row)
