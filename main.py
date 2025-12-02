# main.py

import time
import configparser
from unified_detector import UnifiedDetector
import automovement
import sounddevice as sd
import RPi.GPIO as GPIO
from pushover import Client

# --- Load Configuration ---
config = configparser.ConfigParser()
config.read('config.ini')

# --- Pushover Configuration ---
PUSHOVER_USER_KEY = config.get('Pushover', 'user_key', fallback=None)
PUSHOVER_API_TOKEN = config.get('Pushover', 'api_token', fallback=None)

# --- Audio Configuration ---
INPUT_DEVICE = config.get('Audio', 'input_device', fallback='hw:2,0')
SAMPLE_RATE = config.getint('Audio', 'sample_rate', fallback=48000)

# Uncomment the following lines to print a list of available audio devices
# and then press Ctrl+C to exit. This will help you find the correct
# 'input_device' name for your config.ini file.
#
# print("--- Available Audio Devices ---")
# print(sd.query_devices())

# --- Threshold Configuration ---
BATTLE_THRESHOLD = config.getint('Thresholds', 'battle', fallback=10000)

# --- Timing Configuration ---
PRESS_TIME = config.getfloat('Timings', 'press_time', fallback=0.25)

# --- GPIO Pin Configuration ---
BUTTON_PINS = {
    "A": config.getint('GPIO', 'A'),
    "B": config.getint('GPIO', 'B'),
    "X": config.getint('GPIO', 'X'),
    "Y": config.getint('GPIO', 'Y'),
    "UP": config.getint('GPIO', 'UP'),
    "DOWN": config.getint('GPIO', 'DOWN'),
    "LEFT": config.getint('GPIO', 'LEFT'),
    "RIGHT": config.getint('GPIO', 'RIGHT'),
    "START": config.getint('GPIO', 'START'),
    "SELECT": config.getint('GPIO', 'SELECT'),
    "L": config.getint('GPIO', 'L'),
    "R": config.getint('GPIO', 'R')
}

automovement.BUTTON_PINS = BUTTON_PINS
automovement.PRESS_TIME = PRESS_TIME

GPIO.setmode(GPIO.BCM)

for pin in BUTTON_PINS.values():
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

def send_shiny_notification(encounter_count):
    """Sends a Pushover notification when a shiny is found."""
    if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN or "YOUR_" in PUSHOVER_USER_KEY:
        print("Pushover credentials not configured in config.ini. Skipping notification.")
        return

    try:
        client = Client(PUSHOVER_USER_KEY, api_token=PUSHOVER_API_TOKEN)
        client.send_message(
            f"Shiny found after {encounter_count} encounters!",
            title="✨ Shiny Pokémon Alert! ✨"
        )
    except Exception as e:
        print(f"Failed to send Pushover notification: {e}")

