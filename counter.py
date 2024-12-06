import os

def counter(filename):
    folder_path = 'ignore'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        # Try to read the existing counter value from the file
        with open(filename, 'r') as file:
            counter = int(file.read())
    except (FileNotFoundError, ValueError):
        # If the file doesn't exist or doesn't contain a valid integer, start from 1
        counter = 1

    # Increment the counter
    new_counter = counter + 1

    # Write the updated counter value back to the file
    with open(filename, 'w') as file:
        file.write(str(new_counter))

    return counter

# def repo_counter(filename):
#     try:
#         # Try to read the existing counter value from the file
#         with open(filename, 'r') as file:
#             counter = int(file.read())
#     except (FileNotFoundError, ValueError):
#         # If the file doesn't exist or doesn't contain a valid integer, start from 1
#         counter = 1

#     # Increment the counter
#     new_counter = counter + 1

#     # Write the updated counter value back to the file
#     with open(filename, 'w') as file:
#         file.write(str(new_counter))

#     return counter

# def main():
#     filename = "counter.txt"  # Replace with the desired filename

#     # Get and increment the counter
#     counter = update_counter(filename)

#     # You can use the 'counter' value in your program or print it
#     print(f"Program has been run {counter} times.")

# if __name__ == "__main__":
#     main()
