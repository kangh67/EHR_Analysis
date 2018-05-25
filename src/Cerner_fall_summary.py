# Cerner fall data

import numpy as np
import matplotlib.pyplot as plt


file_clinical_event = "/Users/SPH6555/Cerner Samples/fall reports/clinical_event.txt"


def file_to_dict(file_direction):
    """

    :param file_direction: input file direction, string
    :return: patient_dict_all, patient_dict_8, patient_dict_9, patient_dict_10, dict{"patient id" = count}
    """
    dict_all = {}  # unique patients
    dict_8 = {}
    dict_9 = {}
    dict_10 = {}
    with open(file_clinical_event, 'r') as f:
        for line in f:
            l = line.split("\t")
            if len(l) == 38:
                if dict_all.get(l[0], -1) == -1:  # new patient
                    dict_all[l[0]] = 1
                else:  # existing patient
                    dict_all[l[0]] = dict_all.get(l[0]) + 1

                if l[12] == "8":  # Fall data/time
                    if dict_8.get(l[0], -1) == -1:
                        dict_8[l[0]] = 1
                    else:
                        dict_8[l[0]] = dict_8.get(l[0]) + 1

                elif l[12] == "9":  # Fall during this admission
                    if dict_9.get(l[0], -1) == -1:
                        dict_9[l[0]] = 1
                    else:
                        dict_9[l[0]] = dict_9.get(l[0]) + 1

                elif l[12] == "10":  # Fall, history of
                    if dict_10.get(l[0], -1) == -1:
                        dict_10[l[0]] = 1
                    else:
                        dict_10[l[0]] = dict_10.get(l[0]) + 1
            else:
                print("------ No info line")
                print("       length = " + str(len(l)))
                print("       content = " + line)
    return dict_all, dict_8, dict_9, dict_10


def patient_num_to_event_num(patient_dict):
    """

    :param patient_dict: patient dictionary, dict{"patient id" = count}
    :return: the sum of counts of all patient ids
    """
    sum_of_count = 0
    for key in patient_dict:
        sum_of_count += patient_dict[key]
    return sum_of_count


def patient_dict_to_event_freq(patient_dict):
    """

    :param patient_dict: patient dictionary, dict{"patient id" = count}
    :return: freq_list, [], index indicates the record number, value indicates the freq
    """
    max_value = np.max(list(patient_dict.values()))  # max event record number a patient may have
    freq_list = np.zeros([max_value + 1])  # index indicates the record number, value indicates the freq
    for key in patient_dict:
        freq_list[patient_dict[key]] += 1
    return freq_list


def overlaps_dicts_between_two_dict(dict1, dict2):
    """

    :param dict1: patient dictionary1, dict{"patient id" = count}
    :param dict2: patient dictionary2, dict{"patient id" = count}
    :return: patient dictionary1_o, a subset of patient dictionary1 which overlaps with patient dictionary2
            patient dictionary2_o, a subset of patient dictionary2 which overlaps with patient dictionary1
    """
    dict1_o = {}
    dict2_o = {}

    for key in dict1:
        if dict2.get(key, -1) != -1:
            dict1_o[key] = dict1[key]
            dict2_o[key] = dict2[key]
    return dict1_o, dict2_o


# Overall summary
patient_dict_all, patient_dict_8, patient_dict_9, patient_dict_10 = file_to_dict(file_clinical_event)  # all dicts
count_clinical_event = patient_num_to_event_num(patient_dict_all)  # event entries
count_8 = patient_num_to_event_num(patient_dict_8)  # Fall Date/Time
count_9 = patient_num_to_event_num(patient_dict_9)  # Fall During This Admission
count_10 = patient_num_to_event_num(patient_dict_10)  # Fall, History of

print("------ Total event entries : " + str(count_clinical_event) + ", including " + str(
    len(patient_dict_all)) + " unique patients.")
print("------ 8_Fall data/time : " + str(count_8) + ", including " + str(len(patient_dict_8)) + " unique patients.")
print("------ 9_Fall during this admission : " + str(count_9) + ", including " + str(
    len(patient_dict_9)) + " unique patients.")
print("------ 10_Fall, history of : " + str(count_10) + ", including " + str(
    len(patient_dict_10)) + " unique patients.")


# 9_Fall during admission summary
patient_dict_8_and_9_in_9, patient_dict_8_and_9_in_8 = overlaps_dicts_between_two_dict(
    patient_dict_9, patient_dict_8)  # overlaps between 9 and 8
patient_dict_9_and_10_in_9, patient_dict_9_and_10_in_10 = overlaps_dicts_between_two_dict(
    patient_dict_9, patient_dict_10)  # overlaps between 9 and 10
# how many records do the patient in 9 have in 8
count_8_and_9_in_8 = patient_num_to_event_num(patient_dict_8_and_9_in_8)
# how many records do the patient in 9 have in 10
count_9_and_10_in_10 = patient_num_to_event_num(patient_dict_9_and_10_in_10)
# how many records do the patient in 9 have in all three categories
count_9_all_event = count_9 + count_8_and_9_in_8 + count_9_and_10_in_10

print("************")
print("------ Summary of 9_Fall during admission ------")
print("The " + str(len(patient_dict_9)) + " patient in 9_Fall during this admission (out of the overall "
      + str(len(patient_dict_all)) + ") have totally " + str(count_9_all_event)
      + " event records (out of the overall " + str(count_clinical_event) + ")")
print("\tAmong the 1107 patients, " + str(len(patient_dict_8_and_9_in_8))
      + " also appear in 8_Fall data/time, which refer to " + str(count_8_and_9_in_8)
      + " event records in 8_Fall data/time")
print("\tAmong the 1107 patients, " + str(len(patient_dict_9_and_10_in_10))
      + " also appear in 10_Fall, history of, which refer to " + str(count_9_and_10_in_10)
      + " event records in 10_Fall, history of")


# plot record_number's freq of 9_Fall during this admission
fall_freq = patient_dict_to_event_freq(patient_dict_9)
print(fall_freq)
plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], fall_freq[1:], 'r-')
plt.show()
