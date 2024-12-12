from datetime import datetime, timedelta, time
from prompt import ACTION_DETECT_PROMPT, DATE_EXTRACTION_PROMPT
from config import CHATBOT_MODEL, TEMPERATURE, MAX_ATTEMPTS, MAX_HISTORY

def convert_iso_datetime(timestamp):
    # Remove the trailing 'Z' from the timestamp string
    timestamp = timestamp.rstrip('Z')
    # Convert the string to a datetime object
    dt = datetime.fromisoformat(timestamp)
    return dt

def convert_timestamp_to_datetime(dt):
    # Format the datetime object
    day_of_week = dt.strftime('%A')  # Full day of the week name
    date_str = dt.strftime('%d/%m/%Y')  # Date in dd/mm/yyyy format
    # time_str = dt.strftime('%H:%M')  # Time in hh:mm format
    # Combine the formatted strings
    formatted_string = f"{day_of_week}, {date_str}"
    return formatted_string

def get_two_weeks_later(dt):
    # Define a timedelta of 14 days (2 weeks)
    two_weeks = timedelta(weeks=2)
    # Calculate the new date
    future_date = dt + two_weeks
    return future_date

def get_first_valid_date(dt):
    # Ensure dt is a datetime object and get the day of the week (0=Monday, 6=Sunday)
    day_of_week = dt.weekday()

    # Calculate days to add to reach the next valid date
    if day_of_week < 4:  # Monday to Thursday
        days_to_add = 1  # Go to the next day
    elif day_of_week == 4:  # Friday
        days_to_add = 3  # Skip to Monday
    else:  # Saturday or Sunday
        days_to_add = (7 - day_of_week)  # Days to next Monday

    # Calculate the first valid date
    first_valid_date = dt + timedelta(days=days_to_add)

    return first_valid_date

def format_conversation(history):
    conversation = []
    for h in history:
        conversation.append(f"{h['role']}: {h['content']}")
    return "\n".join(conversation)

def sale_script_get_message_code(openai_client, history):

    system_prompt = ACTION_DETECT_PROMPT
    conversation = format_conversation(history[-MAX_HISTORY:])
    system_prompt = system_prompt.replace("<<conversation>>", conversation)

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    for i in range(MAX_ATTEMPTS):
        try:
            response = openai_client.chat.completions.create(model=CHATBOT_MODEL,
                                                             messages=messages,
                                                             temperature=TEMPERATURE)
            answer = response.choices[0].message.content
        except:
            answer = "None"
    return answer

def sale_script_get_scheduled_time(openai_client, history):
    dt = convert_iso_datetime(history[-1]["timestamp"])
    today = convert_timestamp_to_datetime(dt)

    system_prompt = DATE_EXTRACTION_PROMPT
    system_prompt = system_prompt.replace("<<current_date_time>>", today)

    conversation = format_conversation(history[-MAX_HISTORY:])
    system_prompt = system_prompt.replace("<<conversation>>", conversation)

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    for i in range(MAX_ATTEMPTS):
        try:
            response = openai_client.chat.completions.create(model=CHATBOT_MODEL,
                                                             messages=messages,
                                                             temperature=TEMPERATURE)
            answer = response.choices[0].message.content
        except:
            answer = "None"
    return answer

def get_date_time_condition(timestamp, scheduled_time):

    timestamp = convert_iso_datetime(timestamp)
    scheduled_time = convert_iso_datetime(scheduled_time)
    first_valid_date = get_first_valid_date(timestamp)
    two_weeks_later = get_two_weeks_later(timestamp)

    start_of_business = time(9, 0)  # 9:00 AM
    end_of_business = time(17, 0)  # 5:00 PM

    # print("~~~~", "get_date_time_condition")
    # print(timestamp, convert_timestamp_to_datetime(timestamp))
    # print(scheduled_time, convert_timestamp_to_datetime(scheduled_time))
    # print(first_valid_date, convert_timestamp_to_datetime(first_valid_date))
    # print(two_weeks_later, convert_timestamp_to_datetime(two_weeks_later))
    # print(start_of_business, end_of_business)
    #
    # print(scheduled_time > two_weeks_later)
    # print(scheduled_time < timestamp)
    # print(scheduled_time.weekday() >= 5)
    # print(scheduled_time.time(), scheduled_time.time() < start_of_business)
    # print(scheduled_time.time(), scheduled_time.time() > end_of_business)
    #
    # print("~~~~")

    if scheduled_time > two_weeks_later:
        return f"The date user choose is out of 2 weeks limit. Tell user that we can only schedule time upto 2 weeks in advanced, " \
               f"which is {convert_timestamp_to_datetime(two_weeks_later)}. Ask them to choose another date within 2 weeks from now."
    elif scheduled_time < timestamp:
        return f"User is scheduling for {convert_timestamp_to_datetime(scheduled_time)}, which is a time in the past, tell them to choose another valid date."

    elif scheduled_time.weekday() >= 5:
        return f"The date user chooses {convert_timestamp_to_datetime(scheduled_time)}, which is weekend, " \
               f"tell them to choose another date. " \
               f"Ask if they want to schedule for {convert_timestamp_to_datetime(first_valid_date)}"

    elif scheduled_time.time() < start_of_business or scheduled_time.time() > end_of_business:
        return f"User is scheduling for {convert_timestamp_to_datetime(scheduled_time)}, " \
               f"which is a time out of working hours, " \
               "clarify with them the working hours is from 9am to 5pm, and tell them to choose a new time."

    return ""