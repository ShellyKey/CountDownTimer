import time
import threading

# Global variables to manage the state of the timer
paused = False  # Tracks whether the timer is paused
stopped = False  # Tracks whether the timer is stopped

def countdown_timer(total_time):

    global paused, stopped

    while total_time > 0 and not stopped:
        if not paused:  # If not paused, decrement the timer
            # Calculate days, hours, minutes, and seconds from total_time
            days, remainder = divmod(total_time, 86400)  # 86400 seconds in a day
            hours, remainder = divmod(remainder, 3600)  # 3600 seconds in an hour
            mins, secs = divmod(remainder, 60)         # 60 seconds in a minute

            # Display the remaining time dynamically in the terminal
            print(f"\rTime Remaining: {days:02d}:{hours:02d}:{mins:02d}:{secs:02d}", end="")
            time.sleep(1)  # Wait for 1 second
            total_time -= 1  # to Decrease total_time by 1 second

    # When the timer reaches 0 and is not stopped, print a "Time's up" message
    if total_time == 0 and not stopped:
        print("\nTime's up!")

def user_controls():
    global paused, stopped

    while not stopped:
        # Prompt the user for input to pause, resume, or stop the timer
        user_input = input("\nPress 'p' to pause, 'r' to resume, 'q' to quit: ").strip().lower()
        if user_input == "p":
            paused = True  # Set paused to True to pause the timer
            print("Timer paused. Press 'r' to resume.")
        elif user_input == "r":
            paused = False  # Set paused to False to resume the timer
            print("Timer resumed.")
        elif user_input == "q":
            stopped = True  # Set stopped to True to stop the timer
            print("Timer stopped.")
            break

if __name__ == "__main__":
    # Prompt the user to enter time in the format D:HH:MM:SS
    time_input = input("Enter time in D:HH:MM:SS format (e.g., 0:02:30:00): ")
    try:
        days, hours, minutes, seconds = map(int, time_input.split(":"))
        if (days < 0 or hours < 0 or hours >= 24 or
            minutes < 0 or minutes >= 60 or seconds < 0 or seconds >= 60):
            raise ValueError("Invalid time format.")

        # Convert the total time into seconds
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

        # Start the countdown timer in a separate thread
        timer_thread = threading.Thread(target=countdown_timer, args=(total_seconds,))
        timer_thread.start()

        # Handle user controls in the main thread
        user_controls()

        # Wait for the timer thread to finish
        timer_thread.join()

    except ValueError:
        # Display an error message if the input time is invalid
        print("Please enter a valid time in D:HH:MM:SS format.")