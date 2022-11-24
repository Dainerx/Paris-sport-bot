from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
import argparse
import logging
from plyer import notification

PARIS_TENNIS_COURTS = ['Neuve Saint-Pierre', 'Poliveau', 'Luxembourg', 'Valeyre', 'Candie', 'Philippe Auguste',
                       'Thiéré', 'Alain Mimoun', 'Carnot', 'La Faluère', 'Léo Lagrange', 'Château des Rentiers',
                       'Dunois', 'Cordelières', 'Georges Carpentier', 'Charles Moureu', 'Poterne des Peupliers',
                       'Friant', 'Elisabeth', 'Croix Nivert', 'Suzanne Lenglen', 'Charles Rigoulot',
                       'Rigoulot - La Plaine', 'André et René Mourlon', 'Sablonnière', 'Atlantique',
                       'Henry de Montherlant', 'Niox', 'Fonds des Princes', 'Max Rousié', 'Reims',
                       'Aurelles de Paladines',
                       'Courcelles', 'Porte d’Asnières', 'Bertrand Dauvin', 'Championnet', 'Poissonniers', 'Jandelle',
                       'Jules Ladoumègue', 'Edouard Pailleron', 'Sept Arpents', 'Louis Lumière', 'Les Amandiers',
                       'Porte de Bagnolet', 'Davout', 'Déjerine',
                       'La Faluère', 'Puteaux']  # TODO challenge this list
LOGIN_PAGE = 'https://tennis.paris.fr/tennis/'
BOOKING_PAGE = 'https://tennis.paris.fr/tennis/jsp/site/Portal.jsp?page=recherche&view=recherche_creneau#!'
PLAYER_USERNAME = "myEmail@gmail.com"
PLAYER_PASSWORD = "myPassword"
PARTNER_NAME = 'myPartner'
PARTNER_EMAIL = 'mypartner@gmail.com'

HOLD_MODE = 'hold'
PAY_MODE = 'pay'
BOT_MODES = [PAY_MODE, HOLD_MODE]
BotMode = HOLD_MODE  # by default only hold the court


def login(username, password):
    try:
        logging.info("Logging in")
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(LOGIN_PAGE)
        window_before = driver.window_handles[0]
        driver.find_element_by_id('button_suivi_inscription').click()
        time.sleep(0.5)
        # LOGIN PAGE
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        time.sleep(0.5)
        driver.find_element_by_id('username-login').send_keys(username)
        driver.find_element_by_id('password-login').send_keys(password)
        time.sleep(0.5)
        driver.find_element_by_name('Submit').click()
        time.sleep(1)
        driver.switch_to.window(window_before)
        time.sleep(0.4)
        driver.get(BOOKING_PAGE)
        time.sleep(0.5)
        return driver
    except Exception as e:
        logging.error("Failure to login", e)
        raise e


def pick_tennis_court(driver, day, name):
    try:
        time.sleep(0.5)
        driver.find_element_by_id('whereToken').click()
        driver.find_element_by_class_name('tokens-input-text').send_keys(name)
        time.sleep(1)
        driver.find_element_by_class_name('tokens-suggestions-list-element').click()

        # FIND SLOT
        driver.find_element_by_id('when').click()
        time.sleep(0.5)
        driver.find_elements_by_class_name('date-item')[day].click()
        driver.find_element_by_id('rechercher').click()
        time.sleep(1)
    except Exception as e:
        logging.error("Failure to pick a tennis court", e)
        raise e


def book_and_pay(driver, hour, day, name):
    try:
        # Click on the arrow to make the booking rows available
        driver.find_element_by_id('head{}{}'.format(name.replace(" ", ""), hour)).click()
        time.sleep(2)

        # Click Reserver button
        driver.find_element_by_id('collapse{}{}'.format(name, hour)).find_elements_by_class_name('tennis-court')[
            0].find_element_by_class_name('button').click()
        time.sleep(1)
        # FILL PARTNER INFOS
        driver.find_element_by_class_name('name').find_element_by_class_name(
            'form-control').send_keys(PARTNER_NAME)
        time.sleep(1)
        driver.find_element_by_class_name('firstname').find_element_by_class_name(
            'form-control').send_keys(PARTNER_EMAIL)
        time.sleep(1)
        driver.find_element_by_id('submitControle').click()
        time.sleep(1)

        if BotMode is not HOLD_MODE:
            # PAYMENT AND VALIDATION
            driver.find_element_by_class_name('price-item').click()
            time.sleep(1)
            driver.find_element_by_id('submit').click()
            logging.info("Booked and payed a reservation at {0}, in {1}, {2} days from today".format(hour, name, day))
            notification.notify(
                title='Paris Sport Bot',
                message="Booked and payed a reservation at {0}, in {1}, {2} days from today".format(hour, name, day),
                app_icon=None,
                timeout=10,
            )
        else:
            logging.info(
                "Held a reservation at {0}, in {1}, {2} days from today - you have 10 minutes to manually pay".format(
                    hour,
                    name,
                    day))
            notification.notify(
                title='Paris Sport Bot',
                message="Held a reservation at {0}, in {1}, {2} days from today - you have 10 minutes to manually pay".format(
                    hour,
                    name,
                    day),
                app_icon=None,
                timeout=10,
            )
    except Exception as e:
        logging.error("Failure to book and pay", e)
        raise e


def check_arguments(args):
    if not (args.Hour and args.Day and args.Name):
        logging.error("Hour, Day, and Name arguments are mandatory")
        return False

    if args.Mode:
        if args.Mode not in BOT_MODES:
            logging.error("% s is not a valid bot mode" % args.Mode)
        else:
            global BotMode
            BotMode = args.Mode

    if not (int(args.Day) >= 0 and int(args.Day) <= 7):
        logging.error("% s is not valid day format" % args.Day)
        return False

    if not (str(args.Hour).endswith("h") and (int(str(args.Hour).split("h")[0]) >= 8
                                              and int(str(args.Hour).split("h")[0]) <= 20)):
        logging.error("% s is not valid hour format" % args.Hour)
        return False

    args.Name = str(args.Name).replace("-", " ")
    if not (args.Name in PARIS_TENNIS_COURTS):
        logging.error("% s is not valid paris tennis court name" % args.Name)
        return False

    dt = datetime.datetime.today() + datetime.timedelta(days=int(args.Day))
    logging.info("Chosen Mode: % s" % BotMode)
    logging.info("Chosen Hour: % s" % args.Hour)
    logging.info("Chosen Day: % s" % dt.day)
    logging.info("Chosen Court name: % s" % args.Name)
    return True


if __name__ == '__main__':
    # Read and check arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--Mode", help="Set bot mode: pay or hold")
    parser.add_argument("-ho", "--Hour", help="Set the hour to book")
    parser.add_argument(
        "-d", "--Day", help="Set in how many days from today to book")
    parser.add_argument("-n", "--Name", help="Set tennis court name - composed names should be separated by dash `-`")
    args = parser.parse_args()
    if not check_arguments(args):
        logging.error("Failure to validate arguments")
        exit(1)

try:
    driver = login(PLAYER_USERNAME, PLAYER_PASSWORD)
    pick_tennis_court(driver, day=int(args.Day), name=args.Name)
    book_and_pay(driver, args.Hour, int(args.Day), args.Name)
except Exception as e:
    exit(1)
