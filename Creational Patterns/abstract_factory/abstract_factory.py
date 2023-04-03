from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_text_box(self):
        pass


class AbstractButton(ABC):
    @abstractmethod
    def click(self):
        pass


class AbstractTextBox(ABC):
    @abstractmethod
    def enter_text(self, text):
        pass


class WindowsButton(AbstractButton):
    def click(self):
        print("Windows button clicked")


class WindowsTextBox(AbstractTextBox):
    def enter_text(self, text):
        print(f"Windows text box entered text: {text}")


class MacButton(AbstractButton):
    def click(self):
        print("Mac button clicked")


class MacTextBox(AbstractTextBox):
    def enter_text(self, text):
        print(f"Mac text box entered text: {text}")


class WindowsFactory(AbstractFactory):
    def create_button(self):
        return WindowsButton()

    def create_text_box(self):
        return WindowsTextBox()


class MacFactory(AbstractFactory):
    def create_button(self):
        return MacButton()

    def create_text_box(self):
        return MacTextBox()


class Client:
    def __init__(self, factory):
        self.button = factory.create_button()
        self.text_box = factory.create_text_box()

    def run(self):
        self.button.click()
        self.text_box.enter_text("Hello, world!")


windows_factory = WindowsFactory()
client_windows = Client(windows_factory)
client_windows.run()

mac_factory = MacFactory()
client_mac = Client(mac_factory)
client_mac.run()
