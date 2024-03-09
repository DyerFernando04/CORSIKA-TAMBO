from datetime import datetime
from random import choice

def get_status(statuslog_path: str) -> str:
    try:
        with open(statuslog_path, 'r') as file:
            lines = file.readlines()
            if lines:
                date_format = '%Y-%m-%d %H:%M:%S'

                last_line=lines[-1].strip() 
                first_line =lines[0].strip()    # "start: Script is running simulations from $START_ENERGY GeV to $END_ENERGY GeV with steps of $INCREMENT GeV; general_start=$general_start_time"
                
                general_start=datetime.strptime(first_line.split('=')[1], date_format)
                if last_line==first_line:
                    return "No simulation has started, but the script is running" 
                elif last_line[0:7]=='current':  #indicates that there is a simulation running
                    # Split the line into its components
                    components = last_line.split(';')
                    # Create a dictionary to store the values
                    current_status = {}
                    for component in components:
                        key, value = component.split('=')
                        current_status[key.strip()] = value.strip()
                    #current_sim=1112PeV; start_time=####
                    date_format = '%Y-%m-%d %H:%M:%S'
                    now=datetime.now()
                    current_status['start_time']=datetime.strptime(current_status['start_time'], date_format)
                    elapsed_time_current_sim=str(now-current_status['start_time']).split('.')[0]
                    elapsed_time_general=str(now-general_start).split('.')[0]

                    status= f'''Corsika is currently running a simulation of {current_status['current_sim']}GeV that has been in progress for a duration of [{elapsed_time_current_sim}]. 
                    The entire simulation process for all energies has been running for a time period of [{elapsed_time_general}].'''
                    return status
                elif last_line[0:8]=='finished':
                    finish_time=last_line[12:]
                    return f'Corsika has finished with all the simulations at {finish_time}. Data is ready for processing'
                else:
                    return "Something went wrong. Status log was probably not correctly registered"

            else:
                return 'Empty log. No previous simulation found'  # El archivo está vacío
    except Exception as e:
        return f"Exception while reading status: {e}"

def get_info(statuslog_path: str) -> str:
    try:
        with open(statuslog_path, 'r') as file:
            lines = file.readlines()
            if lines :
                first_line =lines[0].strip()    # "start: Script is running simulations from $START_ENERGY GeV to $END_ENERGY GeV with steps of $INCREMENT GeV; general_start=$general_start_time"
                energy_range_str=first_line.split(';')[0].split(':')[1].strip()
                general_start_str=first_line.split('=')[1]
                return f'{energy_range_str}\nSimulations started running at {general_start_str}'
            else:
                return 'Empty log. No previous simulation found'  # El archivo está vacío
    except Exception as e:
        return f"Exception while reading status: {e}"
    first_line



def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == 'bot status':
        return 'Ready to roll e.e'
    elif lowered == 'simulation status':
        statuslog_path='/corsika-77500/DATA_SCRIPT/statuslog.txt' ##UPDATE PATH
        status: str = get_status(statuslog_path)
        return status
    elif lowered=='simulation info':
        statuslog_path='/corsika-77500/DATA_SCRIPT/statuslog.txt' ##UPDATE PATH (the same)
        info: str = get_info(statuslog_path)
        return info
    elif lowered=='insulta al niu':
        return choice(['niu ctm','el niu se la come','el niu se chocó en el little caesars'])
    elif lowered == 'current time':
        now=datetime.now()
        now_str=str(now).split('.')[0]
        time: str =f'Current time in server: {now_str}'
        return f'Current time in server: {now_str}'
    else:
        return 'Command not found'
