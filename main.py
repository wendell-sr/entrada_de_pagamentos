from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from screens.calendar_screen import CalendarScreen
from screens.payment_screen import PaymentScreen
from screens.report_screen import ReportScreen
from screens.list_payments_screen import ListPaymentsScreen
from screens.edit_payment_screen import EditPaymentScreen

class PaymentApp(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(PaymentScreen(name='payment'))
        sm.add_widget(ReportScreen(name='report'))
        sm.add_widget(ListPaymentsScreen(name='list_payments'))
        sm.add_widget(EditPaymentScreen(name='edit_payment'))
        return sm

if __name__ == '__main__':
    PaymentApp().run()
