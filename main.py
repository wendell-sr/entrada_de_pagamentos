from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from screens.calendar_screen import CalendarScreen
from screens.payment_screen import PaymentScreen
from screens.report_screen import ReportScreen

class PaymentApp(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(PaymentScreen(name='payment'))
        sm.add_widget(ReportScreen(name='report'))
        return sm

if __name__ == '__main__':
    PaymentApp().run()