def main():
    """The main function to run the shiny hunting bot."""

    print("--- Shiny Hunting Automation Setup ---")
    generation = input("Enter Pokémon generation (3, 4, or 5): ")
    if generation not in ['3', '4', '5']:
        print("Invalid generation.")
        return

    try:
        shiny_threshold_key = f'shiny_gen{generation}'
        shiny_threshold = config.getint('Thresholds', shiny_threshold_key)
    except (configparser.NoOptionError, configparser.NoSectionError):
        print(f"Warning: Shiny threshold for Gen {generation} not found in config.ini. Using a default of 750.")
        shiny_threshold = 750

    hunt_type = input("Enter hunt type (e.g., 'soft_reset', 'random_encounter', 'starter', 'fishing'): ")

    default_extra_wait = config.getfloat('Timings', 'extra_wait_time', fallback=0.0)
    extra_wait_input = input(f"Enter extra delay for encounter loading (in seconds, press Enter to use default of {default_extra_wait}s): ")
    if extra_wait_input.strip() == "":
        extra_wait_time = default_extra_wait
    else:
        try:
            extra_wait_time = float(extra_wait_input)
            if extra_wait_time < 0:
                print("Negative time not allowed. Using default.")
                extra_wait_time = default_extra_wait
        except ValueError:
            print("Invalid number. Using default.")
            extra_wait_time = default_extra_wait

    # --- Initialization ---
    detector = UnifiedDetector(
        generation=generation,
        device=INPUT_DEVICE,
        shiny_threshold=shiny_threshold,
        battle_threshold=BATTLE_THRESHOLD,
        sample_rate=SAMPLE_RATE
    )

    detector.start()

    # --- Start the Hunt ---
    print("\n--- Starting the Hunt ---")
    detector.start()
    time.sleep(1)
    encounter_count = 0

    try:
        while True:
            if hunt_type == 'soft_reset' and generation == '4':
                encounter_count += 1
                SR = automovement.SoftReset()
                SR.reset()
                SR.before_listening_gen4()
                print(f"Encounter number {encounter_count}")
                shiny_timeout = 8 + extra_wait_time
                shiny_found = detector.wait_for_shiny(timeout=shiny_timeout)
                if shiny_found:
                    send_shiny_notification(encounter_count)
                    print("\n\n*** SHINY HUNT SUCCESSFUL! Stopping automation. ***")
                    break

            elif hunt_type == 'soft_reset' and generation == '5':
                encounter_count += 1
                SR = automovement.SoftReset()
                SR.reset()
                SR.before_listening_gen5()
                print(f"Encounter number {encounter_count}")
                shiny_timeout = 8 + extra_wait_time
                shiny_found = detector.wait_for_shiny(timeout=shiny_timeout)
                if shiny_found:
                    send_shiny_notification(encounter_count)
                    print("\n\n*** SHINY HUNT SUCCESSFUL! Stopping automation. ***")
                    break

            elif hunt_type == 'starter' and generation == '4':
                encounter_count += 1
                STARTER = automovement.Starter()
                STARTER.reset()
                STARTER.before_listening_gen4()
                print(f"Encounter number {encounter_count}")
                # wait for starly to come in
                time.sleep(9)
                shiny_timeout = 5
                shiny_found = detector.wait_for_shiny(timeout=shiny_timeout)
                if shiny_found:
                    send_shiny_notification(encounter_count)
                    print("\n\n*** SHINY HUNT SUCCESSFUL! Stopping automation. ***")
                    break

            elif hunt_type == 'random_encounter' and (generation == '4' or generation == '5'):
                RE = automovement.RandomEncounter()
                last_battle_time = time.time()
                detector.battle_found_event.clear()

                while True:
                    detector.start_battle_detection()
                    RE.move()
                    battle_started = detector.wait_for_battle(timeout=0.5)
                    detector.stop_battle_detection()
                    current_time = time.time()

                    if battle_started:
                        detector.battle_found_event.clear()
                        encounter_count += 1
                        print(f"Encounter number {encounter_count}")
                        time.sleep(2)

                        if generation == '4':
                            shiny_timeout = 10 + extra_wait_time
                        elif generation == '5':  
                            shiny_timeout = 7 + extra_wait_time

                        shiny_found = detector.wait_for_shiny(timeout=shiny_timeout)
                        if shiny_found:
                            send_shiny_notification(encounter_count)
                            print("\n\n*** SHINY HUNT SUCCESSFUL! Stopping automation. ***")
                            # Break out of the inner while loop
                            break
                        
                        RE.run()
                        last_battle_time = current_time

                    elif current_time - last_battle_time > 120:
                        print("No battle detected for 120s — performing rescue moves.")
                        automovement.press_left()
                        time.sleep(0.2)
                        automovement.press_left()
                        time.sleep(0.2)
                        automovement.press_right()
                        time.sleep(2)
                        automovement.press_a()
                        print("Rescue sequence complete. Continuing...")
                        last_battle_time = current_time
                
                # If a shiny was found, break out of the outer while loop as well
                if shiny_found:
                    break
            else:
                print(f"Unknown or unsupported hunt type '{hunt_type}' for Gen {generation}. Stopping.")
                break

    except KeyboardInterrupt:
        print("\n\nScript stopped by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("Cleaning up resources...")
        if GPIO.getmode() is not None:
            GPIO.cleanup()
        detector.stop()

if __name__ == "__main__":
    main()