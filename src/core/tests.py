from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse
from django.test import override_settings

from django.contrib.auth import get_user_model
from core.models import Room, Task, TaskHint, ScoreHistory


def prepare_db(self):
    get_user_model().objects.create_user(username="brock", email="brock@mail.com", password="123456")
    room = Room(
        title="title",
        preview="preview",
        difficulty=3,
        description="description",
        conclusion="conclusion",
    )
    room.save()

    task1 = Task(
        task_number=1,
        title="task_title1",
        description="task_desc1",
        flag="FLAG{FLAG_1}",
        room=room,
        points=50,
    )
    task1.save()

    task2 = Task(
        task_number=2,
        title="task_title2",
        description="task_desc2",
        flag="FLAG{FLAG_2}",
        room=room,
        points=100,
    )
    task2.save()

    task1.hints.add(TaskHint(hint="task1_hint1"), TaskHint(hint="task1_hint2"), bulk=False)
    task2.hints.add(TaskHint(hint="task2_hint1"), TaskHint(hint="task2_hint2"), bulk=False)

    self.room = room
    self.task1 = task1
    self.task2 = task2



@override_settings(DEBUG=True,)
class CoreSeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)
    
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

    
    def _enter_flag(self, roomid, taskid, flag):
        ROOM_URL = self.live_server_url + reverse("room", args=[roomid])
        self.selenium.get(ROOM_URL)

        task = self.selenium.find_element_by_css_selector(f"#formtask_{taskid} input[name='flag']")
        task_submit = self.selenium.find_element_by_css_selector(f"#formtask_{taskid} button[type='submit']")
        # wrong flag
        task.send_keys(flag)
        task_submit.click()
        # check alert
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())
        ale = self.selenium.switch_to_alert();
        ale.accept();


    def test_login_wrong(self):
        """ login with wrong password """
        self._login_user("this@mail.com", "password.....")

        alert = self.selenium.find_element_by_css_selector(".alert-danger")
        self.assertTrue(alert)

    def test_login_right(self):
        """ login with right password """
        self._login_user("brock@mail.com", "123456")

        alert = self.selenium.find_element_by_css_selector(".alert-success")
        self.assertTrue(alert)
    

    def test_enter_flag(self):
        """ test mechanic when user enter the flag in room """
        self._login_user("brock@mail.com", "123456")

        self._enter_flag(self.room.id, self.task1.id, "FLAG{WRONG}")
        # score not increase
        user = get_user_model().objects.get(email="brock@mail.com")
        self.assertEqual(user.score, 0)

        # right flag
        self._enter_flag(self.room.id, self.task1.id, self.task1.flag)
        # check points increase
        user.refresh_from_db()
        self.assertEqual(user.score, self.task1.points)

        # check score history
        history = ScoreHistory.objects.get(user=user)
        self.assertEqual(history.gained, self.task1.points)
        self.assertEqual(history.type, "task")

        # enter every flag and see if conclusion appear
        self._enter_flag(self.room.id, self.task2.id, self.task2.flag)
        conslusion = self.selenium.find_element_by_css_selector("#roomconclus")
        self.assertTrue(conslusion)






