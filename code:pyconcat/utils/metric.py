import json

def calFrequency(json_data):
    # Calculate the number of files stored in each item
    files_per_item = {key: len(value) for key, value in json_data.items()}
    
    # Calculate the total number of files stored across all items
    total_files = sum(files_per_item.values())
    
    # Calculate the percentage of files stored per item across all items
    if total_files == 0:
        # Set all percentages to zero if there are no files
        percentage_per_item = {key: 0 for key in files_per_item}
    else:
        # Calculate percentages
        percentage_per_item = {key: (value / total_files) * 100 for key, value in files_per_item.items()}
    
    return percentage_per_item



