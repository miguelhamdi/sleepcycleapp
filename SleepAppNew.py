import rumps
import time
import datetime


class SleepCycleApp(rumps.App):
    def __init__(self):
        super(SleepCycleApp, self).__init__("Sleep Cycle")
        self.menu = [
            rumps.MenuItem('Hours sleep:'),
            rumps.MenuItem('6', callback=self.set_hours_slept),
            rumps.MenuItem('7.5', callback=self.set_hours_slept),
            rumps.MenuItem('9', callback=self.set_hours_slept),
            None,  # separator
            rumps.MenuItem('Set wake-up time', callback=self.set_ideal_time),
        ]
        self.hours_slept = 9
        self.wake_up_time = None
        self.update_title()

    def set_hours_slept(self, sender):
        self.hours_slept = float(sender.title)
        self.update_title()

    def set_ideal_time(self, sender):
        window = rumps.Window(title='Enter Wake-Up Time', message='Enter your desired wake up time (format: HH:MM):',
                              default_text='')
        response = window.run()
        if response.clicked:
            user_input = response.text
            try:
                # parse the user input into a datetime object
                self.wake_up_time = datetime.datetime.strptime(user_input, '%H:%M')
                # update the menu item with the new wake-up time
                self.menu['Set wake-up time'].title = f"Wake-up time: {self.wake_up_time.strftime('%H:%M')}"
                self.update_title()
            except ValueError:
                rumps.notification(title='Invalid Input Format', subtitle='Please enter a time in the format HH:MM.',
                                   message='')

    def update_title(self):
        self.title = f"💤{self.best_wake_up_time()}"

    def best_wake_up_time(self):
        TimeToSleep = 15
        SleepCycle = 90
        IdealCycles = int(self.hours_slept / 1.5)
        t = time.localtime()
        current_time_hrs = int(time.strftime("%H", t))
        current_time_min = int(time.strftime("%M", t))
        wake_up_list = [((IdealCycles * SleepCycle) + current_time_min + TimeToSleep) + (current_time_hrs * 60)]
        wake_up_hr = int(wake_up_list[0] / 60) % 24
        wake_up_min = wake_up_list[0] % 60
        WakeUp = str("{:02d}".format(wake_up_hr)) + ":" + str("{:02d}".format(wake_up_min))
        return WakeUp

    def refresh_title(self, _):
        if self.wake_up_time is not None and self.best_wake_up_time() == self.wake_up_time.strftime('%H:%M'):
            if not self.notification_shown:
                rumps.notification(title="Time to sleep!", subtitle=f"If you want to wake up at {self.best_wake_up_time()}, now is the best time to sleep.", message="")
                self.notification_shown = True
        else:
            self.notification_shown = False
        self.title = f"💤{self.best_wake_up_time()}"
        self.icon = None

    def run(self):
        # Call refresh_title() every second
        rumps.Timer(self.refresh_title, interval=1).start()
        super().run()


if __name__ == "__main__":
    sleep_cycle_app = SleepCycleApp()
    sleep_cycle_app.run()

