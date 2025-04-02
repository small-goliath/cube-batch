import os
import random
import string
from dotenv import load_dotenv
import logging
import logging.config
from cube import login, change, driver

load_dotenv()

logging.config.fileConfig('logging.conf')
log = logging.getLogger('update_password')
icon_path = os.getenv('icon')
log_path = os.getenv('log')

def generate_random_string():
    length = 8
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*")
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*"
    remaining = ''.join(random.choices(all_characters, k=length - 4))
    result = list(uppercase + lowercase + digit + special + remaining)
    random.shuffle(result)
    
    return ''.join(result)

def send_mac_notification(is_succeed, title, message):
    if is_succeed:
        button = "확인"
        script = f'osascript -e \'display dialog "{message}" with title "{title}" with icon POSIX file "{icon_path}" buttons {{"{button}"}} default button "{button}"\''
    else:
        log_button = "로그 보기"
        confirm_button = "확인"
        script = f'''
            osascript <<EOF
            set dialogResult to display dialog "{message}" with title "{title}" with icon POSIX file "{icon_path}" buttons {{"{log_button}", "{confirm_button}"}} default button "{log_button}"
            if button returned of dialogResult is "{log_button}" then
                do shell script "open {log_path}"
            end if
            EOF
        '''
    os.system(script)

if __name__ == "__main__":
    try:
        login()
        
        TEMP_1_password = generate_random_string()
        TEMP_2_password = generate_random_string()
        TEMP_3_password = generate_random_string()
        password = os.getenv("password")

        change(password, TEMP_1_password)
        change(TEMP_1_password, TEMP_2_password)
        change(TEMP_2_password, TEMP_3_password)
        change(TEMP_3_password, password)

        send_mac_notification(True, "cube 배치: 패스워드 변경", "패스워드 변경이 완료되었습니다!")
    except Exception as e:
        log.error(e)
        send_mac_notification(False, "cube 배치: 패스워드 변경", "패스워드 변경이 싪패되었습니다!")
    finally:
        if driver is not None:
            driver.quit()
            log.info("driver quited!!!!")