from datetime import timedelta

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from django.urls import reverse
from django.test import override_settings

from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time 


from django.contrib.auth import get_user_model
from game.models import Game, Challenge, ChallengeFlag, GamePeriod

def prepare_db(self):
    self.user1 = get_user_model().objects.create_user(username="brock", email="brock@mail.com", password="123456")
    self.user2 = get_user_model().objects.create_user(username="max", email="max@mail.com", password="123456")

    game_nonperiod = Game(
        title="title1",
        slug="title1",
        description="description",
    )
    game_nonperiod.save()

    challenge1 = Challenge(
        description="challenges descs",
        game=game_nonperiod
    )
    challenge1.save()

    self.flag1 = ChallengeFlag(name="flag1", flag="FLAG{1}", explanation="explanation1", point=10, challenge=challenge1)
    self.flag1.save()

    self.flag2 = ChallengeFlag(name="flag2", flag="FLAG{2}", explanation="explanation2", point=20, challenge=challenge1)
    self.flag2.save()

    self.flag3 = ChallengeFlag(name="flag3", flag="FLAG{3}", explanation="explanation3", point=35, challenge=challenge1)
    self.flag3.save()

    game_with_period = Game(
        title='title2',
        slug="title2",
        description="description",
    )
    game_with_period.save()

    period = GamePeriod(
        start=timezone.now() - timedelta(hours=1),
        end=timezone.now() + timedelta(hours=1),
        game=game_with_period
    )
    period.save()

    challenge1p = Challenge(
        description="challenges period descs",
        game=game_with_period
    )
    challenge1p.save()

    self.flag1p = ChallengeFlag(name="flag1p", flag="FLAG{1p}", explanation="explanation1p", point=10, challenge=challenge1p)
    self.flag1p.save()

    self.flag2p = ChallengeFlag(name="flag2p", flag="FLAG{2p}", explanation="explanation2p", point=20, challenge=challenge1p)
    self.flag2p.save()

    self.flag3p = ChallengeFlag(name="flag3p", flag="FLAG{3p}", explanation="explanation3p", point=35, challenge=challenge1p)
    self.flag3p.save()

    self.game = game_nonperiod
    self.gamep = game_with_period
    


@override_settings(DEBUG=True,)
class GameSeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(20)
    
    def setUp(self):
        prepare_db(self)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    

    def _login_user(self, e, p):
        LOGIN_URL = reverse("login")
        self.selenium.get(self.live_server_url + LOGIN_URL)
        email = self.selenium.find_element_by_name("email")
        password = self.selenium.find_element_by_name("password")
        submit = self.selenium.find_element_by_name("submit")
        email.send_keys(e)
        password.send_keys(p)
        submit.click()


    def _logout_user(self):
        self.selenium.find_element_by_id("logoutLink").click()
    
    
    def _answer_flag(self, flag):
        form = self.selenium.find_element_by_css_selector(".flag-enter form")
        input_flag = form.find_element_by_css_selector("input[name='flag']")
        submit = form.find_element_by_css_selector("button")

        # enter wrong flag
        input_flag.send_keys(flag)
        submit.click()

        input_flag.clear()

    
    def test_play_game_no_period(self):
        """ test when user enter right flag score raise and another user see it """
        self._login_user(self.user1.email, "123456")

        GAME_URL = self.live_server_url + reverse("game", args=["title1"])
        self.selenium.get(GAME_URL)

        # enter wrong flag
        self._answer_flag("FLAG{wrong}")
        # check if score increase
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.score, 0)

        # enter right flag
        self._answer_flag(self.flag2.flag)
        # check if score increase
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.score, 20)

        # see if update the write flag info
        flag_info = self.selenium.find_element_by_id(f"flag_{self.flag2.id}");
        flag_status = flag_info.find_element_by_css_selector(".flag-status");
        flag_point = flag_info.find_element_by_css_selector(".flag-point");
        self.assertIn("Solved", flag_status.text)
        self.assertEqual(flag_point.text, '20')
        
        # enter same flag
        self._answer_flag(self.flag2.flag)
        # check if score the same
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.score, 20)

        # enter another flag
        self._answer_flag(self.flag1.flag)
        # check if score increase
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.score, 30)

        # see score as other user
        self._logout_user()
        self._login_user(self.user2.email, "123456")
        self.selenium.get(GAME_URL)

        # try answer too
        self._answer_flag(self.flag3.flag)
        # check if another user name appear
        self.assertIn(self.user1.username, self.selenium.page_source)

        
    def test_play_game_with_period(self):
        """ A game that has start and end date """
        self._login_user(self.user1.email, "123456")

        GAME_URL = self.live_server_url + reverse("game", args=["title2"])
        self.selenium.get(GAME_URL)

        # see if the timer show
        spanday = self.selenium.find_element_by_id("days")
        self.assertTrue(spanday)

        # check answer flag and get half score
        self._answer_flag(self.flag2p.flag)
        # check if half score
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.score, self.flag2p.point // 2)
    

    def test_play_game_with_period_ends(self):
        """ A game that already end get 0 point """
        # make game ends
        self.gamep.period.end = timezone.now() - timedelta(minutes=1) 
        self.gamep.period.save()

        
        self._login_user(self.user1.email, "123456")
        GAME_URL = self.live_server_url + reverse("game", args=[self.gamep.title])
        self.selenium.get(GAME_URL)

        # see if inform user that game ends
        self.assertIn("ช่วงเวลาของเกมหมดลงแล้วแต่คุณยังตอบ", self.selenium.page_source)

        # check answer flag and get 0 point
        self._answer_flag(self.flag2p.flag)
        # check if get 0 point
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.score, 0)
    

    def test_play_game_that_not_started_yet(self):
         # make not start in the next 1 minute
        self.gamep.period.start = timezone.now() + timedelta(minutes=10) 
        self.gamep.period.save()

        self._login_user(self.user1.email, "123456")
        GAME_URL = self.live_server_url + reverse("game", args=[self.gamep.title])
        self.selenium.get(GAME_URL)

        # must redirect to game index page
        GAME_INDEX_URL = self.live_server_url + reverse("game_index")
        WebDriverWait(self.selenium, 10).until(lambda driver: driver.current_url == GAME_INDEX_URL)

        # find warning alert
        self.assertIn("alert-warning", self.selenium.page_source)

        # try going in the page and enter the flag too
        self.gamep.period.start = timezone.now() - timedelta(minutes=1) 
        self.gamep.period.save()

        GAME_URL = self.live_server_url + reverse("game", args=[self.gamep.title])
        self.selenium.get(GAME_URL)

        self.gamep.period.start = timezone.now() + timedelta(minutes=1) 
        self.gamep.period.save()

        # when enter the flag shold alert and no points gain
        self._answer_flag(self.flag1p.flag)
        self.assertEqual(self.user1.score, 0)





        





